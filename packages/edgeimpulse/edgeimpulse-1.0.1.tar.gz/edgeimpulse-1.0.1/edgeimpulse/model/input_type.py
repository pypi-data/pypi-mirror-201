class AudioInput(dict):
    def __init__(self, frequency_hz: float):
        self["inputType"] = "audio"
        self["frequencyHz"] = frequency_hz


class TimeSeriesInput(dict):
    def __init__(self, frequency_hz: float, windowlength_ms: int):
        self["inputType"] = "time-series"
        self["frequencyHz"] = frequency_hz
        self["windowLengthMs"] = windowlength_ms


class OtherInput(dict):
    def __init__(self):
        self["inputType"] = "other"
