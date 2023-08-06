import warnings
import datetime
import numpy as np
import scipy.fft
import scipy.signal
from .fractional_octave_band import FractionalOctaveBandTools as fob_tools
from ..waveform import Waveform
from .acoustic_weights import AcousticWeights


class Spectrum:
    """
    This is the base class that defines the structure of the spectrum object. It does not calculate the frequency
    spectrum from a waveform, but can be used to represent a single spectrum that was previously created.

    Remarks
    2022-12-13 - FSM - Added a function to calculate the sound quality metrics based on the frequency spectrum

    """
    def __init__(self, a: Waveform = None):
        """
        The default constructor that builds the information within the Spectrum class based on the contents of the
        object "a".

        Parameters
        ----------
        a: Waveform - the acoustic samples that define the source of the time-domain information that we are interested
        in processing
        """

        self._waveform = a
        self._frequencies = None
        self._acoustic_pressures_pascals = None
        self._time0 = None

        self._bandwidth = None
        self._f0 = None
        self._f1 = None

        if a is not None:
            self._time0 = self.waveform.start_time

            if len(a.samples.shape) > 1:
                self._waveform.samples = self._waveform.samples.reshape((-1,))

        self._fft_size = 4096
        self._window_size_seconds = 0.0232
        self._hop_size_seconds = 0.0058
        self._window_size = self._window_size_seconds * self.sample_rate
        self._hop_size = self.hop_size_seconds * self.sample_rate

        self.bin_size = self.sample_rate / self._fft_size
        self.sample_rate_x = self.sample_rate / self.hop_size
        self.sample_rate_y = self._fft_size / self.sample_rate_x
        self.window = np.hamming(self.window_size)
        self.window_overlap = self.window_size - self.hop_size

        #   Define the features

        self.centroid = None
        self._mean_center = None
        self.spread = None
        self.skewness = None
        self.kurtosis = None
        self.slope = None
        self.decrease = None
        self.roll_off = None
        self.energy = None
        self.flatness = None
        self.crest = None
        self.probability_distribution = None
        self.integration_variable = None
        self.geometric_mean = None
        self.arithmetic_mean = None

    #   ------------------------------------------ Protected functions -------------------------------------------------

    def _calculate_spectrum(self):
        import warnings

        warnings.warn("This function does nothing. You will need to implement this function in the child class to build"
                      "the spectrum with the correct units and format.")

        raise ValueError('This method must be implemented and assigned frequencies within the calculation '
                         'of each type of spectrum class.')

    #   ------------------------------------- Class properties ---------------------------------------------------------

    @property
    def waveform(self):
        if self._waveform is None:
            warnings.warn('No Waveform object has been passed to this Spectrum object.')
        return self._waveform

    @property
    def signal(self):
        return self.waveform.samples

    @property
    def sample_rate(self):
        if self._waveform is None:
            return 48000
        else:
            return self.waveform.sample_rate

    @property
    def duration(self):
        if self._waveform is None:
            raise AttributeError("No waveform has been provided to the Spectrum object.")
        return self.waveform.duration

    @property
    def time(self):
        if self._time0 is None:
            raise AttributeError("No time object has been provided to the Spectrum object.")
        return self._time0

    @property
    def time_past_midnight(self):
        if self._time0 is None:
            raise AttributeError("No time has been provided to the Spectrum object.")

        if isinstance(self._time0, datetime.datetime):
            return 60 * (60 * self._time0.hour + self._time0.minute) + self._time0.second + \
                   float(self._time0.microsecond / 1e6)
        else:
            return self._time0

    @property
    def frequencies(self):
        if self._frequencies is None:
            self._calculate_spectrum()

        return self._frequencies

    @frequencies.setter
    def frequencies(self, values):
        self._frequencies = values

    @property
    def pressures_pascals(self):
        if self._frequencies is None or self._acoustic_pressures_pascals is None:
            self._calculate_spectrum()

        return self._acoustic_pressures_pascals

    @pressures_pascals.setter
    def pressures_pascals(self, values):
        self._acoustic_pressures_pascals = values

    @property
    def pressures_decibels(self):
        return 20 * np.log10(self.pressures_pascals / 20e-6)

    @property
    def overall_level(self):
        """
        Overall sound pressure level, unweighted (i.e. flat weighted, Z-weighted).  Calculated as the energetic sum
        of the power spectrum.
        """
        return AcousticWeights.lf(self.pressures_decibels)

    @property
    def overall_a_weighted_level(self):
        """
        A-weighted overall sound pressure level.  Calculated as the energetic sum
        of the A-weighted power spectrum.
        """

        return AcousticWeights.la(self.pressures_decibels, self.frequencies)[0]

    @property
    def perceived_noise_level(self):
        return AcousticWeights.pnl(self.pressures_decibels)

    @property
    def fractional_octave_bandwidth(self):
        return self._bandwidth

    @fractional_octave_bandwidth.setter
    def fractional_octave_bandwidth(self, value):
        self._bandwidth = value

    @property
    def start_fractional_octave_frequency(self):
        return self._f0

    @start_fractional_octave_frequency.setter
    def start_fractional_octave_frequency(self, value):
        self._f0 = value

    @property
    def stop_fractional_octave_frequency(self):
        return self._f1

    @stop_fractional_octave_frequency.setter
    def stop_fractional_octave_frequency(self, value):
        self._f1 = value

    @property
    def narrowband_frequency_count(self):
        return self._fft_size

    @narrowband_frequency_count.setter
    def narrowband_frequency_count(self, value):
        self._fft_size = value

        self.bin_size = self.sample_rate / self._fft_size
        self.sample_rate_x = self.sample_rate / self.hop_size
        self.sample_rate_y = self._fft_size / self.sample_rate_x
        self.window = np.hamming(self.window_size)
        self.window_overlap = self.window_size - self.hop_size

    @property
    def roughness(self):
        from mosqito.sq_metrics import roughness_dw_freq

        return roughness_dw_freq(spectrum=self.pressures_decibels, freqs=self.frequencies)[0]

    @property
    def loudness(self):
        from mosqito.sq_metrics import loudness_zwst_freq

        return loudness_zwst_freq(self.pressures_decibels, self.frequencies)

    @property
    def sharpness(self):
        from mosqito.sq_metrics import sharpness_din_freq

        return sharpness_din_freq(self.pressures_decibels, self.frequencies)

    @property
    def hop_size_seconds(self):
        return self._hop_size_seconds

    @hop_size_seconds.setter
    def hop_size_seconds(self, value: float):
        self._hop_size_seconds = value
        self.hop_size = int(np.floor(self.hop_size_seconds * self.sample_rate))
        self.sample_rate_x = self.sample_rate / self.hop_size
        self.window_overlap = self.window_size - self.hop_size

    @property
    def window_size(self):
        return int(np.floor(self._window_size))

    @window_size.setter
    def window_size(self, value: int):
        self._window_size = value
        self._window_size_seconds = self.window_size / self.sample_rate
        self.window = np.hamming(self.window_size)
        self.window_overlap = self.window_size - self.hop_size

    @property
    def hop_size(self):
        return int(np.floor(self._hop_size))

    @hop_size.setter
    def hop_size(self, value: int):
        self._hop_size = value
        self.hop_size_seconds = self._hop_size / self.sample_rate
        self.sample_rate_x = self.sample_rate / self._hop_size
        self.window_overlap = self.window_size - self._hop_size

    @property
    def spectral_centroid(self):
        """
        Spectral centroid represents the spectral center of gravity.
        """

        if self.centroid is None:
            if self._acoustic_pressures_pascals is None and self._frequencies is None:
                self._calculate_spectrum()

            if self.probability_distribution is None or self.integration_variable is None:
                self.calculate_normalized_distribution()

            self.centroid = np.sum(self.integration_variable * self.probability_distribution, axis=0)

        return self.centroid

    @property
    def spectral_spread(self):
        """
        Spectral spread or spectral standard-deviation represents the spread of the spectrum around its mean value.
        """
        if self.mean_center is None:
            self._calculate_mean_center()

        if self.probability_distribution is None or self.integration_variable is None:
            self.calculate_normalized_distribution()

        if self.spread is None:
            self.spread = np.sqrt(np.sum(self.mean_center ** 2 * self.probability_distribution, axis=0))

        return self.spread

    @property
    def spectral_skewness(self):
        """
        Spectral skewness gives a measure of the asymmetry of the spectrum around its mean value. A value of 0 indicates
        a symmetric distribution, a value < 0 more energy at frequencies lower than the mean value, and values > 0 more
        energy at higher frequencies.
        """
        if self.mean_center is None:
            self._calculate_mean_center()

        if self.probability_distribution is None or self.integration_variable is None:
            self.calculate_normalized_distribution()

        if self.skewness is None:
            self.skewness = np.sum(self.mean_center ** 3 * self.probability_distribution, axis=0) / \
                            self.spectral_spread ** 3

        return self.skewness

    @property
    def spectral_kurtosis(self):
        """
        Spectral kurtosis gives a measure of the flatness of the spectrum around its mean value. Values approximately 3
        indicate a normal (Gaussian) distribution, values less than 3 indicate a flatter distributions, and values
        greater than 3 indicate a peakier distribution.
        """
        if self.mean_center is None:
            self._calculate_mean_center()

        if self.probability_distribution is None or self.integration_variable is None:
            self.calculate_normalized_distribution()

        if self.kurtosis is None:
            self.kurtosis = np.sum(self.mean_center ** 4 * self.probability_distribution, axis=0) / \
                            self.spectral_spread ** 4

        return self.kurtosis

    @property
    def spectral_slope(self):
        """
        Spectral slope is computed using a linear regression over the spectral amplitude values. It should be noted that
        the spectral slope is linearly dependent on the spectral centroid.
        """
        if self._acoustic_pressures_pascals is None and self._frequencies is None:
            self._calculate_spectrum()

        if self.probability_distribution is None or self.integration_variable is None:
            self.calculate_normalized_distribution()

        if self.slope is None:
            numerator = len(self._frequencies) * (self._frequencies.transpose().dot(self.probability_distribution))
            numerator -= np.sum(self._frequencies) * np.sum(self.probability_distribution, axis=0)
            denominator = len(self._frequencies) * sum(self._frequencies ** 2) - np.sum(self._frequencies) ** 2
            self.slope = numerator / denominator

        return self.slope

    @property
    def spectral_decrease(self):
        """
        Spectral decrease was proposed by Krimphoff (1993) in relation to perceptual studies. It averages the set of
        slopes between frequency f[k] and f[1]. It therefore emphasizes the slopes of the lowest frequencies.
        """
        if self._acoustic_pressures_pascals is None and self._frequencies is None:
            self._calculate_spectrum()

        if self.probability_distribution is None or self.integration_variable is None:
            self.calculate_normalized_distribution()

        if self.decrease is None:
            numerator = self._acoustic_pressures_pascals[1:] - self._acoustic_pressures_pascals[0]
            denominator = (1 / np.arange(1, len(self._frequencies)))
            self.decrease = (denominator.dot(numerator)).transpose().reshape((-1,))
            self.decrease /= np.sum(self.probability_distribution[1:], axis=0)

        return self.decrease[0]

    @property
    def spectral_roll_off(self):
        """
        Spectral roll-off was proposed by Scheirer and Slaney (1997). It is defined as the frequency below which 95%
        of the signal energy is contained. The value is returned as the normalized frequency (i.e. you must multiply
        by the sample rate to determine the actual frequency of the roll-off.
        """
        if self._acoustic_pressures_pascals is None and self._frequencies is None:
            self._calculate_spectrum()

        if self.roll_off is None:
            threshold = 0.95
            cum_sum = np.cumsum(self._acoustic_pressures_pascals, axis=0)
            sum = np.ones((len(self.frequencies), )) * (threshold * np.sum(self._acoustic_pressures_pascals))

            bin = np.cumsum(1 * (cum_sum > sum), axis=0)
            idx = np.where(bin == 1)[0]

            self.roll_off = self.frequencies[idx][0]

        return self.roll_off

    @property
    def spectral_energy(self):
        """
        A summation of the energy within the spectrum
        """
        if self._acoustic_pressures_pascals is None and self._frequencies is None:
            self._calculate_spectrum()

        if self.energy is None:
            self.energy = np.sum(self._acoustic_pressures_pascals, axis=0)

        return self.energy

    @property
    def spectral_flatness(self):
        """
        Spectral flatness is obtained by comparing the geometrical mean and the arithmetical mean of the spectrum. The
        original formulation first splot the spectrum into various frequency bands (Johnston, 1988). However, in the
        context of timbre characterization, we use a single frequency band covering the whole frequency range. For
        tonal signals, the spectral flatness is close to 0( a peaky spectrum), whereas for noisy signals it is close to
        1 (flat spectrum).
        """
        if self._acoustic_pressures_pascals is None and self._frequencies is None:
            self._calculate_spectrum()

        if self.flatness is None:
            self.geometric_mean = np.exp((1 / len(self._frequencies)) * np.sum(np.log(self._acoustic_pressures_pascals), axis=0))
            self.arithmetic_mean = np.mean(self._acoustic_pressures_pascals, axis=0)
            self.flatness = self.geometric_mean / self.arithmetic_mean

        return self.flatness

    @property
    def spectral_crest(self):
        """
        The spectral crest measure is obtained by comparing the maximum value and arithmetical mean of the spectrum.
        """
        if self._acoustic_pressures_pascals is None and self._frequencies is None:
            self._calculate_spectrum()

        if self.arithmetic_mean is None:
            self.arithmetic_mean = np.mean(self._acoustic_pressures_pascals, axis=0)

        if self.crest is None:
            self.crest = np.max(self._acoustic_pressures_pascals, axis=0) / self.arithmetic_mean

        return self.crest

    @property
    def mean_center(self):
        if self._mean_center is None:
            self._calculate_mean_center()

        return self._mean_center

    def calculate_engineering_unit_scale_factor(self, calibration_level: float = 94, calibration_frequency=1000):
        """
        This will take the data within the class and build the spectral time history and then determine the value of the
        scale factor to get a specific sound pressure level at a certain frequency.

        Parameters
        ----------
        calibration_level: float - the value of the acoustic level for the calibration
        calibration_frequency: float - the value of the frequency that is supposed to be used for the calibration

        Returns
        -------
        float - the engineering scale factor that can be directly applied to the acoustic data
        """

        if self.fractional_octave_bandwidth is None:
            raise ValueError("This analysis cannot be accomplished on a narrowband spectrum")

        #   Now determine the index of the band within the spectral time history that should be examined for the
        #   calculation of the engineering scaling units.

        # idx = int(np.floor(fob_tools.nearest_band(3, calibration_frequency))) - 10
        idx = np.argmin(np.abs(self.frequencies - calibration_frequency))

        # #   Now this may select the nearest band as the band just above the actual band.  So ensure that the lower band
        # #   is below the desired center frequency
        #
        # if fob_tools.lower_frequency(3, idx + 10) > calibration_frequency:
        #     idx -= 1

        #   From the spectrum obtain the values of the frequency

        calibration_values = self.pressures_decibels[idx]

        #   Calculate the sensitivity of each time history spectra

        sens = calibration_level - calibration_values
        sens /= 20
        sens *= -1
        sens = 10.0 ** sens

        return sens

    def get_average_features(self, include_sq_metrics: bool = True):
        import numpy as np
        """
        This will return a dict of the various elements within the spectrum and waveform (if it was used to create the
        spectrogram object) with any time variant elements averaged.
        """

        features = dict()

        if self.waveform is not None:
            features = self.waveform.get_features(include_sq_metrics)
            features['zero_crossing_rate'] = np.mean(features['zero crossing rate'])
            auto_correlation_coefficients = np.mean(features['auto-correlation'], axis=0)
            if include_sq_metrics:
                features['loudness'] = np.mean(features['loudness'])
                features['sharpness'] = np.mean(features['sharpness'])
                features['roughness'] = np.mean(features['roughness'])

            for i in range(12):
                features['auto_correlation_{:02.0f}'.format(i)] = auto_correlation_coefficients[i]

            del features['zero crossing rate']
            del features['auto-correlation']

        features['spectral_centroid'] = np.mean(self.spectral_centroid)
        features['spectral_spread'] = np.mean(self.spectral_spread)
        features['spectral_skewness'] = np.mean(self.spectral_skewness)
        features['spectral_kurtosis'] = np.mean(self.spectral_kurtosis)
        features['spectral_slope'] = np.mean(self.spectral_slope)
        features['spectral_decrease'] = np.mean(self.spectral_decrease)
        features['spectral_roll_off'] = np.mean(self.spectral_roll_off)
        features['spectral_energy'] = np.mean(self.spectral_energy)
        features['spectral_flatness'] = np.mean(self.spectral_flatness)
        features['spectral_crest'] = np.mean(self.spectral_crest)

        return features

    def calculate_normalized_distribution(self):
        if self._acoustic_pressures_pascals is None:
            self._calculate_spectrum()

        self.probability_distribution = self._acoustic_pressures_pascals
        self.probability_distribution /= np.sum(self._acoustic_pressures_pascals, axis=0)

        self.integration_variable = self.frequencies

    def _calculate_mean_center(self):
        if self._acoustic_pressures_pascals is None:
            self._calculate_spectrum()

        if self.probability_distribution is None or self.integration_variable is None:
            self.calculate_normalized_distribution()

        if self._mean_center is None:
            self._mean_center = self.integration_variable - self.spectral_centroid

        return self._mean_center


class SpectrumByFFT(Spectrum):
    """
    This class is a specialization of the spectrum class that implements the way to define the spectrum. This is
    accomplished with the Fourier Transform, using a chunked overlapping representation of the data within the
    calculation.

    In this class the frequencies property represents the single-sided frequencies of the Fourier transform
    """

    def __init__(self, a: Waveform = None, fft_size: int = None):
        """
        Constructor - This constructor adds the ability of the class to define the specific size of the Fourier
        frequency bins. This also adds a number of elements that represent the double and single sided frequencies
        that originate with the Fourier transform methodologies.
        """
        #   Call the base constructor to define the waveform within the class
        super().__init__(a)

        #   Now define some information within the class related to the frequencies and the information generated
        #   specifically for the FFT methods
        self._fft_size = fft_size
        self._frequencies_double_sided = None
        self._frequencies_nb = None

        #   Define some other representations of the acoustic information that might be needed in various
        #   analyses.
        self._pressures_double_sided_complex = None

        if a is not None:
            #   There is no default value for the FFT size, so let's do some analysis to determine what the most optimal
            #   value of this should be if it is not provided.
            if self._fft_size is None:

                #   Set the default block size
                self._fft_size = int(2 ** np.floor(np.log2(len(self.waveform.samples))))

            elif self._fft_size > len(self.waveform.samples):
                raise ValueError('FFT block size cannot be greater than the total length of the signal.')

    def _calculate_spectrum(self):
        """
        This function generates the complex spectra using an FFT of multiple blocks of an input waveform,
        where the blocks have 50% overlap and are each weighted by a Hanning window.

        The FFT blocks are then scaled to contain the appropriate amount of energy for input into a power
        spectrum calculation.
        """

        #   Create the frequency arrays
        self._frequencies_double_sided = self.sample_rate * np.arange(0, self._fft_size) / self._fft_size
        self._frequencies_nb = self._frequencies_double_sided[:int(self._fft_size / 2)]
        df = self._frequencies_nb[1] - self._frequencies_nb[0]

        #   enforce a zero mean value
        x = self.waveform.samples - np.mean(self.waveform.samples)

        #   Generate a Hanning window
        ww = np.hanning(self._fft_size)
        W = np.mean(ww ** 2)

        #   Divide the total data into blocks with 50% overlap and Hanning window
        blocks = np.zeros(shape=(int(np.floor(2 * len(x) / self._fft_size - 1)), self._fft_size))

        for k in range(blocks.shape[0]):
            i = int(k * self._fft_size / 2)
            j = i + blocks.shape[1]
            blocks[k, :] = ww * x[i:j]

        #   Determine complex pressure amplitude
        self._pressures_double_sided_complex = np.sqrt(2 * df / self._fft_size /
                                                       self.sample_rate / W) * scipy.fft.fft(blocks, n=self._fft_size)

        #   Now assign the values for the acoustic pressures using this information, but only using the first hold of
        #   the frequency data.
        self._frequencies = self._frequencies_nb
        self._acoustic_pressures_pascals = self.auto_correlation_spectrum

    @property
    def frequency_increment(self):
        return self.frequencies[1] - self.frequencies[0]

    @property
    def frequencies_double_sided(self):
        """
        2-D Numpy array of double-sided frequencies from a Fourier transform of each block of a waveform
        with 50% overlap and a Hanning window in units of Pascals.
        """

        if self._frequencies_double_sided is None:
            self._calculate_spectrum()

        return self._frequencies_double_sided

    @property
    def pressures_complex_double_sided(self):
        """
        2-D Numpy array of double-sided complex pressures from a Fourier transform of each block of a waveform
        with 50% overlap and a Hanning window in units of Pascals.
        """
        if self._pressures_double_sided_complex is None:
            self._calculate_spectrum()

        return self._pressures_double_sided_complex

    @property
    def auto_correlation_spectrum(self):
        """
        Numpy array of single-sided real-valued pressures averaged over FFT of all blocks of a waveform with 50%
        overlap and a Hanning window.  Units of Pascals.
        """
        if self._pressures_double_sided_complex is None:
            self._calculate_spectrum()

        pressures_single_sided = self._pressures_double_sided_complex[:, :len(self._frequencies_nb)]
        return np.sqrt(np.mean((pressures_single_sided * np.conj(pressures_single_sided)).real, axis=0))

    @property
    def fft_size(self):
        return self._fft_size

    @property
    def power_spectral_density(self):
        """
        Numpy array of single-sided real-values. Pressures scaled by frequency, in units of Pascals / sqrt(Hz).
        """
        return self.pressures_pascals / np.sqrt(self.frequency_increment)

    @staticmethod
    def convert_nb_to_fob(frequencies_nb, pressures_pascals_nb, fob_band_width: int = 3, f0: float = 10,
                          f1: float = 10000):
        """
        This function converts the frequency and pressure arrays sampled in narrowband resolution to the fractional
        octave band resolution.

        Parameters
        ----------
        frequencies_nb: nd_array - the collection of narrowband frequencies that we want to convert
        pressures_pascals_nb: nd_array - the collection of pressures in units of pascals for the frequencies
        fob_band_width: int, default = 3 - the fractional octave band resolution that we desire
        f0: float, default = 10 - The start frequency of the output fractional octave frequencies
        f1: float, default = 10000 - The end frequency of the output fractional octave frequencies

        Returns
        -------
        frequencies_fob: nd_array - the collection of frequencies from f0 to f1 with the resolution of fob_band_width
        pressures_pascals_fob: nd_array - the fractional octave pressure in pascals at the associated frequencies
        """

        frequencies_fob = fob_tools.get_frequency_array(fob_band_width, f0, f1)

        #   Build the array of pressures that are the same size as the list of frequencies
        pressures_pascals_fob = np.zeros((len(frequencies_fob),))

        for i in range(len(frequencies_fob)):
            pressures_pascals_fob[i] = np.sqrt(sum(pressures_pascals_nb ** 2 *
                                                   fob_tools.filter_shape(fob_band_width, frequencies_fob[i],
                                                                          frequencies_nb)))

        return frequencies_fob, pressures_pascals_fob

    def to_fractional_octave_band(self, bandwidth: int = 3, f0: float = 10, f1: float = 10000):
        """
        This function will convert the spectrum from a narrowband resolution to a factional octave band resolution by
        applying the shape functions to the narrowband spectral values and determining the weighted value within the
        fractional octave band.

        Parameters
        ----------
        bandwidth: float, default = 3 - the fractional octave resolution that we will sample the frequency spectrum
        f0: float, default = 10 - the lowest frequency within the spectrum
        f1: float, default = 10000 - the heighest frequency within the spectrum

        Returns
        -------
        Spectrum - a spectrum object with the frequencies at the specified resolution and between the specified
        frequency values.
        """

        f_fob, p_fob = SpectrumByFFT.convert_nb_to_fob(self.frequencies, self.pressures_pascals, bandwidth, f0, f1)
        s = Spectrum()
        s.frequencies = f_fob
        s.pressures_pascals = p_fob
        s.start_fractional_octave_frequency = f0
        s.stop_fractional_octave_frequency = f1
        s.fractional_octave_bandwidth = bandwidth
        s._time0 = self.time

        return s


class SpectrumByDigitalFilters(Spectrum):

    """
    This class differs from the previous classes in that the determination of the spectrum is accomplished through an
    application of digital filters. A set of filters describing the collection of filters at the highest desired full
    octave band will be constructed. These coefficients will be applied as the signal is recursively down sampled at
    half the sample rate. The minimum number of elements required to generate the filtered data require three times
    the number of coefficients, doubled until we reach the maximum sample rate of the system.

    Development
    20221008 - FSM - Since we added the bandwidth, start and stop frequencies to the base class, this class no longer
        required a separate definition. All references were adjusted to use the base class values for these parameters.
    """

    def __init__(self, a: Waveform, fob_band_width: int = 3, f0: float = 10, f1: float = 10000):
        """
        The constructor - this will determine what the minimum number of samples required is to generate the lowest
        desired frequency.

        Parameters
        ----------
        a: Waveform - the audio signal that we want to process
        fob_band_width: int, default: 3 - the bandwidth of the fractional octave
        f0: float, default: 10 - the lowest frequency in Hz
        f1: float, default: 10000 - the highest frequency in the output
        """
        super().__init__(a)

        self._bandwidth = fob_band_width
        self._f0 = f0
        self._f1 = f1
        self._b_coefficients = list()
        self._a_coefficients = list()

        #   Build the filters for the highest desired full octave
        #
        #   Determine the center frequency of the highest octave
        full_band = int(np.floor(fob_tools.nearest_band(1, self.stop_fractional_octave_frequency)))
        f_full = fob_tools.center_frequency(1, full_band)
        f_lo = fob_tools.lower_frequency(1, full_band)
        f_hi = fob_tools.upper_frequency(1, full_band)

        #   Now that the know the center frequency of the highest band, determine the upper limit, and then the closest
        #   center frequency in the desired bandwidth
        f_band = int(np.floor(fob_tools.nearest_band(self.fractional_octave_bandwidth, f_hi)))
        nyquist = self.sample_rate / 2.0

        #   Loop through the frequencies within the highest octave band and create the associated digital filters for
        #   the element based on the calculated high and low frequencies.
        while fob_tools.lower_frequency(self.fractional_octave_bandwidth, f_band) >= f_lo * 0.90:
            #   Define the window for the bandpass filter
            upper = fob_tools.upper_frequency(self.fractional_octave_bandwidth, f_band)
            lower = fob_tools.lower_frequency(self.fractional_octave_bandwidth, f_band)
            window = np.array([lower, upper]) / nyquist

            #   Create the filter coefficients for this frequency band and add it to the list for each coefficient set
            b, a = scipy.signal.butter(
                3,
                window,
                btype='bandpass',
                analog=False,
                output='ba'
            )

            self._b_coefficients.append(b)
            self._a_coefficients.append(a)

            #   Decrement the band number to move to the next band down.
            f_band -= 1

        #   Convert the lists to arrays
        self._b_coefficients = np.asarray(self._b_coefficients)
        self._a_coefficients = np.asarray(self._a_coefficients)

    @property
    def settle_time(self):
        return self.settle_samples / self.sample_rate

    @property
    def settle_samples(self):
        """
        Based on requirements of Matlab filtering, you must have at least 3 times the number of coefficients to
        accurately filter data. So this will start with that minimum, and then move through the full octave frequency
        band numbers to determine the minimum number of samples that are required for the filter to adequately settle.
        """
        #   Determine the band number for the lowest band
        low_band = int(np.floor(fob_tools.nearest_band(1, self.start_fractional_octave_frequency)))
        hi_band = int(np.floor(fob_tools.nearest_band(1, self.stop_fractional_octave_frequency)))

        minimum_required_points = 3 * self._b_coefficients.shape[1]

        for band_index in range(low_band + 1, hi_band + 1):
            minimum_required_points *= 2

        return minimum_required_points

    def _calculate_spectrum(self):
        """
        This will take the waveform that exist within the class and calculate the fractional octave pressures within
        each band that is adequately covered by the length of the waveform.
        """

        #   Create the list that will hold the frequencies and band pressures
        pressures = list()
        frequency = list()

        #   Determine the octave bands that will need to be calculated to cover the desired frequency range.
        low_band = int(np.floor(fob_tools.nearest_band(1, self.start_fractional_octave_frequency)))
        hi_band = int(np.floor(fob_tools.nearest_band(1, self.stop_fractional_octave_frequency)))

        #   Get the index of the band at the top of the full octave filter
        fob_band_index = int(np.floor(fob_tools.nearest_band(self.fractional_octave_bandwidth,
                                                             fob_tools.upper_frequency(1, hi_band))))

        #   Make a copy of the waveform that can be decimated
        wfm = Waveform(pressures=self.waveform.samples.copy(),
                       sample_rate=self.sample_rate,
                       start_time=self.waveform.start_time)

        #   Loop through the frequencies in reverse order
        for band_index in range(hi_band, low_band - 1, -1):
            #   if there are insufficient number of points in the waveform, terminate the process now
            if len(wfm.samples) < 3 * self._b_coefficients.shape[1]:
                warnings.warn("The number of points within the Waveform are insufficient to calculate digital filters "
                              "lower than these frequencies")
                break

            #   Now loop through the filter definitions that are presented in decreasing frequency magnitude
            for filter_index in range(self._b_coefficients.shape[0]):
                filtered_waveform = wfm.apply_iir_filter(self._b_coefficients[filter_index, :],
                                                         self._a_coefficients[filter_index, :])

                frequency.append(fob_tools.center_frequency(self.fractional_octave_bandwidth, fob_band_index))
                pressures.append(np.std(filtered_waveform.samples))

                fob_band_index -= 1

            #   Decimate the waveform, halving the sample rate and making the filter definitions move down a full octave
            if len(wfm.samples) / 2 < 3 * self._b_coefficients.shape[1]:
                warnings.warn("The number of points within the Waveform are insufficient to calculate digital filters "
                              "lower than these frequencies")

                break

            wfm = Waveform(pressures=scipy.signal.decimate(wfm.samples, 2),
                           sample_rate=wfm.sample_rate,
                           start_time=wfm.start_time)

        #   Convert the information within the pressures and frequency arrays into the correct elements for the class
        frequency = np.asarray(frequency)[::-1]
        pressures = np.asarray(pressures)[::-1]

        idx0 = np.where(frequency > fob_tools.lower_frequency(self.fractional_octave_bandwidth,
                                                              fob_tools.nearest_band(
                                                                  self.fractional_octave_bandwidth,
                                                                  self.start_fractional_octave_frequency)))[0][0]
        idx1 = np.where(frequency < fob_tools.upper_frequency(self.fractional_octave_bandwidth,
                                                              fob_tools.nearest_band(
                                                                  self.fractional_octave_bandwidth,
                                                                  self.stop_fractional_octave_frequency)))[0][-1]
        self._frequencies = frequency[np.arange(idx0, idx1 + 1)]
        self._acoustic_pressures_pascals = pressures[np.arange(idx0, idx1 + 1)]


