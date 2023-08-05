import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack

from picowrap import Channel, Picoscope

TIME_INTERVAL = 16E-9  # [s]
DURATION = 0.02  # [s]

fig, ax = plt.subplots(1, 2)

# with Picoscope("ps3000a", TIME_INTERVAL, DURATION) as pico:
with Picoscope("ps5000a", TIME_INTERVAL, DURATION, resolution=16) as pico:

    chan_A = Channel(pico, "A", "10V")
    chan_A.trigger(0.5, "ABOVE", 0, 0)
    # chan_B = Channel(pico, "B", "10V")
    # chan_C = Channel(pico, "C", "10V")
    # chan_D = Channel(pico, "D", "10V")

    pico.run()

    dataA = chan_A.get_values()
    # dataB = chan_B.get_values()
    # dataC = chan_C.get_values()
    # dataD = chan_D.get_values()

time_list = [i * TIME_INTERVAL for i in range(len(dataA))]
ft_data = fftpack.fft(dataA, axis=0)
frequencies = fftpack.fftfreq(len(dataA), TIME_INTERVAL)

Freq = frequencies[np.argmax(abs(ft_data))]

ax[0].clear()
ax[1].clear()
ax[0].plot(time_list, dataA)
ax[0].set_xlabel("Time (s)")
ax[0].set_ylabel("Voltage (V)")
ax[1].set_title(f"{Freq} Hz")
ax[1].plot(frequencies, abs(ft_data))
ax[1].set_xlabel("Period")
ax[1].set_ylabel("Power")
ax[1].set_xscale("log")
ax[1].set_yscale("log")

# while True:
    # plt.pause(0.5)
    # # break

plt.show()
