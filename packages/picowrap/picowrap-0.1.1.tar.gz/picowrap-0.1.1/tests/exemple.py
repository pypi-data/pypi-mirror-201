import matplotlib.pyplot as plt

from picowrap import Channel, Picoscope

TIME_INTERVAL = 16e-9  # [s]
DURATION = 0.5e-3  # [s]

# with Picoscope("ps3000a", TIME_INTERVAL, DURATION) as pico:
with Picoscope("ps5000a", TIME_INTERVAL, DURATION, resolution=12) as pico:

    chan_A = Channel(pico, "A", "10V")
    # chan_B = Channel(pico, "B", "10V")
    # chan_C = Channel(pico, "C", "10V")
    # chan_D = Channel(pico, "D", "10V")

    chan_A.trigger(4, "ABOVE", 0, 0)

    pico.run()

    dataA = chan_A.get_values()
    # dataB = chan_B.get_values()
    # dataC = chan_C.get_values()
    # dataD = chan_D.get_values()

time = [round(i * TIME_INTERVAL, 10) for i in range(len(dataA))]
# enumerate is 0.04[s] slower in this case

plt.plot(time, dataA)
# plt.plot(time, dataB)
# plt.plot(time, dataC)
# plt.plot(time, dataD)
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.show()
