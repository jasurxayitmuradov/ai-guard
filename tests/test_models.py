import pytest
from unittest.mock import patch

from engine.models import BaseModel, NSFWModel


def test_base_model():
    model = BaseModel()

    with pytest.raises(NotImplementedError):
        model.predict("test.jpg")


def test_load_model():
    fake_classifier = "Fake classifier"

    with patch(
        "engine.models.pipeline",
        return_value=fake_classifier
    ) as mock_pipeline:
        model = NSFWModel("test-model")

    mock_pipeline.assert_called_once_with(
        "image-classification",
        model="test-model"
    )

    assert model.classifier == fake_classifier


def test_load_model_error():
    with patch(
        "engine.models.pipeline",
        side_effect=RuntimeError("Model loading failed")
    ):
        with pytest.raises(RuntimeError, match="Model loading failed"):
            NSFWModel("test-model")


def test_predict():
    fake_results = [
        {"label": "NSFW", "score": 0.8},
        {"label": "Normal", "score": 0.2}
    ]

    model = NSFWModel.__new__(NSFWModel)
    model.classifier = lambda image: fake_results

    result = model.predict("test.jpg")

    assert result == {
        "nsfw": 0.8,
        "normal": 0.2
    }