import re
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


def parse_telemetry_log(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract telemetry batches
    batches = re.findall(r"--- Telemetry Batch Start ---\n(.*?)--- Telemetry Batch End ---", content, re.DOTALL)

    data = []
    for batch in batches:
        entries = re.findall(r"{.*?}", batch)
        for entry in entries:
            try:
                parsed = eval(entry)
                data.append(parsed)
            except Exception as e:
                print(f"Error parsing entry: {entry}\n{e}")

    return pd.DataFrame(data)


def plot_telemetry(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['temperature'], label='Temperature (°C)', color='r')
    plt.plot(df['timestamp'], df['voltage'], label='Voltage (V)', color='b')
    plt.plot(df['timestamp'], df['current'], label='Current (A)', color='g')
    plt.xlabel('Timestamp')
    plt.ylabel('Readings')
    plt.title('Telemetry Readings Over Time')
    plt.legend()
    plt.tight_layout()
    plt.savefig("readings.png")
    plt.show()


def generate_failure_pie_chart(df):
    status_counts = Counter(df["status"])

    plt.figure(figsize=(6, 6))
    plt.pie(status_counts.values(), labels=status_counts.keys(), autopct='%1.1f%%', startangle=140,
            colors=["#4CAF50", "#FFC107", "#F44336"])
    plt.title("Telemetry Status Distribution")
    plt.tight_layout()
    plt.savefig("failures.png")
    plt.show()


if __name__ == "__main__":
    log_file = r"C:\fault_tolerant_task_scheduler\logs\telemetry_new.log"
    df = parse_telemetry_log(log_file)

    if not df.empty:
        plot_telemetry(df)
        generate_failure_pie_chart(df)
    else:
        print("No data found in the log file.")
