from dataclasses import dataclass


@dataclass
class PredictionResult:
    label: str
    confidence: float
    model_version: str
    inference_time: float
    feedback: dict
    expected: str
    correct: bool
    accuracy: float