from typing import Optional, List


class Classification(dict):
    def __init__(self, labels: Optional[List[str]] = None):
        self["modelType"] = "classification"
        self["labels"] = labels


class Regression(dict):
    def __init__(self):
        self["modelType"] = "regression"


class ObjectDetection(dict):
    def __init__(
        self, labels: List[str], last_layer: str, minimum_confidence: float, **kwargs
    ):
        self["modelType"] = "object-detection"
        self["labels"] = labels
        self["lastLayer"] = last_layer
        self["minimumConfidence"] = minimum_confidence
