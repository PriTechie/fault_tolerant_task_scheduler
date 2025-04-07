import os
import logging
from collections import Counter
import matplotlib.pyplot as plt

LOG_FILE = os.path.join("logs", "telemetry.log")

def parse_status_counts(file_path):
    status_counts = Counter()
    with open(file_path, 'r') as file:
        for line in file:
            if "'status':" in line:
                try:
                    parts = line.strip().split("'status': '")
                    if len(parts) > 1:
                        status = parts[1].split("'")[0]
                        status_counts[status] += 1
                except IndexError:
                    continue
    return status_counts

def plot_status_distribution(status_counts):
    labels = status_counts.keys()
    sizes = status_counts.values()
    colors = ['#66c2a5', '#fc8d62', '#8da0cb']
    explode = [0.1 if label == 'FAIL' else 0 for label in labels]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140,
            colors=colors, explode=explode, shadow=True)
    plt.title('System Status Distribution')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if not os.path.exists(LOG_FILE):
        logging.error("Telemetry log file not found.")
    else:
        logging.info("Parsing system health data...")
        counts = parse_status_counts(LOG_FILE)
        logging.info(f"Status Counts: {counts}")
        plot_status_distribution(counts)
