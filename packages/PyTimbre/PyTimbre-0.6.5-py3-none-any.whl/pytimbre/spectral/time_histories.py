import abc
from enum import Enum
import pandas as pd

from .spectra import Spectrum, SpectrumByDigitalFilters, SpectrumByFFT, Waveform
from .acoustic_weights import AcousticWeights
from ..audio_files.wavefile import WaveFile
import numpy as np
import warnings
import datetime


class LeqDurationMode(Enum):
    """
    The available types of time scaling for conversion of a signal to equivalent levels
    """

    steady_state = 0
    transient = 1


class weighting_function(Enum):
    """
    This class provides the options on how to weight the calculation of the overall level values
    """

    unweighted = 0
    a_weighted = 1
    c_weighted = 2


class TimeHistory:
    """
    This class wraps the ability of the analysis to contain multiple spectrum objects and create a variation across
    time.

    Remarks
    2022-12-13 - FSM - added a function to collect the sound quality metrics from each of the spectra
    2022-12-13 - FSM - added a function to collect the times past midnight from the spectra objects
    """

    def __init__(self, a: Waveform = None, integration_time: float = 0.25):
        from ..audio_files.ansi_standard_formatted_files import StandardBinaryFile
        """
        Constructor - this will build a class object for the TimeHistory and instantiate all properties and protected
        elements.

        Parameters
        ----------
        :param a: This is the waveform object that we want to process into a TimeHistory object
        :param integration_time: float - the size of the independent waveforms that will be processed into a series of
            Spectrum objects
        """

        self._spectra = None
        self._times = None
        self._waveform = a
        self._integration_time = integration_time
        self._header = None

        #   Now if the Waveform object possesses a header field then we need to assign it to the header object here
        if isinstance(self.waveform, StandardBinaryFile):
            self._header = self.waveform.header
        elif isinstance(self.waveform, WaveFile):
            if self.waveform.header is not None:
                self._header = self.waveform.header
        elif isinstance(self.header, dict):
            self._header = self.header
            if 'HEADER SIZE' in self._header.keys():
                del self._header['HEADER SIZE']
        else:
            header_dict = None

    @abc.abstractmethod
    def _calculate_spectrogram(self):
        warnings.warn("This function must be implemented in any child class to create the collection of spectra objects"
                      " that define the time history")
        pass

    def save(self, filename: str):
        from ..audio_files.ansi_standard_formatted_files import StandardBinaryFile
        import datetime
        """
        This function saves the data from the waveform's header and the spectral information to a file 

        Parameters:
        -----------
        :param filename: string - the fill path to the output file
        
        Remarks
        -------
        20230221 - FSM - Updated the constructor to assign the header to the time history object if there is a header 
            within the Waveform object passed to the constructor.
        """

        #   open the output file

        file = open(filename, 'wt')

        #   If the header dictionary is present, write it to the output file

        if isinstance(self.waveform, StandardBinaryFile):
            header_dict = self.waveform.header
        elif isinstance(self.waveform, WaveFile):
            if self.waveform.header is not None:
                header_dict = self.waveform.header
        elif isinstance(self.header, dict):
            header_dict = self.header
            if 'HEADER SIZE' in header_dict.keys():
                del header_dict['HEADER SIZE']
        else:
            header_dict = None

        if header_dict is not None:
            header_line = ';{},{}\n'.format("HEADER SIZE", len(header_dict.keys()) + 1)
            file.write(header_line)

            unwanted_strs = [',']

            for key in header_dict.keys():
                for str in unwanted_strs:
                    new_key = key.replace(str, "_")
                header_line = ';{},{}\n'.format(new_key.upper(), header_dict[key])
                file.write(header_line)

        #   Now write the last header row which will have the time and frequency array

        header_line = ';{}'.format('year').ljust(7, ' ')
        header_line += ',{}'.format('month').ljust(7, ' ')
        header_line += ',{}'.format('day').ljust(7, ' ')
        header_line += ',{}'.format('hour').ljust(7, ' ')
        header_line += ',{}'.format('minute').ljust(7, ' ')
        header_line += ',{}'.format('second').ljust(7, ' ')

        for f in self.frequencies:
            header_line += ',{:6.2f}'.format(f).ljust(10, ' ')

        header_line += '\n'
        file.write(header_line)

        #   Now loop through the data
        for time_idx in range(len(self.spectra)):
            if isinstance(self.spectra[time_idx].time, datetime.datetime):
                data_line = '{:04.0f}'.format(self.spectra[time_idx].time.year).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(self.spectra[time_idx].time.month).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(self.spectra[time_idx].time.day).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(self.spectra[time_idx].time.hour).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(self.spectra[time_idx].time.minute).ljust(7, ' ')
                data_line += ',{:02.3f}'.format(self.spectra[time_idx].time.second +
                                                self.spectra[time_idx].time.microsecond * 1e-6).ljust(7, ' ')
            else:
                hour = np.floor(self.spectra[time_idx].time / 3600)
                minute = np.floor((self.spectra[time_idx].time - hour * 3600) / 60)
                second = self.spectra[time_idx].time - 60 * (60 * hour + minute)

                data_line = '{:04.0f}'.format(0).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(0).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(0).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(hour).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(minute).ljust(7, ' ')
                data_line += ',{:02.3f}'.format(second).ljust(7, ' ')

            #   Add the decibel data to the data_line object

            for j in range(len(self.frequencies)):
                data_line += ',{:03.2f}'.format(self.spectra[time_idx].pressures_decibels[j]).ljust(10, ' ')

            data_line += '\n'
            file.write(data_line)

        file.close()

    @staticmethod
    def load(filename: str):
        """
        This function will load the data from a file, and create the spectrum representation from the information within

        Parameters
        ----------

        filename: str - the full path to the
        """
        import os.path
        import pandas as pd

        if not os.path.exists(filename):
            raise ValueError("The filename must exist")

        file = open(filename, "rt")
        contents = file.readlines()
        file.close()

        th = TimeHistory()

        if contents[0][0] == ';':
            th._header = dict()

            n = 0

            while contents[n][0] == ';' and not (contents[n][:5] == ";year"):
                #   Split the data apart based on the comma
                elements = contents[n].split(',')
                if len(elements) == 2:
                    th._header[elements[0][1:]] = elements[1][:-1]
                else:
                    value = elements[-1][:-1]
                    name = ','.join(elements[:-1])
                    th._header[name[1:]] = value

                #   increment the line
                n += 1

                if contents[n] == "\n":
                    n += 1

            elements = contents[n].split(',')
            f = list()
            for freq_index in range(6, len(elements)):
                f.append(float(elements[freq_index]))

            frequencies = np.asarray(f)
            n += 1

            th._spectra = np.empty((len(contents) - n,), dtype=Spectrum)

            for line_index in range(n, len(contents)):
                elements = contents[line_index].split(',')

                if int(elements[0]) == int(elements[1]) == int(elements[2]) == 0:
                    time = 60 * (60 * float(elements[3]) + float(elements[4])) + float(elements[5])
                else:
                    year = int(elements[0])
                    month = int(elements[1])
                    day = int(elements[2])
                    hour = int(elements[3])
                    minute = int(elements[4])
                    seconds = float(elements[5])
                    second = int(np.floor(seconds))
                    microsecond = int(np.floor(1e6 * (seconds - second)))
                    time = datetime.datetime(year, month, day, hour, minute, second, microsecond)

                spl = np.zeros((len(frequencies),))
                for spl_idx in range(6, len(elements)):
                    spl[spl_idx - 6] = float(elements[spl_idx])

                th._spectra[line_index - n] = Spectrum()
                th._spectra[line_index - n]._frequencies = frequencies
                th._spectra[line_index - n]._acoustic_pressures_pascals = 20e-6 * 10 ** (spl / 20)
                th._spectra[line_index - n]._time0 = time

            #   Set the integration time as the difference between the first and second times
            th._integration_time = th.times[1] - th.times[0]
            return th

    @property
    def waveform(self):
        if self._waveform is None:
            warnings.warn('No Waveform object has been passed to this TimeHistory object.')
        return self._waveform

    @property
    def signal(self):
        return self.waveform.samples

    @property
    def sample_rate(self):
        """
        The number of samples per second of evey TimeHistory metric.
        """
        return 1 / self._integration_time

    @property
    def integration_time(self):
        return self._integration_time

    @property
    def duration(self):
        if self._waveform is not None:
            return self._waveform.duration
        else:
            return self.times[-1] - (self.times[0] - self.integration_time)

    @property
    def times(self):
        if self._spectra is None:
            self._calculate_spectrogram()

        if self._times is None:
            if self.spectra[0].time_past_midnight is not None:
                t = np.zeros((len(self._spectra),), dtype=datetime.datetime)
            else:
                t = np.zeros((len(self._spectra),))

            for i in range(len(self.spectra)):
                if self.spectra[i].waveform is not None:
                    t[i] = self.spectra[i].time
                else:
                    t[i] = self.spectra[i].time_past_midnight

            self._times = t

        return self._times

    @property
    def sample_size(self):
        return int(np.floor(self.integration_time * self._waveform.sample_rate))

    @property
    def frequencies(self):
        if self._spectra is None:
            self._calculate_spectrogram()

        return self._spectra[0].frequencies

    @property
    def spectra(self):
        if self._spectra is None:
            self._calculate_spectrogram()

        return self._spectra

    @property
    def spectrogram_array_decibels(self):
        if self._spectra is None:
            self._calculate_spectrogram()

        spectrogram = np.zeros([len(self._spectra), len(self._spectra[0].frequencies)])
        for i in range(len(self._spectra)):
            spectrogram[i, :] = self._spectra[i].pressures_decibels

        return spectrogram

    @property
    def overall_level(self):
        """
        Overall sound pressure level, unweighted (i.e. flat wieghted, Z-weighted) time history.  Calculated as the
        energetic sum of the fractional octave band spectral time history.
        """
        if self.spectra is None:
            self._calculate_spectrogram()

        levels = np.zeros((len(self.times)), )

        for i in range(len(self.spectra)):
            levels[i] = self.spectra[i].overall_level

        return levels

    @property
    def overall_a_weighted_level(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        levels = np.zeros((len(self.times)), )

        for i in range(len(self.spectra)):
            levels[i] = self.spectra[i].overall_a_weighted_level

        return levels

    def equivalent_level(self,
                         weighting: weighting_function = weighting_function.a_weighted,
                         equivalent_duration: float = 8 * 3600,
                         start_sample: int = 0,
                         stop_sample: int = None,
                         leq_mode: LeqDurationMode = None,
                         exposure_duration: float = None):
        """
        This function computes the equivalent level on the spectral time history. If there is a weighting
        function specified this is applied to the spectra. Additionally, the duration of the summation
        is specified (in seconds) for the new value with a default of 8 hours. Finally, if there is a cause to exclude
        portions of the data (i.e. calculating the SEL for the 10 dB down points in community noise) you can specify
        the start and stop index. If the stop index is None, then the last pressure defines the limit of the summation.

        Parameters
        ----------
        weighting   :   weighting_function
            The enumeration to determine filtering function applied to the waveform
        equivalent_duration :   float
            The denominator of the summation - in seconds - representing the desired length of total exposure
            time (e.g. an 8-hour duty day, or a 1-second sound exposure level)
        start_sample    :   int
            default = 0. The start sample of the pressure summation
        stop_sample :   int
            default = None. The stop sample, if the value is None, then it is replaces with the last sample index
        leq_mode    :   LeqDurationMode
            The enumeration to determine whether the input signal contains all energy
            of an exposure to the listener (transient) or the signal represents a sample of a longer-duration
            (steady_state) exposure
        exposure_duration   :   float
            If leq_mode is steady_state, this is the actual time of noise exposure to the
            listener in seconds

        """

        if stop_sample is None:
            stop_sample = len(self.times)

        number_of_samples = stop_sample - start_sample
        signal_duration = number_of_samples * np.mean(np.diff(self.times))

        weights=[]
        if weighting == weighting_function.unweighted:
            weights = np.zeros(np.size(self.frequencies))
        elif weighting == weighting_function.a_weighted:
            weights = AcousticWeights.aw(self.frequencies)
        elif weighting == weighting_function.c_weighted:
            weights = AcousticWeights.cw(self.frequencies)

        spectrogram_array_decibels_weighted = self.spectrogram_array_decibels + \
                                              np.tile(weights, (len(self.times), 1))

        spectrogram_array_pascals_weighted = 10 ** (spectrogram_array_decibels_weighted / 20) * 20e-6

        s = np.sum(np.sum(spectrogram_array_pascals_weighted[start_sample:stop_sample, :] ** 2))

        total_energy_in_signal = s / self.sample_rate

        total_energy_of_exposure = []
        if leq_mode == LeqDurationMode.transient:
            total_energy_of_exposure = total_energy_in_signal
        elif leq_mode == LeqDurationMode.steady_state:
            if exposure_duration is None:
                exposure_duration = signal_duration
            total_energy_of_exposure = total_energy_in_signal * (exposure_duration / signal_duration)
        elif leq_mode is None:
            raise ValueError("User must specify a signal duration mode of class LeqDurationMode.")

        average_energy_over_equivalent_duration = total_energy_of_exposure / equivalent_duration

        return 10.0 * np.log10(average_energy_over_equivalent_duration / 20e-6 / 20e-6)

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, value):
        self._header = value

    @property
    def roughness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        roughness = np.zeros((len(self.times),))

        for i in range(len(self.times)):
            roughness[i] = self.spectra[i].roughness

        return roughness

    @property
    def loudness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        loudness = np.zeros((len(self.times),))

        for i in range(len(self.times)):
            loudness[i] = self.spectra[i].loudness

        return loudness

    @property
    def sharpness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        sharpness = np.zeros((len(self.times),))

        for i in range(len(self.times)):
            sharpness[i] = self.spectra[i].sharpness

        return sharpness

    @property
    def spectral_centroid(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_centroid

        return r

    @property
    def spectral_spread(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_spread

        return r

    @property
    def spectral_skewness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_skewness

        return r

    @property
    def spectral_kurtosis(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_kurtosis

        return r

    @property
    def spectral_slope(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_slope

        return r

    @property
    def spectral_decrease(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_decrease

        return r

    @property
    def spectral_roll_off(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_roll_off

        return r

    @property
    def spectral_energy(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_energy

        return r

    @property
    def spectral_flatness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_flatness

        return r

    @property
    def spectral_crest(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_crest

        return r

    @property
    def times_past_midnight(self):
        tpm = np.zeros((len(self.spectra),))

        for i in range(len(tpm)):
            tpm[i] = self.spectra[i].time_past_midnight

        return tpm

    @property
    def get_features(self):
        """
        This function will obtain the temporal, spectral, sound quality, and level metrics from the waveform and the
        spectra within the time history.

        Returns
        -------
        A Pandas.DataFrame with the information from each spectrum
        """

        #   Create the DataFrame that will hold the data from the waveform and the spectrum objects
        names = ['attack', 'decrease', 'release', 'log_attack', 'attack_slope', 'decrease_slope', 'temporal_centroid',
                 'effective_duration', 'amplitude_modulation', 'frequency_modulation', 'loudness', 'roughness',
                 'sharpness', 'zero_crossing_rate', 'auto_correlation_00', 'auto_correlation_01', 'auto_correlation_02',
                 'auto_correlation_03', 'auto_correlation_04', 'auto_correlation_05', 'auto_correlation_06',
                 'auto_correlation_07', 'auto_correlation_08', 'auto_correlation_09', 'auto_correlation_10',
                 'auto_correlation_11', 'spectral_centroid', 'spectral_spread', 'spectral_skewness',
                 'spectral_kurtosis', 'spectral_slope', 'spectral_decrease', 'spectral_roll_off', 'spectral_energy',
                 'spectral_flatness', 'spectral_crest', 'lf', 'la']
        for f in self.frequencies:
            names.append('F{:06.0f}Hz'.format(f))

        names.append('time')

        df = pd.DataFrame(columns=names, index=np.arange(len(self.times)))

        for i in range(df.shape[0]):
            s = self.spectra[i]
            if isinstance(s, Spectrum):
                if s.waveform is None:
                    df.iloc[i, :14+12] = [np.nan] * (14 + 12)
                else:
                    df.iloc[i, :14] = [s.waveform.attack,
                                       s.waveform.decrease,
                                       s.waveform.release,
                                       s.waveform.log_attack,
                                       s.waveform.attack_slope,
                                       s.waveform.decrease_slope,
                                       s.waveform.temporal_centroid,
                                       s.waveform.effective_duration,
                                       s.waveform.amplitude_modulation,
                                       s.waveform.frequency_modulation,
                                       np.mean(s.waveform.loudness),
                                       np.mean(s.waveform.roughness),
                                       np.mean(s.waveform.sharpness),
                                       np.mean(s.waveform.zero_crossing_rate)]
                    df.iloc[i, 14:14 + 12] = np.mean(s.waveform.auto_correlation, axis=0)

                df.iloc[i, 26:38] = [s.spectral_centroid,
                                     s.spectral_spread,
                                     s.spectral_skewness,
                                     s.spectral_kurtosis,
                                     s.spectral_slope,
                                     s.spectral_decrease,
                                     s.spectral_roll_off,
                                     s.spectral_energy,
                                     s.spectral_flatness,
                                     s.spectral_crest,
                                     s.overall_level,
                                     s.overall_a_weighted_level]
                for band_index in range(len(self.frequencies)):
                    df.iloc[i, 38 + band_index] = s.pressures_decibels[band_index]

                df.iloc[i, -1] = s.time_past_midnight

        return df


class NarrowbandTimeHistory(TimeHistory):
    """
    This class implements the _calculate_spectrogram function using the Narrowband_Spectrum class
    """

    def __init__(self, a: Waveform, integration_time: float = 0.25, fft_size: int = None):
        super().__init__(a, integration_time)

        self._fft_size = fft_size

        #   There is no default value for the FFT size, so let's do some analysis to determine what the most optimal
        #   value of this should be if it is not provided.
        if self._fft_size is None:

            #   Set the default block size
            sub_wfm_length = self.integration_time * self.waveform.sample_rate
            self._fft_size = int(2 ** np.floor(np.log2(sub_wfm_length)))

        elif (self._fft_size > len(self.waveform.samples)) or \
                (self.fft_size > self.integration_time * self.sample_rate):
            raise ValueError('FFT block size cannot be greater than the total length of the signal.')

    @property
    def fft_size(self):
        return self._fft_size

    def _calculate_spectrogram(self):
        from ..waveform import TrimmingMethods

        """
        This function will divide the waveform up into contiguous sections of the waveform
        """

        #   Determine the maximum number of whole samples that exist within the waveform.
        N = int(np.floor(self.duration / self.integration_time))

        #   Create the list of spectra that will be used later
        self._spectra = np.empty((N,), dtype=SpectrumByFFT)

        #   Set the starting sample
        s0 = 0

        #   Loop through the elements and create the spectral object
        for n in range(N):
            #   get the subset of data from the waveform
            subset = self.waveform.trim(s0, s0 + self.sample_size, TrimmingMethods.samples)

            #   Create the spectrum object and add it as the ith element in the array
            self._spectra[n] = SpectrumByFFT(subset, self.fft_size)

            #   increment the starting sample
            s0 += self.sample_size

    def to_logarithmic_band_time_history(self, fob_band_width: int = 3, f0: float = 10, f1: float = 10000):
        """
        This function utilizes the functions within the SpectrumByFFT to generate a collection of
        Spectrum objects within a TimeHistory object.

        Parameters
        ----------
        fob_band_width: int, Default = 3 - the fractional octave bandwidth
        f0: float, default = 10 - the lower frequency band center frequency
        f1: float, default = 10000 - the upper frequency band center frequency

        Returns
        -------
        A TimeHistory object with the information from this time history converted to a different frequency
        representation.
        """

        #   Create the output object
        th = TimeHistory()
        th.header = self.header
        th._spectra = np.empty(len(self.spectra), dtype=Spectrum)

        for i in range(len(self.spectra)):
            if isinstance(self.spectra[i], SpectrumByFFT):
                th._spectra[i] = self.spectra[i].to_fractional_octave_band(fob_band_width, f0, f1)

        return th


class LogarithmicBandTimeHistory(TimeHistory):
    """
    This function possesses the digital filtered version of the spectrum
    """

    def __init__(self, a: Waveform, integration_time: float = 0.25, fob_band_width: int = 3, f0: float = 10,
                 f1: float = 10000):
        super().__init__(a, integration_time)

        self._bandwidth = fob_band_width
        self._start_frequency = f0
        self._stop_frequency = f1

    @property
    def bandwidth(self):
        return self._bandwidth

    @property
    def start_frequency(self):
        return self._start_frequency

    @property
    def stop_frequency(self):
        return self._stop_frequency

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

        return self.spectra[0].settle_samples

    def _calculate_spectrogram(self):
        from ..waveform import TrimmingMethods

        """
        This function will divide the waveform up into contiguous sections of the waveform
        """

        #   Determine the maximum number of whole samples that exist within the waveform.
        N = int(np.floor(self.duration / self.integration_time))

        #   Create the list of spectra that will be used later
        self._spectra = np.empty((N,), dtype=SpectrumByDigitalFilters)

        #   Set the starting sample
        s0 = 0

        #   Loop through the elements and create the spectral object
        for n in range(N):
            #   get the subset of data from the waveform
            subset = self.waveform.trim(s0, s0 + self.sample_size, TrimmingMethods.samples)

            #   Create the spectrum object and add it as the ith element in the array
            self._spectra[n] = SpectrumByDigitalFilters(subset, self.bandwidth, self.start_frequency,
                                                        self.stop_frequency)

            #   increment the starting sample
            s0 += self.sample_size

    def calculate_engineering_scale_factor(self, calibration_level: float = 94, calibration_frequency=1000):
        sensitivities = np.zeros((len(self.spectra),))

        for i in range(len(self.spectra)):
            sensitivities[i] = self.spectra[i].calculate_engineering_unit_scale_factor(calibration_level,
                                                                                       calibration_frequency)

        return np.mean(sensitivities)
