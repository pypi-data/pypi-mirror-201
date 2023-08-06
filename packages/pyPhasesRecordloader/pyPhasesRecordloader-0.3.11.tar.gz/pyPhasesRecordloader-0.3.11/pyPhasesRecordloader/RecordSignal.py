import math
from typing import List

import numpy as np

from pyPhases.util.Logger import classLogger
from .Signal import Signal


@classLogger
class RecordSignal:
    processType = np.float32
    finalType = np.float32
    labelType = np.int32

    def __init__(self, targetFrequency=200, recordId=None):
        self.recordId = recordId
        self.signals: List[Signal] = []
        self.labelSignals = []
        self.signalNames = []
        self.targetFrequency = targetFrequency
        self.shape = None

    def getSignalFrequency(self, y):
        yFrequency = self.targetFrequency / (self.getShape()[1] / y.shape[0])
        return yFrequency

    def getSignalLength(self):
        return self.getShape()[1]

    @staticmethod
    def fromRecord(
        record, frequency=200, names=None, targetName="target", resampleY=False, windowSizeSeconds=None, recordId=None
    ):
        x, y = record
        if x.shape[0] > 0:
            if len(x.shape) == 4:
                x = x.reshape(1, x.shape[0] * x.shape[1], x.shape[2], x.shape[3])
                if windowSizeSeconds:
                    start = int(x.shape[2] / 2 - (windowSizeSeconds * frequency / 2))
                    stop = int(x.shape[2] / 2 + (windowSizeSeconds * frequency / 2))
                    x = x[:, :, start:stop, :]
                x = x.reshape(1, x.shape[1] * x.shape[2], x.shape[3])
            elif len(x.shape) == 3:
                x = x.reshape(1, x.shape[0] * x.shape[1], x.shape[2])
            elif len(x.shape) == 2:
                x = np.expand_dims(x, 0)
        if y.shape[0] > 0:
            if len(y.shape) == 3:
                y = y.reshape(1, y.shape[0] * y.shape[1], y.shape[2])
            if len(y.shape) == 2:
                y = np.expand_dims(y, 0)
        recordSignal = RecordSignal.fromArray(x[0].transpose(), frequency, frequency, names)

        if resampleY:
            yFrequency = frequency / (x.shape[1] / y.shape[1])
        else:
            yFrequency = frequency

        labelSignals = y[0].transpose()
        for s in labelSignals:
            labelSignals = Signal(targetName, s, yFrequency)
            if resampleY:
                labelSignals.resample(frequency, simple=True, antialiaseFIR=False)
            recordSignal.addLabelSignal(labelSignals)

        if recordId is not None:
            recordSignal.recordId = recordId

        return recordSignal

    @staticmethod
    def fromArray(array, targetFrequency=200, sourceFrequency=200, names=None, transpose=False):
        recordSignal = RecordSignal(targetFrequency=targetFrequency)
        if transpose:
            array = array.transpose()
        for i, signalArray in enumerate(array):
            name = names[i] if names is not None else "Signal%i" % i
            signal = Signal(name, signal=signalArray, frequency=sourceFrequency)
            recordSignal.addSignal(signal)

        return recordSignal

    def addSignal(self, signal: Signal, signalLabel=None):
        signalLabel = signal.name if signalLabel is None else signalLabel
        self.signals.append(signal)
        self.signalNames.append(signalLabel)
        signal.signal = signal.signal.astype(self.processType)
        self.shape = None

    def addSignals(self, signals: "list[Signal]"):
        for s in signals:
            self.addSignal(s)

    def addLabelSignal(self, signal: Signal):
        self.labelType = signal.signal.dtype
        self.labelSignals.append(signal)

    def addLabelSignals(self, signals: "list[Signal]"):
        for s in signals:
            self.addLabelSignal(s)

    def getShape(self, forceRecalculate=False):
        if self.shape is None or forceRecalculate:
            count = len(self.signals)
            count += len(self.labelSignals)
            if count == 0:
                raise Exception("can't determine signal shape if no signal is present")
            firstSignal = self.signals[0]
            frequency = firstSignal.frequency
            length = len(firstSignal.signal)
            factor = frequency / self.targetFrequency
            if length % factor > 0:
                self.logWarning("Target frequency might not be unambiguously")

            length = int(length / factor)
            self.shape = (count, length)

        return self.shape

    def getChannelList(self, listOrSlice):
        return list(range(0, self.signals.shape[1]))[listOrSlice] if type(listOrSlice) == slice else listOrSlice

    def generateFlatline(self, name="FLATLINE"):
        if name in self.signalNames:
            return self.getSignalIndexByName(name)

        signal = Signal("FLATLINE", frequency=self.targetFrequency)
        signal.signal = np.full(self.getShape()[1], 0)
        self.addSignal(signal)
        return signal

    def getSignalIndexByName(self, name):
        if name not in self.signalNames:
            if name == "FLATLINE":
                self.generateFlatline()
            else:
                from .RecordLoader import ChannelsNotPresent
                raise ChannelsNotPresent([name])
        return self.signalNames.index(name)

    def getSignalByName(self, name) -> Signal:
        index = self.getSignalIndexByName(name)
        return self.signals[index]

    def getFirstSignalByName(self, nameList) -> Signal:
        try:
            name = next(signalName for signalName in nameList if signalName in self.signalNames)
        except:
            if "FLATLINE" in nameList:
                return self.generateFlatline()
            from .RecordLoader import ChannelsNotPresent
            raise ChannelsNotPresent(nameList, msg="Non of the target signals (%s) is present in the record,: %s you can use FLATLINE as channel name to replace missing channels with a flat line" % (nameList, self.signalNames))

        index = self.getSignalIndexByName(name)
        return self.signals[index]

    def createSignalArray(self, signals, transpose):
        if len(signals) > 1:
            try:
                a = np.concatenate([s.signal.reshape(1, -1) for s in signals], axis=0)
            except ValueError as e:
                # check if signals have different length
                mismatchedSignals = []
                for s in signals:
                    if len(s.signal) != len(signals[0].signal):
                        mismatchedSignals.append(s.name)

                raise Exception(
                    "Not all Signals have the same length, can't create a singla numpy array.\n"
                    + "Make sure all Signals in preprocessing.targetChannels are resampled to a even length.\n"
                    "Signals that have a different shape then the first one: %s\n" % mismatchedSignals + "Error: %s" % e
                )
        else:
            a = signals[0].signal.reshape(1, -1)

        if transpose:
            a = a.transpose(1, 0)

        return a

    def getSignalArray(self, targetChannels=None, transpose=True, fillEmpty=True):
        "get all psg Signals that are present in targetChannels concatenated into one array"

        if targetChannels is not None:
            cList = []

            # target channel can be a string representing the signal name, or an list with
            # channelnames, where the first one is picked
            for channelStringorArray in targetChannels:
                if isinstance(channelStringorArray, list):
                    try:
                        signal = self.getFirstSignalByName(channelStringorArray)
                    except StopIteration:
                        if fillEmpty:
                            signal = Signal("empty", np.full(self.getShape()[1], 0), self.targetFrequency)
                            self.logError(
                                "None of the given targetchannel (%s) is present in the current psg signal"
                                % str(channelStringorArray)
                            )
                        else:
                            raise Exception(
                                "None of the given targetchannel (%s) is present in the current psg signal"
                                % str(channelStringorArray)
                            )
                else:
                    signalName = channelStringorArray
                    signal = self.getSignalByName(signalName)

                cList.append(signal)
        else:
            cList = self.signals

        return self.createSignalArray(cList, transpose).astype(self.finalType)

    def getAnnotationArray(self, transpose=True):
        "get all annotation signals concatenated into one array"

        return self.createSignalArray(self.labelSignals, transpose).astype(self.labelType)

    def reduceSignals(self, keepSignalNames):
        newSignals = []
        for keep in keepSignalNames:
            newSignals.append(self.getSignalByName(keep))
        self.signalNames = keepSignalNames
        self.signals = newSignals
        self.shape = None

    def combine(self, channels, newName="Unknown", mean=True, derive=False):
        count = len(channels)
        mainIndex = self.getSignalIndexByName(channels[0])
        mainSignal = self.signals[mainIndex]
        sig = mainSignal.signal.copy()

        targetFrequency = mainSignal.frequency
        targetLength = len(sig)

        for name in channels:
            i = self.getSignalIndexByName(name)
            if i != mainIndex:
                signal = self.signals[i]
                sArray = signal.signal
                if signal.frequency != targetFrequency:
                    raise Exception(
                        "The Channel %s does not have the same frequency with %s ... unable to combine"
                        % (signal.name, mainSignal.name)
                    )

                if len(sArray) != targetLength:
                    raise Exception("can only combine channels with the same size/sample rate")

                if derive:
                    sig -= signal.signal
                else:
                    sig += signal.signal

        if mean:
            sig = sig / count

        self.addSignal(Signal(newName, sig, frequency=targetFrequency))

    def derive(self, channels, newName="Unknown", mean=True):
        self.combine(channels, newName, mean=False, derive=True)

    def signalOffset(self, startOffset, endOffset=None, offsetFrequency=1):
        startOffset /= offsetFrequency

        if endOffset is not None:
            endOffset /= offsetFrequency

        for s in self.signals + self.labelSignals:
            f = s.frequency
            start = int(startOffset * f)
            end = None if endOffset is None else int(endOffset * f)
            s.signal = s.signal[slice(start, end)]

        self.shape = None

    def signalCut(self, cutStart, cutEnd, offsetFrequency=1):
        cutStart /= offsetFrequency

        if cutEnd is not None:
            cutEnd /= offsetFrequency

        for s in self.signals + self.labelSignals:
            f = s.frequency
            start = int(cutStart * f)
            end = None if cutEnd is None else int(cutEnd * f)
            s.signal = np.concatenate((s.signal[:start], s.signal[end:]))

        self.shape = None

    def signalCutBySignalBoolSignal(self, boolSignal):
        for s in self.signals + self.labelSignals:
            s.signal = s.signal[boolSignal]

    def checkPSGQuality(self):
        low_quality = []
        for signal in self.signals:
            signal.checkSignalQuality()
            if not (signal.quality is None):  # quality == None (default) wird ignoriert
                if signal.quality < 0.75:
                    low_quality.append(signal.name)
        if len(low_quality) > 0:
            qualityMessageString = "".join(["%s (Q: %.2f), " % (i, self.getSignalByName(i).quality) for i in low_quality])[:-2]
            self.logError("Low signal quality in record %s in channel(s) %s." % (self.recordId, qualityMessageString))
        return

    def plot(
        self,
        signalSlice=None,
        channelSlice=slice(None),
        signalNames=None,
        title="signal Plot",
        time_unit="minutes",
        annotations=None,
        returnFigure=False,
        maximalPoints=2000,
        resample=True,
        figsize=None,
        classification=None,
        secondsPerInch=10,
    ):
        import wfdb

        if resample:
            for s in self.signals:
                s.resample(self.targetFrequency, simple=True, antialiaseFIR=False)

        signalArray = self.getSignalArray(signalNames)
        if signalNames is None:
            signalNames = self.signalNames[channelSlice]

        distinct = "distinct" not in classification or classification["distinct"]

        addedSignals = 0
        if len(self.labelSignals) > 0:
            for labelIndex, labelSignal in enumerate(self.labelSignals):
                # make prettier labelSignals
                if classification:
                    classNames = (
                        classification["classNamesTest"] if "classNamesTest" in classification else classification["classNames"]
                    )
                    if "classValues" in classification and classification["classValues"] is not None:
                        classValues = classification["classValues"]
                    else:
                        classValues = {name: i for i, name in enumerate(classNames)}

                    labelSignal = self.labelSignals[labelIndex].signal

                    addSignals = []
                    if distinct:
                        if len(classNames) > 0:
                            self.labelSignals[labelIndex].signal = np.array([classValues[classNames[x]] for x in labelSignal])
                    else:
                        if len(classValues) == 0:
                            self.labelSignals[labelIndex].signal = labelSignal
                        else:
                            for className, value in classValues.items():
                                if value > 0:
                                    addSignal = self.labelSignals[labelIndex].signal & int(math.pow(2, value))
                                    addSignal = np.expand_dims(addSignal, 1)
                                    addSignals.append(addSignal)
                                    signalNames += [className]

                    if "secondsPerInch" in classification:
                        secondsPerInch = classification["secondsPerInch"]
                    elif classification["name"] == "sleepStage":
                        secondsPerInch = 30
                    elif classification["name"] == "legmovements":
                        secondsPerInch = 10
                    elif classification["name"] == "arousals":
                        secondsPerInch = 5
                    elif classification["name"] == "apnea":
                        secondsPerInch = 10

                if distinct:
                    signalNames += [self.labelSignals[labelIndex].name]

            addedSignals = len(addSignals)

            if distinct:
                addSignals = self.getAnnotationArray()
            else:
                addSignals = np.concatenate(addSignals, axis=1)

            signalArray = np.concatenate((signalArray, addSignals), axis=1)

        if signalSlice is None:
            l, channels = signalArray.shape
            step = 1
            if l > maximalPoints:
                step = l // maximalPoints
            signalSlice = slice(0, None, step)

        # if figsize in [[32,32], None]:
        figsize = figsize if figsize is not None else [32, 32]
        l = signalSlice.stop - signalSlice.start
        channels = signalArray.shape[1]
        newFigsize = (math.ceil(l / self.targetFrequency / (7 * secondsPerInch)), int(channels * 1 + 1))
        newFigsize = max(figsize[0], newFigsize[0]), min(figsize[1], newFigsize[1])

        f = wfdb.plot_items(
            signal=signalArray[signalSlice, :],
            fs=self.targetFrequency,
            title=title,
            time_units=time_unit,
            ylabel=signalNames,
            ann_samp=annotations,
            return_fig=returnFigure,
            sharex=True,
            figsize=newFigsize,
        )
        f.tight_layout()

        for i in range(addedSignals):
            f.axes[-i].set_yticks(range(len(classification["classNames"])))
            f.axes[-i].set_yticklabels(classification["classNames"])

        if returnFigure:
            [ax.grid() for ax in f.axes]
            return f

    def __getitem__(self, signalNames) -> "RecordSignal":
        """ Returns a new RecordSignal object with the given signalNames.
        """
        signal = RecordSignal(self.recordId, self.targetFrequency)
        if isinstance(signalNames, str):
            signalNames = [signalNames]
            
        for name in signalNames:
            signal.addSignal(self.getSignalByName(name))
            
        return signal