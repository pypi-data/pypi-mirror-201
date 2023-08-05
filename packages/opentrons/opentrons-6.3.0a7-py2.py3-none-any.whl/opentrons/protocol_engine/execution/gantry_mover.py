"""Gantry movement wrapper for hardware and simulation based movement."""
from typing import Optional, List, Dict
from typing_extensions import Protocol as TypingProtocol

from opentrons.types import Point, Mount

from opentrons.hardware_control import HardwareControlAPI
from opentrons.hardware_control.types import Axis as HardwareAxis
from opentrons.hardware_control.errors import MustHomeError as HardwareMustHomeError

from opentrons.motion_planning import Waypoint

from ..state import StateView
from ..types import MotorAxis, CurrentWell
from ..errors import MustHomeError


_MOTOR_AXIS_TO_HARDWARE_AXIS: Dict[MotorAxis, HardwareAxis] = {
    MotorAxis.X: HardwareAxis.X,
    MotorAxis.Y: HardwareAxis.Y,
    MotorAxis.LEFT_Z: HardwareAxis.Z,
    MotorAxis.RIGHT_Z: HardwareAxis.A,
    MotorAxis.LEFT_PLUNGER: HardwareAxis.B,
    MotorAxis.RIGHT_PLUNGER: HardwareAxis.C,
}


class GantryMover(TypingProtocol):
    """Abstract class for gantry movement handler."""

    async def get_position(
        self,
        pipette_id: str,
        current_well: Optional[CurrentWell] = None,
        fail_on_not_homed: bool = False,
    ) -> Point:
        """Get the current position of the gantry."""
        ...

    def get_max_travel_z(self, pipette_id: str) -> float:
        """Get the maximum allowed z-height for pipette movement."""
        ...

    async def move_to(
        self, pipette_id: str, waypoints: List[Waypoint], speed: Optional[float]
    ) -> Point:
        """Move the hardware gantry to a waypoint."""
        ...

    async def move_relative(
        self,
        pipette_id: str,
        delta: Point,
        speed: Optional[float],
    ) -> Point:
        """Move the hardware gantry in a relative direction by delta."""
        ...

    async def home(self, axes: Optional[List[MotorAxis]]) -> None:
        """Home the gantry."""
        ...


class HardwareGantryMover(GantryMover):
    """Hardware API based gantry movement handler."""

    def __init__(self, hardware_api: HardwareControlAPI, state_view: StateView) -> None:
        self._hardware_api = hardware_api
        self._state_view = state_view

    async def get_position(
        self,
        pipette_id: str,
        current_well: Optional[CurrentWell] = None,
        fail_on_not_homed: bool = False,
    ) -> Point:
        """Get the current position of the gantry.

        Args:
            pipette_id: Pipette ID to get location data for.
            current_well: Optional parameter for getting pipette location data, effects critical point.
            fail_on_not_homed: Raise HardwareMustHomeError if gantry position is not known.
        """
        pipette_location = self._state_view.motion.get_pipette_location(
            pipette_id=pipette_id,
            current_well=current_well,
        )
        try:
            return await self._hardware_api.gantry_position(
                mount=pipette_location.mount.to_hw_mount(),
                critical_point=pipette_location.critical_point,
                fail_on_not_homed=fail_on_not_homed,
            )
        except HardwareMustHomeError as e:
            raise MustHomeError(str(e)) from e

    def get_max_travel_z(self, pipette_id: str) -> float:
        """Get the maximum allowed z-height for pipette movement.

        Args:
            pipette_id: Pipette ID to get max travel z-height for.
        """
        hw_mount = self._state_view.pipettes.get_mount(pipette_id).to_hw_mount()
        return self._hardware_api.get_instrument_max_height(mount=hw_mount)

    async def move_to(
        self, pipette_id: str, waypoints: List[Waypoint], speed: Optional[float]
    ) -> Point:
        """Move the hardware gantry to a waypoint."""
        assert len(waypoints) > 0, "Must have at least one waypoint"

        hw_mount = self._state_view.pipettes.get_mount(pipette_id).to_hw_mount()

        for waypoint in waypoints:
            await self._hardware_api.move_to(
                mount=hw_mount,
                abs_position=waypoint.position,
                critical_point=waypoint.critical_point,
                speed=speed,
            )

        return waypoints[-1].position

    async def move_relative(
        self,
        pipette_id: str,
        delta: Point,
        speed: Optional[float],
    ) -> Point:
        """Move the hardware gantry in a relative direction by delta.

        Args:
            pipette_id: Not used in hardware implementation.
            delta: Relative X/Y/Z distance to move gantry.
            speed: Optional speed parameter for the move.
        """
        pipette_location = self._state_view.motion.get_pipette_location(
            pipette_id=pipette_id,
        )
        critical_point = pipette_location.critical_point
        hw_mount = pipette_location.mount.to_hw_mount()
        try:
            await self._hardware_api.move_rel(
                mount=hw_mount,
                delta=delta,
                fail_on_not_homed=True,
                speed=speed,
            )
            point = await self._hardware_api.gantry_position(
                mount=hw_mount,
                critical_point=critical_point,
                fail_on_not_homed=True,
            )
        except HardwareMustHomeError as e:
            raise MustHomeError(str(e)) from e

        return point

    async def home(self, axes: Optional[List[MotorAxis]]) -> None:
        """Home the gantry."""
        # TODO(mc, 2022-12-01): this is overly complicated
        # https://opentrons.atlassian.net/browse/RET-1287
        if axes is None:
            await self._hardware_api.home()
        elif axes == [MotorAxis.LEFT_PLUNGER]:
            await self._hardware_api.home_plunger(Mount.LEFT)
        elif axes == [MotorAxis.RIGHT_PLUNGER]:
            await self._hardware_api.home_plunger(Mount.RIGHT)
        elif axes == [MotorAxis.LEFT_Z, MotorAxis.LEFT_PLUNGER]:
            await self._hardware_api.home_z(Mount.LEFT)
            await self._hardware_api.home_plunger(Mount.LEFT)
        elif axes == [MotorAxis.RIGHT_Z, MotorAxis.RIGHT_PLUNGER]:
            await self._hardware_api.home_z(Mount.RIGHT)
            await self._hardware_api.home_plunger(Mount.RIGHT)
        else:
            hardware_axes = [_MOTOR_AXIS_TO_HARDWARE_AXIS[a] for a in axes]
            await self._hardware_api.home(axes=hardware_axes)


class VirtualGantryMover(GantryMover):
    """State store based gantry movement handler for simulation/analysis."""

    def __init__(self, state_view: StateView) -> None:
        self._state_view = state_view

    async def get_position(
        self,
        pipette_id: str,
        current_well: Optional[CurrentWell] = None,
        fail_on_not_homed: bool = False,
    ) -> Point:
        """Get the current position of the gantry.

        Args:
            pipette_id: Pipette ID to get position for.
            current_well: Not used in virtual implementation.
            fail_on_not_homed: Not used in virtual implementation.
        """
        origin_deck_point = self._state_view.pipettes.get_deck_point(pipette_id)
        if origin_deck_point is not None:
            origin = Point(
                x=origin_deck_point.x, y=origin_deck_point.y, z=origin_deck_point.z
            )
        else:
            origin = Point(x=0, y=0, z=0)
        return origin

    def get_max_travel_z(self, pipette_id: str) -> float:
        """Get the maximum allowed z-height for pipette movement.

        Args:
            pipette_id: Pipette ID to get instrument height and tip length for.
        """
        instrument_height = self._state_view.pipettes.get_instrument_max_height_ot2(
            pipette_id
        )
        tip_length = self._state_view.tips.get_tip_length(pipette_id)
        return instrument_height - tip_length

    async def move_to(
        self, pipette_id: str, waypoints: List[Waypoint], speed: Optional[float]
    ) -> Point:
        """Move the hardware gantry to a waypoint. No-op in virtual implementation."""
        assert len(waypoints) > 0, "Must have at least one waypoint"
        return waypoints[-1].position

    async def move_relative(
        self,
        pipette_id: str,
        delta: Point,
        speed: Optional[float],
    ) -> Point:
        """Move the hardware gantry in a relative direction by delta.

        Args:
            pipette_id: Pipette ID to get position of for virtual move.
            delta: Relative X/Y/Z distance to move gantry.
            speed: Not used in virtual implementation.
        """
        origin = await self.get_position(pipette_id)
        return origin + delta

    async def home(self, axes: Optional[List[MotorAxis]]) -> None:
        """Home the gantry. No-op in virtual implementation."""
        pass


def create_gantry_mover(
    state_view: StateView, hardware_api: HardwareControlAPI
) -> GantryMover:
    """Create a tip handler."""
    return (
        HardwareGantryMover(hardware_api=hardware_api, state_view=state_view)
        if state_view.config.use_virtual_pipettes is False
        else VirtualGantryMover(state_view=state_view)
    )
