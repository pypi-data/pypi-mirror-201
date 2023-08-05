import threading
import time

import matplotlib.pyplot as plt

from picowrap import Channel, Picoscope

TIME_INTERVAL = 0.001  # [s]
DURATION = 1  # [s]

CHANNEL_DATA = []


def measure():

    with Picoscope("ps5000a", TIME_INTERVAL, DURATION, resolution=12) as pico:

        chan_a = Channel(pico, "A", "10V")
        chan_a.trigger(1, "ABOVE")

        pico.run()

        global CHANNEL_DATA  # pylint: disable=global-statement
        # Should be use in a class context do not use global in your code

        CHANNEL_DATA = chan_a.get_values()


def count_second():
    t_0 = time.time()
    for i in range(11):
        t_1 = time.time()
        print(f"{i} : {t_1-t_0:4f}")
        time.sleep(1)


thread_daq = threading.Thread(target=measure, daemon=True)
thread_daq.start()

count_second()
thread_daq.join()

time_data = [round(i * TIME_INTERVAL, 10) for i in range(len(CHANNEL_DATA))]
# enumerate is 0.04[s] slower in this case

plt.plot(time_data, CHANNEL_DATA)
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.show()
