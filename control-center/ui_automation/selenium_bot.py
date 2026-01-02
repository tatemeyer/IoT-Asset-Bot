import json
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configure logging to match repo
os.makedirs('../logs/', exist_ok=True)
logging.basicConfig(
    filename='../logs/automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ControlCenterBot:
    def __init__(self, config_path='selectors.json', driver_path=r"C:\WebDrivers\msedgedriver.exe"):
        with open(config_path) as f:
            self.config = json.load(f)
        self.driver_path = driver_path
        self.driver = None

    def launch_edge_browser(self):
        try:
            options = EdgeOptions()
            service = Service(self.driver_path)
            self.driver = webdriver.Edge(service=service, options=options)
            self.driver.get(self.config['dashboard_url'])
            logging.info("Edge browser launched and navigated to Pi Dashboard.")
        except Exception as e:
            logging.error(f"Failed to launch Edge browser: {e}")
            raise

    def extract_latest_telemetry(self, timeout=10):
        try:
            # Wait for the first table row
            row = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.config['table_row']))
            )

            # Extract each column safely
            telemetry_data = {}
            for key, selector in self.config['columns'].items():
                element = row.find_element(By.CSS_SELECTOR, selector)
                text = element.text.strip()

                # Convert numeric values where appropriate
                if key in ["asset_id", "battery_health"]:
                    telemetry_data[key] = int(text)
                elif key in ["mileage", "usage_hours"]:
                    telemetry_data[key] = float(text)
                else:
                    telemetry_data[key] = text

            logging.info(f"Successfully extracted data for Asset {telemetry_data['asset_id']}")
            return telemetry_data

        except TimeoutException:
            self.capture_failure_evidence(f"No telemetry row found after {timeout} seconds")
            raise
        except Exception as e:
            self.capture_failure_evidence(e)
            raise

    def extract_all_telemetry(self, timeout=10):
        """
        Extracts telemetry for all assets in the table.
        Returns a list of dictionaries.
        """
        try:
            # Wait until at least one row is present
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.config['table_row']))
            )

            rows = self.driver.find_elements(By.CSS_SELECTOR, self.config['table_row'])
            all_telemetry = []

            for row in rows:
                telemetry_data = {}
                for key, selector in self.config['columns'].items():
                    element = row.find_element(By.CSS_SELECTOR, selector)
                    text = element.text.strip()

                    # Convert numeric fields
                    if key in ["asset_id", "battery_health"]:
                        telemetry_data[key] = int(text)
                    elif key in ["mileage", "usage_hours"]:
                        telemetry_data[key] = float(text)
                    else:
                        telemetry_data[key] = text

                all_telemetry.append(telemetry_data)

            logging.info(f"Successfully extracted telemetry for {len(all_telemetry)} assets")
            return all_telemetry

        except TimeoutException:
            self.capture_failure_evidence(f"No telemetry rows found after {timeout} seconds")
            raise
        except Exception as e:
            self.capture_failure_evidence(e)
            raise

    def capture_failure_evidence(self, error):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f'../logs/failure_{timestamp}.png'
        if self.driver:
            self.driver.save_screenshot(screenshot_path)
        logging.error(f"Automation Failure: {error}. Screenshot saved to {screenshot_path}")

    def close(self):
        if self.driver:
            self.driver.quit()
            logging.info("Browser closed")

if __name__ == "__main__":
    bot = ControlCenterBot()
    try:
        bot.launch_edge_browser()
        data = bot.extract_latest_telemetry()
        data1 = bot.extract_all_telemetry()
        print(f"Extracted 1st Row Telemetry: {data}")
        print(f"Extracted All Telemetry: {data1}")
    finally:
        bot.close()