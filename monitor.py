import time
import re
from collections import Counter
from datetime import datetime

LOG_PATH = "logs/telemetry.log"

def extract_batches(log_file):
    with open(log_file, 'r') as f:
        content = f.read()

    # Find all batches between the start and end markers
    raw_batches = re.findall(r"--- Telemetry Batch Start ---\n(.*?)--- Telemetry Batch End ---", content, re.DOTALL)
    return raw_batches[-3:]  # Only keep last 3 batches to avoid flooding

def parse_entry(entry_line):
    # Extract fields from log string manually
    match = re.search(r"'timestamp': '(.+?)', 'temperature': ([\d.]+), 'voltage': ([\d.]+), 'current': ([\d.]+), 'status': '(\w+)'", entry_line)
    if match:
        timestamp = match.group(1)
        temp = float(match.group(2))
        volt = float(match.group(3))
        curr = float(match.group(4))
        status = match.group(5)
        return {"timestamp": timestamp, "temperature": temp, "voltage": volt, "current": curr, "status": status}
    return None

def analyze_batch(batch):
    lines = batch.strip().split("\n")
    data = [parse_entry(line) for line in lines if parse_entry(line)]
    
    if not data:
        return None

    avg_temp = round(sum(d['temperature'] for d in data) / len(data), 2)
    avg_volt = round(sum(d['voltage'] for d in data) / len(data), 2)
    avg_curr = round(sum(d['current'] for d in data) / len(data), 2)
    statuses = Counter(d['status'] for d in data)

    return {
        "count": len(data),
        "avg_temp": avg_temp,
        "avg_volt": avg_volt,
        "avg_curr": avg_curr,
        "statuses": statuses
    }

if __name__ == "__main__":
    print("📡 Live Telemetry Monitor Started...\n")

    try:
        while True:
            batches = extract_batches(LOG_PATH)
            if not batches:
                print("No batches found.")
                time.sleep(2)
                continue

            latest_batch = analyze_batch(batches[-1])
            if latest_batch:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 Last Batch Stats:")
                print(f"  → Entries: {latest_batch['count']}")
                print(f"  → Avg Temp: {latest_batch['avg_temp']}°C")
                print(f"  → Avg Voltage: {latest_batch['avg_volt']} V")
                print(f"  → Avg Current: {latest_batch['avg_curr']} A")
                print(f"  → Statuses: {dict(latest_batch['statuses'])}")
                print("-" * 40)

            time.sleep(5)

    except KeyboardInterrupt:
        print("\n🛑 Monitor Stopped.")
