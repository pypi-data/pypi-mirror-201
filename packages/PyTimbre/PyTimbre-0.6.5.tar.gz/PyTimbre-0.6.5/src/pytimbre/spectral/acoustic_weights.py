import numpy
import numpy as np
import datetime


class AcousticWeights:
    """
    This class contains a number of calculations for various community noise metrics that are useful for a variety of
    calculations across the study of acoustics.

    FSM - the math module was replaced with references to the numpy module to facilitate use with numpy arrays and the
    pandas DataFrame objects
    """

    #TODO: Frank - make this more generic
    @staticmethod
    def sound_exposure_level(times, levels, dB_down):
        """
        The sound exposure level attempts to determine the equivalent level of the acoustic energy placed within a
        single second of the acoustic level.  The dB_down parameter determines how far below the peak that the algorithm
        seeks to integrate the data.

        times : datetime, array-like
            a collection of datetime objects that represent the times for the acoustic levels
        levels : double, array-like
            a collection of acoustic levels that are selected at the same time values as the times array
        dB_down : double
            the number of decibels below the peak that we will integrate the acoustics levels

        returns : double
            the integrated level between the times marking the location of the dB_down levels.
        """

        #   Find the indices for the integration

        start_index, stop_index = AcousticWeights.find_dB_down_limits(levels, dB_down)

        #   Determine the equivalent level between these times
        if isinstance(times[0], datetime.datetime):
            tin = (times[stop_index] - times[start_index]).total_seconds()
        else:
            tin = times[stop_index] - times[start_index]

        return AcousticWeights.leq(
            levels,
            tin,
            1,
            start_index,
            stop_index)

    @staticmethod
    def find_dB_down_limits(levels, dB_down_level):
        """
        Examine the array of levels and determine the points that were above the peak - dB_down_level

        levels : double, array-like
            the acoustic levels in an array that will be examined
        dB_down_level : double
            the level below the peak that will set the limits of the integration

        returns: double, tuple
            the start and stop index of the points to integrate
        """

        #   Find the maximum level

        max_level = max(levels)

        #   Find the index of the maximum value

        max_index = np.argmax(levels)

        #   Determine the start_index

        start_index = -1
        for i in range(max_index, -1, -1):
            if levels[i] <= (max_level - dB_down_level):
                start_index = i
                break

        #   Determine the stop_index

        stop_index = -1
        for i in range(max_index, len(levels), 1):
            if levels[i] <= (max_level - dB_down_level):
                stop_index = i
                break

        #   Apply some constraints to ensure that we are within the limits of the array

        if start_index < 0:
            start_index = 0
        if stop_index < 0:
            stop_index = len(levels) - 1

        #   Return the arrays

        return start_index, stop_index

    @staticmethod
    def leq(levels, tin, tout, start_index, stop_index):
        """
        The equivalent level is an integration of levels changing the temporal resolution of the acoustic levels.

        levels : double, array-like
            the list of acoustic levels
        tin : double
            the temporal integration of the input level
        tout : double
            the resultant temporal integration of the output level
        start_index : int
            the index within the levels array that we will begin the integration
        stop_index : int
            the index within the levels array that we will stop the integration

        returns : double
            the integrated, equivalent level
        """

        #   Initialize the acoustic equivalent level

        leq = 0.0

        #   Sum the linear elements units of sound

        for i in range(start_index, stop_index + 1, 1):
            leq += 10.0**(levels[i] / 10.0)

        #   apply the logarithmic conversion and the application of the temporal ratio

        return 10 * numpy.log10(leq) + 10 * numpy.log10(tin / tout)

    @staticmethod
    def lf(spl):
        """
        Compute the equal weighted acoustic level across the level array

        spl : double, array-like
            the sound pressure levels across a specific frequency array.  The frequencies are not provided for this
            function because there is an equal weighting across all frequencies.

        return : double
            the overall acoustic level with equal weighting
        """

        x = np.asarray(spl).copy()

        x /= 10.0
        x = 10.0 ** x
        x = np.sum(x, axis=len(x.shape) - 1)
        return 10 * np.log10(x)

    @staticmethod
    def la(spl, frequency):
        """
        Compute the A-weighted acoustic level across the level array

        spl : double, array-like
            the sound pressure levels across a specific frequency array
        frequency : double, array-like
            the array of frequencies to calculate the weighting

        return : double
            the overall acoustic level with equal weighting
        """

        x = np.asarray(spl).copy()
        if len(x.shape) == 1:
            x = np.reshape(x, (len(x), 1)).transpose()

        weights = np.ones((x.shape[0], 1)).dot(np.reshape(AcousticWeights.aw(frequency),
                                                          (len(frequency), 1)).transpose())

        x += weights
        x /= 10
        x = 10.0 ** x
        x = np.nansum(x, axis=(len(x.shape) - 1))
        return 10.0 * np.log10(x)

    @staticmethod
    def aw(frequency):
        """
        Given a frequency, determine the A-weighted correction for the acoustic level

        frequency : double, possible array-like
            the number of cycles per second to calculate the weight at
        """

        frequency = np.asarray(frequency).copy()

        f2 = 107.65265
        f3 = 737.86223
        K3 = 1.562339
        numerator = K3 * frequency ** 4.0
        denominator = (frequency ** 2 + f2 ** 2) * (frequency ** 2 + f3 ** 2)

        return 10 * numpy.log10(numerator / denominator) + AcousticWeights.cw(frequency)

    @staticmethod
    def cw(frequency):
        """
        Given a frequency, determine the C-weighted correction for the acoustic level

        frequency : double, possible array-like
            the number of cycles per second to calculate the weight at
        """
        f1 = 20.598997
        f4 = 12194.22
        K1 = 2.24e16
        numerator = K1 * frequency**4
        denominator = ((frequency**2 + f1**2)**2.0) * ((frequency**2 + f4**2)**2.0)

        frac = numerator / denominator
        # frac[frac <= 0] = np.nextafter(0, 1)
        return 10 * numpy.log10(frac)

    @staticmethod
    def pnl(dSPL):
        """
        Determine the single number perceived noise level (PNL) based on the conversion from dB to Noys

        dSPL : double, array-like
            the sound pressure levels from 10 Hz to 10 kHz

        returns : double
            returns the perceived noise level in NOYS

        Remarks:
        2022-12-13 - FSM - Changed the end of the code to ensure that there is a non-infinite results when the sume of
            the levels is zero because the level is too quiet.
        """

        Ld = [49, 44, 39, 34, 30, 27, 24, 21, 18, 16, 16, 16, 16, 16, 15, 12, 9, 5, 4, 5, 6, 10, 17, 21]
        Le = [55, 51, 46, 42, 39, 36, 33, 30, 27, 25, 25, 25, 25, 25, 23, 21, 18, 15, 14, 14, 15, 17, 23, 29]
        Lb = [64, 60, 56, 53, 51, 48, 46, 44, 42, 40, 40, 40, 40, 40, 38, 34, 32, 30, 29, 29, 30, 31, 37, 41]
        La = [91.01, 85.88, 87.32, 79.85, 79.76, 75.96, 73.96, 74.91, 94.63, 1000, 1000, 1000, 1000, 1000, 1000, 1000,
              1000, 1000, 1000, 1000, 1000, 1000, 44.29, 50.72]
        Lc = [52, 51, 49, 47, 46, 45, 43, 42, 41, 40, 40, 40, 40, 40, 38, 34, 32, 30, 29, 29, 30, 31, 34, 37]
        Md = [0.079520, 0.068160, 0.068160, 0.059640, 0.053013, 0.053013, 0.053013, 0.053013, 0.053013, 0.053013,
              0.053013, 0.053013, 0.053013, 0.053013, 0.059640, 0.053013, 0.053013, 0.047712, 0.047712, 0.053013,
              0.053013, 0.068160, 0.079520, 0.059640]
        Me = [0.058098, 0.058098, 0.052288, 0.047534, 0.043573, 0.043573, 0.040221, 0.037349, 0.034859, 0.034859,
              0.034859, 0.034859, 0.034859, 0.034859, 0.034859, 0.040221, 0.037349, 0.034859, 0.034859, 0.034859,
              0.034859, 0.037349, 0.037349, 0.043573]
        Mc = [0.030103, 0.030103, 0.030103, 0.030103, 0.030103, 0.030103, 0.030103, 0.030103, 0.030103, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0.02996, 0.02996]
        Mb = [0.043478, 0.04057, 0.036831, 0.036831, 0.035336, 0.033333, 0.033333, 0.032051, 0.030675, 0.030103,
              0.030103, 0.030103, 0.030103, 0.030103, 0.030103, 0.02996, 0.02996, 0.02996, 0.02996, 0.02996, 0.02996,
              0.02996, 0.042285, 0.042285]
        dfn = [0.0 for i in range(31)]
        d_sum = 0.0
        fFJ = 0.15
        for j in range(0, 7, 1):
            dfn[j] = 0
        for i in range(7, 31, 1):
            if dSPL[i] > 250:
                return -1000

            if dSPL[i] >= La[i - 7]:
                dfn[i] = AcousticWeights.ILOG10(Mc[i - 7] * (dSPL[i] - Lc[i - 7]))

            elif Lb[i - 7] <= dSPL[i] < La[i - 7]:
                dfn[i] = AcousticWeights.ILOG10(Mb[i - 7] * (dSPL[i] - Lb[i - 7]))

            elif Le[i - 7] <= dSPL[i] < Lb[i - 7]:
                dfn[i] = AcousticWeights.ILOG10(Me[i - 7] * (dSPL[i] - Lb[i - 7]))

            elif Ld[i - 7] <= dSPL[i] < Le[i - 7]:
                dfn[i] = 0.1 * AcousticWeights.ILOG10(Md[i - 7] * (dSPL[i] - Ld[i - 7]))

            if abs(dfn[i]) > 300:
                dfn[i] = 0

            if abs(dfn[i]) < -300:
                dfn[i] = 0

            if abs(dfn[i]) < 1e-10:
                dfn[i] = 0

            if dfn[i] > 2048:
                return -2000

        for i in range(0, 31, 1):
            if dfn[i] == float('inf'):
                dfn[i] = 0.0
        damx = dfn[7]

        for i in range(7, 31, 1):
            if dfn[i] > damx:
                damx = dfn[i]
            d_sum += dfn[i]
        d_sum = (d_sum - damx) * fFJ + damx

        if d_sum == 0:
            d_sum = 1
        return 40 + 33.22 * numpy.log10(d_sum)

    @staticmethod
    def ILOG10(x):
        """
        Determine the inverse log10, or 10**x
        """

        return 10.0 ** x

    @staticmethod
    def tone_correction(dSPL):
        """
        This function determines the tone correction applied to the sound pressure level spectrum.  It is based on the
        description of the calculation within the FAR part 36, Appendix A36.4.3.1.

        dSPL : double, array-like
            the collection of sound pressure levels from 10 Hz to 10 kHz

        returns : double
            the single value tone correction for the spectrum to be applied to the integrated acoustic levels.
        """

        #   Step 1 - Calculate the changes in adjacent sound pressure levels (or slopes)

        slopes = [0.0 for x in range(len(dSPL))]
        for i in range(0, len(slopes), 1):
            if i < 10:
                slopes[i] = 0.0
            else:
                slopes[i] = dSPL[i] - dSPL[i - 1]

        #   Step 2 - find any slope changes greater than 5

        large_slope_changes = [False for x in range(len(dSPL))]
        for i in range(0, len(large_slope_changes), 1):
            if abs(slopes[i]) > 5:
                large_slope_changes[i] = True
            else:
                large_slope_changes[i] = False

        #   Step 3 - select the sound pressure level that needs to be corrected

        select_sound_pressure_level = [False for x in range(len(dSPL))]
        for i in range(1, len(select_sound_pressure_level), 1):
            if large_slope_changes[i]:
                if slopes[i] > 0 and slopes[i] > slopes[i - 1]:
                    select_sound_pressure_level[i] = True
                elif slopes[i] <= 0 and slopes[i - 1] > 0:
                    select_sound_pressure_level[i - 1] = True
                else:
                    select_sound_pressure_level[i] = False
            else:
                select_sound_pressure_level[i] = False

        #   Step 4 - Adjust selected sound pressure levels

        spl_prime = [0.0 for x in range(len(dSPL))]
        for i in range(0, len(select_sound_pressure_level), 1):
            if not select_sound_pressure_level[i]:
                spl_prime[i] = dSPL[i]
            else:
                if 8 < i < 30:
                    spl_prime[i] = 0.5 * (dSPL[i - 1] + dSPL[i + 1])
                elif i == 30:
                    spl_prime[i] = dSPL[i - 1] + slopes[i - 1]

        #   Step 5 - recompute new slopes

        slope_prime = [0.0 for x in range(len(dSPL) + 1)]
        for i in range(1, len(spl_prime), 1):
            slope_prime[i] = spl_prime[i] - spl_prime[i - 1]
        slope_prime[31] = slope_prime[30]

        #   Step 6 - compute the arithmetic mean of adjacent three slopes

        mean_slope = [0.0 for i in range(30)]
        for i in range(0, len(mean_slope), 1):
            mean_slope[i] = (1.0 / 3.0) * (slope_prime[i] + slope_prime[i + 1] + slope_prime[i + 2])

        # Step 7 - compute the final one-third-octave sound pressure levels

        final_spl = [0.0 for x in range(31)]
        for i in range(0, len(final_spl), 1):
            if i < 10:
                final_spl[i] = dSPL[i]
            else:
                final_spl[i] = final_spl[i - 1] + mean_slope[i - 1]

        #   Step 8 - calculate the differences between the original and final SPL values

        F = [0.0 for x in range(len(dSPL))]
        for i in range(0, len(F), 1):
            F[i] = dSPL[i] - final_spl[i]

        #   Step 9 - for each of the relevant one-third-octave bands, determine tone correction factors from the sound
        #   pressure level differences (F[i]) and the table in the FAR

        tone_corrections = [0.0 for x in range(len(dSPL))]
        for i in range(0, len(dSPL), 1):
            if i < 9:
                tone_corrections[i] = 0.0
            elif 9 <= i < 17:
                if F[i] < 1.5:
                    tone_corrections[i] = 0.0
                elif 1.5 <= F[i] < 3:
                    tone_corrections[i] = 0.5
                elif 3 <= F[i] < 20:
                    tone_corrections[i] = F[i] / 6.0
                elif 20 <= F[i]:
                    tone_corrections[i] = 3.0 + (1.0 / 3.0)
            elif 17 <= i <= 27:
                if F[i] < 1.5:
                    tone_corrections[i] = 0.0
                elif 1.5 <= F[i] < 3:
                    tone_corrections[i] = 1
                elif 3 <= F[i] < 20:
                    tone_corrections[i] = F[i] / 3
                elif 20 <= F[i]:
                    tone_corrections[i] = 2 * (3.0 + (1.0 / 3.0))
            elif i > 27:
                if F[i] < 1.5:
                    tone_corrections[i] = 0.0
                elif 1.5 <= F[i] < 3:
                    tone_corrections[i] = 0.5
                elif 3 <= F[i] < 20:
                    tone_corrections[i] = F[i] / 6.0
                elif 20 <= F[i]:
                    tone_corrections[i] = 3.0 + (1.0 / 3.0)

        #   Return the maximum of the corrections

        return max(tone_corrections)
