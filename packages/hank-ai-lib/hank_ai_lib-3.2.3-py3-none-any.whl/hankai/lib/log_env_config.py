#
# MIT License
#
# Copyright © 2022 Hank AI, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Hank AI Base class config for referencing what would have been the base
classes @dataclass attributes. They are referenced this way as having
attributes with default values would require subclasses @dataclass attributes
not start with any non-default attributes; essentially meaning *no* subclass
attributes can be non-default.
"""
from __future__ import annotations

import logging.handlers
import sys
from typing import Optional, Tuple

import loguru

from .enum import LoguruLevel

log_level: LoguruLevel = LoguruLevel.INFO
log_format: str = (
    "<level>{level: <8}</level> | {level.icon} | "
    "<level>{message}</level> | "
    "<light-blue>{thread.name}</light-blue> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
)
verbosity: int = 0
log_stdout: bool = True
log_syslog_port: int = 514
log_syslog_address: Tuple[Optional[str], int] = (None, log_syslog_port)
log_file_path: Optional[str] = None
logger: loguru.Logger = loguru.logger  # pylint: disable=no-member


def set_logger() -> None:
    """Set the logger properties."""
    logger.remove()
    if log_stdout:
        logger.add(
            sys.stdout,
            level=log_level.value,
            format=log_format,
            enqueue=True,
        )
    host, port = log_syslog_address
    if host and port:
        logger.add(
            logging.handlers.SysLogHandler(
                address=(host, port),
            ),
            level=log_level.value,
            format=log_format,
            enqueue=True,
        )
    if log_file_path:
        logger.add(
            log_file_path,
            level=log_level.value,
            format=log_format,
            enqueue=True,
        )
