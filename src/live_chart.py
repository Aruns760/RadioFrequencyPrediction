import pandas as pd
import matplotlib.pyplot as plt

def create_live_chart(history_data):

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        history_data['Prediction'],
        marker='o'
    )

    ax.set_title(
        "Live RF Signal Strength Monitoring"
    )

    ax.set_xlabel("Predictions")

    ax.set_ylabel("Signal Strength (dBm)")

    return fig