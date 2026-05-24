import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
from src.auth import register_user, login_user
from src.predict import predict_signal
from src.failure_detection import detect_signal_issues
from src.visualization import create_chart
from src.live_chart import create_live_chart
from src.heatmap import create_heatmap
from src.database import save_prediction, get_history
from src.anomaly_detection import detect_anomaly
# Auto refresh every 5 seconds
st_autorefresh(
    interval=5000,
    key="rf_dashboard_refresh"
)
# Load dataset
df = pd.read_csv(
    "dataset/signal_metrics.csv"
)

# Page config
st.set_page_config(
    page_title="RF Prediction System",
    layout="wide"
)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# Authentication menu
menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Register"]
)

# Login/Register section
if not st.session_state.logged_in:

    st.title("🔐 RF Prediction Login System")

    username = st.sidebar.text_input(
        "Username"
    )

    password = st.sidebar.text_input(
        "Password",
        type="password"
    )

    # Register
    if menu == "Register":

        if st.sidebar.button("Register"):

            success = register_user(
                username,
                password
            )

            if success:

                st.sidebar.success(
                    "User Registered Successfully ✅"
                )

            else:

                st.sidebar.error(
                    "Username Already Exists ❌"
                )

    # Login
    if menu == "Login":

        if st.sidebar.button("Login"):

            success = login_user(
                username,
                password
            )

            if success:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.sidebar.success(
                    "Login Successful ✅"
                )

                st.rerun()

            else:

                st.sidebar.error(
                    "Invalid Username or Password ❌"
                )

    st.warning(
        "Please Login to Access RF Dashboard"
    )

    st.stop()

# Logout button
if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()

# Dashboard title
st.title("📡 Radio Frequency Prediction System")

st.success(
    f"Welcome {st.session_state.username} 👋"
)

st.metric(
    label="Model Accuracy",
    value="92%"
)

st.markdown(
    "AI-Based RF Signal Strength Prediction Dashboard"
)

# Sidebar inputs
st.sidebar.header("RF Input Parameters")

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

# Network mapping
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

# Prediction button
if st.button("Predict Signal Strength"):

    # Predict
    prediction = predict_signal(
        signal_quality,
        throughput,
        latency,
        network_value,
        bb60c,
        srsran,
        bladerf
    )

    # Prediction result
    st.success(
        f"Predicted Signal Strength: {prediction:.2f} dBm"
    )

    # AI anomaly detection
    is_anomaly = detect_anomaly(
        signal_quality,
        throughput,
        latency,
        prediction
    )

    if is_anomaly:

        st.error(
            "⚠️ RF Anomaly Detected!"
        )

    else:

        st.success(
            "No RF Anomaly Detected ✅"
        )

    # AI signal issue detection
    issues = detect_signal_issues(
        prediction,
        throughput,
        latency,
        bb60c,
        srsran
    )

    if len(issues) == 0:

        st.success(
            "Network Stable ✅"
        )

    else:

        for issue in issues:
            st.warning(issue)

    # Health score

    st.subheader(
        "📊 Network Health Status"
    )

    health_score = 100

    if prediction < -90:
        health_score -= 30

    if latency > 200:
        health_score -= 30

    if throughput < 5:
        health_score -= 20

    if abs(bb60c - srsran) > 15:
        health_score -= 20

    if health_score < 0:
        health_score = 0

    st.progress(
        health_score / 100
    )

    st.write(
        f"Network Health Score: {health_score}%"
    )

    # Save to MongoDB
    save_prediction({
        "Username": st.session_state.username,
        "Signal Quality": signal_quality,
        "Throughput": throughput,
        "Latency": latency,
        "Prediction": prediction
    })

# Load history
history_data = pd.DataFrame(
    get_history(
        st.session_state.username
    )
)

# Charts
st.subheader(
    "📊 RF Parameter Analysis"
)

fig = create_chart(
    signal_quality,
    throughput,
    latency
)

st.pyplot(fig)

# History
st.subheader(
    "Prediction History"
)

if not history_data.empty:

    st.dataframe(
        history_data.tail(10)
    )

    # Live chart
    st.subheader(
        "📈 Live RF Monitoring"
    )

    live_fig = create_live_chart(
        history_data
    )

    st.pyplot(live_fig)

    # Download report
    csv = history_data.to_csv(index=False)

    st.download_button(
        label="Download Prediction Report",
        data=csv,
        file_name="rf_prediction_report.csv",
        mime="text/csv"
    )
# Live user GPS location
st.subheader("📍 Live User GPS Location")

location = streamlit_geolocation()

if location["latitude"] is not None:

    st.success("Live Location Detected ✅")

    st.write(
        f"Latitude: {location['latitude']}"
    )

    st.write(
        f"Longitude: {location['longitude']}"
    )

    # Create live location map
    import folium

    live_map = folium.Map(
        location=[
            location["latitude"],
            location["longitude"]
        ],
        zoom_start=15
    )

    # Marker
    folium.Marker(
        [
            location["latitude"],
            location["longitude"]
        ],
        popup="Current User Location"
    ).add_to(live_map)

    st_folium(
        live_map,
        width=1200,
        height=400
    )

else:

    st.warning(
        "Please Allow Location Access 🌍"
    )
# Heatmap
st.subheader(
    "🌍 RF Signal Heatmap"
)

rf_map = create_heatmap(df)

st_folium(
    rf_map,
    width=1200,
    height=500
)