import pandas as pd
import logging
import os
from rules import apply_business_rules

class ReconciliationEngine:
    def __init__(self, ledger_path):
        self.ledger_path = ledger_path
        # Setup logging as defined in the automation standards [5]
        os.makedirs('../logs', exist_ok=True)
        logging.basicConfig(
            filename='../logs/automation.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.warning("TEST LOG ENTRY")

    def reconcile(self, telemetry_row):
        try:
            # --- Step 1: Load or initialize ledger safely ---
            if not os.path.exists(self.ledger_path):
                logging.warning("Ledger not found. Creating new ledger.")
                df = pd.DataFrame(columns=telemetry_row.keys())
                df.to_excel(self.ledger_path, index=False, engine="openpyxl")

            else:
                try:
                    # Attempt to load existing ledger
                    df = pd.read_excel(self.ledger_path, engine="openpyxl")

                    # Handle edge case: empty Excel file with no columns
                    if df.empty and len(df.columns) == 0:
                        logging.warning("Ledger file is empty. Reinitializing schema.")
                        df = pd.DataFrame(columns=telemetry_row.keys())

                except Exception as read_error:
                    logging.error(f"Ledger read failed, reinitializing ledger: {read_error}")
                    df = pd.DataFrame(columns=telemetry_row.keys())
                    df.to_excel(self.ledger_path, index=False, engine="openpyxl")

            # --- Step 2: Filter by asset_id ---
            asset_records = df[df['asset_id'] == telemetry_row['asset_id']]

            if asset_records.empty:
                logging.warning(f"No existing ledger record for Asset {telemetry_row['asset_id']}")
                self._append_to_ledger(df, telemetry_row)
                return True

            # --- Step 3: Apply business rules against latest record ---
            current_ledger = asset_records.iloc[-1]
            flags = apply_business_rules(telemetry_row, current_ledger)

            if flags:
                logging.warning(f"Anomalies for Asset {telemetry_row['asset_id']}: {flags}")

                # Phase 4 requirement: strict duplicate prevention
                if any("DUPLICATE" in f for f in flags):
                    logging.info("Duplicate telemetry detected. Skipping ledger update.")
                    return False
            else:
                logging.info(f"Asset {telemetry_row['asset_id']} reconciled successfully.")

            # --- Step 4: Append telemetry ---
            self._append_to_ledger(df, telemetry_row)
            return True

        except Exception as e:
            logging.error(f"Exception during reconciliation: {e}", exc_info=True)
            return False


    def _append_to_ledger(self, df, new_row):
        """Helper to append data and save to Excel without manual interaction."""
        new_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        new_df.to_excel(self.ledger_path, index=False)
        logging.info(f"Ledger updated at {self.ledger_path}")

# Example Usage
if __name__ == "__main__":
    engine = ReconciliationEngine("../data/mock_asset_ledger.xlsx")
    # Sample data following TelemetrySchema [4]
    sample_telemetry = {
        "asset_id": 1002,
        "timestamp": "2023-10-27T09:00:00Z",
        "mileage": 1555.5,
        "battery_health": 80,
        "usage_hours": 125.0,
        "error_code": "OK"
    }
    engine.reconcile(sample_telemetry)