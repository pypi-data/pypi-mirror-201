# TimeScope

[![pypi](https://img.shields.io/pypi/v/timescope.svg)](https://pypi.python.org/pypi/timescope)
[![license](https://img.shields.io/github/license/evertoncolling/timescope.svg)](https://github.com/evertoncolling/timescope/blob/main/LICENSE)

Simple Python library written in Rust for analyzing and scoping out patterns in time series data. This is a pet project to practice programming in Rust and currently only contains two algorithms:
* ED-Pelt change point detection
* Steady State detection (based on change points)

## Install
```
pip install timescope
```

## Example Use
```python
from timescope import TimeSeriesData, cpd_ed_pelt, ssd_cpd

A = [0, 0, 0, 0, 10, 10, 10, 10, 10, 0, 0, 0, 0]
B = list(range(len(A)))

cps = cpd_ed_pelt(A, 1)
print(f"change points: {cps}")
# change points: [4, 9]

ts = TimeSeriesData(B, A)
print(ts)
# TimeSeriesData(
#   time=[0, 1, ..., 11, 12],
#   data=[0, 0, ..., 0, 0],
#   granularity=1,
#   is_step=false
# )

resampled_ts = ts.equally_spaced_resampling()
print(resampled_ts.slice(3, 6))
# TimeSeriesData(
#   time=[3, 4, 5, 6],
#   data=[0, 10, 10, 10],
#   granularity=1,
#   is_step=false
# )

ss_map = ssd_cpd(resampled_ts, 1, 1.0, -1.0)
print(f"steady state map: {ss_map.data}")
# steady state map: [1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0]
```

For more comprehensive examples, check the `notebooks` folder.