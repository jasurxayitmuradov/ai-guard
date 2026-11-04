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
        return self.classifier(image)