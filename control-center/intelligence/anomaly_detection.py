import pandas as pd
import logging

LOW_BATTERY_THRESHOLD = 75
MAX_USAGE_HOURS = 10

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def detect_anomalies(row):
    flags = []
    status = "CLEARED"

    if pd.isna(row['battery_health']):
        flags.append("DATA_ERROR: battery_health missing")
        status = "ESCALATED"

    elif row['battery_health'] < LOW_BATTERY_THRESHOLD:
        flags.append(f"LOW_BATTERY: {row['battery_health']}%")

    if row['usage_hours'] > MAX_USAGE_HOURS:
        flags.append(f"HIGH_USAGE: {row['usage_hours']} hrs")

    if row['error_code'] == "FAIL":
        flags.append("CRITICAL: SYSTEM_FAIL_ESCALATE")
        status = "ESCALATED"

    if flags and status != "ESCALATED":
        status = "WARNING"

    logging.info(f"Asset {row.get('asset_id', 'UNKNOWN')} → {status} → {flags}")

    return status, "; ".join(flags)
