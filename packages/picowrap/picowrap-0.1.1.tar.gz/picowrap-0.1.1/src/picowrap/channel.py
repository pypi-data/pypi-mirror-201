import ctypes

from picowrap import constants
from picowrap.picoscope import Picoscope


class Channel:
    """Channel
    Picoscope instance

    Attributes:
        picoscope: Picoscope,
        name: str,
        voltage: str,
        coupling: str = "DC",
        offset: float = 0,

    """

    def __init__(
        self,
        picoscope: Picoscope,
        name: str,
        voltage: str,
        offset: float = 0,
        coupling: str = "DC",
    ) -> None:
        self.picoscope = picoscope

        self.number = constants.CHANNEL_COR[name]
        self.voltage = picoscope.VOLTAGE_COR[voltage.upper()]
        self.offset = offset
        self.coupling = constants.COUPLING_COR[coupling]

        self._create()

        self.maxsamples = sum(self.picoscope.trigscope)
        self.buffer_max = (ctypes.c_int16 * self.maxsamples)()
        self.buffer_min = (ctypes.c_int16 * self.maxsamples)()
        self.set_data_buffers()

    def _create(self):
        self.picoscope.set_channel(
            self.number,
            1,
            self.coupling,
            self.voltage,
            self.offset,
        )

    def trigger(self, threshold: float, direction: str, delay: int = 0, wait: int = 0):
        """
        threshold (float): the value in V at which the trigger will fire

        direction (str): the direction in which the signal must move to cause a
        trigger. The following directions are supported: ABOVE, BELOW,
        RISING, FALLING and RISING_OR_FALLING.

        delay (nb_samples): the time between the trigger occurring and the first sample.

        wait (ms): the number of milliseconds the device will wait
        if no trigger occurs. If this is set to zero,
        the scope device will wait indefinitely for a trigger.
        """

        adc_max = self.picoscope.maximum_value()
        adc_threshold = round(
            (threshold * adc_max) / constants.VOLTAGE_CON[self.voltage]
        )
        self.picoscope.set_simple_trigger(
            1,
            self.number,
            adc_threshold,
            constants.DIRECTION_COR[direction.upper()],
            delay,
            wait,
        )

    def set_data_buffers(self):
        self.picoscope.set_data_buffers(
            self.number, self.buffer_max, self.buffer_min, self.maxsamples
        )

    def get_values(self):
        nb_samples_in_buff = self.picoscope.get_values(0, self.maxsamples)
        if nb_samples_in_buff != self.maxsamples:
            print("nb_samples_in_buff != self.maxsamples")
            print(f"{nb_samples_in_buff} != {self.maxsamples}")

        max_value = self.picoscope.maximum_value()

        value = [
            x * constants.VOLTAGE_CON[self.voltage] / max_value for x in self.buffer_max
        ]
        time_interval_ns, _ = self.picoscope.get_time_base_2(
            self.picoscope.timebase, sum(self.picoscope.trigscope)
        )
        interval_selected = round(self.picoscope.sampling, 15)
        interval_real = round(time_interval_ns * 10**-9, 15)
        if interval_selected != interval_real:
            print(
                f"WARNING sampling ({interval_selected})",
                f"!= real time_interval ({interval_real}) ",
                f"Error = {interval_selected-interval_real} [s]",
            )

        return value
