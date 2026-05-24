import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Page config
st.set_page_config(
    page_title="RF Prediction System",
    layout="wide"
)

# Load trained model
model = joblib.load('models/rf_model.pkl')

# Title
st.title("📡 Radio Frequency Prediction System")

st.metric(
    label="Model Accuracy",
    value="92%"
)

st.markdown(
    "AI-Based RF Signal Strength Prediction Dashboard"
)

# Sidebar
st.sidebar.header("RF Input Parameters")

# Inputs
signal_quality = st.sidebar.slider(
    "Signal Quality (%)",
    0,
    100,
    50
)

throughput = st.sidebar.slider(
    "Data Throughput (Mbps)",
    0,
    100,
    20
)

latency = st.sidebar.slider(
    "Latency (ms)",
    0,
    300,
    50
)

network_type = st.sidebar.selectbox(
    "Network Type",
    ["3G", "4G", "5G", "LTE"]
)

# Convert network type
network_map = {
    "3G": 0,
    "4G": 1,
    "5G": 2,
    "LTE": 3
}

network_value = network_map[network_type]

bb60c = st.sidebar.number_input(
    "BB60C Measurement (dBm)",
    value=-90.0
)

srsran = st.sidebar.number_input(
    "srsRAN Measurement (dBm)",
    value=-95.0
)

bladerf = st.sidebar.number_input(
    "BladeRFxA9 Measurement (dBm)",
    value=-92.0
)

# Predict button
if st.button("Predict Signal Strength"):

    # Prepare features
    features = np.array([[
        signal_quality,
        throughput,
        latency,
        network_value,
        bb60c,
        srsran,
        bladerf
    ]])

    # Prediction
    prediction = model.predict(features)

    # Show prediction
    st.success(
        f"Predicted Signal Strength: {prediction[0]:.2f} dBm"
    )

    # Signal category
    if prediction[0] > -70:
        st.info("Excellent Signal 📶")

    elif prediction[0] > -90:
        st.warning("Moderate Signal ⚠️")

    else:
        st.error("Weak Signal ❌")

    # Create history dataframe
    history = pd.DataFrame({
        'Signal Quality': [signal_quality],
        'Throughput': [throughput],
        'Latency': [latency],
        'Prediction': [prediction[0]]
    })

    # Save prediction history
    if os.path.exists("prediction_history.csv"):

        history.to_csv(
            "prediction_history.csv",
            mode='a',
            header=False,
            index=False
        )

    else:

        history.to_csv(
            "prediction_history.csv",
            index=False
        )

    # Visualization
    sample_data = pd.DataFrame({
        'Parameters': [
            'Signal Quality',
            'Throughput',
            'Latency'
        ],
        'Values': [
            signal_quality,
            throughput,
            latency
        ]
    })

    fig, ax = plt.subplots()

    ax.bar(
        sample_data['Parameters'],
        sample_data['Values']
    )

    ax.set_title("RF Parameter Analysis")

    st.pyplot(fig)

    # Show history
    st.subheader("Prediction History")

    history_data = pd.read_csv(
        "prediction_history.csv"
    )

    st.dataframe(history_data.tail(10))

    # Download report
    csv = history_data.to_csv(index=False)

    st.download_button(
        label="Download Prediction Report",
        data=csv,
        file_name='rf_prediction_report.csv',
        mime='text/csv'
    )