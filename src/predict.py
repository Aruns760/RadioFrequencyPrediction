import joblib
import numpy as np

# Load model
model = joblib.load('models/rf_model.pkl')

def predict_signal(
    signal_quality,
    throughput,
    latency,
    network_value,
    bb60c,
    srsran,
    bladerf
):

    features = np.array([[
        signal_quality,
        throughput,
        latency,
        network_value,
        bb60c,
        srsran,
        bladerf
    ]])

    prediction = model.predict(features)

    return prediction[0]