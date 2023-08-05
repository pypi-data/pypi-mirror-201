import time
from multiprocessing import Manager, Process

import matplotlib.pyplot as plt

from picowrap import Channel, Picoscope

TIME_INTERVAL = 0.001  # [s]
DURATION = 1  # [s]


def measure(return_data_dict):
    with Picoscope("ps5000a", TIME_INTERVAL, DURATION, resolution=12) as pico:

        chan_a = Channel(pico, "A", "10V")
        chan_a.trigger(1, "ABOVE")

        pico.run()
        chan_data = chan_a.get_values()

        time_data = [round(i * TIME_INTERVAL, 10) for i in range(len(chan_data))]
        # enumerate is 0.04[s] slower in this case

        return_data_dict["Time"] = time_data
        return_data_dict["Data"] = chan_data


def count_second():
    t_0 = time.time()
    for i in range(11):
        t_1 = time.time()
        print(f"{i} : {t_1-t_0:4f}")
        time.sleep(1)


if __name__ == "__main__":

    manager = Manager()
    return_dict = manager.dict()

    job0 = Process(target=measure, args=((return_dict),))
    job1 = Process(target=count_second)

    job0.start()
    job1.start()

    job0.join()

    print("Job0: Measure is Done")
    Time = return_dict["Time"]
    Data = return_dict["Data"]
    plt.plot(Time, Data)
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.show()

    job1.join()
