"""Type gt.driver.booleanactuator.cmd, version 100"""
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


class GtDriverBooleanactuatorCmd(BaseModel):
    """ """

    RelayState: int = Field(
        title="RelayState",
    )
    ShNodeAlias: str = Field(
        title="ShNodeAlias",
    )
    CommandTimeUnixMs: int = Field(
        title="CommandTimeUnixMs",
    )
    TypeName: Literal["gt.driver.booleanactuator.cmd"] = "gt.driver.booleanactuator.cmd"
    Version: str = "100"

    @validator("ShNodeAlias")
    def _check_sh_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(f"ShNodeAlias failed LeftRightDot format validation: {e}")
        return v

    @validator("CommandTimeUnixMs")
    def _check_command_time_unix_ms(cls, v: int) -> int:
        try:
            check_is_reasonable_unix_time_ms(v)
        except ValueError as e:
            raise ValueError(
                f"CommandTimeUnixMs failed ReasonableUnixTimeMs format validation: {e}"
            )
        return v

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))  # noqa


class GtDriverBooleanactuatorCmd_Maker:
    type_name = "gt.driver.booleanactuator.cmd"
    version = "100"

    def __init__(self, relay_state: int, sh_node_alias: str, command_time_unix_ms: int):
        self.tuple = GtDriverBooleanactuatorCmd(
            RelayState=relay_state,
            ShNodeAlias=sh_node_alias,
            CommandTimeUnixMs=command_time_unix_ms,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: GtDriverBooleanactuatorCmd) -> str:
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> GtDriverBooleanactuatorCmd:
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
    def dict_to_tuple(cls, d: dict[str, Any]) -> GtDriverBooleanactuatorCmd:
        d2 = dict(d)
        if "RelayState" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing RelayState")
        if "ShNodeAlias" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing ShNodeAlias")
        if "CommandTimeUnixMs" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing CommandTimeUnixMs")
        if "TypeName" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing TypeName")

        return GtDriverBooleanactuatorCmd(
            RelayState=d2["RelayState"],
            ShNodeAlias=d2["ShNodeAlias"],
            CommandTimeUnixMs=d2["CommandTimeUnixMs"],
            TypeName=d2["TypeName"],
            Version="100",
        )
