from enum import Enum

import numpy as np
from pyPhases.util.Logger import classLogger
from scipy.signal import butter, fftconvolve, firwin, iirfilter, kaiserord, lfilter, resample, sosfilt
from scipy.stats import kurtosis, skew


class SignalType(Enum):
    UNKNOWN = 0
    EEG = 1
    EOG = 2
    EMG = 3
    EFFORT = 4
    FLOW = 5
    MIC = 6
    SAO2 = 7
    BODY = 8
    RR = 9
    ECG = 10


signalTypeDict = {
    "sao2": SignalType.SAO2,
    # "hr": ,
    "eeg": SignalType.EEG,
    "eog": SignalType.EOG,
    "emg": SignalType.EMG,
    "ecg": SignalType.ECG,
    "body": SignalType.BODY,
    "effort": SignalType.EFFORT,
    "flow": SignalType.FLOW,
    # "light": ,
    # "oxstat": ,
    "mic": SignalType.MIC,
    # "cpap": ,
    "unknown": SignalType.UNKNOWN,
}

defaultChannelSettings = {
    SignalType.UNKNOWN: {
        "dimension": "",
        "physicalMin": 0,
        "physicalMax": 100,
        "digitalMin": 0,
        "digitalMax": 1023,
    },
    SignalType.EEG: {
        "dimension": "uV",
        "physicalMin": -300,
        "physicalMax": 300,
        "digitalMin": 0,
        "digitalMax": 1023,
    },
    SignalType.EOG: {
        "dimension": "uV",
        "physicalMin": -300,
        "physicalMax": 300,
        "digitalMin": 0,
        "digitalMax": 255,
    },
    SignalType.EMG: {
        "dimension": "uV",
        "physicalMin": -78,
        "physicalMax": 78,
        "digitalMin": 0,
        "digitalMax": 1023,
    },
    SignalType.EFFORT: {
        "dimension": "",
        "physicalMin": -100,
        "physicalMax": 100,
        "digitalMin": 0,
        "digitalMax": 4095,
    },
    SignalType.FLOW: {
        "dimension": "",
        "physicalMin": 0,
        "physicalMax": 4095,
        "digitalMin": 0,
        "digitalMax": 4095,
    },
    SignalType.MIC: {
        "dimension": "",
        "physicalMin": -100,
        "physicalMax": 100,
        "digitalMin": 0,
        "digitalMax": 255,
    },
    SignalType.SAO2: {
        "dimension": "%",
        "physicalMin": 0,
        "physicalMax": 100,
        "digitalMin": 0,
        "digitalMax": 1023,
    },
    SignalType.BODY: {
        "dimension": "",
        "physicalMin": 0,
        "physicalMax": 255,
        "digitalMin": 0,
        "digitalMax": 255,
    },
    SignalType.RR: {
        "dimension": "",
        "physicalMin": 0,
        "physicalMax": 200,
        "digitalMin": 0,
        "digitalMax": 200,
    },
    SignalType.ECG: {
        "dimension": "uV",
        "physicalMin": -300,
        "physicalMax": 300,
        "digitalMin": 0,
        "digitalMax": 1023,
    },
}


@classLogger
class Signal:
    def __init__(
        self, name="Unknown", signal: np.ndarray = None, frequency=100, type=SignalType.UNKNOWN, typeStr="unknown"
    ) -> None:
        self.name = name
        self.signal = signal
        self.frequency = frequency
        self.type = type
        self.typeStr = typeStr
        self.isDigital = False

        self.dimension = None
        self.physicalMin = None
        self.physicalMax = None
        self.digitalMin = None
        self.digitalMax = None
        self.transducer = ""
        self.prefilter = ""
        self.sourceIndex = None
        self.processHistory = []
        self.quality = None

        self.loadDefaultSettings()

    def loadDefaultSettings(self):
        settings = defaultChannelSettings[self.type]
        for _, index in enumerate(settings):
            setattr(self, index, settings[index])

    def setSignalTypeFromTypeStr(self):
        if self.typeStr in signalTypeDict:
            self.type = signalTypeDict[self.typeStr]
        else:
            self.type = SignalType.UNKNOWN
            self.logWarning("Unkown type of signal '%s'" % self.typeStr)

    def getFilterCoefficients(self, tansitionWidth=15.0, cutOffHz=30.0, rippleDB=40.0):
        nyq_rate = self.frequency / 2.0
        width = tansitionWidth / nyq_rate
        N, beta = kaiserord(rippleDB, width)
        if nyq_rate <= cutOffHz:
            cutOffHz = nyq_rate - 0.001
            self.logWarning("Cutoff frequency for FIR was adjusted to nyquist frequency.")

        # Use firwin with a Kaiser window to create a lowpass FIR filter.
        taps = firwin(N, cutOffHz / nyq_rate, window=("kaiser", beta))

        return taps

    def resample(self, targetFrequency, simple=False, antialiaseFIR=True):
        "downsample the signal, if the signal length is not completely divisible with the frequency it will be cut off at the end"
        if antialiaseFIR:
            self.antialiasingFIR()

        l = len(self.signal) * targetFrequency

        if self.frequency > 1 and l % self.frequency != 0 and self.frequency % targetFrequency != 0:
            self.logError("Signal has decimal downscale factor")

        l = int(l / self.frequency)

        if simple:

            factor = self.frequency / targetFrequency
            if factor >= 1:
                self.signal = self.signal[:: int(factor)]
            else:
                self.signal = np.repeat(self.signal, int(1 / factor), axis=0)
        else:
            self.signal = resample(self.signal, l)

        self.frequency = targetFrequency

    def antialiasingFIR(self):
        self.signal = np.convolve(self.signal, self.getFilterCoefficients(), mode="same")

    def bandpass(self, low, high, order=10):
        nyq_rate = self.frequency / 2.0
        if nyq_rate <= high:
            high = nyq_rate - 0.001
            self.logWarning("High frequency for bandpass was adjusted to nyquist frequency.")
        self.filter((low, high), order, "bp")

    def lowpass(self, value, order=10):
        self.filter(value, order, "lp")

    def lowpass(self, value, order=10):
        self.filter(value, order, "hp")

    def filter(self, filterValues, order=10, type="bp"):
        sos = butter(order, filterValues, type, fs=self.frequency, output="sos")

        self.signal = sosfilt(sos, self.signal)

    def simpleNormalize(self, minValue=None, maxValue=None, cut=True):

        signalMin = min(self.signal)
        signalMax = max(self.signal)
        if minValue is None:
            minValue = signalMin

        if maxValue is None:
            maxValue = signalMax

        signal = self.signal

        if cut:
            self.signal[signal > maxValue] = maxValue
            self.signal[signal < minValue] = minValue
            if minValue < 0:
                self.signal += minValue

            self.signal /= maxValue
            self.signal -= 0.5
        else:
            signalMinAbs = -1 * signalMin
            self.signal = (signal + signalMinAbs) / (signalMinAbs + signalMax)
            self.signal *= maxValue - minValue
            self.signal += minValue

    def sigmoid(self):
        self.signal = 1 / (1 + np.exp(-self.signal))

    def tanh(self):
        self.signal = np.tanh(self.signal)

    def scale(self):
        center = np.mean(self.signal)
        scale = np.std(self.signal)
        if scale == 0:
            scale = 1
        self.signal = (self.signal - center) / scale

    def fftConvolution(self, kernel_size):
        # Compute and remove moving average with FFT convolution
        resultShape = self.signal.shape
        center = np.zeros(resultShape)

        center = fftconvolve(self.signal, np.ones(shape=(kernel_size,)) / kernel_size, mode="same")

        self.signal = self.signal - center

        # Compute and remove the rms with FFT convolution of squared signal
        scale = np.ones(resultShape)

        temp = fftconvolve(np.square(self.signal), np.ones(shape=(kernel_size,)) / kernel_size, mode="same")

        # Deal with negative values (mathematically, it should never be negative, but fft artifacts can cause this)
        temp[temp < 0] = 0.0

        # Deal with invalid values
        invalidIndices = np.isnan(temp) | np.isinf(temp)
        temp[invalidIndices] = 0.0
        maxTemp = np.max(temp)
        temp[invalidIndices] = maxTemp

        # Finish rms calculation
        scale = np.sqrt(temp)

        # To correct records that have a zero amplitude signal
        scale[(scale == 0) | np.isinf(scale) | np.isnan(scale)] = 1.0
        self.signal = self.signal / scale

    def notchFilter(self):
        """Perform 60 Hz notch filtering using scipy library.

        Parameters
        ----------
        signal : 1D numpy.array
            Array to filter.
        axis: int
            Choose axis where to perform filtering.
        forward_backward : boolean
            Set True if you want a null phase shift filtered signal

        Returns
        -------
            1D numpy.array
                The signal filtered
        """
        fs = self.frequency

        b1, a1 = iirfilter(2, [0.4 / (fs / 2.0), 18 / (fs / 2.0)], btype="bandpass", ftype="butter")

        b2, a2 = iirfilter(3, [58 / (fs / 2.0), 62 / (fs / 2.0)], btype="bandstop", ftype="butter")
        b3, a3 = iirfilter(3, [48 / (fs / 2.0), 52 / (fs / 2.0)], btype="bandstop", ftype="butter")
        b4, a4 = iirfilter(1, [62 / (fs / 2.0), 63 / (fs / 2.0)], btype="bandstop", ftype="bessel")

        a = np.polymul(np.polymul(np.polymul(a1, a2), a3), a4)
        b = np.polymul(np.polymul(np.polymul(b1, b2), b3), b4)
        result = lfilter(b, a, self.signal, axis=-1)
        return result

    def windowedBandpower(self, lower, upper, windowsize):
        import scipy

        def bandpower(x, fs, fmin, fmax):
            f, Pxx = scipy.signal.periodogram(x, fs, window="hamming")
            ind_min = scipy.argmax(f > fmin) - 1
            ind_max = scipy.argmax(f > fmax)
            f_dist = f[1] - f[0]
            return sum(Pxx[ind_min:ind_max] * f_dist)

        windowsize = int(windowsize)
        bp = np.zeros(int(np.floor(self.signal.size / windowsize)))
        for i in range(bp.size):
            x = self.signal[i * windowsize : (i + 1) * windowsize]
            bp[i] = bandpower(x, self.frequency, lower, upper)

        return bp

    def plot(self, signalSlice=slice(None)):
        import matplotlib.pyplot as plt

        plt.plot(self.signal[signalSlice])
        plt.show()

    def fixedSize(self, size, fillValue=0):

        centerNew = size // 2
        signalSize = len(self.signal)
        centerSignal = signalSize // 2
        startAt = centerNew - centerSignal

        self.signal = np.full(size, fillValue)
        self.signal[startAt:signalSize] = self.signal

    def interpolateByThreshold(self, lowerLimit=None, upperLimit=None):
        if lowerLimit is not None:
            self.signal[self.signal < lowerLimit] = np.nan
        if upperLimit is not None:
            self.signal[self.signal > upperLimit] = np.nan
        nanIndex = np.isnan(self.signal)
        lenRange = np.arange(len(self.signal))
        self.signal[nanIndex] = np.interp(lenRange[nanIndex], lenRange[~nanIndex], self.signal[~nanIndex])

    def checkSignalQuality(self):
        signalBackup = self.signal
        if self.typeStr == "unknown":
            self.logWarning("Unkown type of signal '%s'" % str(self.name))
        elif self.typeStr in ["body", "eog", "mic", "light", "ppg", "movement"]:
            self.logWarning("There is no signal quality check for signals of type '%s' available." % str(self.typeStr))
        elif self.typeStr == "sao2":
            nLowQuality = sum((self.signal < 70) | (self.signal > 99))
            self.quality = 1 - (nLowQuality / len(self.signal))
        elif self.typeStr == "emg":
            if self.dimension in ["uV"]:
                self.filter([10, min(100, self.frequency / 2.01)], order=3)
                # defaultEpochSize = 30
                # if self.signal.shape[0]%(defaultEpochSize*self.frequency):
                #     self.signal = self.signal[0:int(self.signal.shape[0]/(defaultEpochSize*self.frequency))*int(defaultEpochSize*self.frequency)]
                # windowed30 = np.reshape(
                #     self.signal, (round(len(self.signal) / (defaultEpochSize * self.frequency)), round(defaultEpochSize * self.frequency))
                # )
                # numFlatEpochs = sum(np.median(abs(windowed30), axis=1) < 0.1)
                windowed1 = np.reshape(self.signal, (round(len(self.signal) / self.frequency), round(self.frequency)))
                numFlatSeconds = sum(np.median(abs(windowed1), axis=1) < 0.1)
                numNoisySeconds = sum(np.mean(abs(windowed1), axis=1) > 2)
                self.quality = 1 - ((numFlatSeconds + numNoisySeconds) / windowed1.shape[0])
        elif self.typeStr == "eeg":
            if self.dimension in ["uV"]:
                pass
            elif self.dimension in ["mV"]:
                self.signal = self.signal * 1000
            else:
                self.logError("Unkown Signaldimension '%s' in signal '%s', assuming 'uV'" % (str(self.dimension), self.name))
            self.bandpass(low=0.3, high=35, order=3)
            defaultWindowSize = 8
            if self.signal.shape[0] % (defaultWindowSize * self.frequency):
                self.signal = self.signal[
                    0 : int(self.signal.shape[0] / (defaultWindowSize * self.frequency))
                    * int(defaultWindowSize * self.frequency)
                ]
            windowed = np.reshape(
                self.signal,
                (round(len(self.signal) / (defaultWindowSize * self.frequency)), round(defaultWindowSize * self.frequency)),
            )
            # Kriterien inkl. Schwelllwerten aus der Veröffentlichung DOI: 10.1109/JBHI.2019.2920381
            highAmpl = np.sum(abs(windowed) > 151.09, axis=1) / windowed.shape[1] > (
                1 / defaultWindowSize * 0.5
            )  # 95: 95, 100: 151.09
            highStd = np.std(windowed, axis=1) > 33.23  # 95: 22.29, 100: 33.23
            # highApEn = ... > 0.65 # 95: 1.01, 100: 0.65
            # highAmplVar = (np.max(abs(windowed), axis=1) / np.square(np.std(windowed, axis=1))) > 1.02e5 # 95: 1.56e5, 100: 1.02e5
            highKurt = kurtosis(windowed, axis=1, bias=False) > 14.56  # 95: 6.53, 100: 14.56
            highSkew = abs(skew(windowed, axis=1, bias=False)) > 1.79  # 95: 0.69, 100: 1.79

            sumArtefacts = highAmpl + highStd + highKurt + highSkew
            self.quality = 1 - (sum(sumArtefacts) / len(sumArtefacts))

        elif (self.typeStr == "effort") | (self.typeStr == "flow"):
            from teleschlafmedizin.model.TimeseriesSignal import TimeseriesSignal

            timeseries = TimeseriesSignal(self)
            timeseries.bbi()
            lengthUnfilteredPositions = len(timeseries.positions)
            if lengthUnfilteredPositions == 0:
                self.quality = 0
                return
            lowerRespiratoryCycleLimit = 60 / 20
            upperRespiratoryCycleLimit = 60 / 9  # this quality criteria might exclude signals because of high AHI
            self.quality = 1 - (
                len(
                    timeseries.values[
                        (timeseries.values < lowerRespiratoryCycleLimit) | (timeseries.values > upperRespiratoryCycleLimit)
                    ]
                )
                / len(timeseries.values)
            )
        elif self.typeStr in ["ecg", "rr"]:
            from teleschlafmedizin.model.TimeseriesSignal import TimeseriesSignal

            timeseries = TimeseriesSignal(self)
            if self.typeStr == "ecg":
                timeseries.rri(filter=False)
            elif self.typeStr == "rr":
                timeseries.rr2rri()
            lengthUnfilteredPositions = len(timeseries.positions)
            if lengthUnfilteredPositions == 0:
                self.quality = 0
                return
            timeseries.timeseriesFilterPercentage()
            lengthFilteredPositions = len(timeseries.positions)
            if lengthFilteredPositions == 0:
                self.quality = 0
                return
            meanHeartRateBpm = lengthFilteredPositions / ((timeseries.positions[-1] - timeseries.positions[0]) / 60)
            if meanHeartRateBpm < 35:
                self.quality = 0
            elif meanHeartRateBpm > 140:
                self.quality = 0
            else:
                self.quality = lengthFilteredPositions / lengthUnfilteredPositions
                # if self.quality < 0.75: # erstmal diese harte zusätzliche Regel für das EKG für Kompatibilität mit Miriams Vorarbeiten
                # self.quality = 0
        elif self.typeStr in ["hr"]:
            lower35 = self.signal < 35
            higher140 = self.signal > 140
            sumArtefacts = lower35 + higher140
            self.quality = 1 - (sum(sumArtefacts) / len(sumArtefacts))
        else:
            self.logError("Unkown signalTypeStr '%s'." % str(self.typeStr))
        self.signal = signalBackup
        return
