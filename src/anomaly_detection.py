from sklearn.ensemble import IsolationForest
import pandas as pd

# Train anomaly detector
def detect_anomaly(
    signal_quality,
    throughput,
    latency,
    prediction
):

    # Sample data
    data = pd.DataFrame({
        'SignalQuality': [signal_quality],
        'Throughput': [throughput],
        'Latency': [latency],
        'Prediction': [prediction]
    })

    # Isolation Forest model
    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    # Train model
    model.fit(data)

    # Predict anomaly
    result = model.predict(data)

    # -1 means anomaly
    if result[0] == -1:
        return True

    return False