"""Type gt.sh.status, version 110"""
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from gwproto.errors import MpSchemaError
from gwproto.types.gt_sh_booleanactuator_cmd_status import GtShBooleanactuatorCmdStatus
from gwproto.types.gt_sh_booleanactuator_cmd_status import (
    GtShBooleanactuatorCmdStatus_Maker,
)
from gwproto.types.gt_sh_multipurpose_telemetry_status import (
    GtShMultipurposeTelemetryStatus,
)
from gwproto.types.gt_sh_multipurpose_telemetry_status import (
    GtShMultipurposeTelemetryStatus_Maker,
)
from gwproto.types.gt_sh_simple_telemetry_status import GtShSimpleTelemetryStatus
from gwproto.types.gt_sh_simple_telemetry_status import GtShSimpleTelemetryStatus_Maker


def check_is_reasonable_unix_time_s(v: int) -> None:
    """Checks ReasonableUnixTimeS format

    ReasonableUnixTimeS format: unix seconds between Jan 1 2000 and Jan 1 3000

    Args:
        v (int): the candidate

    Raises:
        ValueError: if v is not ReasonableUnixTimeS format
    """
    import pendulum

    if pendulum.parse("2000-01-01T00:00:00Z").int_timestamp > v:  # type: ignore[union-attr]
        raise ValueError(f"{v} must be after Jan 1 2000")
    if pendulum.parse("3000-01-01T00:00:00Z").int_timestamp < v:  # type: ignore[union-attr]
        raise ValueError(f"{v} must be before Jan 1 3000")


def check_is_uuid_canonical_textual(v: str) -> None:
    """Checks UuidCanonicalTextual format

    UuidCanonicalTextual format:  A string of hex words separated by hyphens
    of length 8-4-4-4-12.

    Args:
        v (str): the candidate

    Raises:
        ValueError: if v is not UuidCanonicalTextual format
    """
    try:
        x = v.split("-")
    except AttributeError as e:
        raise ValueError(f"Failed to split on -: {e}")
    if len(x) != 5:
        raise ValueError(f"{v} split by '-' did not have 5 words")
    for hex_word in x:
        try:
            int(hex_word, 16)
        except ValueError:
            raise ValueError(f"Words of {v} are not all hex")
    if len(x[0]) != 8:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[1]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[2]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[3]) != 4:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")
    if len(x[4]) != 12:
        raise ValueError(f"{v} word lengths not 8-4-4-4-12")


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


class GtShStatus(BaseModel):
    """.

    Status message sent by a Spaceheat SCADA every 5 minutes
    """

    FromGNodeAlias: str = Field(
        title="FromGNodeAlias",
    )
    FromGNodeId: str = Field(
        title="FromGNodeId",
    )
    AboutGNodeAlias: str = Field(
        title="AboutGNodeAlias",
    )
    SlotStartUnixS: int = Field(
        title="SlotStartUnixS",
    )
    ReportingPeriodS: int = Field(
        title="ReportingPeriodS",
    )
    SimpleTelemetryList: List[GtShSimpleTelemetryStatus] = Field(
        title="SimpleTelemetryList",
    )
    MultipurposeTelemetryList: List[GtShMultipurposeTelemetryStatus] = Field(
        title="MultipurposeTelemetryList",
    )
    BooleanactuatorCmdList: List[GtShBooleanactuatorCmdStatus] = Field(
        title="BooleanactuatorCmdList",
    )
    StatusUid: str = Field(
        title="StatusUid",
    )
    TypeName: Literal["gt.sh.status"] = "gt.sh.status"
    Version: str = "110"

    @validator("FromGNodeAlias")
    def _check_from_g_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(
                f"FromGNodeAlias failed LeftRightDot format validation: {e}"
            )
        return v

    @validator("FromGNodeId")
    def _check_from_g_node_id(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"FromGNodeId failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    @validator("AboutGNodeAlias")
    def _check_about_g_node_alias(cls, v: str) -> str:
        try:
            check_is_left_right_dot(v)
        except ValueError as e:
            raise ValueError(
                f"AboutGNodeAlias failed LeftRightDot format validation: {e}"
            )
        return v

    @validator("SlotStartUnixS")
    def _check_slot_start_unix_s(cls, v: int) -> int:
        try:
            check_is_reasonable_unix_time_s(v)
        except ValueError as e:
            raise ValueError(
                f"SlotStartUnixS failed ReasonableUnixTimeS format validation: {e}"
            )
        return v

    @validator("SimpleTelemetryList")
    def _check_simple_telemetry_list(cls, v: List) -> List:
        for elt in v:
            if not isinstance(elt, GtShSimpleTelemetryStatus):
                raise ValueError(
                    f"elt {elt} of SimpleTelemetryList must have type GtShSimpleTelemetryStatus."
                )
        return v

    @validator("MultipurposeTelemetryList")
    def _check_multipurpose_telemetry_list(cls, v: List) -> List:
        for elt in v:
            if not isinstance(elt, GtShMultipurposeTelemetryStatus):
                raise ValueError(
                    f"elt {elt} of MultipurposeTelemetryList must have type GtShMultipurposeTelemetryStatus."
                )
        return v

    @validator("BooleanactuatorCmdList")
    def _check_booleanactuator_cmd_list(cls, v: List) -> List:
        for elt in v:
            if not isinstance(elt, GtShBooleanactuatorCmdStatus):
                raise ValueError(
                    f"elt {elt} of BooleanactuatorCmdList must have type GtShBooleanactuatorCmdStatus."
                )
        return v

    @validator("StatusUid")
    def _check_status_uid(cls, v: str) -> str:
        try:
            check_is_uuid_canonical_textual(v)
        except ValueError as e:
            raise ValueError(
                f"StatusUid failed UuidCanonicalTextual format validation: {e}"
            )
        return v

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()

        # Recursively call as_dict() for the SubTypes
        simple_telemetry_list = []
        for elt in self.SimpleTelemetryList:
            simple_telemetry_list.append(elt.as_dict())
        d["SimpleTelemetryList"] = simple_telemetry_list

        # Recursively call as_dict() for the SubTypes
        multipurpose_telemetry_list = []
        for elt in self.MultipurposeTelemetryList:
            multipurpose_telemetry_list.append(elt.as_dict())
        d["MultipurposeTelemetryList"] = multipurpose_telemetry_list

        # Recursively call as_dict() for the SubTypes
        booleanactuator_cmd_list = []
        for elt in self.BooleanactuatorCmdList:
            booleanactuator_cmd_list.append(elt.as_dict())
        d["BooleanactuatorCmdList"] = booleanactuator_cmd_list
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))  # noqa


class GtShStatus_Maker:
    type_name = "gt.sh.status"
    version = "110"

    def __init__(
        self,
        from_g_node_alias: str,
        from_g_node_id: str,
        about_g_node_alias: str,
        slot_start_unix_s: int,
        reporting_period_s: int,
        simple_telemetry_list: List[GtShSimpleTelemetryStatus],
        multipurpose_telemetry_list: List[GtShMultipurposeTelemetryStatus],
        booleanactuator_cmd_list: List[GtShBooleanactuatorCmdStatus],
        status_uid: str,
    ):
        self.tuple = GtShStatus(
            FromGNodeAlias=from_g_node_alias,
            FromGNodeId=from_g_node_id,
            AboutGNodeAlias=about_g_node_alias,
            SlotStartUnixS=slot_start_unix_s,
            ReportingPeriodS=reporting_period_s,
            SimpleTelemetryList=simple_telemetry_list,
            MultipurposeTelemetryList=multipurpose_telemetry_list,
            BooleanactuatorCmdList=booleanactuator_cmd_list,
            StatusUid=status_uid,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: GtShStatus) -> str:
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> GtShStatus:
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
    def dict_to_tuple(cls, d: dict[str, Any]) -> GtShStatus:
        d2 = dict(d)
        if "FromGNodeAlias" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing FromGNodeAlias")
        if "FromGNodeId" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing FromGNodeId")
        if "AboutGNodeAlias" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing AboutGNodeAlias")
        if "SlotStartUnixS" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing SlotStartUnixS")
        if "ReportingPeriodS" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing ReportingPeriodS")
        if "SimpleTelemetryList" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing SimpleTelemetryList")
        simple_telemetry_list = []
        if not isinstance(d2["SimpleTelemetryList"], List):
            raise MpSchemaError("SimpleTelemetryList must be a List!")
        for elt in d2["SimpleTelemetryList"]:
            if not isinstance(elt, dict):
                raise MpSchemaError(
                    f"elt {elt} of SimpleTelemetryList must be "
                    "GtShSimpleTelemetryStatus but not even a dict!"
                )
            simple_telemetry_list.append(
                GtShSimpleTelemetryStatus_Maker.dict_to_tuple(elt)
            )
        d2["SimpleTelemetryList"] = simple_telemetry_list
        if "MultipurposeTelemetryList" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing MultipurposeTelemetryList")
        multipurpose_telemetry_list = []
        if not isinstance(d2["MultipurposeTelemetryList"], List):
            raise MpSchemaError("MultipurposeTelemetryList must be a List!")
        for elt in d2["MultipurposeTelemetryList"]:
            if not isinstance(elt, dict):
                raise MpSchemaError(
                    f"elt {elt} of MultipurposeTelemetryList must be "
                    "GtShMultipurposeTelemetryStatus but not even a dict!"
                )
            multipurpose_telemetry_list.append(
                GtShMultipurposeTelemetryStatus_Maker.dict_to_tuple(elt)
            )
        d2["MultipurposeTelemetryList"] = multipurpose_telemetry_list
        if "BooleanactuatorCmdList" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing BooleanactuatorCmdList")
        booleanactuator_cmd_list = []
        if not isinstance(d2["BooleanactuatorCmdList"], List):
            raise MpSchemaError("BooleanactuatorCmdList must be a List!")
        for elt in d2["BooleanactuatorCmdList"]:
            if not isinstance(elt, dict):
                raise MpSchemaError(
                    f"elt {elt} of BooleanactuatorCmdList must be "
                    "GtShBooleanactuatorCmdStatus but not even a dict!"
                )
            booleanactuator_cmd_list.append(
                GtShBooleanactuatorCmdStatus_Maker.dict_to_tuple(elt)
            )
        d2["BooleanactuatorCmdList"] = booleanactuator_cmd_list
        if "StatusUid" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing StatusUid")
        if "TypeName" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing TypeName")

        return GtShStatus(
            FromGNodeAlias=d2["FromGNodeAlias"],
            FromGNodeId=d2["FromGNodeId"],
            AboutGNodeAlias=d2["AboutGNodeAlias"],
            SlotStartUnixS=d2["SlotStartUnixS"],
            ReportingPeriodS=d2["ReportingPeriodS"],
            SimpleTelemetryList=d2["SimpleTelemetryList"],
            MultipurposeTelemetryList=d2["MultipurposeTelemetryList"],
            BooleanactuatorCmdList=d2["BooleanactuatorCmdList"],
            StatusUid=d2["StatusUid"],
            TypeName=d2["TypeName"],
            Version="110",
        )
