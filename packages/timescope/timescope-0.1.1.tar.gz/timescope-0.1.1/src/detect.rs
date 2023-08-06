use std::cmp;
use crate::utils::{constrain, get_line_slope, std_dev, mean, TimeSeriesData};

pub struct EdPelt {
    tolerance: f64,
}

/// The ED-PELT algorithm for change point detection.
///
/// The algorithm detects change points in a given array of values, indicating moments when the
/// statistical properties of the distribution are changing and the series can be divided into
/// "statistically homogeneous" segments. This method supports nonparametric distributions and has
/// an algorithmic complexity of O(N*log(N)).
///
/// This implementation is adapted from a C# implementation created by Andrey Akinshin in 2019 and
/// licensed under the MIT License https://opensource.org/licenses/MIT
impl EdPelt {
    pub fn new() -> Self {
        Self {
            tolerance: 1e-5,
        }
    }

    /// For given array of `float` values, detects locations of change points that splits original
    /// series of values into "statistically homogeneous" segments. Such points correspond to
    /// moments when statistical properties of the distribution are changing.
    ///
    /// This method supports nonparametric distributions and has O(N*log(N)) algorithmic
    /// complexity.
    ///
    /// # Arguments
    /// * `data` - An array of float values
    /// * `min_distance` - Minimum distance between change points
    ///
    /// # Returns
    /// Returns an `Vec<i64>` array with 1-based indexes of change points. Change points correspond
    /// to the end of the detected segments. For example, change points for { 0, 0, 0, 0, 0, 0, 1,
    /// 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2 } are { 6, 12 }.
    pub fn get_change_point_indexes(&self, data: &[f64], min_distance: &usize) -> Vec<i64> {
        // We will use `n` as the number of elements in the `data` array
        let n = data.len();

        // Checking corner cases
        if n <= 2 {
            let res: Vec<i64> = vec![];
            return res;
        }
        if *min_distance < 1 || *min_distance > n {
            panic!("min_distance must be in the range [1, {}]", n);
        }

        // The penalty which we add to the final cost for each additional change point
        // Here we use the Modified Bayesian Information Criterion
        let penalty: f64 = 3.0 * (n as f64).ln();

        // `k` is the number of quantiles that we use to approximate an integral during the segment
        // cost evaluation. We use `k=Ceiling(4*log(n))` as suggested in the Section 4.3 "Choice of
        // K in ED-PELT" in [Haynes2017]. `k` can't be greater than `n`, so we should always use the
        // `min` function here (important for n <= 8)
        let k = cmp::min(n, (4.0 * (n as f64).ln()).ceil() as usize);

        // We should precalculate sums for empirical CDF, it will allow fast evaluating of the
        // segment cost
        let partial_sums = self.get_partial_sums(data, &k);

        // Since we use the same values of `partialSums`, `k`, `n` all the time,
        // we introduce a shortcut `Cost(tau1, tau2)` for segment cost evaluation.
        // Hereinafter, we use `tau` to name variables that are change point candidates.
        let cost = |tau1: &usize, tau2: &usize| self.get_segment_cost(&partial_sums, tau1, tau2, &k, &n);

        // We will use dynamic programming to find the best solution; `bestCost` is the cost array.
        // `bestCost[i]` is the cost for subarray `data[0..i-1]`.
        // It's a 1-based array (`data[0]`..`data[n-1]` correspond to `bestCost[1]`..`bestCost[n]`)
        let mut best_cost = vec![0.0; n + 1];
        best_cost[0] = -penalty;
        for current_tau in *min_distance..(2 * *min_distance) {
            best_cost[current_tau] = cost(&0, &current_tau);
        }

        // `previous_change_point_index` is an array of references to previous change points. If the
        // current segment ends at the position `i`, the previous segment ends at the position
        // `previous_change_point_index[i]`. It's a 1-based array (`data[0]`..`data[n-1]` correspond
        // to the `previous_change_point_index[1]`..`previous_change_point_index[n]`)
        let mut previous_change_point_index: Vec<i64> = vec![0; n + 1];

        // We use PELT (Pruned Exact Linear Time) approach which means that instead of enumerating
        // all possible previous tau values, we use a whitelist of "good" tau values that can be
        // used in the optimal solution. If we are 100% sure that some of the tau values will not
        // help us to form the optimal solution, such values should be removed. See [Killick2012]
        // for details.
        let mut previous_taus: Vec<usize> = vec![];
        previous_taus.push(0);
        previous_taus.push(*min_distance);
        let mut cost_for_previous_tau: Vec<f64> = vec![];

        // Following the dynamic programming approach, we enumerate all tau positions. For each
        // `current_tau`, we pretend that it's the end of the last segment and trying to find the
        // end of the previous segment.
        for current_tau in (2 * min_distance)..(n + 1) {
            // For each previous tau, we should calculate the cost of taking this tau as the end of
            // the previous segment. This cost equals the cost for the `previous_tau` plus cost of
            // the new segment (from `previous_tau` to `current_tau`) plus penalty for the new
            // change point.
            cost_for_previous_tau.clear();
            for previous_tau in previous_taus.iter() {
                cost_for_previous_tau.push(
                    best_cost[*previous_tau] +
                        cost(previous_tau, &current_tau) + penalty
                );
            }

            // Now we should choose the tau that provides the minimum possible cost.
            let best_previous_tau_index = self.which_min(&cost_for_previous_tau);
            best_cost[current_tau] = cost_for_previous_tau[best_previous_tau_index];
            previous_change_point_index[current_tau] = previous_taus[best_previous_tau_index] as i64;

            // Prune phase: we remove "useless" tau values that will not help to achieve minimum
            // cost in the future
            let current_best_cost = best_cost[current_tau];
            let mut new_previous_taus_size = 0;
            for i in 0..previous_taus.len() {
                if cost_for_previous_tau[i] < current_best_cost + penalty {
                    previous_taus[new_previous_taus_size] = previous_taus[i];
                    new_previous_taus_size += 1;
                }
            }
            previous_taus.drain(new_previous_taus_size..previous_taus.len());

            // We add a new tau value that is located on the `min_distance` distance from the next
            // `current_tau` value
            previous_taus.push(current_tau - (min_distance - 1));
        }

        // Here we collect the result list of change point indexes `change_point_indexes` using
        // `previous_change_point_index`
        let mut change_point_indexes: Vec<i64> = vec![];
        let mut current_index = previous_change_point_index[n]; // The index of the end of the last segment is `n`
        while current_index != 0 {
            change_point_indexes.push(current_index);
            current_index = previous_change_point_index[current_index as usize];
        }

        // Sort the change_point_indexes
        change_point_indexes.sort();

        change_point_indexes
    }

    /// Partial sums for empirical CDF (formula (2.1) from Section 2.1 "Model" in [Haynes2017])
    ///
    /// `partialSums[i, tau] = (count(data[j] &lt; t) * 2 + count(data[j] == t) * 1)` for
    /// j=0..tau-1 where t is the i-th quantile value (see Section 3.1 "Discrete approximation" in
    /// [Haynes2017] for details)
    ///
    /// We use doubled sum values in order to use `Vec<Vec<i64>>` instead of `Vec<Vec<f64>>` (it
    /// provides noticeable performance boost). Thus, multipliers for `count(data[j] &lt; t)` and
    /// `count(data[j] == t)` are 2 and 1 instead of 1 and 0.5 from the [Haynes2017].
    ///
    /// Note that these quantiles are not uniformly distributed: tails of the `data` distribution
    /// contain more quantile values than the center of the distribution.
    fn get_partial_sums(&self, data: &[f64], k: &usize) -> Vec<Vec<i64>> {
        let n = data.len();
        let mut partial_sums = vec![vec![0; n + 1]; *k];
        // sort the data in ascending order and save to a vector
        let mut sorted_data = data.to_vec();
        sorted_data.sort_by(|a, b| a.partial_cmp(b).unwrap());

        for i in 0..*k {
            let z: f64 = -1.0 + (2.0 * i as f64 + 1.0) / *k as f64; // Values from (-1+1/k) to (1-1/k) with step = 2/k
            let p: f64 = 1.0 / (1.0 + (2.0 * n as f64 - 1.0).powf(-z)); // Values from 0.0 to 1.0
            let idx: f64 = (n as f64 - 1.0) * p;
            let t: f64 = sorted_data[idx as usize]; // Quantile value, formula (2.1) in [Haynes2017]

            for tau in 1..(n + 1)
            {
                partial_sums[i][tau] = partial_sums[i][tau - 1];
                if data[tau - 1] < t {
                    partial_sums[i][tau] += 2; // We use doubled value (2) instead of original 1.0
                }
                if (data[tau - 1] - t).abs() < self.tolerance {
                    partial_sums[i][tau] += 1; // We use doubled value (1) instead of original 0.5
                }
            }
        }
        partial_sums
    }

    /// Calculates the cost of the (tau1; tau2] segment.
    fn get_segment_cost(
        &self, partial_sums: &Vec<Vec<i64>>, tau1: &usize, tau2: &usize, k: &usize, n: &usize
    ) -> f64 {
        let mut sum = 0.0;
        for i in 0..*k {
            // actual_sum is (count(data[j] < t) * 2 + count(data[j] == t) * 1) for j=tau1..tau2-1
            let actual_sum = partial_sums[i][*tau2] - partial_sums[i][*tau1];

            // We skip these two cases (correspond to fit = 0 or fit = 1) because of invalid ln values
            if actual_sum != 0 && actual_sum != ((*tau2 as i64 - *tau1 as i64) * 2){
                // Empirical CDF $\hat{F}_i(t)$ (Section 2.1 "Model" in [Haynes2017])
                let fit = actual_sum as f64 * 0.5 / (*tau2 as f64 - *tau1 as f64);
                // Segment cost $\mathcal{L}_{np}$ (Section 2.2 "Nonparametric maximum likelihood" in [Haynes2017])
                let lnp = (*tau2 as f64 - *tau1 as f64) * (fit * fit.ln() + (1.0 - fit) * (1.0 - fit).ln());
                sum += lnp;
            }
        }
        let c = -(2.0 * *n as f64 - 1.0).ln(); // Constant from Lemma 3.1 in [Haynes2017]
        2.0 * c / *k as f64 * sum // See Section 3.1 "Discrete approximation" in [Haynes2017]
    }

    /// Returns the index of the minimum element.
    /// In case if there are several minimum elements in the given list, the index of the first one
    /// will be returned.
    fn which_min(&self, values: &[f64]) -> usize {
        let mut min_idx = 0;
        let mut min_val = values[0];
        for i in 1..values.len() {
            if values[i] < min_val {
                min_idx = i;
                min_val = values[i];
            }
        }
        min_idx
    }

}

pub struct SteadyStateDetector {
}

/// Steady State Detection algorithm based on Change Point Detection associated with variance and
/// slope thresholds.
impl SteadyStateDetector {
    pub fn new() -> Self {
        Self {}
    }

    /// Steady State Detection (based on Change Point Detection).
    ///
    /// Evaluates the given time series with respect to steady behavior. First the time series is
    /// split into "statistically homogeneous" segments using the ED Pelt change point detection
    /// algorithm. Then each segment is tested with regards to a normalized standard deviation and
    /// the slope of the line of best fit to determine if the segment can be considered a steady or
    /// transient region.
    ///
    /// # Arguments
    /// * `time_series` - A TimeSeries object
    /// * `min_distance` - Minimum segment distance. Specifies the minimum distance for each
    /// segment that will be considered in the Change Point Detection algorithm.
    /// * `var_threshold` - Variance threshold. Specifies the variance threshold. If the normalized
    /// variance calculated for a given segment is greater than the threshold, the segment will be
    /// labeled as transient (value = 0).
    /// * `slope_threshold` - Slope threshold. Specifies the slope threshold. If the slope of a
    /// line fitted to the data of a given segment is greater than 10 to the power of the threshold
    /// value, the segment will be labeled as transient (value = 0).
    ///
    /// # Return
    /// TimeSeries object with the steady state condition (0: transient region, 1: steady region)
    /// for all timestamps.
    pub fn get_steady_state_status(
        &self, time_series: &TimeSeriesData,
        min_distance: &usize, var_threshold: &f64,
        slope_threshold: &f64,
    ) -> TimeSeriesData {
        // resamples the given time series so that it contains equally spaced elements
        let resampled_time_series = time_series.equally_spaced_resampling(
            None, None, None
        );

        // store locally the x and y arrays
        let x = resampled_time_series.time;
        let y = resampled_time_series.data;

        // the maximum allowable distance is half the number of data points so we override the
        // min_distance value if the current value is not valid
        let max_distance = x.len() / 2;
        let curr_min_distance = cmp::min(*min_distance, max_distance);

        // instantiate the array that will store the results
        let mut ss_map = vec![0.0; x.len()];

        // compute the change points
        let ed_pelt = EdPelt::new();
        let mut cp = ed_pelt.get_change_point_indexes(&y, &curr_min_distance);
        // Add zero and the last index to the List
        cp.push(0);
        cp.push(y.len() as i64);
        cp.sort();

        // compute the mean value of the input vector
        let avg = mean(&y);

        // constrains the mean of the data into predefined limits
        // this will prevent generating infinite values on the var calculation below
        let divisor = constrain(avg, 1.0e-4, 1.0e6);

        let mut old_mean: f64 = 0.0;
        let mut curr_mean: f64;

        for i in 1..cp.len() {
            let i0 = cp[i - 1] as usize;
            let i1 = cp[i] as usize;
            let xi = &x[i0..i1];
            let xid = xi.iter().map(|x| *x as f64).collect::<Vec<f64>>();
            let yi = &y[i0..i1];

            let std = std_dev(yi) / (i1 - i0) as f64;
            let std_normalised = 1.0e5 * std / divisor;

            // save the mean of the segment
            if i == 1 {
                old_mean = mean(yi);
            }
            curr_mean = mean(yi);

            // We consider a region as transient unless it passed the subsequent logical tests
            let mut ss_region = 0.0;

            // First check if the variance criteria is met
            if std_normalised.abs() < *var_threshold {
                // Only fit a line if the first criteria is met
                let slope = get_line_slope(&xid, yi);
                if slope.abs() < 10f64.powf(*slope_threshold) {
                    // The region is considered as steady
                    ss_region = 1.0;
                }
            }

            // Assigns the Steady State map flag to all timestamps of the current region
            for j in i0..i1 {
                // check if the previous region was steady and if the difference between the mean
                // values of each segment is significant, we add one time step of transient between
                // consecutive steady regions
                if j == i0 && i > 1 && ss_map[i0 - 1] == 1.0 && (old_mean - curr_mean).abs() > 3. * *var_threshold {
                    ss_map[j] = 0.0;
                }
                else {
                    ss_map[j] = ss_region;
                }
            }
            old_mean = curr_mean;
        }
        TimeSeriesData::new(x, ss_map, resampled_time_series.granularity, false)
    }
}


#[cfg(test)]
mod tests {
    use crate::sample_data::{get_data, get_ssd_data};
    use super::*;

    #[test]
    fn test_change_point_detection() {
        // input data
        let data: Vec<f64> = vec![1., 1., 1., 1., 10., 10., 10., 10., 10., 1., 1., 1., 1.];
        let min_distance: usize = 1;

        // expected results
        let expected_change_points: Vec<i64> = vec![4, 9];

        // run the detection
        let ed_pelt = EdPelt::new();
        let change_points = ed_pelt.get_change_point_indexes(&data, &min_distance);
        for i in 0..expected_change_points.len() {
            assert_eq!(change_points[i], expected_change_points[i]);
        }
    }

    #[test]
    fn test_steady_state_detection() {
        // input data
        let time_series = get_data();

        // expected results
        let ssd_map_expected = get_ssd_data();

        // run the detection
        let ssd = SteadyStateDetector::new();
        let ssd_map = ssd.get_steady_state_status(&time_series, &60, &1.0, &-1.0);
        for i in 0..ssd_map_expected.time.len() {
            assert_eq!(ssd_map.time[i], ssd_map_expected.time[i]);
            assert_eq!(ssd_map.data[i], ssd_map_expected.data[i]);
        }
    }
}