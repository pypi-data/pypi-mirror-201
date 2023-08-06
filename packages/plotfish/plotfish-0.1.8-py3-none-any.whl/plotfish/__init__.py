__version__ = "0.1.0"

from decimal import Decimal
from datetime import datetime, timezone
import time
from typing import Union, Optional, Dict, Any
import os
import logging
import socketio
from enum import Enum
import json

NumberLike = Union[int, float, Decimal]
TimestampLike = Union[int, float, datetime]

# Configuration
api_key = os.environ.get("PLOTFISH_API_KEY")
riverbed_url = os.environ.get("RIVERBED_URL") or "https://api.plot.fish"


class PlotfishLoggingAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f"[plotfish] {msg}", kwargs


logger = PlotfishLoggingAdapter(logging.getLogger(__name__), {})


class PlotfishError(RuntimeError):
    """For Plotfish SDK related exceptions"""


socket = socketio.Client(logger=logger)

plots: Dict[str, object] = {}

# TODO: is it possible to get mypy?


class PlotType(str, Enum):
    Line = "line"
    ProgressBar = "progress_bar"
    Counter = "counter"


# TODO: move into seperate thread


def raise_for_error_callback(error_message: Optional[str]) -> None:
    if error_message:
        raise PlotfishError(error_message)


# TODO: store datapoints in a temp buffer and upload once connection happens


def _record_datapoint(
    name: str,
    value: NumberLike,
    timestamp: Optional[TimestampLike],
    metadata: dict,
) -> None:
    if not socket.connected:
        try:
            if api_key is None:
                raise PlotfishError("api_key cannot be null.")

            if riverbed_url is None:
                raise PlotfishError("riverbed_url cannot be null.")

            socket.connect(url=riverbed_url, auth={"apiKey": api_key})
        except Exception as err:
            logger.error(
                "Cannot connect to Plotfish server at %s: %s", riverbed_url, err
            )
            return

    if name not in plots or metadata != plots[name]:
        try:
            socket.emit(
                "updatePlotMetadata",
                (name, json.dumps(metadata)),
                callback=raise_for_error_callback,
            )
            plots[name] = metadata
        except Exception as err:
            logger.error(
                "Ran into error while updating the metadata for plot `%s`: %s",
                name,
                err,
            )

    try:
        if isinstance(timestamp, datetime):
            timestamp = timestamp.replace(tzinfo=timezone.utc).timestamp()
        elif isinstance(timestamp, int):
            timestamp = float(timestamp)
        elif timestamp is None:
            timestamp = time.time()

        socket.emit("recordDatapoints", (name, [[timestamp, value, None]]))

        # TODO [critical]: Remove this after moving to REST
        socket.disconnect()
    except Exception as err:
        logger.error(
            "Ran into error while recording datapoint for plot `%s`: %s", name, err
        )


def line(
    name: str,
    value: NumberLike,
    timestamp: Optional[TimestampLike] = None,
) -> None:
    _record_datapoint(name, value, timestamp, metadata={"type": PlotType.Line})


def progress_bar(
    name: str,
    value: NumberLike,
    total: NumberLike,
    timestamp: Optional[TimestampLike] = None,
) -> None:
    _record_datapoint(
        name, value, timestamp, metadata={"type": PlotType.ProgressBar, "total": total}
    )


def counter(
    name: str,
    change: NumberLike,
    timestamp: Optional[TimestampLike] = None,
) -> None:
    _record_datapoint(name, change, timestamp, metadata={"type": PlotType.Counter})


def increment(
    name: str,
    timestamp: Optional[TimestampLike] = None,
) -> None:
    _record_datapoint(name, 1, timestamp, metadata={"type": PlotType.Counter})
