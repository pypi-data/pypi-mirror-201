"""A base module interacting with the picoscope sdk.

For using this CBase you should have PicoSDK installed.
Check https://www.picotech.com/downloads

  Typical usage example:

  class Picoscope(Cpicoscope):

"""

import ctypes
import math
import os
from typing import Any

from picowrap import constants, errors


class CBase:
    """CPicoscope class for interacting with PicoSDK in python

    Attributes:
        status: A dict for storing sdk response,
        chandle: A c_int16 for storing handle,
        name: A str for accessing model relative dll and fonction in sdk
        clib_path: A str representing the dll path

        PICO_INFO: A dict for converting hex to str info
        PICO_STATUS: A dict for converting hex to str status
        PICO_STATUS_LOOKUP: Inverted dict of PICO_STATUS

    TODO: Docstring (from 118)
    """

    PICO_INFO = constants.PICO_INFO
    PICO_STATUS = constants.PICO_STATUS
    PICO_STATUS_LOOKUP = {v: k for k, v in PICO_STATUS.items()}
    VOLTAGE_COR = None  # Define in subclass
    # MAX_MEMORY = 2**29 = 536 MS (or better 512 MS)

    def __init__(self, name: str, sampling: float, resolution: Any) -> None:
        """Inits CPicoscope"""

        self.status: dict = {}
        self.chandle = ctypes.c_int16()
        self.name = name
        self.sampling = sampling
        self.resolution = resolution

        self.clib_path = self.find_clib()

    @property
    def timebase(self):
        raise NotImplementedError("To be define in subclass")

    def find_clib(self) -> str:
        """Find PicoSDK in PATH.

        Iterate through PATH directories to find the specific DLL relative to the entered path

        Raises:
            errors.CannotFindPicoSDKError: PicoSDK not found in PATH.

        Returns:
            str: fullpath of the DLL
        """
        for directory in os.environ["PATH"].split(os.pathsep):
            fname = os.path.join(directory, self.name) + ".dll"
            if os.path.isfile(fname):
                return fname
        raise errors.CannotFindPicoSDKError(
            f"PicoSDK {self.name} not found, check PATH"
        )

    @property
    def _clib(self) -> ctypes.WinDLL:
        """Load DLL

        Raises:
            errors.CannotOpenPicoSDKError: Opening DLL fail

        Returns:
           ctypes.WinDLL: DLL object
        """
        try:
            result = ctypes.WinDLL(self.clib_path)
        except OSError as err:
            raise errors.CannotOpenPicoSDKError(
                f"PicoSDK {self.name} not compatible (check 32 vs 64-bit): {err}"
            )
        return result

    def _assert_pico_ok(self, status: int) -> None:
        """Checks for PICO_OK status return else return specified Error

        Args:
            status (int): Status hex value

        Raises:
            errors.PicoSDKCtypesError: Response not ok
        """
        if status != self.PICO_STATUS["PICO_OK"]:
            raise errors.PicoSDKCtypesError(
                f"PicoSDK returned {self.PICO_STATUS_LOOKUP[status]}"
            )

    def _c_func(self, c_name: str, return_type, argument_types: list) -> Any:
        """Create a python c function

        Args:
            c_name (str): Function name
            return_type (c_uint32): Return type of the function
            argument_types (list[c_type]): List of c_type used in argument

        Returns:
            _type_: _description_
        """
        c_function = getattr(self._clib, c_name)
        c_function.restype = return_type
        c_function.argtypes = argument_types
        return c_function

    def open_unit(self, serial=None, resolution=None) -> None:
        """

        int16_t *handle,
        int8_t  *serial

        ### Raises:

        """
        c_name = self.name + "OpenUnit"
        return_type = ctypes.c_uint32

        serial = None  # Serial not implemented

        if resolution:
            argument_types = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int32]
            c_function = self._c_func(c_name, return_type, argument_types)
            resolution = constants.DEVICE_RES[resolution]
            cresolution = ctypes.c_int32()
            cresolution.value = resolution
            self.status["openunit"] = c_function(
                ctypes.byref(self.chandle), serial, cresolution
            )
        else:
            argument_types = [ctypes.c_void_p, ctypes.c_char_p]
            c_function = self._c_func(c_name, return_type, argument_types)
            self.status["openunit"] = c_function(ctypes.byref(self.chandle), serial)
        try:
            self._assert_pico_ok(self.status["openunit"])

        except errors.PicoSDKCtypesError as typerr:
            if self.PICO_STATUS_LOOKUP[self.status["openunit"]] == "PICO_NOT_FOUND":
                raise errors.DeviceNotFoundError(
                    f"Pico {self.name} not connected"
                ) from typerr

            powerstate = self.status["openunit"]

            if powerstate == 282:  # PICO_POWER_SUPPLY_NOT_CONNECTED
                self.status["ChangePowerSource"] = self._change_power_source(282)

            elif powerstate == 286:  # PICO_USB3_0_DEVICE_NON_USB3_0_PORT
                self.status["ChangePowerSource"] = self._change_power_source(286)
            else:
                raise errors.PicoError(
                    "[DEV] Status from openUnit not implemented"
                ) from typerr

    def set_data_buffers(
        self, channel, buff_max, buff_min, buff_len
    ) -> tuple[list[int], list[int]]:
        """

        # Handle = Chandle
        # source = ps3000A_channel_A = 0
        # Buffer max = ctypes.byref(bufferAMax)
        # Buffer min = ctypes.byref(bufferAMin)
        # Buffer length = maxsamples
        # Segment index = 0
        # Ratio mode = ps3000A_Ratio_Mode_None = 0

        int16_t            handle,
        int32_t            channel Or Port,
        int16_t           *bufferMax,
        int16_t           *bufferMin,
        int32_t            bufferLth,
        uint32_t           segmentIndex,
        PS3000a_RATIO_MODE mode
        """
        c_name = self.name + "SetDataBuffers"
        return_type = ctypes.c_uint32
        argument_types = [
            ctypes.c_int16,
            ctypes.c_int32,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_int32,
            ctypes.c_uint32,
            ctypes.c_int32,
        ]

        seg_index = 0
        ratio_mode = 0
        c_function = self._c_func(c_name, return_type, argument_types)
        self.status["SetDataBuffers"] = c_function(
            self.chandle,
            channel,
            ctypes.byref(buff_max),
            ctypes.byref(buff_min),
            buff_len,
            seg_index,
            ratio_mode,
        )
        self._assert_pico_ok(self.status["SetDataBuffers"])
        return buff_max, buff_min

    def is_ready(self):
        """
        int16_t  handle,
        int16_t *ready
        """
        c_name = self.name + "IsReady"
        return_type = ctypes.c_uint32
        argument_types = [ctypes.c_int16, ctypes.c_void_p]

        c_function = self._c_func(c_name, return_type, argument_types)

        ready = ctypes.c_int16(0)
        self.status["isReady"] = c_function(self.chandle, ctypes.byref(ready))
        return ready

    def run_block(self, pre_trig, post_trig, timebase, *args):
        """
        int16_t            handle,
        int32_t            noOfPreTriggerSamples,
        int32_t            noOfPostTriggerSamples,
        uint32_t           timebase,
        int16_t            oversample,
        int32_t           *timeIndisposedMs,
        uint32_t           segmentIndex,
        ps3000aBlockReady  lpReady,
        void              *pParameter
        """
        if not args:
            oversample = 0
            time_indisposed = None
            segment_index = 0
            lp_read = None
            p_parameter = None
        else:
            oversample, time_indisposed, segment_index, lp_read, p_parameter = args

        c_name = self.name + "RunBlock"
        return_type = ctypes.c_uint32
        argument_types = [
            ctypes.c_int16,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_uint32,
            ctypes.c_int16,
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_void_p,
            ctypes.c_void_p,
        ]

        c_function = self._c_func(c_name, return_type, argument_types)
        self.status["runblock"] = c_function(
            self.chandle,
            pre_trig,
            post_trig,
            timebase,
            oversample,
            time_indisposed,
            segment_index,
            lp_read,
            p_parameter,
        )
        self._assert_pico_ok(self.status["runblock"])

    def _change_power_source(self, powerstate: int):
        """
        Change power source
        """
        c_name = self.name + "ChangePowerSource"
        return_type = ctypes.c_uint32
        argument_types = [ctypes.c_int16, ctypes.c_uint32]

        c_function = self._c_func(c_name, return_type, argument_types)
        self.status["ChangePowerSource"] = c_function(self.chandle, powerstate)
        self._assert_pico_ok(self.status["ChangePowerSource"])
        return self.status["ChangePowerSource"]

    def set_channel(self, channel, enabled, coupling, voltage, offset):
        """
        channel = PS3000A_CHANNEL_A = 0
        enabled = 1
        coupling type = PS3000A_DC = 1
        range = PS3000A_10V = 8
        analogue offset = 0 V

        PS3000a_CHANNEL  channel,
        int16_t          enabled,
        PS3000a_COUPLING type,
        PS3000a_RANGE    range,
        float            analogOffset
        """
        c_name = self.name + "SetChannel"
        return_type = ctypes.c_uint32
        argument_types = [
            ctypes.c_int16,
            ctypes.c_int32,
            ctypes.c_int16,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_float,
        ]

        c_function = self._c_func(c_name, return_type, argument_types)
        self.status[f"setCh{channel}"] = c_function(
            self.chandle,
            channel,
            enabled,
            coupling,
            voltage,
            offset,
        )
        self._assert_pico_ok(self.status[f"setCh{channel}"])

    def set_simple_trigger(
        self, enable, source, threshold, direction, delay, autotrigger_ms
    ):
        """
        int16_t                      handle,
        int16_t                      enable,
        PS3000A_CHANNEL              source,
        int16_t                      threshold,
        PS3000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     delay,
        int16_t                      autoTrigger_ms
        Enable = 0
        Source = ps3000A_channel_A = 0
        Threshold = 1024 ADC counts
        Direction = ps3000A_Falling = 3
        Delay = 0
        autoTrigger_ms = 0
        """
        c_name = self.name + "SetSimpleTrigger"
        return_type = ctypes.c_uint32
        argument_types = [
            ctypes.c_int16,
            ctypes.c_int16,
            ctypes.c_int32,
            ctypes.c_int16,
            ctypes.c_int32,
            ctypes.c_uint32,
            ctypes.c_int16,
        ]

        c_function = self._c_func(c_name, return_type, argument_types)
        self.status["trigger"] = c_function(
            self.chandle,
            enable,
            source,
            threshold,
            direction,
            delay,
            autotrigger_ms,
        )
        self._assert_pico_ok(self.status["trigger"])

    def get_time_base_2(
        self, timebase: int, n_samples: int, oversample=1, segment_index=0
    ):
        """
        handle, device identifier returned by ps3000aOpenUnit
        timebase, see timebase guide. This value can be supplied to
        ps3000aRunBlock to define the sampling interval.
        noSamples, the number of samples required
        segmentIndex, the index of the memory segment to use

        * timeIntervalNanoseconds, on exit, the time interval between
        readings at the selected timebase. Use NULL if not required.
        oversample, not used
        * maxSamples, on exit, the maximum number of samples available.
        The scope allocates a certain amount of memory for internal
        overheads and this may vary depending on the number of segments,
        number of channels enabled, and the timebase chosen. Use NULL if
        not required.
        """
        c_name = self.name + "GetTimebase2"
        return_type = ctypes.c_uint32
        argument_types = [
            ctypes.c_int16,
            ctypes.c_uint32,
            ctypes.c_int32,
            ctypes.c_void_p,
            ctypes.c_int16,
            ctypes.c_void_p,
            ctypes.c_uint32,
        ]

        c_function = self._c_func(c_name, return_type, argument_types)

        time_interval_ns = ctypes.c_float()
        returned_max_samples = ctypes.c_int16()

        self.status["GetTimebase"] = c_function(
            self.chandle,
            timebase,
            n_samples,
            ctypes.byref(time_interval_ns),
            oversample,
            ctypes.byref(returned_max_samples),
            segment_index,
        )
        self._assert_pico_ok(self.status["GetTimebase"])
        return time_interval_ns.value, returned_max_samples.value

    def get_values(self, start_index, nb_samples, segment_index=0):
        """
        handle, device identifier returned by ps3000aOpenUnit
        startIndex, a zero-based index that indicates the start point for
        data collection. It is measured in sample intervals from the start of
        the buffer.
        * noOfSamples, on entry, the number of samples required. On exit,
        the actual number retrieved. The number of samples retrieved will
        not be more than the number requested, and the data retrieved
        starts at startIndex.
        downSampleRatio, the downsampling factor that will be applied to
        the raw data
        downSampleRatioMode, which downsampling mode to use. The
        available values are: -
        PS3000A_RATIO_MODE_NONE (downSampleRatio is ignored)
        PS3000A_RATIO_MODE_AGGREGATE
        PS3000A_RATIO_MODE_AVERAGE
        PS3000A_RATIO_MODE_DECIMATE
        AGGREGATE, AVERAGE, DECIMATE are single-bit constants that can be
        ORed to apply multiple downsampling modes to the same data
        segmentIndex, the zero-based number of the memory segment
        where the data is stored
        * overflow, on exit, a set of flags that indicate whether an
        overvoltage has occurred on
        # Handle = chandle
        # start index = 0
        # noOfSamples = ctypes.byref(cmaxSamples)
        # DownSampleRatio = 0
        # DownSampleRatioMode = 0
        # SegmentIndex = 0
        # Overflow = ctypes.byref(overflow)
        """
        c_name = self.name + "GetValues"
        return_type = ctypes.c_uint32
        argument_types = [
            ctypes.c_int16,
            ctypes.c_uint32,
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_int32,
            ctypes.c_uint32,
            ctypes.c_void_p,
        ]

        c_function = self._c_func(c_name, return_type, argument_types)

        down_sample_ratio = 0
        down_sample_ratio_mode = 0

        # overflow = (ctypes.c_int16 * 10)()
        overflow_input = ctypes.c_void_p(0)
        overflow = overflow_input

        self.status["GetValues"] = c_function(
            self.chandle,
            start_index,
            ctypes.byref(ctypes.c_int32(nb_samples)),
            down_sample_ratio,
            down_sample_ratio_mode,
            segment_index,
            ctypes.byref(overflow),
        )
        self._assert_pico_ok(self.status["GetValues"])

        if overflow_input != overflow:
            print(overflow.value)
        samples = nb_samples
        return samples

    def maximum_value(self) -> int:
        """
        int16_t  handle,
        int16_t *value
        """
        c_name = self.name + "MaximumValue"
        return_type = ctypes.c_uint32
        argument_types = [
            ctypes.c_int16,
            ctypes.c_void_p,
        ]

        c_function = self._c_func(c_name, return_type, argument_types)

        max_adc = ctypes.c_int16()

        self.status["maximumValue"] = c_function(self.chandle, ctypes.byref(max_adc))
        self._assert_pico_ok(self.status["maximumValue"])
        return max_adc.value

    def stop(self):
        c_name = self.name + "Stop"
        return_type = ctypes.c_uint32
        argument_types = [
            ctypes.c_int16,
        ]

        c_function = self._c_func(c_name, return_type, argument_types)

        self.status["stop"] = c_function(self.chandle)
        self._assert_pico_ok(self.status["stop"])

    def close_unit(self):
        c_name = self.name + "CloseUnit"
        return_type = ctypes.c_uint32
        argument_types = [ctypes.c_int16]

        c_function = self._c_func(c_name, return_type, argument_types)

        self.status["close"] = c_function(self.chandle)
        self._assert_pico_ok(self.status["close"])


class C3000a(CBase):
    VOLTAGE_COR = constants.VOLTAGE_COR["ps3000a"]

    @property
    def timebase(self):
        if self.sampling in [1e-9, 2e-9, 4e-9]:
            return int(math.log2(self.sampling * 1000000000))
        if (self.sampling * 1e9) % 8 == 0:
            return int(self.sampling * 125000000 + 2)
        raise errors.InvalidTimebaseError("Sampling should be 1, 2, 4, %8[ns]")

    def run_block(self, pre_trig, post_trig, timebase, *args):
        """
        int16_t            handle,
        int32_t            noOfPreTriggerSamples,
        int32_t            noOfPostTriggerSamples,
        uint32_t           timebase,
        # int16_t            oversample,
        int32_t           *timeIndisposedMs,
        uint32_t           segmentIndex,
        ps3000aBlockReady  lpReady,
        void              *pParameter
        """
        if not args:
            oversample = 0
            time_indisposed = None
            segment_index = 0
            lp_read = None
            p_parameter = None
        else:
            oversample, segment_index, lp_read, p_parameter = args

        c_name = self.name + "RunBlock"
        return_type = ctypes.c_uint32
        argument_types = [
            ctypes.c_int16,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_uint32,
            ctypes.c_int16,
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_void_p,
            ctypes.c_void_p,
        ]

        c_function = self._c_func(c_name, return_type, argument_types)
        self.status["runblock"] = c_function(
            self.chandle,
            pre_trig,
            post_trig,
            timebase,
            oversample,
            time_indisposed,
            segment_index,
            lp_read,
            p_parameter,
        )

        self._assert_pico_ok(self.status["runblock"])

    def get_time_base_2(
        self, timebase: int, n_samples: int, oversample=1, segment_index=0
    ):
        """
        handle, device identifier returned by ps3000aOpenUnit
        timebase, see timebase guide. This value can be supplied to
        ps3000aRunBlock to define the sampling interval.
        noSamples, the number of samples required
        segmentIndex, the index of the memory segment to use

        * timeIntervalNanoseconds, on exit, the time interval between
        readings at the selected timebase. Use NULL if not required.
        oversample, not used
        * maxSamples, on exit, the maximum number of samples available.
        The scope allocates a certain amount of memory for internal
        overheads and this may vary depending on the number of segments,
        number of channels enabled, and the timebase chosen. Use NULL if
        not required.
        """
        c_name = self.name + "GetTimebase2"
        return_type = ctypes.c_uint32
        argument_types = [
            ctypes.c_int16,
            ctypes.c_uint32,
            ctypes.c_int32,
            ctypes.c_void_p,
            ctypes.c_int16,
            ctypes.c_void_p,
            ctypes.c_uint32,
        ]

        c_function = self._c_func(c_name, return_type, argument_types)

        time_interval_ns = ctypes.c_float()
        returned_max_samples = ctypes.c_int16()

        self.status["GetTimebase"] = c_function(
            self.chandle,
            timebase,
            n_samples,
            ctypes.byref(time_interval_ns),
            oversample,
            ctypes.byref(returned_max_samples),
            segment_index,
        )
        self._assert_pico_ok(self.status["GetTimebase"])
        return time_interval_ns.value, returned_max_samples.value


class C5000a(CBase):
    VOLTAGE_COR = constants.VOLTAGE_COR["ps5000a"]

    @property
    def timebase(self):
        if self.resolution == 8:
            if self.sampling in [1e-9, 2e-9, 4e-9]:
                return int(math.log2(self.sampling * 1000000000))
            if (self.sampling * 1e9) % 8 == 0:
                return int(self.sampling * 125000000 + 2)
            raise errors.InvalidTimebaseError("Sampling should be 1, 2, 4, %8[ns]")
        if self.resolution == 12:
            if self.sampling in [2e-9, 4e-9, 8e-9]:
                return int(math.log2(self.sampling * 1000000000))
            if (self.sampling * 1e9) % 16 == 0:
                return int(self.sampling * 62500000 + 3)
            raise errors.InvalidTimebaseError("Sampling should be 2, 4, 8, %16[ns]")

        if self.resolution in [14, 15]:
            if self.sampling in [8e-9]:
                return 3
            if (self.sampling * 1e9) % 8 == 0:
                return int(self.sampling * 125000000 + 2)
            raise errors.InvalidTimebaseError("Sampling should be %8[ns]")

        if self.resolution == 16:
            if self.sampling in [16e-9]:
                return 4
            if (self.sampling * 1e9) % 16 == 0:
                return int(self.sampling * 62500000 + 3)
            raise errors.InvalidTimebaseError("Sampling should be %16[ns]")

    def run_block(self, pre_trig, post_trig, timebase, *args):
        """
        int16_t            handle,
        int32_t            noOfPreTriggerSamples,
        int32_t            noOfPostTriggerSamples,
        uint32_t           timebase,
        # int16_t            oversample,
        int32_t           *timeIndisposedMs,
        uint32_t           segmentIndex,
        ps3000aBlockReady  lpReady,
        void              *pParameter
        """
        if not args:
            oversample = 0
            # time_indisposed = None
            segment_index = 0
            lp_read = None
            p_parameter = None
        else:
            oversample, segment_index, lp_read, p_parameter = args

        c_name = self.name + "RunBlock"
        return_type = ctypes.c_uint32
        argument_types = [
            ctypes.c_int16,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_uint32,
            # ctypes.c_int16,
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_void_p,
            ctypes.c_void_p,
        ]

        c_function = self._c_func(c_name, return_type, argument_types)
        self.status["runblock"] = c_function(
            self.chandle,
            pre_trig,
            post_trig,
            timebase,
            oversample,
            # time_indisposed,
            segment_index,
            lp_read,
            p_parameter,
        )

        self._assert_pico_ok(self.status["runblock"])

    def get_time_base_2(
        self, timebase: int, n_samples: int, oversample=1, segment_index=0
    ):
        """
        handle, device identifier returned by ps3000aOpenUnit
        timebase, see timebase guide. This value can be supplied to
        ps3000aRunBlock to define the sampling interval.
        noSamples, the number of samples required
        segmentIndex, the index of the memory segment to use

        * timeIntervalNanoseconds, on exit, the time interval between
        readings at the selected timebase. Use NULL if not required.
        oversample, not used
        * maxSamples, on exit, the maximum number of samples available.
        The scope allocates a certain amount of memory for internal
        overheads and this may vary depending on the number of segments,
        number of channels enabled, and the timebase chosen. Use NULL if
        not required.
        """
        c_name = self.name + "GetTimebase2"
        return_type = ctypes.c_uint32
        argument_types = [
            ctypes.c_int16,
            ctypes.c_uint32,
            ctypes.c_int32,
            ctypes.c_void_p,
            # ctypes.c_int16,
            ctypes.c_void_p,
            ctypes.c_uint32,
        ]

        c_function = self._c_func(c_name, return_type, argument_types)

        time_interval_ns = ctypes.c_float()
        returned_max_samples = ctypes.c_int16()

        self.status["GetTimebase"] = c_function(
            self.chandle,
            timebase,
            n_samples,
            ctypes.byref(time_interval_ns),
            # oversample,
            ctypes.byref(returned_max_samples),
            segment_index,
        )
        self._assert_pico_ok(self.status["GetTimebase"])
        return time_interval_ns.value, returned_max_samples.value


class CPicoscope(CBase):
    def __new__(cls, name: str, *args, **kwargs):
        _ = args, kwargs
        mixin = {"ps3000a": C3000a, "ps5000a": C5000a}[name]
        cls_type = type(mixin.__name__, (cls, mixin), {})
        return super().__new__(cls_type)
