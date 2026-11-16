
import pytest
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


@pytest.fixture
def setup_test(monkeypatch, tmp_path):
    # Зберігаємо тестові фото в тимчасову папку
    monkeypatch.setattr(
        main,
        "UPLOAD_FOLDER",
        str(tmp_path)
    )

    return tmp_path


# 1запуску сервера
def test_server_working():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "AI Bird Server працює"


# 2 Аналіз без фото
def test_analyze_without_file():
    response = client.post("/analyze")

    assert response.status_code == 422


# 3 HTTP-метод
def test_wrong_http_method():
    response = client.get("/analyze")

    assert response.status_code == 405


# 4 аналіз фотографії
def test_successful_analysis(monkeypatch, setup_test):

    def fake_analyze(file_path):
        return [
            {"label": "Sparrow", "score": 0.95}
        ]

    monkeypatch.setattr(
        main,
        "analyze_bird",
        fake_analyze
    )

    response = client.post(
        "/analyze",
        files={
            "file": (
                "bird.jpg",
                b"fake image data",
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 200
    assert response.json()["image_name"] == "bird.jpg"


# 5Перев результату AI
def test_prediction_values(monkeypatch, setup_test):

    def fake_analyze(file_path):
        return [
            {"label": "Eagle", "score": 0.88}
        ]

    monkeypatch.setattr(
        main,
        "analyze_bird",
        fake_analyze
    )

    response = client.post(
        "/analyze",
        files={
            "file": (
                "eagle.jpg",
                b"fake image data",
                "image/jpeg"
            )
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["predictions"][0]["species"] == "Eagle"
    assert data["predictions"][0]["confidence"] == 0.88


# 6 Перев кількох прогнозів
def test_multiple_predictions(monkeypatch, setup_test):

    def fake_analyze(file_path):
        return [
            {"label": "Eagle", "score": 0.80},
            {"label": "Hawk", "score": 0.15},
            {"label": "Falcon", "score": 0.05}
        ]

    monkeypatch.setattr(
        main,
        "analyze_bird",
        fake_analyze
    )

    response = client.post(
        "/analyze",
        files={
            "file": (
                "bird.jpg",
                b"fake image data",
                "image/jpeg"
            )
        }
    )

    predictions = response.json()["predictions"]

    assert response.status_code == 200
    assert len(predictions) == 3
    assert predictions[0]["species"] == "Eagle"
    assert predictions[1]["species"] == "Hawk"
    assert predictions[2]["species"] == "Falcon"


# 7 Порожній результат аналізу
def test_empty_predictions(monkeypatch, setup_test):

    def fake_analyze(file_path):
        return []

    monkeypatch.setattr(
        main,
        "analyze_bird",
        fake_analyze
    )

    response = client.post(
        "/analyze",
        files={
            "file": (
                "empty.jpg",
                b"fake image data",
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 200
    assert response.json()["predictions"] == []


# 8 Помилка AI-моделі
def test_ai_model_error(monkeypatch, setup_test):

    def fake_analyze(file_path):
        raise Exception("Model error")

    monkeypatch.setattr(
        main,
        "analyze_bird",
        fake_analyze
    )

    response = client.post(
        "/analyze",
        files={
            "file": (
                "bird.jpg",
                b"fake image data",
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "Model error"
