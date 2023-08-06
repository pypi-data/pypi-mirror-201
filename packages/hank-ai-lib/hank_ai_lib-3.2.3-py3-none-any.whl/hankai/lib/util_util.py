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
"""Classes for Util."""
from __future__ import annotations

import ast
import base64
import importlib
import re
import sys
import traceback
from typing import Any, List, Optional, Tuple, Union

import pendulum
from pendulum.datetime import DateTime
from pendulum.tz.timezone import Timezone

from .enum import EncodeBinaryBase, EncodeStringCodec


class Util:
    """Class for Util. Primarily staticmethod helpers and utils to
    check for common base types and return defaults if inputs don't validate.
    """

    @staticmethod
    def formatted_traceback_exceptions() -> List[str]:
        """Collect the current, point in time, exception stack. Should be called
        immediately after try/except catch.
        """
        exc_type, exc_value, exc_traceback = sys.exc_info()
        return traceback.format_exception(exc_type, exc_value, exc_traceback)

    @staticmethod
    def date_now(  # pylint: disable=invalid-name
        tz: Optional[Union[str, Timezone]] = "UTC",
    ) -> DateTime:
        """Return the Pendulum datetime with timezone. Default TZ is UTC.
        Timezone is any valid zoneinfo from pytzdata.

        https://pendulum.eustace.io/
        """
        return pendulum.now(tz=tz)

    @staticmethod
    def elapsed_seconds(  # pylint: disable=invalid-name
        start: DateTime,
        tz: Optional[Union[str, Timezone]] = "UTC",
        precision: int = 2,
    ) -> float:
        """Return the elapsed seconds from start datetime and current datetime
        at invocation. Precision maximum is 6. Timezone is any valid zoneinfo
        from pytzdata.
        """
        precision = min(precision, 6)
        end = Util.date_now(tz=tz)
        elapsed = end.float_timestamp - start.float_timestamp
        return float(round(elapsed, precision))

    @staticmethod
    def duration_seconds(start: DateTime, end: DateTime, precision: int = 2) -> float:
        """Return the elapsed seconds from start datetime and current datetime
        at invocation. Precision maximum is 6.
        """
        precision = min(precision, 6)
        duration = end.float_timestamp - start.float_timestamp
        return float(round(duration, precision))

    @staticmethod
    def base_encode(
        decoded: bytes, base: EncodeBinaryBase, codec: EncodeStringCodec
    ) -> str:
        """Encode the decoded bytes."""
        if base == EncodeBinaryBase.BASE_64:
            return base64.b64encode(decoded).decode(encoding=codec.value)
        if base == EncodeBinaryBase.BASE_85:
            return base64.b85encode(decoded).decode(encoding=codec.value)

        raise AssertionError("Unable to encode the decoded bytes.")

    @staticmethod
    def base_decode(encoded: Union[str, bytes], base: EncodeBinaryBase) -> bytes:
        """Decode the encoded bytes."""
        if base == EncodeBinaryBase.BASE_64:
            return base64.b64decode(encoded)
        if base == EncodeBinaryBase.BASE_85:
            return base64.b85decode(encoded)

        raise AssertionError("Unable to decode the encoded bytes.")

    @staticmethod
    def is_none(value: str, is_json: bool = False) -> bool:
        """Return true if string is strictly 'None'."""
        match = False
        if not is_json:
            if re.search(r"^None$", value):
                match = True
        else:
            if re.search(r"^null$", value):
                match = True

        return match

    @staticmethod
    def class_by_hint(
        type_str: str, type_hint: Optional[Any] = None
    ) -> Tuple[Optional[str], Any]:
        """Get the class from the type hint. Returns Tuple[str, Any] where the
        first element is the module name and the second element is the class
        attributes.

        Examples:
            [type_str=SomeCoolClass] [type_hint=None] local module __main__ but
        SomeCoolClass is in co.module.classes.SomeCoolClass. The class will not
        load as it is not in the current module.

            [type_str=SomeCoolClass] [type_hint=<enum 'SomeCoolClass'>] The
        class will load as the type_hint provided by Python typing
        get_type_hints <enum 'SomeCoolClass'> can be interrogated for the
        __module__ name co.module.classes.
        """
        match = re.search(r"^typing\.Type\[(.+)\]$", str(type_str))
        if match and match.group(1):
            type_str = match.group(1)
            type_hint = None

        mod_cls = type_str.split(".")
        class_name = mod_cls[-1]
        module_name = ".".join(mod_cls[:-1])

        if not module_name and type_hint is not None:
            try:
                module_name = str(type_hint.__dict__.get("__module__", ""))
            except Exception:  # pylint: disable=broad-except
                return (None, None)

        try:
            module = importlib.import_module(module_name)
            return (module_name, getattr(module, class_name))
        except Exception:  # pylint: disable=broad-except
            return (None, None)

    @staticmethod
    def obj_member_by(type_hint: Any, type_str: str, value: str) -> Tuple[bool, Any]:
        """Get Enum class member by string of the Enum __str__. The Enum class
        must have a method [member_by].
        """
        module_name, cls = Util.class_by_hint(type_hint=type_hint, type_str=type_str)
        if not module_name or not cls:
            return (False, None)
        # Best effort.
        try:
            if getattr(cls, "member_by"):
                member = cls.member_by(value)
                if member is not None:
                    return (True, member)
        except AttributeError:
            pass

        return (False, None)

    @staticmethod
    def obj_by_unpicklable(
        type_hint: Any, type_str: str, value: str
    ) -> Tuple[bool, Any]:
        """Get object by unpicklable()."""
        module_name, cls = Util.class_by_hint(type_hint=type_hint, type_str=type_str)
        if not module_name or not cls:
            return (False, None)
        # Best effort.
        if cls.__dict__.get("unpicklable"):
            val = cls.unpicklable(value)
            if val is not None:
                return (True, val)

        return (False, None)

    @staticmethod
    def obj_by_init(type_hint: Any, type_str: str, value: str) -> Tuple[bool, Any]:
        """Get object by instantiating."""
        module_name, cls = Util.class_by_hint(type_hint=type_hint, type_str=type_str)
        if not module_name or not cls:
            return (False, None)
        # Best effort. Classes that are intendend to be set from ENV should
        # assure that the first parameter is a string type.
        try:
            obj = cls(value)
            return (True, obj)
        except Exception:  # pylint: disable=broad-except
            return (False, None)

    @staticmethod
    def retrieve_by_hint(  # pylint: disable=too-many-return-statements,too-many-branches
        type_hint: Any, type_str: str, value: str, is_json: bool
    ) -> Tuple[bool, Any]:  # pylint: disable-too-many-statements
        """Attempt to retrieve the object by type hint."""
        # Type str requires no action; can not reason for type Any.
        if type_str in ["str", "Any"]:
            return (True, value)

        if type_str == "bool":
            if not is_json:
                try:
                    return (True, ast.literal_eval(value))
                except Exception:  # pylint: disable=broad-except
                    return (False, None)
            else:
                if re.search(r"^true$", value):
                    return (True, True)
                if re.search(r"^false$", value):
                    return (True, False)
                if re.search(r"^null$", value):
                    return (True, None)

        if type_str == "NoneType":
            if Util.is_none(value=value, is_json=is_json):
                return (True, None)

            return (False, None)

        if type_str == "bytes":
            return (True, value.encode("utf-8"))

        if type_str not in ["tuple", "list", "dict", "set", "int", "float"]:
            # Try enum first before trying to retrieve by object instantiation.
            retrieved, obj = Util.obj_member_by(
                type_hint=type_hint, type_str=type_str, value=value
            )
            if retrieved:
                return (True, obj)

            retrieved, obj = Util.obj_by_unpicklable(
                type_hint=type_hint, type_str=type_str, value=value
            )
            if retrieved:
                return (True, obj)

            retrieved, obj = Util.obj_by_init(
                type_hint=type_hint, type_str=type_str, value=value
            )
            if retrieved:
                return (True, obj)

        # Return literal eval for everything else; correct return object type is
        # incumbent on user.
        try:
            result = ast.literal_eval(value)
            # Rough cross check for expected type.
            mis_match = False
            if (
                type_str.lower() == "tuple"
                and type(result) is not tuple  # pylint: disable=unidiomatic-typecheck
            ):
                mis_match = True
            if (
                type_str.lower() == "list"
                and type(result) is not list  # pylint: disable=unidiomatic-typecheck
            ):
                mis_match = True
            if (
                type_str.lower() == "dict"
                and type(result) is not dict  # pylint: disable=unidiomatic-typecheck
            ):
                mis_match = True
            if (
                type_str.lower() == "set"
                and type(result) is not set  # pylint: disable=unidiomatic-typecheck
            ):
                mis_match = True
            if (
                type_str == "int"
                and type(result) is not int  # pylint: disable=unidiomatic-typecheck
            ):
                mis_match = True
            if (
                type_str == "float"
                and type(result) is not float  # pylint: disable=unidiomatic-typecheck
            ):
                mis_match = True
            if mis_match:
                raise AssertionError(
                    f"Value [{value}] type hint [{type_hint}]; result "
                    f"[{result}] type [{type(result)}] is mismatched with expected type."
                )
            return (True, result)
        except (
            ValueError,
            TypeError,
            SyntaxError,
            MemoryError,
            RecursionError,
            AssertionError,
        ) as exc:
            raise ValueError(
                f"Unable to evaluate value [{value}] type_hint [{type_hint}]."
            ) from exc

    # pylint: disable=too-many-branches disable=unidiomatic-typecheck disable=too-many-return-statements
    @staticmethod
    def objectify(
        value: str,
        type_hint: Any,
        is_json: bool = False,
    ) -> Optional[Any]:
        """Return the literal result of a string based on the type hint."""
        # Catch Optional/NoneType first. If not None keep processing.
        match = re.search(r"^typing\.Optional\[(.+)\]$", str(type_hint))
        if match and match.group(1):
            if Util.is_none(value=value, is_json=is_json):
                return None

            type_hint = match.group(1)

        # Nothing to reason about for type Any.
        match = re.search(r"^typing\.(Any)$", str(type_hint))
        if match:
            return value

        match = re.search(r"^<class '([^']+)'>$", str(type_hint))
        if match and match.group(1):
            retrieved, ret_value = Util.retrieve_by_hint(
                type_hint=type_hint,
                type_str=match.group(1),
                value=value,
                is_json=is_json,
            )
            if retrieved:
                return ret_value

        match = re.search(r"^<enum '([^']+)'>$", str(type_hint))
        if match and match.group(1):
            retrieved, ret_value = Util.obj_member_by(
                type_hint=type_hint, type_str=match.group(1), value=value
            )
            if retrieved:
                return ret_value

        match = re.search(r"^typing\.Union\[(.+)\]$", str(type_hint))
        if match and match.group(1):
            hints = match.group(1).split(", ")
            has_str_any = False
            for hint in hints:
                # Hold back on "str" alone to see if other type hints
                # produce a result.
                if hint in ["str", "Any"]:
                    has_str_any = True
                    continue

                retrieved, ret_value = Util.retrieve_by_hint(
                    type_hint=hint, type_str=hint, value=value, is_json=is_json
                )
                if retrieved:
                    return ret_value

            # If nothing else matched and "str|Any" was one of the type hints
            # so simply return the value.
            if has_str_any:
                return value

        match = re.search(r"^typing\.(Tuple|List|Dict|Set)\[.+\]$", str(type_hint))
        if match and match.group(1):
            retrieved, ret_value = Util.retrieve_by_hint(
                type_hint=type_hint,
                type_str=match.group(1).lower(),
                value=value,
                is_json=is_json,
            )
            if retrieved:
                return ret_value

        match = re.search(r"^typing\.Type\[(.+)\]$", str(type_hint))
        if match and match.group(1):
            module_name, cls = Util.class_by_hint(type_str=type_hint)
            if module_name and cls:
                return cls

        retrieved, ret_value = Util.retrieve_by_hint(
            type_hint=type_hint, type_str=str(type_hint), value=value, is_json=is_json
        )
        if retrieved:
            return ret_value

        raise ValueError(
            f"Value [{value}] type hint [{type_hint}] could not be objectified.",
        )
