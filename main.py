from engine.core import AIEngine
from engine.models import NSFWModel
from pathlib import Path
model = NSFWModel("Falconsai/nsfw_image_detection")

engine = AIEngine(model)

images_dir = Path("rasmlar")

for image_path in images_dir.iterdir():
    if image_path.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
        result = model.predict(str(image_path))

        print(image_path.name, result)
