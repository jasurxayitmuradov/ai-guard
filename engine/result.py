from dataclasses import dataclass


@dataclass
class DetectionResult:
    label: str
    score: float
    model_name: str
    threshold: float
    image_name: str
