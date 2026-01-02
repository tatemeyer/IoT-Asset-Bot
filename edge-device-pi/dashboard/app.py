from flask import Flask, render_template
from datetime import datetime
import random

app = Flask(__name__)

# Sample assets
assets = [
    {"asset_id": 1001, "name": "Asset A"},
    {"asset_id": 1002, "name": "Asset B"},
    {"asset_id": 1003, "name": "Asset C"},
]

def get_asset_status():
    """
    Updates each asset with mandatory telemetry fields:
    - timestamp: ISO 8601 UTC string
    - mileage: float (100.0 - 5000.0)
    - battery_health: int (5 - 100)
    - usage_hours: float (0.0 - 6000.0)
    - error_code: string ("OK" or "FAIL")
    """
    for asset in assets:
        asset["timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        asset["mileage"] = random.randint(100, 5000)
        asset["battery_health"] = random.randint(5, 100)
        asset["usage_hours"] = random.randint(0, 6000)
        asset["error_code"] = random.choice(["OK", "FAIL"])
    return assets

@app.route("/")
def index():
    data = get_asset_status()
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("index.html", assets=data, last_updated=last_updated)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
