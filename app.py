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

# ─── Page Config (must be first) ────────────────────────────────────────────
st.set_page_config(
    page_title="RF·PRED | Signal Intelligence",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root theme ── */
:root {
    --rf-bg:        #080d14;
    --rf-surface:   #0d1520;
    --rf-card:      #111d2b;
    --rf-border:    #1e3048;
    --rf-accent:    #00d4ff;
    --rf-accent2:   #7b61ff;
    --rf-success:   #00e5a0;
    --rf-warn:      #ffb347;
    --rf-danger:    #ff4d6d;
    --rf-text:      #c9dff0;
    --rf-muted:     #4d7a9e;
    --rf-mono:      'Space Mono', monospace;
    --rf-sans:      'DM Sans', sans-serif;
}

/* ── Global overrides ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--rf-bg) !important;
    color: var(--rf-text) !important;
    font-family: var(--rf-sans) !important;
}

[data-testid="stSidebar"] {
    background: var(--rf-surface) !important;
    border-right: 1px solid var(--rf-border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--rf-text) !important;
    font-family: var(--rf-sans) !important;
}

/* ── Sidebar header ── */
[data-testid="stSidebar"]::before {
    content: "📡  RF·PRED";
    display: block;
    font-family: var(--rf-mono) !important;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: var(--rf-accent) !important;
    padding: 1.4rem 1.2rem 0.6rem;
    border-bottom: 1px solid var(--rf-border);
    margin-bottom: 0.5rem;
}

/* ── Sliders ── */
[data-testid="stSlider"] > div > div > div > div {
    background: var(--rf-accent) !important;
}

/* ── Selectbox / Input ── */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: var(--rf-card) !important;
    border-color: var(--rf-border) !important;
    color: var(--rf-text) !important;
    font-family: var(--rf-mono) !important;
    border-radius: 6px !important;
}

/* ── Primary button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #00d4ff22, #7b61ff22) !important;
    border: 1px solid var(--rf-accent) !important;
    color: var(--rf-accent) !important;
    font-family: var(--rf-mono) !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.08em !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #00d4ff44, #7b61ff44) !important;
    box-shadow: 0 0 18px #00d4ff44 !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--rf-card) !important;
    border: 1px solid var(--rf-border) !important;
    border-radius: 10px !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--rf-mono) !important;
    color: var(--rf-accent) !important;
    font-size: 2rem !important;
}
[data-testid="stMetricLabel"] {
    color: var(--rf-muted) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ── Success / Warning / Error alerts ── */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    font-family: var(--rf-sans) !important;
}
div[data-baseweb="notification"][kind="positive"] {
    background: #00e5a011 !important;
    border-left: 3px solid var(--rf-success) !important;
    color: var(--rf-success) !important;
}
div[data-baseweb="notification"][kind="warning"] {
    background: #ffb34711 !important;
    border-left: 3px solid var(--rf-warn) !important;
    color: var(--rf-warn) !important;
}
div[data-baseweb="notification"][kind="error"] {
    background: #ff4d6d11 !important;
    border-left: 3px solid var(--rf-danger) !important;
    color: var(--rf-danger) !important;
}

/* ── Progress bar ── */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--rf-accent), var(--rf-accent2)) !important;
    border-radius: 99px !important;
}
[data-testid="stProgress"] > div {
    background: var(--rf-border) !important;
    border-radius: 99px !important;
    height: 8px !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--rf-border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: var(--rf-card) !important;
    border: 1px solid var(--rf-border) !important;
    color: var(--rf-muted) !important;
    font-family: var(--rf-mono) !important;
    font-size: 0.8rem !important;
    border-radius: 8px !important;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: var(--rf-accent2) !important;
    color: var(--rf-accent2) !important;
}

/* ── Subheader text ── */
h2, h3 {
    font-family: var(--rf-mono) !important;
    letter-spacing: 0.05em !important;
    color: var(--rf-text) !important;
}

/* ── Section divider ── */
hr {
    border-color: var(--rf-border) !important;
    margin: 2rem 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--rf-surface); }
::-webkit-scrollbar-thumb { background: var(--rf-border); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ─── Auto refresh ────────────────────────────────────────────────────────────
st_autorefresh(interval=5000, key="rf_dashboard_refresh")

# ─── Load dataset ────────────────────────────────────────────────────────────
df = pd.read_csv("dataset/signal_metrics.csv")

# ─── Session state ───────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ════════════════════════════════════════════════════════════════════════════
# AUTH SCREEN
# ════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:

    # Centered login hero
    st.markdown("""
    <div style="text-align:center; padding: 3rem 0 1.5rem;">
        <div style="font-family:'Space Mono',monospace; font-size:2.6rem; font-weight:700;
                    letter-spacing:0.12em; color:#00d4ff; margin-bottom:0.4rem;">
            RF·PRED
        </div>
        <div style="font-family:'DM Sans',sans-serif; font-size:1rem;
                    color:#4d7a9e; letter-spacing:0.2em; text-transform:uppercase;">
            Signal Intelligence Platform
        </div>
        <div style="margin: 1.5rem auto; width:60px; height:2px;
                    background:linear-gradient(90deg,#00d4ff,#7b61ff);
                    border-radius:99px;"></div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown("""
        <div style="background:#0d1520; border:1px solid #1e3048; border-radius:14px;
                    padding:2rem 2rem 1.5rem;">
        """, unsafe_allow_html=True)

        tab_login, tab_reg = st.tabs(["  Sign In  ", "  Register  "])

        with tab_login:
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
            username = st.text_input("Username", key="login_user", placeholder="your_username")
            password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
            if st.button("→ Authenticate", use_container_width=True, key="btn_login"):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try again.")

        with tab_reg:
            st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
            reg_user = st.text_input("Choose Username", key="reg_user", placeholder="new_username")
            reg_pass = st.text_input("Choose Password", type="password", key="reg_pass", placeholder="••••••••")
            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
            if st.button("→ Create Account", use_container_width=True, key="btn_reg"):
                if register_user(reg_user, reg_pass):
                    st.success("Account created. Sign in now.")
                else:
                    st.error("Username already taken.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# MAIN DASHBOARD
# ════════════════════════════════════════════════════════════════════════════

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace; font-size:0.75rem;
                color:#4d7a9e; padding:0.6rem 0 1.2rem; letter-spacing:0.08em;">
        OPERATOR  ·  <span style="color:#00d4ff">{st.session_state.username.upper()}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.7rem;
                color:#4d7a9e; letter-spacing:0.15em; padding-bottom:0.8rem;">
        INPUT PARAMETERS
    </div>
    """, unsafe_allow_html=True)

    signal_quality = st.slider("Signal Quality (%)", 0, 100, 50)
    throughput     = st.slider("Throughput (Mbps)", 0, 100, 20)
    latency        = st.slider("Latency (ms)", 0, 300, 50)
    network_type   = st.selectbox("Network Type", ["3G", "4G", "5G", "LTE"])

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.7rem;
                color:#4d7a9e; letter-spacing:0.15em; padding-bottom:0.8rem;">
        SDR MEASUREMENTS
    </div>
    """, unsafe_allow_html=True)

    bb60c   = st.number_input("BB60C (dBm)",       value=-90.0, step=0.5)
    srsran  = st.number_input("srsRAN (dBm)",      value=-95.0, step=0.5)
    bladerf = st.number_input("BladeRFxA9 (dBm)",  value=-92.0, step=0.5)

    st.markdown("---")
    if st.button("⏻  Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# ─── Network map ─────────────────────────────────────────────────────────────
network_map   = {"3G": 0, "4G": 1, "5G": 2, "LTE": 3}
network_value = network_map[network_type]

# ─── Page header ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex; align-items:center; gap:1rem; padding-bottom:1.2rem;
            border-bottom:1px solid #1e3048; margin-bottom:1.8rem;">
    <div style="font-family:'Space Mono',monospace; font-size:1.6rem;
                font-weight:700; letter-spacing:0.1em; color:#00d4ff;">
        RF·PRED
    </div>
    <div style="font-family:'DM Sans',sans-serif; font-size:0.85rem;
                color:#4d7a9e; letter-spacing:0.12em; text-transform:uppercase;
                margin-top:4px;">
        / Signal Intelligence Dashboard
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Top KPI row ─────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Model Accuracy",   "92%")
k2.metric("Network Type",     network_type)
k3.metric("Signal Quality",   f"{signal_quality}%")
k4.metric("Latency",          f"{latency} ms")

st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)

# ─── Predict button ───────────────────────────────────────────────────────────
col_btn, _ = st.columns([1, 3])
with col_btn:
    run_predict = st.button("⬡  RUN PREDICTION", use_container_width=True)

if run_predict:
    prediction = predict_signal(
        signal_quality, throughput, latency,
        network_value, bb60c, srsran, bladerf
    )

    # ── Result banner ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#00d4ff11,#7b61ff11);
                border:1px solid #00d4ff44; border-radius:12px;
                padding:1.2rem 1.6rem; margin:1.2rem 0;">
        <div style="font-family:'Space Mono',monospace; font-size:0.7rem;
                    color:#4d7a9e; letter-spacing:0.15em; margin-bottom:0.3rem;">
            PREDICTED SIGNAL STRENGTH
        </div>
        <div style="font-family:'Space Mono',monospace; font-size:2.2rem;
                    font-weight:700; color:#00d4ff;">
            {prediction:.2f} <span style="font-size:1rem;color:#4d7a9e;">dBm</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Anomaly + Issues in two columns ──
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div style="font-family:'Space Mono',monospace; font-size:0.7rem;
                    color:#4d7a9e; letter-spacing:0.12em; margin-bottom:0.6rem;">
            ANOMALY DETECTION
        </div>""", unsafe_allow_html=True)

        is_anomaly = detect_anomaly(signal_quality, throughput, latency, prediction)
        if is_anomaly:
            st.error("⚠  RF Anomaly Detected")
        else:
            st.success("✓  No Anomaly Detected")

    with c2:
        st.markdown("""
        <div style="font-family:'Space Mono',monospace; font-size:0.7rem;
                    color:#4d7a9e; letter-spacing:0.12em; margin-bottom:0.6rem;">
            SIGNAL ISSUES
        </div>""", unsafe_allow_html=True)

        issues = detect_signal_issues(prediction, throughput, latency, bb60c, srsran)
        if not issues:
            st.success("✓  Network Stable")
        else:
            for issue in issues:
                st.warning(issue)

    # ── Health score ──
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.7rem;
                color:#4d7a9e; letter-spacing:0.12em; margin-bottom:0.6rem;">
        NETWORK HEALTH SCORE
    </div>""", unsafe_allow_html=True)

    health_score = 100
    if prediction < -90:      health_score -= 30
    if latency > 200:         health_score -= 30
    if throughput < 5:        health_score -= 20
    if abs(bb60c - srsran) > 15: health_score -= 20
    health_score = max(health_score, 0)

    # colour the score
    if health_score >= 70:
        score_color = "#00e5a0"
    elif health_score >= 40:
        score_color = "#ffb347"
    else:
        score_color = "#ff4d6d"

    h_col1, h_col2 = st.columns([4, 1])
    with h_col1:
        st.progress(health_score / 100)
    with h_col2:
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace; font-size:1.1rem;
                    font-weight:700; color:{score_color}; text-align:right;
                    margin-top:2px;">
            {health_score}%
        </div>""", unsafe_allow_html=True)

    # ── Save ──
    save_prediction({
        "Username":       st.session_state.username,
        "Signal Quality": signal_quality,
        "Throughput":     throughput,
        "Latency":        latency,
        "Prediction":     prediction,
    })

# ─── Divider ─────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)

# ─── RF Parameter chart ──────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'Space Mono',monospace; font-size:0.75rem;
            color:#4d7a9e; letter-spacing:0.15em; margin-bottom:1rem;">
    RF PARAMETER ANALYSIS
</div>""", unsafe_allow_html=True)

fig = create_chart(signal_quality, throughput, latency)
st.pyplot(fig)

# ─── History + Live chart ────────────────────────────────────────────────────
history_data = pd.DataFrame(get_history(st.session_state.username))

if not history_data.empty:
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.75rem;
                color:#4d7a9e; letter-spacing:0.15em; margin-bottom:1rem;">
        PREDICTION HISTORY
    </div>""", unsafe_allow_html=True)

    st.dataframe(history_data.tail(10), use_container_width=True)

    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.75rem;
                color:#4d7a9e; letter-spacing:0.15em; margin:1.4rem 0 0.8rem;">
        LIVE RF MONITORING
    </div>""", unsafe_allow_html=True)

    live_fig = create_live_chart(history_data)
    st.pyplot(live_fig)

    csv = history_data.to_csv(index=False)
    st.download_button(
        label="↓  Export Prediction Report (.csv)",
        data=csv,
        file_name="rf_prediction_report.csv",
        mime="text/csv",
    )

# ─── GPS location ────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'Space Mono',monospace; font-size:0.75rem;
            color:#4d7a9e; letter-spacing:0.15em; margin-bottom:1rem;">
    LIVE GPS LOCATION
</div>""", unsafe_allow_html=True)

location = streamlit_geolocation()

if location["latitude"] is not None:
    g1, g2 = st.columns(2)
    g1.metric("Latitude",  f"{location['latitude']:.6f}°")
    g2.metric("Longitude", f"{location['longitude']:.6f}°")

    import folium

    # ── Satellite tile with morning warm overlay ──
    live_map = folium.Map(
        location=[location["latitude"], location["longitude"]],
        zoom_start=16,
        tiles=None,
    )

    # Esri World Imagery (satellite)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite",
        max_zoom=19,
    ).add_to(live_map)

    # Warm morning colour wash on top
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Labels",
        name="Labels",
        opacity=0.55,
    ).add_to(live_map)

    # Golden sunrise marker with pulsing ring via DivIcon
    pulse_html = """
    <div style="position:relative; width:40px; height:40px;">
      <div style="position:absolute; top:0; left:0; width:40px; height:40px;
                  border-radius:50%; background:rgba(255,180,60,0.25);
                  animation:pulse 1.8s ease-out infinite;"></div>
      <div style="position:absolute; top:10px; left:10px; width:20px; height:20px;
                  border-radius:50%; background:#ffb347;
                  border:2px solid #fff3cd; box-shadow:0 0 10px #ffb34799;"></div>
    </div>
    <style>
      @keyframes pulse {
        0%   { transform:scale(0.6); opacity:0.8; }
        100% { transform:scale(2.2); opacity:0; }
      }
    </style>
    """
    folium.Marker(
        [location["latitude"], location["longitude"]],
        icon=folium.DivIcon(html=pulse_html, icon_size=(40, 40), icon_anchor=(20, 20)),
        popup=folium.Popup(
            "<b style='font-family:monospace;color:#7a4f00;'>📍 Live Position</b><br>"
            f"<span style='font-size:11px;color:#555;'>"
            f"{location['latitude']:.5f}°, {location['longitude']:.5f}°</span>",
            max_width=200,
        ),
    ).add_to(live_map)

    st_folium(live_map, width=None, height=400)
else:
    st.info("📍  Allow location access to enable GPS tracking.")

# ─── Heatmap ─────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'Space Mono',monospace; font-size:0.75rem;
            color:#4d7a9e; letter-spacing:0.15em; margin-bottom:1rem;">
    RF SIGNAL HEATMAP
</div>""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'Space Mono',monospace; font-size:0.75rem;
            color:#4d7a9e; letter-spacing:0.15em; margin-bottom:1rem;">
    RF SIGNAL HEATMAP
</div>""", unsafe_allow_html=True)

# Patch create_heatmap to use satellite base then overlay heatmap
import folium
from folium.plugins import HeatMap

# Build satellite base map centred on dataset average if possible
try:
    lat_center = df["latitude"].mean()  if "latitude"  in df.columns else 13.08
    lon_center = df["longitude"].mean() if "longitude" in df.columns else 80.27
except Exception:
    lat_center, lon_center = 13.08, 80.27

rf_map = folium.Map(
    location=[lat_center, lon_center],
    zoom_start=12,
    tiles=None,
)

# Satellite layer
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri World Imagery",
    name="Satellite",
    max_zoom=19,
).add_to(rf_map)

# Label overlay (morning warm opacity)
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
    attr="Esri Labels",
    name="Labels",
    opacity=0.5,
).add_to(rf_map)

# Heatmap — warm sunrise gradient (yellow → orange → red)
try:
    heat_data = df[["latitude", "longitude", "signal_strength"]].dropna().values.tolist()
    HeatMap(
        heat_data,
        min_opacity=0.35,
        max_zoom=16,
        radius=22,
        blur=18,
        gradient={0.2: "#ffe066", 0.5: "#ffb347", 0.75: "#ff6b35", 1.0: "#ff1744"},
    ).add_to(rf_map)
except Exception:
    # Fallback to original helper if columns differ
    rf_map = create_heatmap(df)

st_folium(rf_map, width=None, height=500)