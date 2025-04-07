import time
import random
from datetime import datetime, timezone
from custom_logger import get_logger

logger = get_logger("TelemetryLogger", "telemetry_new.log")

TELEMETRY_BATCH = []
BATCH_SIZE = 5
BATCH_INTERVAL = 3  # seconds


def get_telemetry():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": round(random.uniform(20.0, 80.0), 2),
        "voltage": round(random.uniform(3.0, 4.2), 2),
        "current": round(random.uniform(0.1, 2.0), 2),
        "status": random.choices(
            ["OK", "WARN", "FAIL"],
            weights=[80, 15, 5],  # Lower failure rate
            k=1
        )[0],
    }


def flush_batch():
    global TELEMETRY_BATCH
    if TELEMETRY_BATCH:
        logger.info("--- Telemetry Batch Start ---")
        for entry in TELEMETRY_BATCH:
            logger.info(entry)
        logger.info("--- Telemetry Batch End ---\n")
        TELEMETRY_BATCH = []


if __name__ == "__main__":
    logger.info("🚀 Telemetry Logger Started")
    last_flush = time.time()
    try:
        while True:
            telemetry = get_telemetry()
            TELEMETRY_BATCH.append(telemetry)

            now = time.time()
            if len(TELEMETRY_BATCH) >= BATCH_SIZE or now - last_flush >= BATCH_INTERVAL:
                flush_batch()
                last_flush = now

            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Telemetry Logger Stopped by User")
        flush_batch()
