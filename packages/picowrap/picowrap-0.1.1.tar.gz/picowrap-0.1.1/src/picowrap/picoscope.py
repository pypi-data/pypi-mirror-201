import ctypes

from picowrap.cbase import CPicoscope


class Picoscope(CPicoscope):
    """Picoscope class for interact with picoscope

    Attributes:
        sampling: [s] Time between 2 mesures i.e: 0.0001[s]
        duration: [s] Total time of the mesure i.e: 1[s]

    TODO : warn for max memorie
    TODO : clean adress storage
    """

    # MAX_MEMORY = 2**29 = 536 MS (512 MS)

    def __init__(
        self, name: str, sampling: float, duration: float, resolution=None
    ) -> None:
        # super(Picoscope, self).__init__(name=name)
        super().__init__(name=name, sampling=sampling, resolution=resolution)
        self.name = name

        mid_sample = int(duration / (2 * sampling))
        self.trigscope = [mid_sample, mid_sample]
        self.sampling = sampling
        self.resolution = resolution

    def __enter__(self):
        self.open_unit(resolution=self.resolution)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close_unit()

    def run(self):
        self.run_block(self.trigscope[0], self.trigscope[1], self.timebase)
        self.wait_ready()

    def wait_ready(self):
        ready = ctypes.c_int16(0)
        check = ctypes.c_int16(0)
        while ready.value == check.value:
            ready = self.is_ready()
