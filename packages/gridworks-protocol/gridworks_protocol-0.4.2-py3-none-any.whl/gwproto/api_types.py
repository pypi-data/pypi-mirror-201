""" List of all the types used"""
from typing import Dict
from typing import List
from typing import no_type_check

from gwproto.types import ComponentAttributeClassGt_Maker
from gwproto.types import ComponentGt_Maker
from gwproto.types import DataChannel_Maker
from gwproto.types import EgaugeIo_Maker
from gwproto.types import EgaugeRegisterConfig_Maker
from gwproto.types import ElectricMeterCacGt_Maker
from gwproto.types import ElectricMeterComponentGt_Maker
from gwproto.types import GtBooleanActuatorCac_Maker
from gwproto.types import GtBooleanActuatorComponent_Maker
from gwproto.types import GtDispatchBoolean_Maker
from gwproto.types import GtDispatchBooleanLocal_Maker
from gwproto.types import GtDriverBooleanactuatorCmd_Maker
from gwproto.types import GtShBooleanactuatorCmdStatus_Maker
from gwproto.types import GtShCliAtnCmd_Maker
from gwproto.types import GtShMultipurposeTelemetryStatus_Maker
from gwproto.types import GtShSimpleTelemetryStatus_Maker
from gwproto.types import GtShStatus_Maker
from gwproto.types import GtShTelemetryFromMultipurposeSensor_Maker
from gwproto.types import GtTelemetry_Maker
from gwproto.types import HeartbeatB_Maker
from gwproto.types import MultipurposeSensorCacGt_Maker
from gwproto.types import MultipurposeSensorComponentGt_Maker
from gwproto.types import PipeFlowSensorCacGt_Maker
from gwproto.types import PipeFlowSensorComponentGt_Maker
from gwproto.types import PowerWatts_Maker
from gwproto.types import ResistiveHeaterCacGt_Maker
from gwproto.types import ResistiveHeaterComponentGt_Maker
from gwproto.types import SimpleTempSensorCacGt_Maker
from gwproto.types import SimpleTempSensorComponentGt_Maker
from gwproto.types import SnapshotSpaceheat_Maker
from gwproto.types import SpaceheatNodeGt_Maker
from gwproto.types import TelemetryReportingConfig_Maker
from gwproto.types import TelemetrySnapshotSpaceheat_Maker


TypeMakerByName: Dict[str, HeartbeatB_Maker] = {}


@no_type_check
def type_makers() -> List[HeartbeatB_Maker]:
    return [
        ComponentAttributeClassGt_Maker,
        ComponentGt_Maker,
        DataChannel_Maker,
        EgaugeIo_Maker,
        EgaugeRegisterConfig_Maker,
        ElectricMeterCacGt_Maker,
        ElectricMeterComponentGt_Maker,
        GtBooleanActuatorCac_Maker,
        GtBooleanActuatorComponent_Maker,
        GtDispatchBoolean_Maker,
        GtDispatchBooleanLocal_Maker,
        GtDriverBooleanactuatorCmd_Maker,
        GtShBooleanactuatorCmdStatus_Maker,
        GtShCliAtnCmd_Maker,
        GtShMultipurposeTelemetryStatus_Maker,
        GtShSimpleTelemetryStatus_Maker,
        GtShStatus_Maker,
        GtShTelemetryFromMultipurposeSensor_Maker,
        GtTelemetry_Maker,
        HeartbeatB_Maker,
        MultipurposeSensorCacGt_Maker,
        MultipurposeSensorComponentGt_Maker,
        PipeFlowSensorCacGt_Maker,
        PipeFlowSensorComponentGt_Maker,
        PowerWatts_Maker,
        ResistiveHeaterCacGt_Maker,
        ResistiveHeaterComponentGt_Maker,
        SimpleTempSensorCacGt_Maker,
        SimpleTempSensorComponentGt_Maker,
        SnapshotSpaceheat_Maker,
        SpaceheatNodeGt_Maker,
        TelemetryReportingConfig_Maker,
        TelemetrySnapshotSpaceheat_Maker,
    ]


for maker in type_makers():
    TypeMakerByName[maker.type_name] = maker


def version_by_type_name() -> Dict[str, str]:
    """
    Returns:
        Dict[str, str]: Keys are TypeNames, values are versions
    """

    v: Dict[str, str] = {
        "component.attribute.class.gt": "000",
        "component.gt": "000",
        "data.channel": "000",
        "egauge.io": "000",
        "egauge.register.config": "000",
        "electric.meter.cac.gt": "000",
        "electric.meter.component.gt": "000",
        "gt.boolean.actuator.cac": "000",
        "gt.boolean.actuator.component": "000",
        "gt.dispatch.boolean": "110",
        "gt.dispatch.boolean.local": "110",
        "gt.driver.booleanactuator.cmd": "100",
        "gt.sh.booleanactuator.cmd.status": "100",
        "gt.sh.cli.atn.cmd": "110",
        "gt.sh.multipurpose.telemetry.status": "100",
        "gt.sh.simple.telemetry.status": "100",
        "gt.sh.status": "110",
        "gt.sh.telemetry.from.multipurpose.sensor": "100",
        "gt.telemetry": "110",
        "heartbeat.b": "001",
        "multipurpose.sensor.cac.gt": "000",
        "multipurpose.sensor.component.gt": "000",
        "pipe.flow.sensor.cac.gt": "000",
        "pipe.flow.sensor.component.gt": "000",
        "power.watts": "000",
        "resistive.heater.cac.gt": "000",
        "resistive.heater.component.gt": "000",
        "simple.temp.sensor.cac.gt": "000",
        "simple.temp.sensor.component.gt": "000",
        "snapshot.spaceheat": "000",
        "spaceheat.node.gt": "100",
        "telemetry.reporting.config": "000",
        "telemetry.snapshot.spaceheat": "000",
    }

    return v


def status_by_versioned_type_name() -> Dict[str, str]:
    """
    Returns:
        Dict[str, str]: Keys are versioned TypeNames, values are type status
    """

    v: Dict[str, str] = {
        "component.attribute.class.gt.000": "Active",
        "component.gt.000": "Active",
        "data.channel.000": "Active",
        "egauge.io.000": "Active",
        "egauge.register.config.000": "Active",
        "electric.meter.cac.gt.000": "Active",
        "electric.meter.component.gt.000": "Active",
        "gt.boolean.actuator.cac.000": "Active",
        "gt.boolean.actuator.component.000": "Active",
        "gt.dispatch.boolean.110": "Active",
        "gt.dispatch.boolean.local.110": "Active",
        "gt.driver.booleanactuator.cmd.100": "Active",
        "gt.sh.booleanactuator.cmd.status.100": "Active",
        "gt.sh.cli.atn.cmd.110": "Active",
        "gt.sh.multipurpose.telemetry.status.100": "Active",
        "gt.sh.simple.telemetry.status.100": "Active",
        "gt.sh.status.110": "Active",
        "gt.sh.telemetry.from.multipurpose.sensor.100": "Active",
        "gt.telemetry.110": "Active",
        "heartbeat.b.001": "Active",
        "multipurpose.sensor.cac.gt.000": "Active",
        "multipurpose.sensor.component.gt.000": "Active",
        "pipe.flow.sensor.cac.gt.000": "Active",
        "pipe.flow.sensor.component.gt.000": "Active",
        "power.watts.000": "Active",
        "resistive.heater.cac.gt.000": "Active",
        "resistive.heater.component.gt.000": "Active",
        "simple.temp.sensor.cac.gt.000": "Active",
        "simple.temp.sensor.component.gt.000": "Active",
        "snapshot.spaceheat.000": "Active",
        "spaceheat.node.gt.100": "Active",
        "telemetry.reporting.config.000": "Active",
        "telemetry.snapshot.spaceheat.000": "Active",
    }

    return v
