"""OT3 Hardware Controller Backend."""

from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager
import logging
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Sequence,
    AsyncIterator,
    cast,
    Set,
    Union,
    Mapping,
)

from opentrons.config.types import OT3Config, GantryLoad
from opentrons.config import ot3_pipette_config, gripper_config
from .ot3utils import (
    axis_convert,
    create_move_group,
    get_current_settings,
    node_to_axis,
    axis_to_node,
    create_gripper_jaw_hold_group,
    create_gripper_jaw_grip_group,
    create_gripper_jaw_home_group,
    create_tip_action_group,
    PipetteAction,
)

from opentrons_hardware.firmware_bindings.constants import NodeId, SensorId
from opentrons_hardware.hardware_control.motion_planning import (
    Move,
    Coordinates,
)

from opentrons.hardware_control.module_control import AttachedModulesControl
from opentrons.hardware_control import modules
from opentrons.hardware_control.types import (
    BoardRevision,
    OT3Axis,
    OT3Mount,
    OT3AxisMap,
    CurrentConfig,
    InstrumentProbeType,
    MotorStatus,
    PipetteSubType,
    UpdateStatus,
)
from opentrons_hardware.hardware_control.motion import MoveStopCondition

from opentrons_shared_data.pipette.dev_types import PipetteName, PipetteModel
from opentrons_shared_data.gripper.gripper_definition import GripperModel
from opentrons.hardware_control.dev_types import (
    InstrumentHardwareConfigs,
    PipetteSpec,
    GripperSpec,
    OT3AttachedPipette,
    AttachedGripper,
    OT3AttachedInstruments,
)
from opentrons.util.async_helpers import ensure_yield

log = logging.getLogger(__name__)


class OT3Simulator:
    """OT3 Hardware Controller Backend."""

    _position: Dict[NodeId, float]
    _encoder_position: Dict[NodeId, float]
    _motor_status: Dict[NodeId, MotorStatus]

    @classmethod
    async def build(
        cls,
        attached_instruments: Dict[OT3Mount, Dict[str, Optional[str]]],
        attached_modules: List[str],
        config: OT3Config,
        loop: asyncio.AbstractEventLoop,
        strict_attached_instruments: bool = True,
    ) -> OT3Simulator:
        """Create the OT3Simulator instance.

        Args:
            config: Robot configuration

        Returns:
            Instance.
        """
        return cls(
            attached_instruments,
            attached_modules,
            config,
            loop,
            strict_attached_instruments,
        )

    def __init__(
        self,
        attached_instruments: Dict[OT3Mount, Dict[str, Optional[str]]],
        attached_modules: List[str],
        config: OT3Config,
        loop: asyncio.AbstractEventLoop,
        strict_attached_instruments: bool = True,
    ) -> None:
        """Construct.

        Args:
            config: Robot configuration
            driver: The Can Driver
        """
        self._configuration = config
        self._loop = loop
        self._strict_attached = bool(strict_attached_instruments)
        self._stubbed_attached_modules = attached_modules
        self._update_required = False

        def _sanitize_attached_instrument(
            mount: OT3Mount, passed_ai: Optional[Dict[str, Optional[str]]] = None
        ) -> Union[PipetteSpec, GripperSpec]:
            if mount is OT3Mount.GRIPPER:
                gripper_spec: GripperSpec = {"model": None, "id": None}
                if passed_ai and passed_ai.get("model"):
                    gripper_spec["model"] = GripperModel.v1
                    gripper_spec["id"] = passed_ai.get("id")
                return gripper_spec

            # TODO (lc 12-5-2022) need to not always pass in defaults here
            # but doing it to satisfy linter errors for now.
            pipette_spec: PipetteSpec = {"model": None, "id": None}
            if not passed_ai or not passed_ai.get("model"):
                return pipette_spec

            if ot3_pipette_config.supported_pipette(
                cast(PipetteModel, passed_ai["model"])
            ):
                pipette_spec["model"] = cast(PipetteModel, passed_ai.get("model"))
                pipette_spec["id"] = passed_ai.get("id")
                return pipette_spec
            # TODO (lc 12-05-2022) When the time comes we should properly
            # support backwards compatibility
            raise KeyError(
                "If you specify attached_instruments, the model "
                "should be pipette names or pipette models, but "
                f'{passed_ai["model"]} is not'
            )

        self._attached_instruments = {
            m: _sanitize_attached_instrument(m, attached_instruments.get(m))
            for m in OT3Mount
        }
        self._module_controls: Optional[AttachedModulesControl] = None
        self._position = self._get_home_position()
        self._encoder_position = self._get_home_position()
        self._motor_status = {}
        self._present_nodes: Set[NodeId] = set()
        self._current_settings: Optional[OT3AxisMap[CurrentConfig]] = None

    @property
    def board_revision(self) -> BoardRevision:
        """Get the board revision"""
        return BoardRevision.UNKNOWN

    @property
    def module_controls(self) -> AttachedModulesControl:
        """Get the module controls."""
        if self._module_controls is None:
            raise AttributeError("Module controls not found.")
        return self._module_controls

    @module_controls.setter
    def module_controls(self, module_controls: AttachedModulesControl) -> None:
        """Set the module controls"""
        self._module_controls = module_controls

    @ensure_yield
    async def update_to_default_current_settings(self, gantry_load: GantryLoad) -> None:
        self._current_settings = get_current_settings(
            self._configuration.current_settings, gantry_load
        )

    def _handle_motor_status_update(self, response: Dict[NodeId, float]) -> None:
        self._position.update(response)
        self._encoder_position.update(response)
        self._motor_status.update(
            (node, MotorStatus(True, True)) for node in response.keys()
        )

    @ensure_yield
    async def update_motor_status(self) -> None:
        """Retreieve motor and encoder status and position from all present nodes"""
        # Simulate condition at boot, status would not be ok
        self._motor_status.update(
            (node, MotorStatus(False, False)) for node in self._present_nodes
        )

    @ensure_yield
    async def update_motor_estimation(self, axes: Sequence[OT3Axis]) -> None:
        """Update motor position estimation for commanded nodes, and update cache of data."""
        # Simulate conditions as if there are no stalls, aka do nothing
        return None

    def check_ready_for_movement(self, axes: Sequence[OT3Axis]) -> bool:
        get_stat: Callable[
            [Sequence[OT3Axis]], List[Optional[MotorStatus]]
        ] = lambda ax: [self._motor_status.get(axis_to_node(a)) for a in ax]
        return all(
            isinstance(status, MotorStatus) and status.motor_ok
            for status in get_stat(axes)
        )

    @ensure_yield
    async def update_position(self) -> OT3AxisMap[float]:
        """Get the current position."""
        return axis_convert(self._position, 0.0)

    @ensure_yield
    async def update_encoder_position(self) -> OT3AxisMap[float]:
        """Get the encoder current position."""
        return axis_convert(self._encoder_position, 0.0)

    @ensure_yield
    async def liquid_probe(
        self,
        mount: OT3Mount,
        max_z_distance: float,
        mount_speed: float,
        plunger_speed: float,
        threshold_pascals: float,
        log_pressure: bool = True,
        sensor_id: SensorId = SensorId.S0,
    ) -> None:

        head_node = axis_to_node(OT3Axis.by_mount(mount))
        pos = self._position
        pos[head_node] = max_z_distance - 2
        self._position.update(pos)
        self._encoder_position.update(pos)

    @ensure_yield
    async def move(
        self,
        origin: Coordinates[OT3Axis, float],
        moves: List[Move[OT3Axis]],
        stop_condition: MoveStopCondition = MoveStopCondition.none,
    ) -> None:
        """Move to a position.

        Args:
            target_position: Map of axis to position.
            home_flagged_axes: Whether to home afterwords.
            speed: Optional speed
            axis_max_speeds: Optional map of axis to speed.

        Returns:
            None
        """
        _, final_positions = create_move_group(origin, moves, self._present_nodes)
        self._position.update(final_positions)
        self._encoder_position.update(final_positions)

    @ensure_yield
    async def home(self, axes: Optional[List[OT3Axis]] = None) -> OT3AxisMap[float]:
        """Home axes.

        Args:
            axes: Optional list of axes.

        Returns:
            Homed position.
        """
        if axes:
            homed = [axis_to_node(a) for a in axes]
        else:
            homed = list(self._position.keys())
        for h in homed:
            self._motor_status[h] = MotorStatus(True, True)
        return axis_convert(self._position, 0.0)

    @ensure_yield
    async def fast_home(
        self, axes: Sequence[OT3Axis], margin: float
    ) -> OT3AxisMap[float]:
        """Fast home axes.

        Args:
            axes: List of axes to home.
            margin: Margin

        Returns:
            New position.
        """
        homed = [axis_to_node(a) for a in axes] if axes else self._position.keys()
        for h in homed:
            self._motor_status[h] = MotorStatus(True, True)
        return axis_convert(self._position, 0.0)

    @ensure_yield
    async def gripper_grip_jaw(
        self,
        duty_cycle: float,
        stop_condition: MoveStopCondition = MoveStopCondition.none,
    ) -> None:
        """Move gripper inward."""
        _ = create_gripper_jaw_grip_group(duty_cycle, stop_condition)

    @ensure_yield
    async def gripper_home_jaw(self, duty_cycle: float) -> None:
        """Move gripper outward."""
        _ = create_gripper_jaw_home_group(duty_cycle)
        self._motor_status[NodeId.gripper_g] = MotorStatus(True, True)

    @ensure_yield
    async def gripper_hold_jaw(
        self,
        encoder_position_um: int,
    ) -> None:
        _ = create_gripper_jaw_hold_group(encoder_position_um)

    @ensure_yield
    async def tip_action(
        self,
        axes: Sequence[OT3Axis],
        distance: float = 33,
        speed: float = -5.5,
        tip_action: str = "drop",
    ) -> None:
        _ = create_tip_action_group(
            axes, distance, speed, cast(PipetteAction, tip_action)
        )

    def _attached_to_mount(
        self, mount: OT3Mount, expected_instr: Optional[PipetteName]
    ) -> OT3AttachedInstruments:
        init_instr = self._attached_instruments.get(mount, {"model": None, "id": None})  # type: ignore
        if mount is OT3Mount.GRIPPER:
            return self._attached_gripper_to_mount(cast(GripperSpec, init_instr))
        return self._attached_pipette_to_mount(
            mount, cast(PipetteSpec, init_instr), expected_instr
        )

    def _attached_gripper_to_mount(self, init_instr: GripperSpec) -> AttachedGripper:
        found_model = init_instr["model"]
        if found_model:
            return {
                "config": gripper_config.load(GripperModel.v1),
                "id": init_instr["id"],
            }
        else:
            return {"config": None, "id": None}

    def _attached_pipette_to_mount(
        self,
        mount: OT3Mount,
        init_instr: PipetteSpec,
        expected_instr: Optional[PipetteName],
    ) -> OT3AttachedPipette:
        found_model = init_instr["model"]

        # TODO (lc 12-05-2022) When the time comes, we should think about supporting
        # backwards compatability -- hopefully not relying on config keys only,
        # but TBD.
        if expected_instr and not ot3_pipette_config.supported_pipette(
            cast(PipetteModel, expected_instr)
        ):
            raise RuntimeError(
                f"mount {mount.name} requested a {expected_instr} which is not supported on the OT3"
            )
        if found_model and expected_instr and (expected_instr != found_model):
            if self._strict_attached:
                raise RuntimeError(
                    "mount {}: expected instrument {} but got {}".format(
                        mount.name, expected_instr, found_model
                    )
                )
            else:
                return {
                    "config": ot3_pipette_config.load_ot3_pipette(
                        ot3_pipette_config.convert_pipette_name(expected_instr)
                    ),
                    "id": None,
                }
        if found_model and expected_instr or found_model:
            # Instrument detected matches instrument expected (note:
            # "instrument detected" means passed as an argument to the
            # constructor of this class)

            # OR Instrument detected and no expected instrument specified
            return {
                "config": ot3_pipette_config.load_ot3_pipette(
                    ot3_pipette_config.convert_pipette_model(found_model)
                ),
                "id": init_instr["id"],
            }
        elif expected_instr:
            # Expected instrument specified and no instrument detected
            return {
                "config": ot3_pipette_config.load_ot3_pipette(
                    ot3_pipette_config.convert_pipette_name(expected_instr)
                ),
                "id": None,
            }
        else:
            # No instrument detected or expected
            return {"config": None, "id": None}

    @ensure_yield
    async def get_attached_instruments(
        self, expected: Mapping[OT3Mount, Optional[PipetteName]]
    ) -> Mapping[OT3Mount, OT3AttachedInstruments]:
        """Get attached instruments.

        Args:
            expected: Which mounts are expected.

        Returns:
            A map of mount to pipette name.
        """
        return {
            mount: self._attached_to_mount(mount, expected.get(mount))
            for mount in OT3Mount
        }

    @ensure_yield
    async def get_limit_switches(self) -> OT3AxisMap[bool]:
        """Get the state of the gantry's limit switches on each axis."""
        return {}

    @ensure_yield
    async def set_active_current(self, axis_currents: OT3AxisMap[float]) -> None:
        """Set the active current.

        Args:
            axis_currents: Axes' currents

        Returns:
            None
        """
        return None

    @asynccontextmanager
    async def restore_current(self) -> AsyncIterator[None]:
        """Save the current."""
        yield

    @ensure_yield
    async def watch(self, loop: asyncio.AbstractEventLoop) -> None:
        new_mods_at_ports = [
            modules.ModuleAtPort(port=f"/dev/ot_module_sim_{mod}{str(idx)}", name=mod)
            for idx, mod in enumerate(self._stubbed_attached_modules)
        ]
        await self.module_controls.register_modules(new_mods_at_ports=new_mods_at_ports)

    @property
    def axis_bounds(self) -> OT3AxisMap[Tuple[float, float]]:
        """Get the axis bounds."""
        # TODO (AL, 2021-11-18): The bounds need to be defined
        phony_bounds = (0, 10000)
        return {
            OT3Axis.Z_R: phony_bounds,
            OT3Axis.Z_L: phony_bounds,
            OT3Axis.P_L: phony_bounds,
            OT3Axis.P_R: phony_bounds,
            OT3Axis.Y: phony_bounds,
            OT3Axis.X: phony_bounds,
            OT3Axis.Z_G: phony_bounds,
        }

    @property
    def fw_version(self) -> Optional[str]:
        """Get the firmware version."""
        return None

    @property
    def update_required(self) -> bool:
        return self._update_required

    @update_required.setter
    def update_required(self, value: bool) -> None:
        if value != self._update_required:
            log.info(f"Firmware Update Flag set {self._update_required} -> {value}")
            self._update_required = value

    def get_update_progress(self) -> Tuple[Set[UpdateStatus], int]:
        return set(), 0

    async def update_firmware(
        self,
        attached_pipettes: Dict[OT3Mount, PipetteSubType],
        nodes: Optional[Set[NodeId]] = None,
    ) -> AsyncIterator[Tuple[Set[UpdateStatus], int]]:
        """Updates the firmware on the OT3."""
        yield (set(), 0)

    def engaged_axes(self) -> OT3AxisMap[bool]:
        """Get engaged axes."""
        return {}

    @ensure_yield
    async def disengage_axes(self, axes: List[OT3Axis]) -> None:
        """Disengage axes."""
        return None

    @ensure_yield
    async def engage_axes(self, axes: List[OT3Axis]) -> None:
        """Engage axes."""
        return None

    def set_lights(self, button: Optional[bool], rails: Optional[bool]) -> None:
        """Set the light states."""
        return None

    def get_lights(self) -> Dict[str, bool]:
        """Get the light state."""
        return {}

    def pause(self) -> None:
        """Pause the controller activity."""
        return None

    def resume(self) -> None:
        """Resume the controller activity."""
        return None

    @ensure_yield
    async def halt(self) -> None:
        """Halt the motors."""
        return None

    @ensure_yield
    async def hard_halt(self) -> None:
        """Halt the motors."""
        return None

    @ensure_yield
    async def probe(self, axis: OT3Axis, distance: float) -> OT3AxisMap[float]:
        """Probe."""
        return {}

    @ensure_yield
    async def clean_up(self) -> None:
        """Clean up."""
        pass

    @ensure_yield
    async def configure_mount(
        self, mount: OT3Mount, config: InstrumentHardwareConfigs
    ) -> None:
        """Configure a mount."""
        return None

    @staticmethod
    def _get_home_position() -> Dict[NodeId, float]:
        return {
            NodeId.head_l: 0,
            NodeId.head_r: 0,
            NodeId.gantry_x: 0,
            NodeId.gantry_y: 0,
            NodeId.pipette_left: 0,
            NodeId.pipette_right: 0,
            NodeId.gripper_z: 0,
            NodeId.gripper_g: 0,
        }

    @staticmethod
    def home_position() -> OT3AxisMap[float]:
        return {
            node_to_axis(k): v for k, v in OT3Simulator._get_home_position().items()
        }

    @ensure_yield
    async def probe_network(self) -> None:
        nodes = set((NodeId.head_l, NodeId.head_r, NodeId.gantry_x, NodeId.gantry_y))
        if self._attached_instruments[OT3Mount.LEFT].get("model", None):
            nodes.add(NodeId.pipette_left)
        if self._attached_instruments[OT3Mount.RIGHT].get("model", None):
            nodes.add(NodeId.pipette_right)
        if self._attached_instruments.get(
            OT3Mount.GRIPPER
        ) and self._attached_instruments[OT3Mount.GRIPPER].get("model", None):
            nodes.add(NodeId.gripper)
        self._present_nodes = nodes

    @ensure_yield
    async def capacitive_probe(
        self,
        mount: OT3Mount,
        moving: OT3Axis,
        distance_mm: float,
        speed_mm_per_s: float,
        sensor_threshold_pf: float,
        probe: InstrumentProbeType,
    ) -> None:
        self._position[axis_to_node(moving)] += distance_mm

    @ensure_yield
    async def capacitive_pass(
        self,
        mount: OT3Mount,
        moving: OT3Axis,
        distance_mm: float,
        speed_mm_per_s: float,
        probe: InstrumentProbeType,
    ) -> List[float]:
        self._position[axis_to_node(moving)] += distance_mm
        return []
