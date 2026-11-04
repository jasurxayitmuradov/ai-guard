from engine.core import AIEngine
from engine.models import NSFWModel
from pathlib import Path

model = NSFWModel("Falconsai/nsfw_image_detection")

engine = AIEngine(model, threshold=0.7)

images_dir = Path("rasmlar")

for image_path in images_dir.iterdir():
    if image_path.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
        result = engine.analyze(str(image_path))

        print(result.image_name, result.label, result.score, result.model_name, result.threshold)
        
