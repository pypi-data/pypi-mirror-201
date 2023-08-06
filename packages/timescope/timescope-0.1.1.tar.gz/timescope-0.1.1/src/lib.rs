mod detect;
mod utils;
mod sample_data;

use pyo3::prelude::*;
use crate::utils::{TimeSeriesData, calculate_delta_time};
use crate::detect::{EdPelt, SteadyStateDetector};


#[derive(Clone)]
#[pyclass(name = "TimeSeriesData")]
struct TimeSeriesDataPy {
    #[pyo3(get)]
    time: Vec<i64>,
    #[pyo3(get)]
    data: Vec<f64>,
    #[pyo3(get)]
    granularity: Option<i64>,
    #[pyo3(get)]
    is_step: Option<bool>
}

#[pymethods]
impl TimeSeriesDataPy {
    #[new]
    fn init(
        time: Vec<i64>, data: Vec<f64>, granularity: Option<i64>, is_step: Option<bool>
    ) -> Self {
        let granularity = granularity.unwrap_or(
            calculate_delta_time(&time)
        );
        let is_step = is_step.unwrap_or(false);
        let ts = TimeSeriesData::new(time, data, granularity, is_step);
        let ts: TimeSeriesDataPy = ts.into();
        ts
    }
    fn equally_spaced_resampling(
        &self,
        start_time: Option<i64>,
        end_time: Option<i64>,
        granularity: Option<i64>
    ) -> TimeSeriesDataPy {
        let ts: TimeSeriesData = self.clone().into();
        let resampled_ts: TimeSeriesDataPy = ts.equally_spaced_resampling(
            start_time,
            end_time,
            granularity
        ).into();
        resampled_ts
    }
    fn slice(&self, start_time: i64, end_time: i64) -> TimeSeriesDataPy {
        let ts: TimeSeriesData = self.clone().into();
        let sliced_ts: TimeSeriesDataPy = ts.slice(start_time, end_time).into();
        sliced_ts
    }
    fn __repr__(&self) -> String {
        let n = &self.time.len();
        let time_display: String;
        let data_display: String;
        if n < &5 {
            time_display = self.time.iter()
                    .map(|x| x.to_string())
                    .collect::<Vec<String>>()
                    .join(", ");
            data_display = self.data.iter()
                    .map(|x| x.to_string())
                    .collect::<Vec<String>>()
                    .join(", ");
        } else {
            time_display = format!(
                "{}, {}, ..., {}, {}",
                &self.time[0], &self.time[1], &self.time[n-2], &self.time[n-1]
            );
            data_display = format!(
                "{}, {}, ..., {}, {}",
                &self.data[0], &self.data[1], &self.data[n-2], &self.data[n-1]
            );
        }
        format!(
            "TimeSeriesData(\n  time=[{}],\n  data=[{}],\n  granularity={},\n  is_step={}\n)",
            time_display,
            data_display,
            self.granularity.unwrap(),
            self.is_step.unwrap()
        )
    }
    fn __str__(&self) -> String {
        self.__repr__()
    }
}

impl From<TimeSeriesDataPy> for TimeSeriesData {
    fn from(value: TimeSeriesDataPy) -> Self {
        TimeSeriesData::new(
            value.time,
            value.data,
            value.granularity.unwrap(),
            value.is_step.unwrap()
        )
    }
}

impl From<TimeSeriesData> for TimeSeriesDataPy {
    fn from(value: TimeSeriesData) -> Self {
        TimeSeriesDataPy {
            time: value.time,
            data: value.data,
            granularity: Some(value.granularity),
            is_step: Some(value.is_step)
        }
    }
}

#[pyfunction]
fn cpd_ed_pelt(data: Vec<f64>, min_distance: usize) -> PyResult<Vec<i64>> {
    let cpd = EdPelt::new();
    let cp = cpd.get_change_point_indexes(&data, &min_distance);
    Ok(cp)
}

#[pyfunction]
fn ssd_cpd(
    time_series: TimeSeriesDataPy,
    min_distance: usize,
    var_threshold: f64,
    slope_threshold: f64
) -> PyResult<TimeSeriesDataPy> {
    let time_series: TimeSeriesData = time_series.into();
    let ssd = SteadyStateDetector::new();
    let ssd_map = ssd.get_steady_state_status(
        &time_series, &min_distance, &var_threshold, &slope_threshold);
    let ssd_map: TimeSeriesDataPy = ssd_map.into();
    Ok(ssd_map)
}

/// Simple Python library written in Rust for analyzing and scoping out patterns in time series
/// data.
#[pymodule]
fn timescope(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(cpd_ed_pelt, m)?)?;
    m.add_function(wrap_pyfunction!(ssd_cpd, m)?)?;
    m.add_class::<TimeSeriesDataPy>()?;
    Ok(())
}
