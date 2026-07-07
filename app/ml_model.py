import requests

API_URL = "https://reversion-mocha-angular.ngrok-free.dev/predict"

def predict_image(image):
    files = {"image": image}
    response = requests.post(API_URL, files=files)

    result = response.json()["result"]
    return result