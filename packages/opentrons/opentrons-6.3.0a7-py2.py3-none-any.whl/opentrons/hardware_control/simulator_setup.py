import asyncio
from typing import Dict, Optional, Any, List, cast
from dataclasses import dataclass, asdict, field
import json
from pathlib import Path

from opentrons.config import robot_configs
from opentrons.config.types import RobotConfig
from opentrons.types import Mount
from opentrons.hardware_control import API, HardwareControlAPI, ThreadManager


# Name and kwargs for a module function
@dataclass(frozen=True)
class ModuleCall:
    function_name: str
    args: List[Any] = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SimulatorSetup:
    attached_instruments: Dict[Mount, Dict[str, Optional[str]]] = field(
        default_factory=dict
    )
    attached_modules: Dict[str, List[ModuleCall]] = field(default_factory=dict)
    config: Optional[RobotConfig] = None
    strict_attached_instruments: bool = True


async def create_simulator(
    setup: SimulatorSetup, loop: Optional[asyncio.AbstractEventLoop] = None
) -> HardwareControlAPI:
    """Create a simulator"""
    simulator = await API.build_hardware_simulator(
        attached_instruments=setup.attached_instruments,
        attached_modules=list(setup.attached_modules.keys()),
        config=setup.config,
        strict_attached_instruments=setup.strict_attached_instruments,
        loop=loop,
    )

    for attached_module in simulator.attached_modules:
        calls = setup.attached_modules[attached_module.name()]
        for call in calls:
            f = getattr(attached_module, call.function_name)
            await f(*call.args, **call.kwargs)

    return simulator


async def load_simulator(
    path: Path, loop: Optional[asyncio.AbstractEventLoop] = None
) -> HardwareControlAPI:
    """Create a simulator from a JSON file."""
    return await create_simulator(setup=load_simulator_setup(path), loop=loop)


async def load_simulator_thread_manager(
    path: Path,
) -> ThreadManager[HardwareControlAPI]:
    """Create a simulator wrapped in a ThreadManager from a JSON file."""
    setup = load_simulator_setup(path)
    thread_manager: ThreadManager[HardwareControlAPI] = ThreadManager(
        API.build_hardware_simulator,
        attached_instruments=setup.attached_instruments,
        attached_modules=list(setup.attached_modules.keys()),
        config=setup.config,
        strict_attached_instruments=setup.strict_attached_instruments,
    )
    await thread_manager.managed_thread_ready_async()

    for attached_module in thread_manager.wrapped().attached_modules:
        calls = setup.attached_modules[attached_module.name()]
        for call in calls:
            f = getattr(attached_module, call.function_name)
            await f(*call.args, **call.kwargs)

    return thread_manager


def save_simulator_setup(simulator_setup: SimulatorSetup, path: Path) -> None:
    """Write a simulator setup to a file."""
    as_dict = asdict(simulator_setup)
    as_dict = {k: _prepare_for_dict(k, v) for (k, v) in as_dict.items()}
    with path.open("w") as f:
        json.dump(as_dict, f)


def load_simulator_setup(path: Path) -> SimulatorSetup:
    """Load a simulator setup from a file."""
    with path.open() as f:
        obj = json.load(f)
        return SimulatorSetup(
            **{k: _prepare_for_simulator_setup(k, v) for (k, v) in obj.items()}
        )


def _prepare_for_dict(key: str, value: Dict[str, Any]) -> Dict[str, Any]:
    """Convert an element in SimulatorSetup to be a serializable dict"""
    if key == "attached_instruments" and value:
        return {
            mount.name.lower(): data
            for (mount, data) in cast(Dict[Mount, Any], value).items()
        }
    return value


def _prepare_for_simulator_setup(key: str, value: Dict[str, Any]) -> Any:
    """Convert value to a SimulatorSetup"""
    if key == "attached_instruments" and value:
        return {Mount[mount.upper()]: data for (mount, data) in value.items()}
    if key == "config" and value:
        return robot_configs.build_config_ot2(value)
    if key == "attached_modules" and value:
        return {k: [ModuleCall(**data) for data in v] for (k, v) in value.items()}
    return value
