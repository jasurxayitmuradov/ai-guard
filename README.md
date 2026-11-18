# AI Guard

AI Guard is an image classification API that detects potentially Not Safe For Work (NSFW) content using a pretrained deep learning model.

The project uses Hugging Face Transformers and FastAPI to analyze uploaded images and classify them as either `NSFW` or `Normal`.

## Features

- AI-powered NSFW image detection.
- Image classification using a pretrained Hugging Face model.
- Configurable classification threshold.
- REST API built with FastAPI.
- Image validation and file size restrictions.
- Structured JSON responses and error handling.
- Docker support for containerized deployment.

## Technologies Used

- Python
- FastAPI
- Hugging Face Transformers
- PyTorch
- Pillow
- Docker
- Pytest

## Model

AI Guard uses the pretrained model:

`Falconsai/nsfw_image_detection`

The model analyzes an image and returns classification scores. AI Guard extracts the NSFW score and compares it with a configurable threshold.

The default threshold is `0.7`.

- If the NSFW score is greater than or equal to `0.7`, the image is classified as `NSFW`.
- Otherwise, it is classified as `Normal`.

## Project Structure

```text
ai-engine/
├── api/
│   ├── main.py
│   └── validators.py
├── engine/
│   ├── core.py
│   ├── models.py
│   └── result.py
├── tests/
│   ├── test_core.py
│   └── test_models.py
├── Dockerfile
├── requirements.txt
├── main.py
└── README.md
```

## How It Works

1. A user uploads an image through the `/analyze` API endpoint.
2. The API validates the uploaded file.
3. The image is loaded and converted to RGB format.
4. The pretrained model generates classification scores.
5. The AIEngine extracts the NSFW score and applies the configured threshold.
6. The API returns the classification result as JSON.

## Image Validation

Uploaded images must meet the following requirements:

- Maximum file size: 5 MB.
- Allowed formats: JPEG, PNG, and WebP.
- Maximum width: 4096 pixels.
- Maximum height: 4096 pixels.

## API Endpoints

### GET /

Checks whether the API is running.

### POST /analyze

Analyzes an uploaded image.

The endpoint accepts an image using multipart/form-data with the field name `file`.

Example successful response:

```json
{
  "success": true,
  "data": {
    "filename": "example.jpg",
    "label": "Normal",
    "score": 0.12,
    "model": "Falconsai/nsfw_image_detection",
    "threshold": 0.7
  }
}
```

The score and label depend on the uploaded image.

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd ai-engine
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn api.main:app --reload
```

Open the interactive API documentation:

`http://127.0.0.1:8000/docs`

## Running with Docker

Build the Docker image:

```bash
docker build -t ai-guard .
```

Run the container:

```bash
docker run -d --name ai-guard -p 8000:8080 ai-guard
```

Open:

`http://localhost:8000/docs`

## Running Tests

Run the test suite:

```bash
pytest -v
```

## Design Decisions

The classification logic is separated from the model implementation. This makes the AIEngine independent of a specific model and allows different image classification models to be integrated in the future.

Image validation is handled separately from the classification engine to keep API responsibilities organized and to reject unsupported or invalid uploads before inference.

## Limitations

AI Guard is an image classification tool and may produce incorrect predictions. Its results should not be treated as definitive judgments about image content.