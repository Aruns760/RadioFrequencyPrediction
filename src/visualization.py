import pandas as pd
import matplotlib.pyplot as plt

def create_chart(
    signal_quality,
    throughput,
    latency
):

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

    return fig