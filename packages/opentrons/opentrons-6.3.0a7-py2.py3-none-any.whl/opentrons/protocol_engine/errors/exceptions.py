"""Protocol engine exceptions."""


class ProtocolEngineError(RuntimeError):
    """Base Protocol Engine error class."""


class UnexpectedProtocolError(ProtocolEngineError):
    """An error raised when an unexpected error occurs.

    This error is indicative of a software bug. If it happens, it means an
    exception was raised somewhere in the stack and it was not properly caught
    and wrapped.
    """

    def __init__(self, original_error: Exception) -> None:
        """Initialize an UnexpectedProtocolError with an original error."""
        super().__init__(str(original_error))
        self.original_error: Exception = original_error


# TODO(mc, 2020-10-18): differentiate between pipette missing vs incorrect.
# By comparison, loadModule uses ModuleAlreadyPresentError and ModuleNotAttachedError.
class FailedToLoadPipetteError(ProtocolEngineError):
    """An error raised when executing a LoadPipette command fails.

    This failure may be caused by:
    - An incorrect pipette already attached to the mount
    - A missing pipette on the requested mount
    """


# TODO(mc, 2020-10-18): differentiate between pipette missing vs incorrect
class PipetteNotAttachedError(ProtocolEngineError):
    """An error raised when an operation's required pipette is not attached."""


class TipNotAttachedError(ProtocolEngineError):
    """An error raised when an operation's required pipette tip is not attached."""


class TipAttachedError(ProtocolEngineError):
    """An error raised when a tip shouldn't be attached, but is."""


class CommandDoesNotExistError(ProtocolEngineError):
    """An error raised when referencing a command that does not exist."""


class PipetteTipInfoNotFoundError(ProtocolEngineError):
    """An error raised when fetching information (like tiprack id) of attached tip."""


class LabwareNotLoadedError(ProtocolEngineError):
    """An error raised when referencing a labware that has not been loaded."""


class LabwareNotLoadedOnModuleError(ProtocolEngineError):
    """An error raised when referencing a labware on a module that has not been loaded."""


class LabwareNotOnDeckError(ProtocolEngineError):
    """An error raised when a labware can't be used because it's off-deck."""


class LiquidDoesNotExistError(ProtocolEngineError):
    """An error raised when referencing a liquid that has not been loaded."""


class LabwareDefinitionDoesNotExistError(ProtocolEngineError):
    """An error raised when referencing a labware definition that does not exist."""


class LabwareOffsetDoesNotExistError(ProtocolEngineError):
    """An error raised when referencing a labware offset that does not exist."""


class LabwareIsNotTipRackError(ProtocolEngineError):
    """An error raised when trying to use a regular labware as a tip rack."""


class LabwareIsTipRackError(ProtocolEngineError):
    """An error raised when trying to use a command not allowed on tip rack."""


class TouchTipDisabledError(ProtocolEngineError):
    """An error raised when touch tip is used on well with touchTipDisabled quirk."""


class WellDoesNotExistError(ProtocolEngineError):
    """An error raised when referencing a well that does not exist."""


class PipetteNotLoadedError(ProtocolEngineError):
    """An error raised when referencing a pipette that has not been loaded."""


class ModuleNotLoadedError(ProtocolEngineError):
    """And error raised when referencing a module that has not been loaded."""

    def __init__(self, *, module_id: str) -> None:
        super().__init__(f"Module {module_id} not found.")


class ModuleNotOnDeckError(ProtocolEngineError):
    """And error raised when trying to use a module that is loaded off the deck."""


class SlotDoesNotExistError(ProtocolEngineError):
    """An error raised when referencing a deck slot that does not exist."""


# TODO(mc, 2020-11-06): flesh out with structured data to replicate
# existing LabwareHeightError
class FailedToPlanMoveError(ProtocolEngineError):
    """An error raised when a requested movement could not be planned."""


class MustHomeError(ProtocolEngineError):
    """An error raised when motors must be homed due to unknown current position."""


class SetupCommandNotAllowedError(ProtocolEngineError):
    """An error raised when adding a setup command to a non-idle/non-paused engine."""


class PauseNotAllowedError(ProtocolEngineError):
    """An error raised when attempting to pause a run that is not running."""


class RunStoppedError(ProtocolEngineError):
    """An error raised when attempting to interact with a stopped engine."""


class ModuleNotAttachedError(ProtocolEngineError):
    """An error raised when a requested module is not attached."""


class ModuleAlreadyPresentError(ProtocolEngineError):
    """An error raised when a module is already present in a requested location."""


class WrongModuleTypeError(ProtocolEngineError):
    """An error raised when performing a module action on the wrong kind of module."""


class ThermocyclerNotOpenError(ProtocolEngineError):
    """An error raised when trying to move to labware that's covered inside a TC."""


class RobotDoorOpenError(ProtocolEngineError):
    """An error raised when executing a protocol command when a robot door is open."""


class PipetteMovementRestrictedByHeaterShakerError(ProtocolEngineError):
    """An error raised when trying to move to labware that's restricted by a module."""


class HeaterShakerLabwareLatchNotOpenError(ProtocolEngineError):
    """An error raised when heater-shaker latch is not open when it is expected to be so."""


class EngageHeightOutOfRangeError(ProtocolEngineError):
    """An error raised when a Magnetic Module engage height is out of bounds."""


class NoMagnetEngageHeightError(ProtocolEngineError):
    """Error raised if a Magnetic Module engage height is missing."""


class NoTargetTemperatureSetError(ProtocolEngineError):
    """An error raised when awaiting temperature when no target was set."""


class InvalidTargetTemperatureError(ProtocolEngineError):
    """An error raised when attempting to set an invalid target temperature."""


class InvalidBlockVolumeError(ProtocolEngineError):
    """An error raised when attempting to set an invalid block max volume."""


class InvalidTargetSpeedError(ProtocolEngineError):
    """An error raised when attempting to set an invalid target speed."""


class CannotPerformModuleAction(ProtocolEngineError):
    """An error raised when trying to perform an illegal hardware module action."""


class ProtocolCommandFailedError(ProtocolEngineError):
    """An error raised if a fatal command execution error has occurred."""


class HardwareNotSupportedError(ProtocolEngineError):
    """An error raised when executing a command on the wrong hardware."""


class GripperNotAttachedError(ProtocolEngineError):
    """An error raised when executing a gripper action without an attached gripper."""


class LabwareMovementNotAllowedError(ProtocolEngineError):
    """An error raised when attempting an illegal labware movement."""


class LocationIsOccupiedError(ProtocolEngineError):
    """An error raised when attempting to place labware in a non-empty location."""


class FirmwareUpdateRequired(ProtocolEngineError):
    """An error raised when the firmware needs to be updated."""


class PipetteNotReadyToAspirateError(ProtocolEngineError):
    """An error raised when the pipette is not ready to aspirate."""


class InvalidPipettingVolumeError(ProtocolEngineError):
    """An error raised when pipetting a volume larger than the pipette volume."""
