from transformers import pipeline


MODEL_NAME = "chriamue/bird-species-classifier"


print("Завантаження моделі птахів...")

classifier = pipeline(
    "image-classification",
    model=MODEL_NAME
)

print("Модель завантажена!")


def analyze_bird(image_path):
    results = classifier(image_path, top_k=3)

    return results