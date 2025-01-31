import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
sns.set(style='white')

monthlyTemp_df = pd.read_csv(r"C:\Users\User2\Desktop\Proyek Akhir Analisis\Dashboard\chang_monthly.csv")
highTemp = pd.read_csv(r"C:\Users\User2\Desktop\Proyek Akhir Analisis\Dashboard\highest_temp_df.csv")
lowTemp = pd.read_csv(r"C:\Users\User2\Desktop\Proyek Akhir Analisis\Dashboard\lowest_temp_df.csv")

st.title("Temperature in Changping City")

with st.sidebar:
    # Add company logo
    st.markdown("<h3 style='text-align: center; font-size: 20px;'>Weatheroo Company</h3>", unsafe_allow_html=True,)
    st.image(r"C:\Users\User2\Desktop\Proyek Akhir Analisis\Dashboard\Logo Cuaca.png", use_container_width=True)

    # Replace year and month dropdowns with a single selectbox
    analysis_type = st.selectbox(
        "Select Yearly Visualization",
        options=["Temperature Trend", "Highest and Lowest Temperature"]
    )

def visualize_temperature_trend(data, start_year, end_year):
    # Filter data for the specified year range
    data["date"] = pd.to_datetime(data["date"])
    filtered_data = data[
        (data["date"].dt.year >= start_year) &
        (data["date"].dt.year <= end_year)
    ]

    # Set y-axis order using an ordered categorical type
    weather_condition_order = ["Extreme", "Hot", "Humid", "Warm", "Cold", "Freezing"]
    filtered_data["weather_condition"] = pd.Categorical(filtered_data["weather_condition"], categories=weather_condition_order.reverse(), ordered=True)

    # Create the line chart using Seaborn with the ordered categorical data
    plt.figure(figsize=(12, 6))  
    sns.lineplot(x=filtered_data["date"].dt.month, y=filtered_data["weather_condition"], marker="o", color="b")

    # Customize the chart
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Temperature", fontsize=12)
    plt.xticks(range(1, 13), ["Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb"])
    plt.gca().set_facecolor('#f0f0f0')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Make the range
    temperature_ranges = {
        "Freezing": "<0\u00b0C",
        "Cold": "0-20\u00b0C",
        "Warm": "21-26\u00b0C",
        "Humid": "27-30\u00b0C",
        "Hot": "31-39\u00b0C",
        "Extreme": ">39\u00b0C"
    }

    y_labels = [f"{condition} ({temperature_ranges[condition]})" for condition in weather_condition_order]

    plt.yticks(range(len(weather_condition_order)), y_labels)
    plt.gca().invert_yaxis()

    # Display the plot in Streamlit
    st.pyplot(plt)

def plot_highest_lowest_temperature(highTemp, lowTemp):
    # Extract unique years
    years = highTemp["Year"].unique()

    # Create arrays for highest and lowest temperatures and months
    highest_temps = highTemp["Highest Temp"].values
    lowest_temps = lowTemp["Lowest Temp"].values
    highest_months = highTemp["Month"].values
    lowest_months = lowTemp["Month"].values

    # Set the width
    bar_width = 0.35

    # Set the positions on the x-axis
    r1 = np.arange(len(years))
    r2 = [x + bar_width for x in r1]

    # Create the grouped bar chart
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('#f0f0f0')
    bars1 = ax.bar(r1, highest_temps, color="red", width=bar_width, edgecolor="white", label="Highest Temp")
    bars2 = ax.bar(r2, lowest_temps, color="blue", width=bar_width, edgecolor="white", label="Lowest Temp")

    # Add labels, title, and legend
    ax.set_xlabel("Year", fontweight="bold", fontsize=14)
    ax.set_xticks([r + bar_width for r in range(len(years))], years, fontsize=14)
    ax.set_ylabel("Temperature", fontweight="bold", fontsize=14)
    ax.tick_params(axis='y', labelsize=14)
    ax.set_facecolor('#f0f0f0')
    ax.grid(True, color='white', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.legend(fontsize=14)

    # Adjust y-axis limits to include negative values
    ax.set_ylim(min(lowest_temps) - 5, max(highest_temps) + 5)

    # Add month labels on top of the bars
    for bar, month in zip(bars1, highest_months):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, month, ha="center", va="bottom", rotation=45, fontsize=14)

    for bar, month, year in zip(bars2, lowest_months, years):
        x_pos = bar.get_x() + bar.get_width() / 2
        y_pos = bar.get_height() + 1

        if month == "January" and year in [2016]:
            y_pos += 4.3

        if month == "January" and year in [2017]:
            y_pos += 2.2

        ax.text(x_pos, y_pos, month, ha="center", va="bottom", rotation=45, fontsize=14)

    # Show chart
    plt.axhline(0, color="black", linewidth=1, linestyle="--")
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

def main():
    st.title("Yearly Temperature")

    if analysis_type == "Temperature Trend":
        # Define the periods to visualize
        periods = [
            (2013, 2014),
            (2014, 2015),
            (2015, 2016),
            (2016, 2017)
        ]

        # Loop through each period and display the visualization
        for start_year, end_year in periods:
            st.subheader(f"Temperature Trend ({start_year} - {end_year})")
            visualize_temperature_trend(monthlyTemp_df, start_year, end_year)

    elif analysis_type == "Highest and Lowest Temperature":
        st.subheader("Highest and Lowest Temperatures (2013-2017)")
        plot_highest_lowest_temperature(highTemp, lowTemp)

if __name__ == "__main__":
    main()