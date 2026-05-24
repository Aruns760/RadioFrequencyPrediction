import folium
from folium.plugins import HeatMap

def create_heatmap(df):

    # Center map
    center_lat = df['Latitude'].mean()
    center_lon = df['Longitude'].mean()

    # Create map
    rf_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12
    )

    # Heatmap data
    heat_data = [
        [
            row['Latitude'],
            row['Longitude'],
            abs(row['Signal Strength (dBm)'])
        ]
        for index, row in df.iterrows()
    ]

    # Add heatmap layer
    HeatMap(heat_data).add_to(rf_map)

    return rf_map