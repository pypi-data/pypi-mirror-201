"""Deck state accessors for the Protocol API."""
from dataclasses import dataclass
from typing import Iterator, List, Mapping, Optional, Tuple, Union

from opentrons_shared_data.deck.dev_types import SlotDefV3
from opentrons.motion_planning import adjacent_slots_getters
from opentrons.types import DeckLocation, DeckSlotName, Location, Point

from .core.common import ProtocolCore
from .core.core_map import LoadedCoreMap
from .labware import Labware
from .module_contexts import ModuleContext
from . import validation


DeckItem = Union[Labware, ModuleContext]


@dataclass(frozen=True)
class CalibrationPosition:
    """A calibration point on the deck of the robot.

    Attributes:
        id: Unique identifier for the calibration point.
        position: The absolute x, y, z coordinate of the point.
        displayName: A human-readable nickname for this point.
    """

    id: str
    position: Tuple[float, float, float]
    displayName: str


def _get_slot_name(slot_key: DeckLocation) -> DeckSlotName:
    try:
        return validation.ensure_deck_slot(slot_key)
    except (TypeError, ValueError) as error:
        raise KeyError(str(error)) from error


class Deck(Mapping[DeckLocation, Optional[DeckItem]]):
    """A dictionary-like object to access Protocol API objects loaded on the deck.

    Accessible via :py:meth:`ProtocolContext.deck`.
    """

    def __init__(self, protocol_core: ProtocolCore, core_map: LoadedCoreMap) -> None:
        self._protocol_core = protocol_core
        self._core_map = core_map

        deck_locations = protocol_core.get_deck_definition()["locations"]

        self._slot_definitions_by_name = {
            slot["id"]: slot for slot in deck_locations["orderedSlots"]
        }
        self._calibration_positions = [
            CalibrationPosition(
                id=point["id"],
                displayName=point["displayName"],
                position=(
                    point["position"][0],
                    point["position"][1],
                    point["position"][2],
                ),
            )
            for point in deck_locations["calibrationPoints"]
        ]

    def __getitem__(self, key: DeckLocation) -> Optional[DeckItem]:
        """Get the item, if any, located in a given slot."""
        slot_name = _get_slot_name(key)
        item_core = self._protocol_core.get_slot_item(slot_name)
        item = self._core_map.get(item_core)

        return item

    def __iter__(self) -> Iterator[str]:
        """Iterate through all deck slots."""
        return iter(self._slot_definitions_by_name)

    def __len__(self) -> int:
        """Get the number of slots on the deck."""
        return len(self._slot_definitions_by_name)

    def right_of(self, slot: DeckLocation) -> Optional[DeckItem]:
        """Get the item directly to the right of the given slot, if any."""
        slot_name = _get_slot_name(slot)
        east_slot = adjacent_slots_getters.get_east_slot(slot_name.as_int())

        return self[east_slot] if east_slot is not None else None

    def left_of(self, slot: DeckLocation) -> Optional[DeckItem]:
        """Get the item directly to the left of the given slot, if any."""
        slot_name = _get_slot_name(slot)
        west_slot = adjacent_slots_getters.get_west_slot(slot_name.as_int())

        return self[west_slot] if west_slot is not None else None

    def position_for(self, slot: DeckLocation) -> Location:
        """Get the absolute location of a deck slot's front-left corner."""
        slot_definition = self.get_slot_definition(slot)
        x, y, z = slot_definition["position"]

        return Location(point=Point(x, y, z), labware=slot_definition["id"])

    def get_slot_definition(self, slot: DeckLocation) -> SlotDefV3:
        """Get the geometric definition data of a slot."""
        slot_name = _get_slot_name(slot)
        return self._slot_definitions_by_name[slot_name.value]

    def get_slot_center(self, slot: DeckLocation) -> Point:
        """Get the absolute coordinates of a slot's center."""
        slot_name = _get_slot_name(slot)
        return self._protocol_core.get_slot_center(slot_name)

    @property
    def highest_z(self) -> float:
        """Get the height of the tallest known point on the deck."""
        return self._protocol_core.get_highest_z()

    @property
    def slots(self) -> List[SlotDefV3]:
        """Get a list of all slot definitions."""
        return list(self._slot_definitions_by_name.values())

    @property
    def calibration_positions(self) -> List[CalibrationPosition]:
        """Get a list of all calibration positions on the deck."""
        return list(self._calibration_positions)
