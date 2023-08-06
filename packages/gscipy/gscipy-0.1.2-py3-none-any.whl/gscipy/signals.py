"""Module for signal processing."""
from __future__ import annotations

__author__ = "Matteo Gabba"
__copyright__ = "Copyright 2022, all right reserved Gabba Scientific"
__status__ = "Development"

import math
import warnings
from dataclasses import dataclass
from typing import Iterable

import numpy as np
from pywt import wavedec, waverec
from scipy import signal
from scipy.integrate import cumulative_trapezoid
from statsmodels.tsa.ar_model import ar_select_order
from statsmodels.tsa.stattools import adfuller

from gscipy.general import TypeCheckedList
from gscipy.utils import _isnan, cluster_size_generator


@dataclass
class Peak:
    is_type: str = "unknown"
    index: int = None
    position: float = None
    fwhm: float = None
    std: float = None
    width_height: float = None
    width_start: float = None
    width_end: float = None
    height: float = None
    contour_height: float = None
    prominence: float = None

    @property
    def area(self) -> float:
        """See: # https://www.savarese.org/math/gaussianintegral.html#S3.E20."""
        return self.prominence * self.std * np.sqrt(2 * math.pi)

    def __lt__(self, other: Peak) -> bool:
        if isinstance(other, Peak):
            return self.position < other.position
        return NotImplemented

    def __eq__(self, other: Peak) -> bool:
        if isinstance(other, Peak):
            return (
                (self.index == other.index)
                & (self.position == other.position)
                & (self.fwhm == other.fwhm)
                & (self.height == other.height)
            )
        return NotImplemented

    def __ne__(self, other: Peak) -> bool:
        return not self == other

    def __hash__(self):
        return hash((self.is_type, self.position, self.std, self.height))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.is_type}, position={self.position:.1f})"


class PeaksList(TypeCheckedList):
    def __init__(
        self,
        iterator_arg: Iterable[Peak] = None,
    ):
        """
        Iterator_arg : List[Peak], optional, default to None.

            List of Peak
        """
        # Initialize the parent class to type check for Peak instances
        super().__init__(iterator_arg=iterator_arg, instance_type=Peak)

    @property
    def indexes(self) -> np.ndarray:
        return np.array([peak.index for peak in self])

    @property
    def positions(self) -> np.ndarray:
        return np.array([peak.position for peak in self])

    @property
    def fwhms(self) -> np.ndarray:
        return np.array([peak.fwhm for peak in self])

    @property
    def stds(self) -> np.ndarray:
        return np.array([peak.std for peak in self])

    @property
    def width_heights(self) -> np.ndarray:
        return np.array([peak.width_height for peak in self])

    @property
    def width_starts(self) -> np.ndarray:
        return np.array([peak.width_start for peak in self])

    @property
    def width_ends(self) -> np.ndarray:
        return np.array([peak.width_end for peak in self])

    @property
    def heights(self) -> np.ndarray:
        return np.array([peak.height for peak in self])

    @property
    def prominences(self) -> np.ndarray:
        return np.array([peak.prominence for peak in self])

    @property
    def contour_heights(self) -> np.ndarray:
        return np.array([peak.contour_height for peak in self])

    @property
    def areas(self) -> np.ndarray:
        return np.array([peak.area for peak in self])

    def compute_features(
        self,
        y: np.ndarray,
        x: np.ndarray,
    ) -> None:
        compute_peaks_width_features(
            y,
            x,
            self,
        )

        compute_peaks_height_features(
            y,
            self,
        )

    def detect(
        self,
        y: np.ndarray,
        x: np.ndarray,
        min_peak_prominence: float,
        min_inter_peak_distance: float,
    ) -> None:
        """Populate input list with detected peaks."""
        inter_sample_distance = x[1] - x[0]
        min_inter_peak_distance_cts = int(
            min_inter_peak_distance / inter_sample_distance
        )

        peaks_indexes, _ = signal.find_peaks(
            y,
            prominence=min_peak_prominence,
            distance=min_inter_peak_distance_cts,
        )
        peaks_iter = (
            Peak(index=index, position=x[index]) for index in peaks_indexes
        )

        self.extend(peaks_iter)


def compute_peaks_width_features(
    y: np.ndarray,
    x: np.ndarray,
    peaks: PeaksList,
) -> None:
    inter_sample_distance = x[1] - x[0]
    x0 = x[0]

    results_fwhm = signal.peak_widths(
        y,
        peaks.indexes,
        rel_height=0.5,
    )
    fwhms = results_fwhm[0] * inter_sample_distance
    stds = fwhms / 2.355
    width_heights = results_fwhm[1]
    width_starts = (results_fwhm[2] * inter_sample_distance) + x0
    width_ends = width_starts + fwhms

    for n, peak in enumerate(peaks):
        peak.fwhm = fwhms[n]
        peak.std = stds[n]
        peak.width_height = width_heights[n]
        peak.width_start = width_starts[n]
        peak.width_end = width_ends[n]


def compute_peaks_height_features(
    y: np.ndarray,
    peaks: PeaksList,
) -> None:
    prominences = signal.peak_prominences(y, peaks.indexes)[0]
    contour_heights = y[peaks.indexes] - prominences
    heights = y[peaks.indexes]

    for n, peak in enumerate(peaks):
        peak.prominence = prominences[n]
        peak.contour_height = contour_heights[n]
        peak.height = heights[n]


def get_weights(n_train: int, n_steps: int) -> np.ndarray:
    """
    Compute weights (reliability) of predicted values.

    Parameters
    ----------
        n_train : int
            Number of points used for training the AR-model and making predictions.

        n_steps : int
            Number of predicted points.

    Returns
    -------
        w : np.ndarray
            Weights indicating the reliability of the predicted values, dim(n_steps,).
            The weights are linearly proportional to the number of points used for the prediction
            and inversely proportional to the number of steps into the future.
    """
    # Total weights: are linearly proportional to the number of points used for the prediction
    # and inversely proportional to the number of steps into the future
    linear_w = np.arange(1, n_steps + 1)[::-1]

    return n_train * linear_w


def autoregress_predict(
    seg: np.ndarray, n_steps: int, max_lag: int
) -> np.ndarray:
    """
    Predict (forecast) n-steps into the future using an autoregressive (AR) model that minimizes the Akaike information.

     criterion (AIC).
     # TODO: implement possibility to choose the width of the region for prediction.

    See:
        https://www.statsmodels.org/devel/examples/notebooks/generated/autoregressions.html
        https://vitalflux.com/autoregressive-ar-models-with-python-examples/#:~:text=Autoregressive%20(AR)%20models%20are%20a,order%20to%20make%20accurate%20predictions.
        https://machinelearningmastery.com/autoregression-models-time-series-forecasting-python/

    Parameters
    ----------
        seg : np.ndarray
            Segment of a time-series used for training the AR-model.

        n_steps : np.ndarray
            Forecast n-steps into the future based on the past behavior of the time-series.

        max_lag : int
            Select max lag for automatic selection of the lags structure.
            See: https://www.statsmodels.org/devel/generated/statsmodels.tsa.ar_model.ar_select_order.html

    Returns
    -------
        prediction : np.ndarray
            Array of len = n_steps with AR-predicted values.
    """
    # Number of points used for training of the AR-model
    n_samples = len(seg)

    # Check for stationarity of the time-series data
    # We will look for p-value. In case, p-value is less than 0.05, the time series
    # data can be said to have stationarity
    df_stationarityTest = adfuller(seg, autolag="AIC")
    p_value = df_stationarityTest[1]

    # Raise warning if time-series segment used for prediction is not stationary
    if p_value > 0.05:
        warnings.warn(
            "P-value = {} is > 0.05! The time-series segment used for prediction may "
            "not be stationary!".format(p_value)
        )

    # Automatically select AR-model lag
    select = ar_select_order(seg, ic="aic", maxlag=max_lag)

    # Train AR-model
    trained_model = select.model.fit()

    # Make predictions (forecast) to refill gap
    prediction = trained_model.predict(
        start=n_samples, end=n_samples + n_steps - 1, dynamic=True
    )

    return prediction


def find_gaps_and_segments(x: np.ndarray | list[float]) -> list[np.ndarray]:
    """
    Get indexes of gaps (of NaN's) and segments (not-NaN) in the input array.

    Parameters
    ----------
        x : array-like
            Array with NaN gaps.

    Returns
    -------
        A list of indexes arrays corresponding to the segments and gaps in the input array.
    """
    # Get indexes of segments (not-NaN) and gaps (NaN) in the array
    return [idx for (value, _, idx) in cluster_size_generator(np.isnan(x))]


def gap_is_first(x: np.ndarray | list[float]) -> bool:
    """
    Check if a gap (of NaN's) or a segment is in first position of the input array.

    Parameters
    ----------
        x : array-like
            Array with NaN gaps.

    Returns
    -------
        True if the input array starts with a gap of NaN's, False, otherwise.
    """
    # If a gap is in first position: gap-segment-gap-segment-etc..
    if _isnan(x[0]):
        return True

    # if a segment is in first position: segment-gap-segment-etc..
    return False


def autoregress_fill(
    x: np.ndarray, max_lag: int
) -> tuple[np.ndarray, np.ndarray]:
    """
    Fill gaps of NaN's in a time-series using an autoregressive model that minimizes the Akaike information.

    criterion (AIC).
    # TODO: implement possibility to choose the width of the region for prediction.

    Parameters
    ----------
        x : array-like
            Array with NaN gaps, dim(n,).

        max_lag : int
            Select max lag for automatic selection of the lags structure.

    Returns
    -------
        y : np.ndarray
            A copy of the input array with gaps filled with the AR-predicted values, dim(n,).

        w : np.ndarray
            Weights indicating the reliability of the predicted values, dim(n,).
    """
    # Copy input array
    y = np.copy(x)

    # Initialize weights
    w = np.ones_like(x)

    # Get labels and indexes of NaN gaps (label: True) and segments (label: False)
    # in the input array
    idx = find_gaps_and_segments(y)

    # Total number of segments and gaps
    n = len(idx)

    # Initialize variables
    idx_first_seg = 0
    prediction = np.empty(0)
    w_i = np.empty(0)

    # Array starts with a gap
    if gap_is_first(y):

        # position of the first segment in the array
        idx_first_seg = 1

        # indexes of first gap
        idx_first_gap = idx[0]
        first_gap = y[idx_first_gap]

        # nothing to predict
        prediction = np.zeros_like(first_gap)

        # fill first gap with zeros
        y[idx_first_gap] = prediction
        w[idx_first_gap] = np.zeros_like(first_gap)

    # array starts with a segment
    elif not gap_is_first(y):

        # position of the first segment in the array
        idx_first_seg = 0

    # Predict from segment immediately prior to the gap starting from first segment in the array
    for i in range(idx_first_seg, n - 1, 2):

        # get segment and gap indexes
        idx_seg = idx[i]
        idx_gap = idx[i + 1]

        # initialize segment and gap arrays with right length
        seg = y[idx_seg]
        gap = y[idx_gap]

        # for a segment only one sample long
        if len(seg) == 1:

            # predict a constant
            prediction = np.ones_like(gap) * seg[0]

        # for a segment longer than one sample
        elif len(seg) > 1:

            # predict with autoregressive model
            prediction = autoregress_predict(seg, len(gap), max_lag)
            w_i = get_weights(len(seg), len(gap))

        # fill gap with predicted values
        y[idx_gap] = prediction
        w[idx_gap] = w_i

    return y, w


def refill_gaps(x: np.ndarray, max_lag: int) -> np.ndarray:
    """
    Replaces NaN values of an input vector, X, by fitting an autoregressive (AR) model that.

    minimizes the Akaike information criterion. Each NaN value is replaced by a weighted average
    of the values estimated by forward and backward prediction.

    # TODO: implement possibility to choose the width of the region for prediction.

    Parameters
    ----------
        x : array-like
            Array with NaN gaps, dim(n,).

        max_lag : int
            Select max lag for automatic selection of the lags structure.

    Returns
    -------
        y : np.ndarray
            A copy of the input array with NaN gaps refilled with AR-predicted values.
    """
    # Refill NaN's gaps in forward direction
    x_fwd, w_fwd = autoregress_fill(x, max_lag)

    # Refill NaN's gaps in backward direction
    x_bwd, w_bwd = autoregress_fill(x[::-1], max_lag)

    # Invert refilled array
    x_bwd = x_bwd[::-1]
    w_bwd = w_bwd[::-1]

    # Compute weighted average of the refilled arrays in backward and forward directions
    y = (x_bwd * w_bwd + x_fwd * w_fwd) / (w_bwd + w_fwd)

    return y


def cumulative_integral(
    y: np.ndarray,
    x: np.ndarray = None,
    dx: float = None,
    max_lag: int = 5,
) -> np.ndarray:
    y_filled = refill_gaps(y, max_lag)
    return cumulative_trapezoid(y_filled, x, dx, initial=0)


def central_diff(
    y: np.ndarray | list[float],
    axis: int = -1,
    kernel_half_size: int = 1,
) -> np.ndarray:
    """
    Compute sum of central finite differences of input array along the given axis using a convolution kernel.

    The half width M of the kernel determines the number of terms in the summation:
    dy[i] = sum_m (dy[i+m] - dy[i-m]) with m in [-M, M].

    See: https://numpy.org/doc/stable/reference/generated/numpy.convolve.html

    Keep in mind that: "the convolution operator flips the second array before “sliding” the two across one another."

    Parameters
    ----------
        y : array-like
            One or multidimensional array.

        axis : int
            The axis along which the difference is taken, default is the last axis.

        kernel_half_size : int
            Half size M of the family of convolution kernels: g[m] = [1, 0, -1], [1, 1, 0, -1, -1], ...

    Returns
    -------
        dy : np.ndarray
        The summation of the m-th central finite differences of the input array:
        dy[i] = sum_m (dy[i+m] - dy[i-m]) with m in [-M, M]
        The output array is padded with NaN along the chosen axis to keep the same dimensions of the input array.

    Version history
    ---------------
        v1 : 18-05-2022 (m.gabba)
    """
    assert (
        kernel_half_size > 0
    ), "kernel_half_size: must be a not-zero positive integer!"

    # Base convolution kernel
    base_kernel = [0]

    # Create convolution kernel for calculation of central difference with chosen half-width histrange: M // 2
    kernel = np.pad(
        base_kernel,
        pad_width=kernel_half_size,
        mode="constant",
        constant_values=[1, -1],
    )

    # Apply convolution kernel along the given axis
    dy = np.apply_along_axis(
        lambda m: np.convolve(m, kernel, mode="valid"), axis=axis, arr=y
    )

    # Pad with NaN along the given axis to keep the same dimensions of the input array.
    dy_padded = np.apply_along_axis(
        lambda m: np.pad(
            m,
            pad_width=kernel_half_size,
            mode="constant",
            constant_values=np.nan,
        ),
        axis=axis,
        arr=dy,
    )

    return dy_padded


def smooth_signal_by_differentiation_and_reintegration(
    y: np.ndarray,
    x: np.ndarray,
    kernel_half_size: int,
) -> np.ndarray:
    delta_y = central_diff(y, kernel_half_size=kernel_half_size)
    delta_x = central_diff(x, kernel_half_size=kernel_half_size)
    derivative = delta_y / delta_x
    return cumulative_integral(derivative, x)


def correlation(
    sig1: np.ndarray | list[float],
    sig2: np.ndarray | list[float],
    freq: float,
    normed: bool,
) -> tuple[np.ndarray, np.ndarray, float]:
    """
    Compute correlation between two signals.

    See:
        https://en.wikipedia.org/wiki/Cross-correlation
        https://scicoding.com/cross-correlation-in-python-3-popular-packages/
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.correlate.html

    Parameters
    ----------
        sig1, sig2 : array-like
            Signal(s) to correlate. If sig1=sig2 returns the auto-correlation; otherwise,
            the cross-correlation.

        freq : float
            Sampling frequency of the input signal(s).

        normed : bool
            If True return the normalized correlation with values between [-1, 1]
            as per definition; if False, the not-normalized correlation.

    Returns
    -------
        corr, lag_times, lags, lag : tuple
            The correlation function, the lag times and the lag time corresponding to the max
            correlation.
    """
    # Length of the signals
    n1 = len(sig1)
    n2 = len(sig2)

    # Length of longer signal
    N = np.max([n1, n2])

    if normed:

        # subtract mean signal value
        nsig1 = sig1 - np.mean(sig1)
        nsig2 = sig2 - np.mean(sig2)

        # correlate normed signals
        corr = signal.correlate(nsig1, nsig2, mode="full")

        # normalize correlation between [-1, 1] using the signal std
        norm = N * np.std(nsig1) * np.std(nsig2)
        corr /= norm

    if not normed:

        # correlate raw signals
        corr = signal.correlate(sig1, sig2, mode="full")

        # divide by the number of sample
        corr /= N

    # Get lag indixes: k
    lags = signal.correlation_lags(n1, n2)

    # Convert lag indexes to time: k * dt = k / freq
    lag_times = lags / freq

    # Lag time corresponding to the max correlation
    lag = lag_times[np.argmax(corr)]

    return corr, lag_times, lag


def wavelet_filter(
    signal: np.ndarray,
    wavelet_type: str,
    extension_mode: str,
    filtered_levels: tuple[int, ...],
) -> tuple[np.ndarray, list[float]]:
    """
    Filter signal with discrete wavelet transformation (DWT) and reconstruction.

    See : https://ataspinar.com/2018/12/21/a-guide-for-using-the-wavelet-transform-in-machine-learning/

    Parameters
    ----------
        signal : np.ndarray
            Input data series.

        wavelet_type : wavelet object or str
            Valid discrete wavelet type.
                See :
                    https://pywavelets.readthedocs.io/en/latest/ref/wavelets.html
                    http://wavelets.pybytes.com/wavelet/

        extension_mode : str
            Signal extension mode.
                See : https://pywavelets.readthedocs.io/en/latest/ref/signal-extension-modes.html#ref-modes

        filtered_levels : tuple
            Choose decomposition levels to remove from signal reconstruction in order to filter specific frequencies.
            Levels are positive integers. Low values corresponds to high-frequency wavelets, high values to
             low-frequency wavelets. Thus, removing low (high) value levels corresponds to a  low(high)pass wavelet
              filter.
                See : https://pywavelets.readthedocs.io/en/latest/ref/idwt-inverse-discrete-wavelet-transform.html

    Returns
    -------
        reconstructed_signal : np.ndarray
            The input signal after wavelet decomposition and recomposition with filtered coefficients.

         coefficients : List
            The wavelet decomposition coefficients after filtering.

    Version history
    ---------------
        v1 : 18-05-2022 (m.gabba)
    """
    # Discrete wavelet transformation DWT of signal with automatic selection of the decomposition level
    # See: https://pywavelets.readthedocs.io/en/latest/ref/dwt-discrete-wavelet-transform.html
    # The output coefficients are ordered as follows: [cA_n, cD_n, cD_n-1, …, cD2, cD1] with decreasing level order
    coefficients = wavedec(
        signal, wavelet_type, mode=extension_mode, level=None
    )

    # Set to zero coefficients at the chosen levels
    for level in filtered_levels:
        coefficients[-level] = np.zeros_like(coefficients[-level])

    # Reconstruct wavelet filtered signal
    reconstructed_signal = waverec(
        coefficients, wavelet_type, mode=extension_mode
    )

    # Handle issues with reconstructed signal longer than the original signal, I don't understand the origin of
    # this behavior!!

    # If the reconstructed signal is longer than the original signal
    if len(reconstructed_signal) > len(signal):
        # remove last point
        reconstructed_signal = reconstructed_signal[:-1]

    return reconstructed_signal, coefficients
