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
"""Hank AI Base class containing the most widely scoped classes and functions
that Hank AI Python projects will need for ease of development; especially in
Docker container situations where ENV variables are passed in at runtime.

Most notable:
envs - Supersede local fields of any inheritnance classes that
    have EnvEnum base enum, call the method and have ENV variables
    defined in the OS. Many base types will be cast for the string based on the
    fields type hint. e.g ENV VARX="123": str -> int(123) if varx: int.

logger - Provide execution scope wide and consistent Loguru logging format for
    all inheritance classes. Format and log level may be superseded by ENV vars.

verbosity - Provides scope wide verbosity level for all inheritance classes.
    Verbosity level may be superseded by ENV var.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple, Type, get_type_hints

import loguru

import hankai.lib.log_env_config as base_config

from .enum import EnvEnum, LoguruLevel
from .util_util import Util


class LogEnvEnv(EnvEnum):
    """Convenience class of ENV variables and LogEnv attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_LOG_LEVEL = "log_level"
    HANK_LOG_FORMAT = "log_format"
    HANK_VERBOSITY = "verbosity"
    HANK_LOG_SYSLOG = "log_syslog"
    HANK_LOG_FILE = "log_file"
    HANK_LOG_STDOUT = "log_stdout"


# pylint: disable=too-many-instance-attributes
@dataclass
class LogEnv:
    """Hank AI Base class containing the most widely scoped classes and functions
    that Hank AI Python projects will need for ease of development; especially
    in Docker container situations where ENV variables are passed in at runtime.

    Most notable:
    env - Supersede local fields of any inheritnance classes
        that have EnvEnum base enum, call the method and have ENV
        variables defined in the OS environment. Many base types will be cast
        for the string based on the fields type hint.
        e.g ENV VARX="123": str -> int(123) if varx: int.

        ENV enum must value be a tuple of (ENV_VAR_NAME: str, attribute: str)

    logger - Provide execution scope wide and consistent Loguru logging format
        for all inheritance classes. Format and log level may be superseded by
        ENV vars.

    verbosity - Provides scope wide verbosity level for all inheritance classes.
        Verbosity level may be superseded by ENV var.

    NOTE! logger and verbosity are global in scope. If superseded in another
    class or method - it will impact all other occurrences of logger and
    verbosity.
    """

    env: Optional[Type[EnvEnum]] = None

    @property
    def logger(self) -> loguru.Logger:  # pylint: disable=no-member
        """Return the Loguru logger."""
        return base_config.logger

    @property
    def log_level(self) -> LoguruLevel:
        """Return the Loguru level."""
        return base_config.log_level

    @staticmethod
    def set_log_level(level: LoguruLevel) -> None:
        """Set the Loguru level by LoguruLevel."""
        base_config.log_level = level
        base_config.set_logger()

    @property
    def verbosity(self) -> int:
        """Return the verbosity level."""
        return base_config.verbosity

    @staticmethod
    def set_verbosity(level: int) -> None:
        """Set the verbosity level."""
        base_config.verbosity = max(level, 0)

    @property
    def log_syslog(self) -> Tuple[Optional[str], int]:
        """Return the Loguru syslog address and port."""
        return base_config.log_syslog_address

    @staticmethod
    def set_log_syslog(
        address: Tuple[Optional[str], int] = (None, base_config.log_syslog_port)
    ) -> None:
        """Set Loguru SysLog handler."""
        base_config.log_syslog_address = address
        base_config.set_logger()

    @property
    def log_file(self) -> Optional[str]:
        """Return the Loguru file."""
        return base_config.log_file_path

    @staticmethod
    def set_log_file(path: Optional[str]) -> None:
        """Set Loguru File handler."""
        base_config.log_file_path = path
        base_config.set_logger()

    @property
    def log_format(self) -> str:
        """Return the Loguru format."""
        return base_config.log_format

    @property
    def log_stdout(self) -> bool:
        """Return the Loguru suppress STDOUT."""
        return base_config.log_stdout

    @staticmethod
    def set_log_stdout(enable: bool) -> None:
        """Set the Loguru suppress STDOUT."""
        base_config.log_stdout = enable
        base_config.set_logger()

    @staticmethod
    def set_log_format(pattern: str) -> None:
        """Set the Loguru format. This format will be applied to all of the log
        sinks: STDOUT, SYSLOG and file.
        """
        if pattern:
            base_config.log_format = pattern
            base_config.set_logger()

    def set_logger(self) -> None:
        """Set and configure the Loguru logger.

        This should only be called for multiprocessing situations.

        There is an open issue with Loguru and multiprocessing and 'spawn'.
        Multiprocessing 'spawn' launches new interpreter per thread. The
        global Loguru logger id() is different in the main thread and the
        child thread; but that the new object was not instantiated in such
        a way that the __post_init__ is called. And the child logenv.logger
        does not have any of the configurations set from the main thread.

        https://github.com/Delgan/loguru/issues/108
        """
        if self.env:
            self.env_supersede(clz=self, env_type=self.env)
        base_config.set_logger()

    def __post_init__(self) -> None:
        if self.env:
            self.env_supersede(clz=self, env_type=self.env)
        base_config.set_logger()

    # pylint: disable=too-many-branches,too-many-locals, disable=too-many-statements
    @staticmethod
    def env_supersede(clz: Any, env_type: Type[EnvEnum]) -> None:
        """Given the ENV Enum if an ENV variable exists it will supersede the
        instantiated class instance attribute value in the class namespace.

        NOTE! All attributes must exist in the class namespace to be superseded.
        The exception are [log_level], [log_format] and [verbosity]. They
        may be defined in any EnvEnum regardless of whether they are in the
        current scope.
        NOTE! All attributes enumerated for supersede must have a type hint.
        NOTE! Class must posses __dict__. Slots are not supported.
        """
        if clz.__dict__ is None:
            raise AssertionError(f"Class [{clz}] __dict__ is required.")

        logenv = LogEnv()

        # Get the base classes and current class to scan type hints.
        classes: Tuple[type, ...] = (clz.__class__).__bases__ + (clz.__class__,)

        # # ! CAUTION: get_type_hints here affects __dict__ and masks set field
        # # ! values. Save __dict__ prior to invocation and use the saved
        # # ! __dict__ for evaluations/assignments as needed.
        saved_dict = clz.__dict__
        type_hints: Dict[str, Any] = {}
        for cls in classes:
            type_hints.update(get_type_hints(cls))

        for member in env_type:
            env_var_name = member.name
            attribute = member.value
            if not isinstance(attribute, str):
                raise AssertionError(
                    f"EnvEnum [{env_type}] ENV variable [{env_var_name}] "
                    f"attribute [{attribute}] is not type [str]."
                )
            env_var_value = os.environ.get(env_var_name, None)

            if env_var_value is None:
                if logenv.verbosity > 1:
                    logenv.logger.warning(
                        "EnvEnum [{}] ENV variable [{}] was not found in "
                        "environment.",
                        env_type,
                        env_var_name,
                    )
                continue

            # Handle this class properties as they are not in the __dict__
            # as this class enumerate any natural attributes.
            if attribute == "log_level":
                if env_var_value:
                    obj = Util.objectify(
                        value=env_var_value, type_hint=LoguruLevel, is_json=False
                    )

                    if obj:
                        logenv.set_log_level(level=obj)
                continue
            if attribute == "verbosity":
                if env_var_value:
                    obj = Util.objectify(
                        value=env_var_value, type_hint=int, is_json=False
                    )
                    if obj:
                        logenv.set_verbosity(level=obj)
                continue
            if attribute == "log_syslog":
                if env_var_value:
                    obj = Util.objectify(
                        value=env_var_value,
                        type_hint=Tuple[Optional[str], int],
                        is_json=False,
                    )
                    if obj:
                        logenv.set_log_syslog(address=obj)
                continue
            if attribute == "log_file":
                if env_var_value:
                    obj = Util.objectify(
                        value=env_var_value,
                        type_hint=Optional[str],
                        is_json=False,
                    )
                    if obj:
                        logenv.set_log_file(path=obj)
                continue
            if attribute == "log_format":
                if env_var_value:
                    logenv.set_log_format(pattern=env_var_value)
                continue
            if attribute == "log_stdout":
                if env_var_value:
                    obj = Util.objectify(
                        value=env_var_value,
                        type_hint=bool,
                        is_json=False,
                    )
                    logenv.set_log_stdout(enable=bool(obj))
                continue

            if not attribute in clz.__dict__:
                raise AssertionError(
                    f"EnvEnum [{env_type}] ENV variable [{env_var_name}] "
                    f"attribute [{attribute}] was not in found in "
                    f"class {clz} __dict__.':\n"
                    f"{clz.__dict__}"
                )

            type_hint: Any = type_hints.get(attribute)
            if type_hint:
                if logenv.verbosity > 0:
                    logenv.logger.debug(
                        "EnvEnum [{}] ENV variable [{}] attribute [{}] "
                        "has type hint [{}]. Supersede attribute value [{}] "
                        "with ENV variable value [{}].",
                        env_type,
                        env_var_name,
                        attribute,
                        type_hint,
                        saved_dict[attribute],
                        env_var_value,
                    )

                saved_dict[attribute] = Util.objectify(
                    value=env_var_value, type_hint=type_hint, is_json=False
                )

                if logenv.verbosity > 0:
                    logenv.logger.debug(
                        "EnvEnum [{}] ENV variable [{}] attribute [{}] original "
                        "value [{}] superseded by [{}] with type [{}].",
                        env_type,
                        env_var_name,
                        attribute,
                        saved_dict[attribute],
                        env_var_value,
                        type(saved_dict[attribute]),
                    )
            else:
                raise AssertionError(f"Attribute [{attribute}] has no type hint.")
