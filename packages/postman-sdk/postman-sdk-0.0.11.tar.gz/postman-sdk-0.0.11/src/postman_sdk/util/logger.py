import sys
import loguru

HANDLER_ID = 0  # The preset logging handler id
_LOG = loguru.logger


def set_log_level(log_level="ERROR"):
    global HANDLER_ID, _LOG

    # This is done to keep the formatting close to the original loguru.logger.
    # While not showcasing the <INFO> level to the user.
    _LOG.remove(HANDLER_ID)

    HANDLER_ID = _LOG.add(
        sys.stderr,
        format=(
            "<green>{time}</green> | <blue>{name}:{function}:{line}</blue> | {message}"
        ),
        colorize=True,
        level=log_level,
    )
