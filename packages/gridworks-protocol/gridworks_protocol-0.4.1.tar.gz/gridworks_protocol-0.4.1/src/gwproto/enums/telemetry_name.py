""" Enum with TypeName spaceheat.telemetry.name, Version 000, Status Active"""
from enum import auto
from typing import List

from fastapi_utils.enums import StrEnum


class TelemetryName(StrEnum):
    """
    Specifies the name of sensed data reported by a Spaceheat SCADA
    [More Info](https://gridworks-protocol.readthedocs.io/en/latest/telemetry-name.html).

    Name (EnumSymbol, Version): description
    
      * Unknown (00000000, 000): Default Value - unknown telemetry name
      * PowerW (af39eec9, 000): Power in Watts
      * RelayState (5a71d4b3, 000): State of a Relay. 0 means open, 1 means closed
      * WaterTempCTimes1000 (c89d0ba1, 000): Water temperature, in Degrees Celcius multiplied by 1000. So 43200 means 43.2 deg C
      * WaterTempFTimes1000 (793505aa, 000): Water temperature, in Degrees F multiplied by 1000. So 142100 means 142.1 deg F
      * GpmTimes100 (d70cce28, 000): Gallons Per Minute multiplied by 100. So 433 means 4.33 gallons per minute.
      * CurrentRmsMicroAmps (ad19e79c, 000): Current measurement in Root Mean Square MicroAmps
      * GallonsTimes100 (329a68c0, 000): Gallons multipled by 100
    """
    Unknown = auto()
    PowerW = auto()
    RelayState = auto()
    WaterTempCTimes1000 = auto()
    WaterTempFTimes1000 = auto()
    GpmTimes100 = auto()
    CurrentRmsMicroAmps = auto()
    GallonsTimes100 = auto()
    VoltageRmsMilliVolts = auto()
    MilliWattHours = auto()
    FrequencyMicroHz = auto()
    AirTempCTimes1000 = auto()
    AirTempFTimes1000 = auto()
    
    @classmethod
    def default(cls) -> "TelemetryName":
        """
        Returns default value Unknown
        """
        return cls.Unknown

    @classmethod
    def values(cls) -> List[str]:
        """
        Returns enum choices
        """
        return [elt.value for elt in cls]
