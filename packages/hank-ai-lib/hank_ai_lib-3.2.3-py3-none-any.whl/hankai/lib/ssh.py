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
"""Classes for SSH Utilities."""
from dataclasses import dataclass
from typing import Optional, Type

from .enum import EnvEnum
from .log_env import LogEnv
from .sys import Sys


class SSHEnv(EnvEnum):
    """Convenience class of ENV variables and SSH attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_SSH_PUBLIC_KEY = "public_key"
    HANK_SSH_AUTHORIZED_KEYS_PATH = "authorized_keys_path"
    HANK_SSH_AUTHORIZED_KEYS_CHMOD = "authorized_keys_chmod"
    HANK_SSH_AUTHORIZED_KEYS_APPEND = "authorized_keys_append"


@dataclass
class SSH:
    """Collection of SSH support utilities."""

    public_key: str
    authorized_keys_path: str = "/home/ubuntu/.ssh/authorized_keys"
    authorized_keys_chmod: int = 0o600
    authorized_keys_append: bool = False
    env: Optional[Type[EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            LogEnv().env_supersede(clz=self, env_type=self.env)

    def ssh_update_public_key(self) -> None:
        """Update the [authorized_keys_path] with the provided [public_key].
        [authorized_keys_chmod] should be an octal.
        e.g. 0o600 for Linux files is rw-------; 0o400 is r--------
        """
        Sys.write_file(
            file=self.authorized_keys_path,
            data=self.public_key,
            chmod=self.authorized_keys_chmod,
            append=self.authorized_keys_append,
        )
