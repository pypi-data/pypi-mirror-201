from typing import List, Optional, Union
import numpy as np


class TimeSeriesData:
    """
    A time series with `time` represented by an array of milliseconds since epoch and `data` represented
    by an array of data point values.

    :param time: Array of timestamps in milliseconds since epoch.
    :param data: Array of data point values.
    :param granularity: Granularity (in milliseconds) of the time series. If no value is provided, the granularity is calculated based on the `time` array.
    :param is_step: Whether the time series is a step time series. If no value is provided, the time series is considered continuous.
    """
    time: List[int]
    data: List[float]
    granularity: int
    is_step: bool
    def __init__(
            self,
            time: Union[List[int], np.ndarray[int]],
            data: Union[List[float], np.ndarray[float]],
            granularity: Optional[int],
            is_step: Optional[bool]
    ) -> "TimeSeriesData":
        """Creates a time series.

        :param time: Array of timestamps in milliseconds since epoch.
        :param data: Array of data point values.
        :param granularity: Granularity (in milliseconds) of the time series. If no value is provided, the granularity is calculated based on the `time` array.
        :param is_step: Whether the time series is a step time series. If no value is provided, the time series is considered continuous.
        :return: New TimeSeriesData object.
        """
        ...
    def equally_spaced_resampling(
            self,
            start_time: Optional[int],
            end_time: Optional[int],
            granularity: Optional[int]
    ) -> "TimeSeriesData":
        """Resamples the time series into an equally spaced time series.

        :param start_time: Defines the start time of the resampled array.
        :param end_time: Defines the end time of the resampled array.
        :param granularity: Defines the granularity (in milliseconds) of the resampled array.
        :return: Resampled time series.
        """
        ...
    def slice(self, start_time: int, end_time: int) -> "TimeSeriesData":
        """Slices the time series according to the provided boundaries.

        :param start_time: Defines the start time of the sliced array.
        :param end_time: Defines the end time of the sliced array.
        :return: Sliced time series.
        """
        ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...


def cpd_ed_pelt(data: Union[List[float], np.ndarray[float]], min_distance: int) -> List[int]:
    """The ED-PELT algorithm for change point detection.

    The algorithm detects change points in a given array of values, indicating moments when the statistical
    properties of the distribution are changing and the series can be divided into "statistically homogeneous"
    segments. This method supports nonparametric distributions and has an algorithmic complexity of O(N*log(N)).

    This implementation is adapted from a C# implementation created by Andrey Akinshin in 2019 and licensed under the
    MIT License https://opensource.org/licenses/MIT

    :param data: Array of data point values.
    :param min_distance: Minimum distance between change points.
    :return: Returns an array with 1-based indexes of change points. Change points correspond to the end of the
        detected segments. For example, change points for [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
        are [6, 12].
    """
    ...

def ssd_cpd(
        time_series: "TimeSeriesData",
        min_distance: int,
        var_threshold: float,
        slope_threshold: float
) -> "TimeSeriesData":
    """Detects steady state behavior in a time series using the ED Pelt change point detection algorithm.

    The time series is split into "statistically homogeneous" segments, and each segment is evaluated based on its
    normalized variance and the slope of the line of best fit. If a segment's variance or slope exceeds the given
    thresholds, it is considered a transient region, otherwise, it is labeled as steady region.

    :param time_series: TimeSeriesData object.
    :param min_distance: Minimum distance between change points.
    :param var_threshold: The variance threshold for determining steady state regions.
    :param slope_threshold: The slope threshold for determining steady state regions.
    :return: A tuple containing two lists: 1) timestamps; 2) steady state condition
        (0: transient region, 1: steady region) for all timestamps.
    """
    ...
