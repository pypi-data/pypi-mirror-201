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
"""Classes to enumerate supported features or common information.

https://www.cosmicpython.com/blog/2020-10-27-i-hate-enums.html
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Union


class MemberCase(Enum):
    """Member case options."""

    UPPER = "upper"
    LOWER = "lower"
    EXACT = "exact"


class MemberFeature(Enum):
    """Member features."""

    NAME = "name"
    VALUE = "value"


class Member(Enum):
    """BaseEnum with universal member methods used especially for ENV
    overrides.
    """

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError()

    @classmethod
    def members(cls) -> List[Any]:
        """Return list of enum."""
        enums: List[Member] = []
        for enum in cls:
            enums.append(enum)

        return enums

    @classmethod
    def members_str(cls) -> List[str]:
        """Return list of enum string."""
        enums: List[str] = []
        for enum in cls:
            enums.append(str(enum))

        return enums

    @classmethod
    @abstractmethod
    def member_by(cls, member: str) -> Optional[Any]:
        """Inheriting class should call cls.member_by_profile."""
        raise NotImplementedError()

    @classmethod
    def member_by_profile(
        cls, member: str, feature: MemberFeature, case: MemberCase = MemberCase.EXACT
    ) -> Optional[Any]:
        """Return matching enum by string match on enum.name base on
        MemberCase. Note! [member] is matched with the str(enum). The inheriting
        class will have to accommodate based on its __str__ method. Value
        comparisons require that the Enum 'value' has a string representation.
        """
        if member is not None:
            if case is MemberCase.LOWER:
                member = member.lower()
            elif case is MemberCase.UPPER:
                member = member.upper()

            for enum in cls:
                enum_case: str
                if feature is MemberFeature.NAME:
                    enum_case = enum.name
                    if case is MemberCase.LOWER:
                        enum_case = enum_case.lower()
                    elif case is MemberCase.UPPER:
                        enum_case = enum_case.upper()
                elif feature is MemberFeature.VALUE:
                    enum_case = str(enum.value)
                    if case is MemberCase.LOWER:
                        enum_case = enum_case.lower()
                    if case is MemberCase.UPPER:
                        enum_case = enum_case.upper()

                if member == enum_case:
                    return enum

        return None


class MemberName(Member):
    """Member enum name in exact case."""

    def __str__(self) -> str:
        return self.name

    @classmethod
    def member_by(cls, member: str) -> Optional[Any]:
        """Return matching enum by string match on enum.name; exact case."""
        return cls.member_by_profile(
            member=member, feature=MemberFeature.NAME, case=MemberCase.EXACT
        )


class MemberValue(Member):
    """Member enum value in exact case."""

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def member_by(cls, member: str) -> Optional[Any]:
        """Return matching enum by string match on enum.value; exact case."""
        return cls.member_by_profile(
            member=member, feature=MemberFeature.VALUE, case=MemberCase.EXACT
        )


class MemberNameLower(Member):
    """Member enum name in lower case."""

    def __str__(self) -> str:
        return self.name.lower()

    @classmethod
    def member_by(cls, member: str) -> Optional[Any]:
        """Return matching enum by string match on enum.name; lower case."""
        return cls.member_by_profile(
            member=member, feature=MemberFeature.NAME, case=MemberCase.LOWER
        )


class MemberValueLower(Member):
    """Member enum value in lower case."""

    def __str__(self) -> str:
        return str(self.value).lower()

    @classmethod
    def member_by(cls, member: str) -> Optional[Any]:
        """Return matching enum by string match on enum.value; lower case."""
        return cls.member_by_profile(
            member=member, feature=MemberFeature.VALUE, case=MemberCase.LOWER
        )


class MemberNameUpper(Member):
    """Member enum name in upper case."""

    def __str__(self) -> str:
        return self.name.upper()

    @classmethod
    def member_by(cls, member: str) -> Optional[Any]:
        """Return matching enum by string match on enum.name; upper case."""
        return cls.member_by_profile(
            member=member, feature=MemberFeature.NAME, case=MemberCase.UPPER
        )


class MemberValueUpper(Member):
    """Member enum value in upper case."""

    def __str__(self) -> str:
        return str(self.value).upper()

    @classmethod
    def member_by(cls, member: str) -> Optional[Any]:
        """Return matching enum by string match on enum.value; upper case."""
        return cls.member_by_profile(
            member=member, feature=MemberFeature.VALUE, case=MemberCase.UPPER
        )


class MemberNameLowerValue(MemberNameLower):
    """Member enum name in lower case returning the value."""

    def __str__(self) -> str:
        return str(self.value).lower()

    @classmethod
    def member_by(cls, member: str) -> Optional[Any]:
        """Return matching enum by string match on enum.value; lower case."""
        return cls.member_by_profile(
            member=member, feature=MemberFeature.NAME, case=MemberCase.LOWER
        )


class EnvEnum(MemberName):
    """Base class for ENV enum for ENV variable name and corresponding attribute
    name. The Enum name is the expected ENV name and the value is the class
    instance variable name.

    e.g. ENV_VAR1 = "log_level"

    The ENV_VAR1 and value must exist in the system environment and the
    attribute name must be in the calling classes namespace. Additionally all
    attributes must have a type hint.

    ! IMPORTANT: As a base Enum - it *must* have zero members!
    """


class LoguruLevel(MemberNameLower):
    """LoguruConfig doesn't have an enum to reference; creating one.

    https://loguru.readthedocs.io/en/stable/api/hankai_logger.html
    """

    TRACE = 5  # hankai_logger.trace()
    DEBUG = 10  # hankai_logger.debug()
    INFO = 20  # hankai_logger.info()
    SUCCESS = 25  # hankai_logger.success()
    WARNING = 30  # hankai_logger.warning()
    ERROR = 40  # hankai_logger.error()
    CRITICAL = 50  # hankai_logger.critical()


class RedactString(MemberNameLower):
    """Replacement strings for redacted items."""

    BYTES = b"...redacted..."
    STRING = "...redacted..."


class EncodeBinaryBase(MemberValueLower):
    """Supported binary encoding base items."""

    BASE_64 = "base64"
    BASE_85 = "base85"


class EncodeStringCodec(MemberValueLower):
    """Supported binary decoding codec items."""

    ASCII = "ascii"
    UTF_8 = "utf-8"


class JsonPickleSeparator(MemberNameLowerValue):
    """Default JSON item and dictionary separators."""

    COMPACT = (",", ":")
    DEFAULT = (", ", ": ")


class MimeTypeApplication(MemberValueLower):
    """Application MIME Types. String application/type."""

    PDF = "pdf"
    JSON = "json"

    def __str__(self) -> str:
        return "application/" + self.value

    @property
    def ext(self) -> str:
        """Return the mime type file name extension."""
        return self.value

    @classmethod
    def members_str(cls) -> List[str]:
        """Return list of enum extension and mime type by string."""
        enums: List[str] = []
        for enum in cls:
            enums.append(enum.ext)
            enums.append(str(enum))

        return enums

    @classmethod
    def member_by(cls, member: str) -> Optional[MimeTypeApplication]:
        """Return matching enum by string match by either the extension or full
        mime type.
        """
        if member is not None:
            member = member.lower()
            for enum in cls:
                enum_str = str(enum)
                if enum_str in (member, "application/" + member):
                    return enum

        return None


class MimeTypeImage(MemberValueLower):
    """Image MIME Types. String image/type."""

    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    GIF = "gif"
    BMP = "bmp"
    WEBP = "webp"

    def __str__(self) -> str:
        return "image/" + self.value

    @property
    def ext(self) -> str:
        """Return the mime type file name extension."""
        return self.value

    @classmethod
    def members_str(cls) -> List[str]:
        """Return list of enum extension and mime type by string."""
        enums: List[str] = []
        for enum in cls:
            enums.append(enum.ext)
            enums.append(str(enum))

        return enums

    @classmethod
    def member_by(cls, member: str) -> Optional[MimeTypeImage]:
        """Return matching enum by string match by either the extension or full
        mime type.
        """
        if member is not None:
            member = member.lower()
            for enum in cls:
                enum_str = str(enum)
                if enum_str in (member, "image/" + member):
                    return enum

        return None


class MimeTypeText(MemberValueLower):
    """Text MIME Types. String text/type."""

    TXT = "txt"
    CSV = "csv"
    HTML = "html"

    def __str__(self) -> str:
        if self is MimeTypeText.TXT:
            return "text/plain"

        return "text/" + str(self.value)

    @property
    def ext(self) -> str:
        """Return the mime type file name extension."""
        return self.value

    @classmethod
    def members_str(cls) -> List[str]:
        """Return list of enum extension and mime type by string."""
        enums: List[str] = []
        for enum in cls:
            enums.append(enum.ext)
            enums.append(str(enum))

        return enums

    @classmethod
    def member_by(cls, member: str) -> Optional[MimeTypeText]:
        """Return matching enum by string match by either the extension or full
        mime type.
        """
        if member is not None:
            member = member.lower()
            for enum in cls:
                enum_str = str(enum)
                if enum_str in (member, "text/" + member):
                    return enum

            # One last try for oddity 'txt'.
            if member in (MimeTypeText.TXT.value, "text/plain"):
                return MimeTypeText.TXT

        return None


@dataclass
class MimeType:
    """Convenience class for providing the mime type."""

    mime_type: Union[MimeTypeApplication, MimeTypeImage, MimeTypeText]

    def __str__(self) -> str:
        return str(self.mime_type)

    @property
    def ext(self) -> str:
        """Return the mime type file name extension."""
        return self.mime_type.ext

    @staticmethod
    def members_str() -> List[str]:
        """Return the list of all mime type members."""
        members: List[str] = []
        for member in MimeTypeApplication.members_str():
            members.append(member)
        for member in MimeTypeImage.members_str():
            members.append(member)
        for member in MimeTypeText.members_str():
            members.append(member)

        return members

    @staticmethod
    def members() -> List[MimeType]:
        """Return the list of all mime type members."""
        members: List[MimeType] = []
        for member_app in MimeTypeApplication.members():
            members.append(member_app)
        for member_img in MimeTypeImage.members():
            members.append(member_img)
        for member_txt in MimeTypeText.members():
            members.append(member_txt)

        return members

    @staticmethod
    def member_by(
        member: str,
    ) -> Optional[MimeType]:
        """Return matching enum by string match by either the extension or full
        mime type.
        """
        if member is not None:
            match: Optional[Union[MimeTypeApplication, MimeTypeImage, MimeTypeText]]
            match = MimeTypeApplication.member_by(member=member)
            if match is None:
                match = MimeTypeImage.member_by(member=member)
            if match is None:
                match = MimeTypeText.member_by(member=member)

            if match is not None:
                return MimeType(mime_type=match)

        return None


class PathItemType(MemberNameLower):
    """Item type."""

    DIRECTORY = 0
    FILE = 1
    SYMLINK = 2
    OTHER = 3


class PathItemState(MemberNameLower):
    """Item state."""

    INCLUDED = 0
    EXCLUDED = 1


class Argparse(MemberNameLower):
    """Convenience Argparse elements to assist with None and other logic."""

    NOT_PROVIDED = "ARGPARSE_OPTION_NOT_PROVIDED"

    def __str__(self) -> str:
        return self.name.lower()
