from engine.core import AIEngine
import pytest

class MockModel():
    def __init__(self, nsfw_score):
        self.nsfw_score = nsfw_score

    def predict(self,image):
        return {
            "nsfw": self.nsfw_score,
            "normal": 1 - float(self.nsfw_score)
        }

def test_nsfw_detection():
    model = MockModel(0.8)
    engine = AIEngine(model, threshold=0.7)

    result = engine.analyze("test.jpg")

    assert result.label == "NSFW"


def test_normal_detection():
    model = MockModel(0.2)
    engine = AIEngine(model, threshold=0.7)

    result = engine.analyze("test.jpg")

    assert result.label == "Normal"

def test_threshold_boundary():
    model = MockModel(0.7)
    engine = AIEngine(model, threshold=0.7)

    result = engine.analyze("test.jpg")

    assert result.label == "NSFW"

def test_missing_nsfw_score():
    class BrokenModel():
        def predict(self, image):
            return {"normal": 1.0}

    engine = AIEngine(BrokenModel())

    try:
        engine.analyze("test.jpg")
    except ValueError as error:
        assert str(error) == "NSFW score is missing"
    else:
        assert False, "ValuError was not raised"

def test_invalid_nsfw_score_negative():
    model = MockModel(-0.1)
    engine = AIEngine(model)

    with pytest.raises(ValueError, match="Score must be between 0 and 1"):
        engine.analyze("test.jpg")

def test_invalid_nsfw_score_positive():
    model = MockModel(1.1)
    engine = AIEngine(model)

    with pytest.raises(ValueError, match="Score must be between 0 and 1"):
        engine.analyze("test.jpg")

def test_invalid_nsfw_score_str():
    model = MockModel("0.7")
    engine = AIEngine(model)

    with pytest.raises(TypeError, match="Score must be a number"):
        engine.analyze("test.jpg")

def test_invalid_threshold_negative():
    model = MockModel(0.7)

    with pytest.raises(ValueError, match="Threshold must be between 0 and 1"):
        AIEngine(model, -0.1)

def test_invalid_threshold_positive():
    model = MockModel(0.7)

    with pytest.raises(ValueError, match="Threshold must be between 0 and 1"):
        AIEngine(model, 1.1)

def test_invalid_scores():
    class BrokenModel():
        def predict(self, image):
            return None
    engine = AIEngine(BrokenModel())

    with pytest.raises(TypeError, match="Model must return a dictionary"):
        engine.analyze("test.jpg")
def test_invalid_nsfw_none():
    class BrokenModel():
        def predict(self, image):
            return {
                "nsfw": None,
                "normal": 1
            }
    engine = AIEngine(BrokenModel())

    with pytest.raises(TypeError, match="Score must be a number"):
        engine.analyze("test.jpg")

def test_error_model():
    class BrokenModel():
        def predict(self, image):
            raise RuntimeError("Model prediction failed")

    engine = AIEngine(BrokenModel())

    with pytest.raises(RuntimeError, match="Model prediction failed"):
        engine.analyze("test.jpg")
            