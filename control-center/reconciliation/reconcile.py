import logging
import pandas as pd
import os
from datetime import datetime

def apply_business_rules(new_data, current_ledger):
    anomalies = []

    # BR-01: Asset mileage must not decrease
    if new_data['mileage'] < current_ledger['mileage']:
        anomalies.append("BR-01: Mileage Decrease Detected")

    # BR-02: Battery health below threshold
    if new_data['battery_health'] < 20:
        anomalies.append("BR-02: Low Battery Detected")

    # BR-03: Error codes marked as FAIL
    if new_data['error_code'] == "FAIL":
        anomalies.append("BR-03: Error Code Detected")

    # BR-04: Usage hours exceed threshold (example: 5000 hours)
    if new_data['usage_hours'] > 5000:
        anomalies.append("BR-04: Usage Hours Anomaly Detected")

    # BR-05: Timestamp is earlier than last ledger entry
    new_ts = datetime.fromisoformat(new_data['timestamp'].replace("Z", "+00:00"))
    last_ts = datetime.fromisoformat(str(current_ledger['timestamp']).replace("Z", "+00:00"))
    if new_ts < last_ts:
        anomalies.append("BR-05: Timestamp Anomaly Detected")

    return anomalies


class ReconciliationEngine:
    def __init__(self, ledger_path):
        self.ledger_path = ledger_path
        os.makedirs(os.path.dirname('../logs/automation.log'), exist_ok=True)
        logging.basicConfig(filename='../logs/automation.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def reconcile(self, telemetry_row):
        try:
            # Load Excel-based ledger
            df = pd.read_excel(self.ledger_path)
            asset_records = df[df['asset_id'] == telemetry_row['asset_id']]

            if asset_records.empty:
                logging.warning(f"No existing ledger record for Asset {telemetry_row['asset_id']}")
                return False

            current_ledger = asset_records.iloc[0]  # First matching record
            flags = apply_business_rules(telemetry_row, current_ledger)

            if flags:
                logging.warning(f"Anomalies for Asset {telemetry_row['asset_id']}: {flags}")
            else:
                logging.info(f"Asset {telemetry_row['asset_id']} reconciled successfully.")

            # TODO: Update ledger, interact with UI
            return True
        except Exception as e:
            logging.error(f"Exception during reconciliation: {e}")
            return False
