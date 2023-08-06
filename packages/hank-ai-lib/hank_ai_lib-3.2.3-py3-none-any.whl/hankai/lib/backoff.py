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
"""Classes for Backoff @backoff decarator."""
from dataclasses import dataclass
from typing import Optional, Type

from .enum import EnvEnum
from .log_env import LogEnv


class BackoffEnv(EnvEnum):
    """Convenience class of ENV variables and Backoff attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_BACKOFF_MAX_VALUE_SECONDS = "max_value_seconds"
    HANK_BACKOFF_MAX_TIME_SECONDS = "max_time_seconds"


@dataclass
class Backoff:
    """Set @backoff decorator values.

    expo()
    max_value: The maximum value to yield. Once the value in the
             true exponential sequence exceeds this, the value
             of max_value will forever after be yielded.

    fibo()
    max_value: The maximum value to yield. Once the value in the
             true fibonacci sequence exceeds this, the value
             of max_value will forever after be yielded.

    ! CAUTION: [max_time] should only be set to a value if you
    ! want to limit the retries. Set [max_time=None] to run
    ! indefinitely. [max_time] should likely only be used for testing.
    ! However, [max_value_seconds] SHOULD be set to a reasonable lower bound
    ! to assure it doesn't block for longer and longer times until the next try.

    https://github.com/litl/backoff
    """

    max_value_seconds: int = 60  # FIBO will be 55
    max_time_seconds: Optional[float] = None
    env: Optional[Type[EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            LogEnv().env_supersede(clz=self, env_type=self.env)

        self.set_floor()

    def set_floor(self) -> None:
        """Set the max floors."""
        self.max_value_seconds = max(self.max_value_seconds, 0)
        if self.max_time_seconds is not None:
            self.max_time_seconds = max(self.max_time_seconds, 0.0)
