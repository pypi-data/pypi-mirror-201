use std::cmp;


/// Returns the mean value of a vector of floats
/// # Arguments
/// * `values` - Vector of floats
/// # Returns
/// * `f64` - Mean value of the vector
pub fn mean(values: &[f64]) -> f64 {
    let sum: f64 = values.iter().sum();
    sum / values.len() as f64
}

/// Returns the standard deviation of a vector of floats
/// # Arguments
/// * `values` - Vector of floats
/// # Returns
/// * `f64` - Standard deviation of the vector
pub fn std_dev(values: &[f64]) -> f64 {
    let mean = mean(values);
    let mut sum = 0.0;
    for value in values {
        sum += (value - mean).powi(2);
    }
    (sum / values.len() as f64).sqrt()
}

/// Generates a Vector of equally spaced integers between `start` and `end`
/// # Arguments
/// * `start` - The starting value of the vector
/// * `end` - The ending value of the vector
/// * `step` - The step size of the vector
/// # Returns
/// * `Vec<i64>` - A Vector of equally spaced integers between `start` and `end`
fn linspace_int(start: i64, stop: i64, step: i64) -> Vec<i64> {
    let mut ret = Vec::new();
    let mut i = start;
    while i <= stop {
        ret.push(i);
        i += step;
    }
    ret
}

/// Performs Linear Interpolation to predict an intermediary data point between two known data points
/// # Arguments
/// * `x0` - The first known x value
/// * `y0` - The first known y value
/// * `x1` - The second known x value
/// * `y1` - The second known y value
/// * `xp` - The x value to predict
/// # Returns
/// * `f64` - The predicted y value
fn linear_interpolation(x0: i64, y0: f64, x1: i64, y1: f64, xp: i64) -> f64 {
    let x0d = x0 as f64;
    let x1d = x1 as f64;
    let xpd = xp as f64;
    
    y0 + (y1 - y0) / (x1d - x0d) * (xpd - x0d)
}

/// Constrains a value to not exceed a maximum and minimum value
/// # Arguments
/// * `value` - The value to constrain
/// * `min` - The minimum value
/// * `max` - The maximum value
/// # Returns
/// * `f64` - The constrained value
pub fn constrain(value: f64, min: f64, max: f64) -> f64 {
    if value < min {
        min
    } else if value > max {
        max
    } else {
        value
    }
}

/// Calculates the slope of the best fit line for the provided x and y arrays
/// # Arguments
/// * `x` - The x values
/// * `y` - The y values
/// # Returns
/// * `f64` - The slope of the best fit line
pub fn get_line_slope(x: &[f64], y: &[f64]) -> f64 {
    let n: usize = y.len();
    let sum_x: f64 = x.iter().sum();
    let sum_y: f64 = y.iter().sum();
    let mut sum_xy: f64 = 0.0;
    let mut sum_xx: f64 = 0.0;

    for i in 0..n {
        sum_xy += x[i] * y[i];
        sum_xx += x[i] * x[i];
    }

    (n as f64 * sum_xy - sum_x * sum_y) / (n as f64 * sum_xx - sum_x * sum_x)
}

/// Sort an array of integers and return the indexes of the sorted array
/// # Arguments
/// * `array` - array to be sorted
/// # Returns
/// * `Vec<usize>` - sorted indexes
fn get_sort_indexes_int(arr: &[i64]) -> Vec<usize> {
    let mut result = vec![];
    for i in 0..arr.len() {
        result.push(i);
    }
    result.sort_by(|a, b| arr[*a].partial_cmp(&arr[*b]).unwrap());
    result
}

/// Sort an integer array based on a vector of indexes
/// # Arguments
/// * `array` - array to be sorted
/// * `indexes` - vector of indexes
/// # Returns
/// * `Vec<i64>` - sorted array
fn sort_by_indexes_int(arr: &[i64], indexes: &[usize]) -> Vec<i64> {
    let mut result = vec![];
    for i in 0..indexes.len() {
        result.push(arr[indexes[i]]);
    }
    result
}

/// Sort a float array based on a vector of indexes
/// # Arguments
/// * `array` - array to be sorted
/// * `indexes` - vector of indexes
/// # Returns
/// * `Vec<f64>` - sorted array
fn sort_by_indexes_float(arr: &[f64], indexes: &[usize]) -> Vec<f64> {
    let mut result = vec![];
    for i in 0..indexes.len() {
        result.push(arr[indexes[i]]);
    }
    result
}

/// Calculates the smallest delta between two values in a vector of integers
/// # Arguments
/// * `values` - Vector of integers
/// # Returns
/// * `i64` - Smallest delta between two values in the vector
pub fn calculate_delta_time(values: &Vec<i64>) -> i64 {
    if values.len() > 1 {
        let mut min_delta_time = values[1] - values[0];
        let n = values.len() - 1;
        for i in 1..n {
            let dt = values[i + 1] - values[i];
            if dt < min_delta_time {
                min_delta_time = dt;
            }
        }
        min_delta_time
    }
    else { 60000 } // Default to 1 minute if there is only one data point
}

/// Models a time series with `time` represented by an int array of milliseconds since epoch and
/// `data` represented by an double array of data point values.
pub struct TimeSeriesData {
    pub time: Vec<i64>,
    pub data: Vec<f64>,
    pub granularity: i64,
    pub is_step: bool,
}

impl TimeSeriesData {
    pub fn new(time: Vec<i64>, data: Vec<f64>, granularity: i64, is_step: bool) -> TimeSeriesData {
        if time.len() != data.len() {
            panic!("Time and data arrays must be the same length");
        }
        if time.is_empty() {
            panic!("Time and data arrays must be non-empty");
        }
        let mut ts = TimeSeriesData { time, data, granularity, is_step };
        ts.sort_by_time();
        ts.remove_duplicates();
        ts
    }

    /// Counts the number of data points in the time series
    pub fn get_count(&self) -> usize {
        self.time.len()
    }

    /// Returns the time of the first data point in the time series
    pub fn min_time(&self) -> i64 {
        self.time[0]
    }

    /// Returns the time of the last data point in the time series
    pub fn max_time(&self) -> i64 {
        self.time[self.time.len() - 1]
    }

    /// Checks if the time series contains gaps
    pub fn check_gaps(&self) -> bool {
        let points = (self.max_time() - self.min_time()) / self.granularity + 1;
        if points != self.get_count() as i64 {
            return true;
        }
        false
    }

    fn sort_by_time(&mut self) {
        let indexes = get_sort_indexes_int(&self.time);
        self.time = sort_by_indexes_int(&self.time, &indexes);
        self.data = sort_by_indexes_float(&self.data, &indexes);
    }

    fn remove_duplicates(&mut self) {
        let n = self.get_count();
        let mut time_unique = vec![];
        let mut data_unique = vec![];
        for i in 0..n {
            if !time_unique.contains(&self.time[i]) {
                time_unique.push(self.time[i]);
                data_unique.push(self.data[i]);
            }
        }
        self.time = time_unique;
        self.data = data_unique;
    }

    /// Resamples the time series into an equally spaced time series.
    /// # Arguments
    /// * `start_time` - Defines the start time of the resampled array.
    /// * `end_time` - Defines the end time of the resampled array.
    /// * `granularity` - Defines the granularity (in milliseconds) of the resampled array.
    /// # Returns
    /// * `TimeSeries` - The resampled time series.
    pub fn equally_spaced_resampling(
        &self,
        start_time: Option<i64>,
        end_time: Option<i64>,
        granularity: Option<i64>
    ) -> TimeSeriesData {
        let start_time = start_time.unwrap_or(self.min_time());
        let end_time = end_time.unwrap_or(self.max_time());
        let curr_granularity = granularity.unwrap_or(self.granularity);

        let time_resampled: Vec<i64>;
        let mut data_resampled: Vec<f64>;

        // it is only possible to extrapolate beyond the last data point for step time series
        if !self.is_step && (end_time > self.max_time()) {
            panic!("The given end_time would result in extrapolation which is only allowed for step time series.");
        }
        // It is not possible to extrapolate beyond the first data point for any time series
        if start_time < self.min_time() {
            panic!("The given start_time is before the start of the time series.");
        }

        // if there are no gaps in the time array and there is no need to extrapolate, we can skip the resampling
        if !self.check_gaps() && (end_time == self.max_time()) && (start_time == self.min_time()) {
            time_resampled = self.time.clone();
            data_resampled = self.data.clone();
        }
        else {
            time_resampled = linspace_int(start_time, end_time, curr_granularity);
            data_resampled = vec![0.0; time_resampled.len()];

            // counter for the original array index
            let mut i = 0;
            // counter for the resampled array index
            let mut j = 0;
            while j != data_resampled.len() {
                // the new point is positioned after the current point in the original array
                if time_resampled[j] > self.time[i]
                {
                    data_resampled[j] = self.resample(i, time_resampled[j]);
                    // we cannot increase i past the end of the original array
                    i = cmp::min(i + 1, self.time.len() - 1);
                }
                // the new point is positioned exactly on top of the current point in the original array
                else if time_resampled[j] == self.time[i]
                {
                    data_resampled[j] = self.data[i];
                    // we cannot increase i past the end of the original array
                    i = cmp::min(i + 1, self.time.len() - 1);
                }
                // the new point is positioned before the current point in the original array
                else if time_resampled[j] < self.time[i]
                {
                    data_resampled[j] = self.resample(i - 1, time_resampled[j]);
                }
                j += 1;
            }
        }
        TimeSeriesData::new(time_resampled, data_resampled, curr_granularity, self.is_step)
    }

    fn resample(&self, idx: usize, xp: i64) -> f64 {
        if self.is_step
        {
            self.data[idx]
        }
        else {
            linear_interpolation(
                self.time[idx], self.data[idx],
                self.time[idx + 1], self.data[idx + 1], xp
            )
        }
    }

    /// Slices the time series according to the provided boundaries.
    /// # Arguments
    /// * `start_time` - Defines the start time of the sliced array.
    /// * `end_time` - Defines the end time of the sliced array.
    /// # Returns
    /// * `TimeSeries` - The sliced time series.
    pub fn slice(&self, start_time: i64, end_time: i64) -> TimeSeriesData {
        let i0 = self.time.iter().position(|&r| r == start_time);
        let i1 = self.time.iter().position(|&r| r == end_time);
        if i0.is_some() && i1.is_some() {
            let i0 = i0.unwrap();
            let i1 = i1.unwrap();
            TimeSeriesData::new(
                self.time[i0..=i1].to_vec(),
                self.data[i0..=i1].to_vec(),
                self.granularity,
                self.is_step
            )
        }
        else {
            panic!("Invalid time range");
        }
    }

    /// Returns the average value of the data points in the time series.
    #[allow(dead_code)]
    pub fn get_average(&self) -> f64 {
        let ts_resampled = self.equally_spaced_resampling(
            None, None, None
        );
        mean(&ts_resampled.data)
    }

    /// Returns the standard deviation of the data points in the time series.
    #[allow(dead_code)]
    pub fn get_std(&self) -> f64 {
        let ts_resampled = self.equally_spaced_resampling(
            None, None, None
        );
        std_dev(&ts_resampled.data)
    }
}


#[cfg(test)]
mod tests {
    use approx::relative_eq;
    use super::*;

    #[test]
    fn test_time_series() {
        // Define inputs
        let ts_test_1 = TimeSeriesData::new(
            vec![1, 2, 5, 6, 8],
            vec![1., 2., 5., 6., 8.],
            1, false
        );
        let ts_test_step_1 = TimeSeriesData::new(
            vec![1, 2, 5, 6, 8],
            vec![1., 2., 5., 6., 8.],
            1, true
        );

        let ts_test_2 = TimeSeriesData::new(
            vec![2, 4, 5, 8, 8, 10, 11, 12, 14, 15, 17, 18],
            vec![1., 1., 2., 3., 5., 6., 5., 5., 3.5, 3.2, 3.1, 1.],
            1, false
        );
        let ts_test_step_2 = TimeSeriesData::new(
            vec![2, 4, 5, 8, 8, 10, 11, 12, 14, 15, 17, 18],
            vec![1., 1., 2., 3., 5., 6., 5., 5., 3.5, 3.2, 3.1, 1.],
            1, true
        );

        // test the min and max functions
        assert_eq!(ts_test_1.min_time(), 1);
        assert_eq!(ts_test_1.max_time(), 8);
        assert_eq!(ts_test_2.min_time(), 2);
        assert_eq!(ts_test_2.max_time(), 18);

        // test the resampling function
        let ts_resampled_1 = ts_test_1.equally_spaced_resampling(
            None, None, None
        );
        let ts_resampled_1_expected = TimeSeriesData::new(
            vec![1, 2, 3, 4, 5, 6, 7, 8],
            vec![1., 2., 3., 4., 5., 6., 7., 8.],
            1, false
        );
        for i in 0..ts_resampled_1_expected.get_count() {
            assert_eq!(ts_resampled_1.time[i], ts_resampled_1_expected.time[i]);
            assert_eq!(ts_resampled_1.data[i], ts_resampled_1_expected.data[i]);
        }

        let ts_resampled_2 = ts_test_2.equally_spaced_resampling(
            None, None, None
        );
        let ts_resampled_2_expected = TimeSeriesData::new(
            vec![2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            vec![
                1., 1., 1., 2., 2.33333, 2.66666, 3., 4.5, 6.,
                5., 5., 4.25, 3.5, 3.2, 3.15, 3.1, 1.
            ],
            1, false
        );
        for i in 0..ts_resampled_2_expected.get_count() {
            assert_eq!(ts_resampled_2.time[i], ts_resampled_2_expected.time[i]);
            let _ = relative_eq!(ts_resampled_2.data[i], ts_resampled_2_expected.data[i], epsilon = 1e-4);
        }

        let ts_resampled_step_1 = ts_test_step_1.equally_spaced_resampling(
            None, None, None
        );
        let ts_resampled_step_1_expected = TimeSeriesData::new(
            vec![1, 2, 3, 4, 5, 6, 7, 8],
            vec![1., 2., 2., 2., 5., 6., 6., 8.],
            1, true
        );
        for i in 0..ts_resampled_step_1_expected.get_count() {
            assert_eq!(ts_resampled_step_1.time[i], ts_resampled_step_1_expected.time[i]);
            assert_eq!(ts_resampled_step_1.data[i], ts_resampled_step_1_expected.data[i]);
        }

        let ts_resampled_step_2 = ts_test_step_2.equally_spaced_resampling(
            None, None, None
        );
        let ts_resampled_step_2_expected = TimeSeriesData::new(
            vec![2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            vec![1., 1., 1., 2., 2., 2., 3., 3., 6., 5., 5., 5., 3.5, 3.2, 3.2, 3.1, 1.],
            1, true
        );
        for i in 0..ts_resampled_step_2_expected.get_count() {
            assert_eq!(ts_resampled_step_2.time[i], ts_resampled_step_2_expected.time[i]);
            assert_eq!(ts_resampled_step_2.data[i], ts_resampled_step_2_expected.data[i]);
        }

        // test the extrapolation
        let ts_step_extrapolated = ts_test_step_1.equally_spaced_resampling(
            None, Some(10), None
        );
        let ts_step_extrapolated_expected = TimeSeriesData::new(
            vec![1, 2, 3, 4, 5, 6, 7, 8 , 9, 10],
            vec![1., 2., 2., 2., 5., 6., 6., 8., 8., 8.],
            1, true
        );
        for i in 0..ts_step_extrapolated_expected.get_count() {
            assert_eq!(ts_step_extrapolated.time[i], ts_step_extrapolated_expected.time[i]);
            assert_eq!(ts_step_extrapolated.data[i], ts_step_extrapolated_expected.data[i]);
        }

        // test time series slicing
        let ts_sliced = ts_test_1.slice(2, 6);
        let ts_sliced_expected = TimeSeriesData::new(
            vec![2, 5, 6],
            vec![2., 5., 6.],
            1, false
        );
        for i in 0..ts_sliced_expected.get_count() {
            assert_eq!(ts_sliced.time[i], ts_sliced_expected.time[i]);
            assert_eq!(ts_sliced.data[i], ts_sliced_expected.data[i]);
        }

        // test the average
        assert_eq!(ts_test_1.get_average(), 4.5);

        // test the standard deviation
        let _ = relative_eq!(ts_test_1.get_std(), 2.2912878, epsilon = 1e-4);
    }

    #[test]
    #[should_panic(expected = "The given end_time would result in extrapolation which is only allowed for step time series.")]
    fn test_invalid_extrapolation() {
        let ts_test = TimeSeriesData::new(
            vec![1, 2, 5, 6, 8],
            vec![1., 2., 5., 6., 8.],
            1, false
        );
        ts_test.equally_spaced_resampling(
            None, Some(10), None
        );
    }

    #[test]
    fn test_duplicate_removal() {
        let ts_with_duplicates = TimeSeriesData::new(
            vec![1, 2, 2, 5, 6, 6, 8],
            vec![1., 2., 2., 5., 6., 7., 8.],
            1, false
        );
        let ts_without_duplicates = TimeSeriesData::new(
            vec![1, 2, 5, 6, 8],
            vec![1., 2., 5., 6., 8.],
            1, false
        );
        for i in 0..ts_without_duplicates.get_count() {
            assert_eq!(ts_with_duplicates.time[i], ts_without_duplicates.time[i]);
            assert_eq!(ts_with_duplicates.data[i], ts_without_duplicates.data[i]);
        }
    }

    #[test]
    fn test_utils() {
        let data = vec![2.0, 6.0, 7.0, 1.2, -1.2, 6.0, 8.3, -5.5];
        let avg = mean(&data);
        assert_eq!(avg, 2.975);
        let std = std_dev(&data);
        let _ = relative_eq!(std, 4.4189223, epsilon = 1e-5);
    }
}