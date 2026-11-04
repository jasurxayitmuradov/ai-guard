from engine.result import DetectionResult

class AIEngine:
    def __init__(self, model, threshold=0.7):
        self.model_name = model.__class__.__name__
        self.model = model
        
        if not 0 <= threshold <= 1:
            raise ValueError("Threshold must be between 0 and 1")
        self.threshold = threshold

    def classify(self, nsfw_score):
        if nsfw_score >= self.threshold:
            return "NSFW"
        return "Normal"

    def analyze(self, image):

        scores = self.model.predict(image)
          

        if not isinstance(scores, dict):
            raise TypeError("Model must return a dictionary")
        
        if "nsfw" not in scores:
            raise ValueError("NSFW score is missing")
        
        nsfw_score = scores["nsfw"]
        if not isinstance(nsfw_score, (int, float)):
            raise TypeError("Score must be a number")
        if not 0 <= nsfw_score <= 1:
            raise ValueError("Score must be between 0 and 1")
        
        result = self.classify(nsfw_score)

        return DetectionResult(
            label=result,
            score=nsfw_score,
            model_name=self.model_name,
            threshold=self.threshold,
            image_name=image
        )
