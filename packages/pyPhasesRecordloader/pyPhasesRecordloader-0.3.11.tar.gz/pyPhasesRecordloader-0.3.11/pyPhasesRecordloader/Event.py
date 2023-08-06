from dataclasses import dataclass


@dataclass
class Event:

    name: str = ""
    start: float = 0
    duration: float = 0
    amplitude: float = 0
    power: float = 0
    frequency: int = 1
    owner: str = None
    manual: bool = False
    data = {}

    def end(self):
        return self.start + self.duration

    def updateFrequency(self, frequency, originalFrequency=None):
        originalFrequency = self.frequency if originalFrequency is None else originalFrequency
        factor = frequency / originalFrequency
        self.start *= factor
        self.duration *= factor
        self.frequency = frequency

    def todict(self):
        return {
            "name": self.name,
            "start": self.start,
            "duration": self.duration,
            "amplitude": self.amplitude,
            "power": self.power,
            "frequency": self.frequency,
            "owner": self.owner,
            "manual": self.manual,
            "data": self.data,
        }

    @classmethod
    def fromdict(cls, d):
        return cls(
            name=d["name"] if "name" in d else "",
            start=d["start"] if "start" in d else 0,
            duration=d["duration"] if "duration" in d else 0,
        )


class RecordEvents:
    events: dict = {}
    recordId: str = ""

    def __init__(self, recordId) -> None:
        self.recordId = recordId

    def addEvent(self, channel: str, event: Event):
        if channel not in self.events:
            self.events[channel] = []
        self.events[channel].append(event)

    def toPandas(self):
        from pandas.core.frame import DataFrame

        pandasList = []

        for c in self.events:
            for e in self.events[c]:
                pandasList.append({**{"channel": c}, **e.__dict__})

        return DataFrame(pandasList)
