<p align="center">
  <a href=""><img src="" alt="PicoWrap"></a>
</p>
<p align="center">
    <em>Picoscope SDK wrapper for python</em>
</p>
<p align="center">
<a href=""><img src="" alt="pipeline status"></a> 
</a>
<a href=""><img  src=""alt="coverage report"></a>
</a>
<a href="" target="_blank">
    <img src="https://img.shields.io/badge/version-0.1.0-blue" alt="Package version">
</a>
<a href="" target="_blank">
    <img src="https://img.shields.io/badge/python-3.10-brightgreen" alt="Supported Python versions">
</a>
</p>


---

**Documentation**: 

**Source Code**: 

---

## Requirements

Python 3.10+
PicoSDK September 16 2021

## Installation

```powershell
> pip install picowrap

---> 100%
```

## Examples

```Python
import matplotlib.pyplot as plt

from picowrap import Channel, Picoscope

TIME_INTERVAL = 0.00001  # [s]
DURATION = 0.5  # [s]

# with Picoscope("ps3000a", TIME_INTERVAL, DURATION) as pico:
with Picoscope("ps5000a", TIME_INTERVAL, DURATION, resolution=12) as pico:

    chan_A = Channel(pico, "A", "10V")
    chan_A.trigger(4, "ABOVE", 0, 0)

    pico.run()
    dataA = chan_A.get_values()

time = [round(i * TIME_INTERVAL, 10) for i in range(len(dataA))]
plt.plot(time, dataA)
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.show()

```


## License

TBD
