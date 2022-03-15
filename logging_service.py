# https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry#LogSeverity

import logging
import sys

from pydantic_schemas import LogPydantic


def log_data(log_object: LogPydantic) -> None:
    """"""

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    root.addHandler(handler)
    logging.info(log_object.dict(by_alias=True))