"""Shared utilities for ot3 hardware control."""
from typing import Dict, Iterable, List, Set, Tuple, TypeVar, Sequence
from typing_extensions import Literal
from opentrons.config.types import OT3MotionSettings, OT3CurrentSettings, GantryLoad
from opentrons.hardware_control.types import (
    OT3Axis,
    OT3AxisKind,
    OT3AxisMap,
    CurrentConfig,
    OT3SubSystem,
    OT3Mount,
    InstrumentProbeType,
    PipetteSubType,
    UpdateState,
    UpdateStatus,
)
import numpy as np

from opentrons_hardware.firmware_bindings.constants import (
    NodeId,
    PipetteType,
    SensorId,
    PipetteTipActionType,
)
from opentrons_hardware.firmware_update.types import FirmwareUpdateStatus, StatusElement
from opentrons_hardware.hardware_control.motion_planning import (
    AxisConstraints,
    SystemConstraints,
    Coordinates,
    Move,
    CoordinateValue,
)
from opentrons_hardware.hardware_control.tool_sensors import ProbeTarget
from opentrons_hardware.hardware_control.motion_planning.move_utils import (
    unit_vector_multiplication,
)
from opentrons_hardware.hardware_control.motion import (
    create_step,
    NodeIdMotionValues,
    create_home_step,
    MoveGroup,
    MoveType,
    MoveStopCondition,
    create_gripper_jaw_step,
    create_tip_action_step,
)

GRIPPER_JAW_HOME_TIME: float = 10
GRIPPER_JAW_GRIP_TIME: float = 10

PipetteAction = Literal["clamp", "home"]

# TODO: These methods exist to defer uses of NodeId to inside
# method bodies, which won't be evaluated until called. This is needed
# because the robot server doesn't have opentrons_ot3_firmware as a dep
# which is where they're defined, and therefore you can't have references
# to NodeId that are interpreted at import time because then the robot
# server tests fail when importing hardware controller. This is obviously
# terrible and needs to be fixed.

SUBSYSTEM_NODEID: Dict[OT3SubSystem, NodeId] = {
    OT3SubSystem.gantry_x: NodeId.gantry_x,
    OT3SubSystem.gantry_y: NodeId.gantry_y,
    OT3SubSystem.head: NodeId.head,
    OT3SubSystem.pipette_left: NodeId.pipette_left,
    OT3SubSystem.pipette_right: NodeId.pipette_right,
    OT3SubSystem.gripper: NodeId.gripper,
}


def axis_nodes() -> List["NodeId"]:
    return [
        NodeId.gantry_x,
        NodeId.gantry_y,
        NodeId.head_l,
        NodeId.head_r,
        NodeId.pipette_left,
        NodeId.pipette_right,
        NodeId.gripper_z,
        NodeId.gripper_g,
    ]


def node_axes() -> List[OT3Axis]:
    return [
        OT3Axis.X,
        OT3Axis.Y,
        OT3Axis.Z_L,
        OT3Axis.Z_R,
        OT3Axis.P_L,
        OT3Axis.P_R,
        OT3Axis.Z_G,
        OT3Axis.G,
    ]


def home_axes() -> List[OT3Axis]:
    return [
        OT3Axis.P_L,
        OT3Axis.P_R,
        OT3Axis.G,
        OT3Axis.Z_L,
        OT3Axis.Z_R,
        OT3Axis.Z_G,
        OT3Axis.X,
        OT3Axis.Y,
    ]


def axis_to_node(axis: OT3Axis) -> "NodeId":
    anm = {
        OT3Axis.X: NodeId.gantry_x,
        OT3Axis.Y: NodeId.gantry_y,
        OT3Axis.Z_L: NodeId.head_l,
        OT3Axis.Z_R: NodeId.head_r,
        OT3Axis.P_L: NodeId.pipette_left,
        OT3Axis.P_R: NodeId.pipette_right,
        OT3Axis.Z_G: NodeId.gripper_z,
        OT3Axis.G: NodeId.gripper_g,
        OT3Axis.Q: NodeId.pipette_left,
    }
    return anm[axis]


def node_to_axis(node: "NodeId") -> OT3Axis:
    nam = {
        NodeId.gantry_x: OT3Axis.X,
        NodeId.gantry_y: OT3Axis.Y,
        NodeId.head_l: OT3Axis.Z_L,
        NodeId.head_r: OT3Axis.Z_R,
        NodeId.pipette_left: OT3Axis.P_L,
        NodeId.pipette_right: OT3Axis.P_R,
        NodeId.gripper_z: OT3Axis.Z_G,
        NodeId.gripper_g: OT3Axis.G,
    }
    return nam[node]


def node_is_axis(node: "NodeId") -> bool:
    try:
        node_to_axis(node)
        return True
    except KeyError:
        return False


def axis_is_node(axis: OT3Axis) -> bool:
    try:
        axis_to_node(axis)
        return True
    except KeyError:
        return False


def sub_system_to_node_id(sub_sys: OT3SubSystem) -> "NodeId":
    """Convert a sub system to a NodeId."""
    return SUBSYSTEM_NODEID[sub_sys]


def node_id_to_subsystem(node_id: NodeId) -> "OT3SubSystem":
    """Convert a NodeId to a Subsystem"""
    node_to_subsystem = {
        node: subsystem for subsystem, node in SUBSYSTEM_NODEID.items()
    }
    return node_to_subsystem[node_id]


def get_current_settings(
    config: OT3CurrentSettings,
    gantry_load: GantryLoad,
) -> OT3AxisMap[CurrentConfig]:
    conf_by_pip = config.by_gantry_load(gantry_load)
    currents = {}
    for axis_kind in conf_by_pip["hold_current"].keys():
        for axis in OT3Axis.of_kind(axis_kind):
            currents[axis] = CurrentConfig(
                conf_by_pip["hold_current"][axis_kind],
                conf_by_pip["run_current"][axis_kind],
            )
    return currents


def get_system_constraints(
    config: OT3MotionSettings,
    gantry_load: GantryLoad,
) -> "SystemConstraints[OT3Axis]":
    conf_by_pip = config.by_gantry_load(gantry_load)
    constraints = {}
    for axis_kind in [
        OT3AxisKind.P,
        OT3AxisKind.X,
        OT3AxisKind.Y,
        OT3AxisKind.Z,
        OT3AxisKind.Z_G,
    ]:
        for axis in OT3Axis.of_kind(axis_kind):
            constraints[axis] = AxisConstraints.build(
                conf_by_pip["acceleration"][axis_kind],
                conf_by_pip["max_speed_discontinuity"][axis_kind],
                conf_by_pip["direction_change_speed_discontinuity"][axis_kind],
                conf_by_pip["default_max_speed"][axis_kind],
            )
    return constraints


def _convert_to_node_id_dict(
    axis_pos: Coordinates[OT3Axis, CoordinateValue],
) -> NodeIdMotionValues:
    target: NodeIdMotionValues = {}
    for axis, pos in axis_pos.items():
        if axis_is_node(axis):
            target[axis_to_node(axis)] = np.float64(pos)
    return target


def create_move_group(
    origin: Coordinates[OT3Axis, CoordinateValue],
    moves: List[Move[OT3Axis]],
    present_nodes: Iterable[NodeId],
    stop_condition: MoveStopCondition = MoveStopCondition.none,
) -> Tuple[MoveGroup, Dict[NodeId, float]]:
    pos = _convert_to_node_id_dict(origin)
    move_group: MoveGroup = []
    for move in moves:
        unit_vector = move.unit_vector
        for block in move.blocks:
            distances = unit_vector_multiplication(unit_vector, block.distance)
            node_id_distances = _convert_to_node_id_dict(distances)
            velocities = unit_vector_multiplication(unit_vector, block.initial_speed)
            accelerations = unit_vector_multiplication(unit_vector, block.acceleration)
            step = create_step(
                distance=node_id_distances,
                velocity=_convert_to_node_id_dict(velocities),
                acceleration=_convert_to_node_id_dict(accelerations),
                duration=block.time,
                present_nodes=present_nodes,
                stop_condition=stop_condition,
            )
            for ax in pos.keys():
                pos[ax] += node_id_distances.get(ax, 0)
            move_group.append(step)
    return move_group, {k: float(v) for k, v in pos.items()}


def create_home_group(
    distance: Dict[OT3Axis, float], velocity: Dict[OT3Axis, float]
) -> MoveGroup:
    node_id_distances = _convert_to_node_id_dict(distance)
    node_id_velocities = _convert_to_node_id_dict(velocity)
    step = create_home_step(
        distance=node_id_distances,
        velocity=node_id_velocities,
    )
    move_group: MoveGroup = [step]
    return move_group


def create_tip_action_group(
    axes: Sequence[OT3Axis], distance: float, velocity: float, action: PipetteAction
) -> MoveGroup:
    current_nodes = [axis_to_node(ax) for ax in axes]
    step = create_tip_action_step(
        velocity={node_id: np.float64(velocity) for node_id in current_nodes},
        distance={node_id: np.float64(distance) for node_id in current_nodes},
        present_nodes=current_nodes,
        action=PipetteTipActionType[action],
    )
    return [step]


def create_gripper_jaw_grip_group(
    duty_cycle: float,
    stop_condition: MoveStopCondition = MoveStopCondition.none,
) -> MoveGroup:
    step = create_gripper_jaw_step(
        duration=np.float64(GRIPPER_JAW_GRIP_TIME),
        duty_cycle=np.float32(duty_cycle),
        stop_condition=stop_condition,
        move_type=MoveType.grip,
    )
    move_group: MoveGroup = [step]
    return move_group


def create_gripper_jaw_home_group(dc: float) -> MoveGroup:
    step = create_gripper_jaw_step(
        duration=np.float64(GRIPPER_JAW_HOME_TIME),
        duty_cycle=np.float32(dc),
        stop_condition=MoveStopCondition.limit_switch,
        move_type=MoveType.home,
    )
    move_group: MoveGroup = [step]
    return move_group


def create_gripper_jaw_hold_group(encoder_position_um: int) -> MoveGroup:
    step = create_gripper_jaw_step(
        duration=np.float64(GRIPPER_JAW_GRIP_TIME),
        duty_cycle=np.float32(0),
        encoder_position_um=np.int32(encoder_position_um),
        stop_condition=MoveStopCondition.encoder_position,
        move_type=MoveType.linear,
    )
    move_group: MoveGroup = [step]
    return move_group


AxisMapPayload = TypeVar("AxisMapPayload")


def axis_convert(
    axis_map: Dict["NodeId", AxisMapPayload], default_value: AxisMapPayload
) -> OT3AxisMap[AxisMapPayload]:
    ret: OT3AxisMap[AxisMapPayload] = {k: default_value for k in node_axes()}
    for node, value in axis_map.items():
        if node_is_axis(node):
            ret[node_to_axis(node)] = value
    return ret


_sensor_node_lookup: Dict[OT3Mount, ProbeTarget] = {
    OT3Mount.LEFT: NodeId.pipette_left,
    OT3Mount.RIGHT: NodeId.pipette_right,
    OT3Mount.GRIPPER: NodeId.gripper,
}


def sensor_node_for_mount(mount: OT3Mount) -> ProbeTarget:
    return _sensor_node_lookup[mount]


_instr_sensor_id_lookup: Dict[InstrumentProbeType, SensorId] = {
    InstrumentProbeType.PRIMARY: SensorId.S0,
    InstrumentProbeType.SECONDARY: SensorId.S1,
}


def sensor_id_for_instrument(probe: InstrumentProbeType) -> SensorId:
    return _instr_sensor_id_lookup[probe]


_pipette_subtype_lookup = {
    PipetteSubType.pipette_single: PipetteType.pipette_single,
    PipetteSubType.pipette_multi: PipetteType.pipette_multi,
    PipetteSubType.pipette_96: PipetteType.pipette_96,
}


def pipette_type_for_subtype(pipette_subtype: PipetteSubType) -> PipetteType:
    return _pipette_subtype_lookup[pipette_subtype]


_update_state_lookup = {
    FirmwareUpdateStatus.queued: UpdateState.queued,
    FirmwareUpdateStatus.updating: UpdateState.updating,
    FirmwareUpdateStatus.done: UpdateState.done,
}


def fw_update_state_from_status(state: FirmwareUpdateStatus) -> UpdateState:
    return _update_state_lookup[state]


class UpdateProgress:
    """Class to keep track of Update progress."""

    def __init__(self, nodes: Set[NodeId]):
        self._tracker: Dict[OT3SubSystem, UpdateStatus] = {}
        self._total_progress = 0
        for node in nodes:
            subsystem = node_id_to_subsystem(node)
            self._tracker[subsystem] = UpdateStatus(subsystem, UpdateState.queued, 0)

    def get_progress(self) -> Tuple[Set[UpdateStatus], int]:
        """Gets the update status and total progress"""
        return set(self._tracker.values()), self._total_progress

    def update(
        self, node_id: NodeId, status_element: StatusElement
    ) -> Tuple[Set[UpdateStatus], int]:
        """Update internal states/progress of firmware updates."""
        fw_update_status, progress = status_element
        subsystem = node_id_to_subsystem(node_id)
        state = fw_update_state_from_status(fw_update_status)
        progress = int(progress * 100)
        self._tracker[subsystem] = UpdateStatus(subsystem, state, progress)
        # calculate the total progress of all updates
        progress_sum = 0
        for update_status in self._tracker.values():
            progress_sum += update_status.progress
        self._total_progress = int(progress_sum / len(self._tracker))
        return set(self._tracker.values()), self._total_progress
