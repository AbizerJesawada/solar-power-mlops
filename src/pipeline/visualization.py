import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualizations():
    os.makedirs("reports", exist_ok=True)
    
    df = pd.read_csv("data/processed/final_data.csv")
    
    # Plot 1: AC Power Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(df['AC_POWER'], bins=50, color='orange')
    plt.title("Solar AC Power Distribution")
    plt.xlabel("AC Power (kW)")
    plt.ylabel("Frequency")
    plt.savefig("reports/ac_power_distribution.png")
    plt.close()
    print("Plot 1 saved!")

    # Plot 2: Irradiation vs AC Power
    plt.figure(figsize=(10, 5))
    sns.scatterplot(x=df['IRRADIATION'], y=df['AC_POWER'], alpha=0.3, color='blue')
    plt.title("Irradiation vs AC Power")
    plt.xlabel("Irradiation")
    plt.ylabel("AC Power (kW)")
    plt.savefig("reports/irradiation_vs_power.png")
    plt.close()
    print("Plot 2 saved!")

    # Plot 3: Temperature vs AC Power
    plt.figure(figsize=(10, 5))
    sns.scatterplot(x=df['AMBIENT_TEMPERATURE'], y=df['AC_POWER'], alpha=0.3, color='red')
    plt.title("Temperature vs AC Power")
    plt.xlabel("Ambient Temperature (C)")
    plt.ylabel("AC Power (kW)")
    plt.savefig("reports/temperature_vs_power.png")
    plt.close()
    print("Plot 3 saved!")

    # Plot 4: Hourly Average Power
    plt.figure(figsize=(10, 5))
    hourly = df.groupby('HOUR')['AC_POWER'].mean()
    sns.barplot(x=hourly.index, y=hourly.values, color='green')
    plt.title("Average Solar Power by Hour of Day")
    plt.xlabel("Hour")
    plt.ylabel("Average AC Power (kW)")
    plt.savefig("reports/hourly_power.png")
    plt.close()
    print("Plot 4 saved!")

    # Plot 5: Correlation Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, fmt='.2f', cmap='coolwarm')
    plt.title("Feature Correlation Heatmap")
    plt.savefig("reports/correlation_heatmap.png")
    plt.close()
    print("Plot 5 saved!")

    print("\nAll visualizations saved in reports/ folder!")

if __name__ == "__main__":
    create_visualizations()
