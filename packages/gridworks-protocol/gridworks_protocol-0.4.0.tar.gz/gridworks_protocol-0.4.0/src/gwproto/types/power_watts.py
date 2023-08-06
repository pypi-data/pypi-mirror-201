"""Type power.watts, version 000"""
import json
from typing import Any
from typing import Dict
from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from gwproto.errors import MpSchemaError


class PowerWatts(BaseModel):
    """Real-time power of TerminalAsset in Watts..

        Used by a SCADA -> Atn or Atn -> AggregatedTNode to report real-time power of their TerminalAsset. Positive number means WITHDRAWAL from the grid - so generating electricity creates a negative number. This message is considered worse than useless to send after the first attempt, and does not require an ack.

    Shares the same purpose as gs.pwr, but comes with extra meta data. The idea is this message, instantaneous reporting of power, is the highest priority message in the system and thus gets to have its metadata made explicit in the structure of the code instead of parameterized. One result is the size of the sent data is very small. Sometimes bandwidth can be an issue, and smaller messages are very useful.
    """

    Watts: int = Field(
        title="Current Power in Watts",
    )
    TypeName: Literal["power.watts"] = "power.watts"
    Version: str = "000"

    def as_dict(self) -> Dict[str, Any]:
        d = self.dict()
        return d

    def as_type(self) -> str:
        return json.dumps(self.as_dict())

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))  # noqa


class PowerWatts_Maker:
    type_name = "power.watts"
    version = "000"

    def __init__(self, watts: int):
        self.tuple = PowerWatts(
            Watts=watts,
            #
        )

    @classmethod
    def tuple_to_type(cls, tuple: PowerWatts) -> str:
        """
        Given a Python class object, returns the serialized JSON type object
        """
        return tuple.as_type()

    @classmethod
    def type_to_tuple(cls, t: str) -> PowerWatts:
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
    def dict_to_tuple(cls, d: dict[str, Any]) -> PowerWatts:
        d2 = dict(d)
        if "Watts" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing Watts")
        if "TypeName" not in d2.keys():
            raise MpSchemaError(f"dict {d2} missing TypeName")

        return PowerWatts(
            Watts=d2["Watts"],
            TypeName=d2["TypeName"],
            Version="000",
        )
