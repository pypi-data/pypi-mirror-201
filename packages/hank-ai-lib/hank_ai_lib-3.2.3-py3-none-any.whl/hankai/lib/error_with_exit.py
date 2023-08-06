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
"""Classes for Error with Exit."""
import sys
from dataclasses import dataclass
from typing import Optional, Type

from .enum import EnvEnum
from .log_env import LogEnv


class ErrorExitEnv(EnvEnum):
    """Convenience class of ENV variables and ErrorExit attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_ERROREXIT_MAX_EXCEPTIONS = "max_exceptions"
    HANK_ERROREXIT_EXIT_STATUS = "exit_status"


@dataclass
class ErrorExit:
    """Exception, but abort after a maximum number of times the exception is
    raised. Relies on ExceptionCounter to track the state as this
    class is stateless each time it's invoked. Default number of exceptions
    is 5 at which the 6th exception will cause a system exit.
    """

    logenv: LogEnv
    max_exceptions: int = 5
    exit_status: int = 127
    env: Optional[Type[EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

        self.max_exceptions = max(self.max_exceptions, 1)
        self.__exception_count = 0

    def exception_handler(self, exception: Exception) -> None:
        """Increment the exception counter."""
        self.logenv.logger.exception("Error exit exception caught:\n{}", exception)
        self.__exception_count += 1

        if self.__exception_count >= self.max_exceptions:
            self.logenv.logger.critical(
                "Error exit max exception count [{}] reached; aborting with "
                "sys.exit status [{}].",
                self.__exception_count,
                self.exit_status,
            )
            sys.exit(self.exit_status)
        else:
            self.logenv.logger.warning(
                "Error exit exception count [{}] of [{}] before abort.",
                self.__exception_count,
                self.max_exceptions,
            )
