from transformers import pipeline

class BaseModel:
    def predict(self, image):
        raise NotImplementedError

class NSFWModel(BaseModel):
    def __init__(self, model_name):
        self.model_name = model_name
        self.load() 

    def load(self):
        self.classifier = pipeline(
            "image-classification",
            model=self.model_name
        )


    def predict(self, image):
        results = self.classifier(image)

        scores = {}

        for item in results:
            key = item["label"].lower()
            value = item["score"]
            scores[key] = value
        return scores
    