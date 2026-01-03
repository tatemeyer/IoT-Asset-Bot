import json
import time
import logging
import os
import datetime as datetime

from control_center.reconciliation.reconcile import  ReconciliationEngine
from control_center.ui_automation.selenium_bot import ControlCenterBot
from control_center.intelligence.anomaly_detection import run_intelligence_layer

with open('config.json', 'r') as f:
    CONFIG = json.load(f)

log_file = CONFIG['log_file']
log_dir = os.path.dirname(log_file)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)


def run_pipeline():
    """Sequences the execution and handles critical failures."""
    logging.info("Starting Orchestrated Automation Pipeline.")

    # Step 1: UI Extraction with Retry Logic
    bot = ControlCenterBot()
    telemetry_data = None

    for attempt in range(CONFIG.get('retry_attempts', 3)):
        try:
            bot.launch_edge_browser()
            telemetry_data = bot.extract_latest_telemetry()
            break
        except Exception as e:
            logging.error(f"UI Extraction attempt {attempt + 1} failed: {e}")
            if attempt < CONFIG.get('retry_attempts', 3) - 1:
                time.sleep(CONFIG.get('retry_delay_seconds', 5))
            else:
                logging.critical("Max retries reached. Stopping pipeline.")
                return
        finally:
            bot.close()

    # Step 2: Validation and Reconciliation
    if telemetry_data:
        engine = ReconciliationEngine(CONFIG['ledger_path'])
        success = engine.reconcile(telemetry_data)

        if not success:
            logging.error("Reconciliation failed or duplicate detected. Check logs.")
            return

    # Step 3: Intelligence Layer
    try:
        run_intelligence_layer(CONFIG['ledger_path'], CONFIG['annotated_output'])
        logging.info("Intelligence layer successfully annotated the ledger.")
    except Exception as e:
        logging.error(f"Intelligence layer failure: {e}")

    logging.info("Pipeline execution completed successfully.")


if __name__ == "__main__":
    run_pipeline()