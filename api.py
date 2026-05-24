from fastapi import FastAPI
from src.predict import predict_signal

app = FastAPI()

@app.get("/")
def home():

    return {
        "message": "RF Prediction API Running"
    }

@app.get("/predict")
def predict(
    signal_quality: float,
    throughput: float,
    latency: float,
    network_value: int,
    bb60c: float,
    srsran: float,
    bladerf: float
):

    prediction = predict_signal(
        signal_quality,
        throughput,
        latency,
        network_value,
        bb60c,
        srsran,
        bladerf
    )

    return {
        "Predicted Signal Strength": prediction
    }