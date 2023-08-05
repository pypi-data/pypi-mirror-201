""" Errors """


class PicoError(Exception):
    """All errors thrown explicitly by this package will be PicoError's."""


class FeatureNotSupportedError(PicoError):
    """Raised when a feature is not supported on the connected device."""


class CannotFindPicoSDKError(PicoError, IOError):
    """SDK can't be found"""


class CannotOpenPicoSDKError(PicoError, IOError):
    """SDK can't be opened"""


class DeviceNotFoundError(PicoError, IOError):
    pass


class ArgumentOutOfRangeError(PicoError, ValueError):
    pass


class ValidRangeEnumValueNotValidForThisDevice(FeatureNotSupportedError, ValueError):
    pass


class DeviceCannotSegmentMemoryError(FeatureNotSupportedError, TypeError):
    pass


class InvalidMemorySegmentsError(PicoError, ValueError):
    pass


class InvalidTimebaseError(PicoError, ValueError):
    pass


class InvalidTriggerParameters(PicoError, ValueError):
    pass


class InvalidCaptureParameters(PicoError, ValueError):
    pass


class PicoSDKCtypesError(PicoError, IOError):
    pass


class ClosedDeviceError(PicoError, IOError):
    pass


class NoChannelsEnabledError(PicoError, ValueError):
    pass


class NoValidTimebaseForOptionsError(PicoError, ValueError):
    pass


class UnknownConstantError(PicoError, TypeError):
    pass
