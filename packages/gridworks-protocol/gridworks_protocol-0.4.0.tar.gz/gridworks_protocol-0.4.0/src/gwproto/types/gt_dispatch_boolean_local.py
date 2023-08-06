"""Type gt.dispatch.boolean.local, version 110"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from gwproto.errors import MpSchemaError


def check_is_left_right_dot(v: str) -> None:
    """Checks LeftRightDot Format

    LeftRightDot format: Lowercase alphanumeric words separated by periods,
    most significant word (on the left) starting with an alphabet character.

    Args:
        v (str): the candidate

    Raises:
        ValueError: if v is not LeftRightDot format
    """
    from typing import List

    try:
        x: List[str] = v.split(".")
    except:
        raise ValueError(f"Failed to seperate {v} into words with split'.'")
    first_word = x[0]
    first_char = first_word[0]
    if not first_char.isalpha():
        raise ValueError(f"Most significant word of {v} must start with alphabet char.")
    for word in x:
        if not word.isalnum():
            raise ValueError(f"words of {v} split by by '.' must be alphanumeric.")
    if not v.islower():
        raise ValueError(f"All characters of {v} must be lowercase.")


def check_is_reasonable_unix_time_ms(v: int) -> None:
    """Checks ReasonableUnixTimeMs format

    ReasonableUnixTimeMs format: unix milliseconds between Jan 1 2000 and Jan 1 3000

    Args:
        v (int): the candidate

    Raises:
        ValueError: if v is not ReasonableUnixTimeMs format
    """
    import pendulum

    if pendulum.parse("2000-01-01T00:00:00Z").int_timestamp * 1000 > v:  # type: ignore[union-attr]
        raise ValueError(f"{v} must be after Jan 1 2000")
    if pendulum.parse("3000-01-01T00:00:00Z").int_timestamp * 1000 < v:  # type: ignore[union-attr]
        raise ValueError(f"{v} must be before Jan 1 3000")


class GtDispatchBooleanLocal(BaseModel):
    """Dispatch message sent locally by SCADA HomeAlone actor.

    By Locally, this means sent without access to Internet. The HomeAlone actor must reside within the Local Area Network of the SCADA - typically it should reside on the same hardware.
    """

    RelayState: int = Field(
        title="RelayState",
    )
    AboutNodeName: str = Field(
        title="AboutNodeName",
    )
    FromNodeName: str = Field(
        title="FromNodeName",
    )
    SendTimeUnixMs: int = Field(
        title="SendTimeUnixMs",
    )
    TypeName: Literal["gt.dispatch.boolean.local"] = "gt.dispatch.boolean.local"
    Version: str = "110"

    @validator("AboutNodeName")
    def _check_about_node_name(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(
                f"AboutNodeName failed LeftRightDot format validation: {e}"
            )
        return v

    @validator("FromNodeName")
    def _check_from_node_name(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(f"FromNodeName failed LeftRightDot format validation: {e}")
        return v

    @validator("SendTimeUnixMs")
    def _check_send_time_unix_ms(cls, v: int) -> int:
        try:
            check_is_reasonable_unix_time_ms(v)
        except ValueError as e:
            raise ValueError(
                f"SendTimeUnixMs failed ReasonableUnixTimeMs format validation: {e}"
            )
        return v

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))  # noqa


class GtDispatchBooleanLocal_Maker:
    type_name = "gt.dispatch.boolean.local"
    version = "110"

    def __init__(
        self,
        relay_state: int,
        about_node_name: str,
        from_node_name: str,
        send_time_unix_ms: int,
    ):
        self.tuple = GtDispatchBooleanLocal(
            RelayState=relay_state,
            AboutNodeName=about_node_name,
            FromNodeName=from_node_name,
            SendTimeUnixMs=send_time_unix_ms,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: GtDispatchBooleanLocal) -> str:
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> GtDispatchBooleanLocal:
        """
        Given a serialized JSON type object, returns the Python class object
        """
        try:
            d = json.loads(t)
        except TypeError:
            raise MpSchemaError("Type must be string or bytes!")
        if not isinstance(d, dict):
            raise MpSchemaError(f"Deserializing {t} must result in dict!")
        return cls.dict_to_tuple(d)

    @classmethod
    def dict_to_tuple(cls, d: dict[str, Any]) -> GtDispatchBooleanLocal:
        d2 = dict(d)
        if "RelayState" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing RelayState")
        if "AboutNodeName" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing AboutNodeName")
        if "FromNodeName" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing FromNodeName")
        if "SendTimeUnixMs" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing SendTimeUnixMs")
        if "TypeName" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing TypeName")

        return GtDispatchBooleanLocal(
            RelayState=d2["RelayState"],
            AboutNodeName=d2["AboutNodeName"],
            FromNodeName=d2["FromNodeName"],
            SendTimeUnixMs=d2["SendTimeUnixMs"],
            TypeName=d2["TypeName"],
            Version="110",
        )
