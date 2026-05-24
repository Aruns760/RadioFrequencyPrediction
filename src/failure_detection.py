def detect_signal_issues(
    prediction,
    throughput,
    latency,
    bb60c,
    srsran
):

    issues = []

    # Weak Signal
    if prediction < -90:
        issues.append("Weak Signal Detected 🚨")

    # Tower Failure
    if throughput < 1 and latency > 200:
        issues.append("Possible Tower Failure 🛰️")

    # RF Interference
    if abs(bb60c - srsran) > 15:
        issues.append("High RF Interference 📡")

    # Connection Drop
    if latency > 250:
        issues.append("Connection Drop Risk 🔴")

    return issues