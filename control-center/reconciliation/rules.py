from datetime import datetime


def apply_business_rules(new_data, current_ledger):
    """
    Evaluates new telemetry against historical ledger data using 
    predefined Business Rules (Phase 4 MVP + domain extensions).
    """
    anomalies = []

    # BR-00: Asset ID must match (MVP requirement)
    if new_data['asset_id'] != current_ledger['asset_id']:
        anomalies.append("BR-00: Asset ID Mismatch")

    # BR-01: Asset mileage must not decrease
    if new_data['mileage'] < current_ledger['mileage']:
        anomalies.append("BR-01: Mileage Decrease Detected")

    # BR-02: Battery health below threshold (20%)
    if new_data.get('battery_health') is not None and new_data['battery_health'] < 20:
        anomalies.append("BR-02: Low Battery Detected")

    # BR-03: Error codes marked as FAIL
    if new_data.get('error_code') == "FAIL":
        anomalies.append("BR-03: Error Code Detected")

    # BR-04: Usage hours exceed threshold (5000 hours)
    if new_data.get('usage_hours') is not None and new_data['usage_hours'] > 5000:
        anomalies.append("BR-04: Usage Hours Anomaly Detected")

    # BR-05: Timestamp must be newer than the last ledger entry
    new_ts = datetime.fromisoformat(new_data['timestamp'].replace("Z", "+00:00"))
    last_ts = datetime.fromisoformat(str(current_ledger['timestamp']).replace("Z", "+00:00"))

    if new_ts < last_ts:
        anomalies.append("BR-05: Timestamp Older Than Ledger")
    elif new_ts == last_ts:
        anomalies.append("DUPLICATE: Entry already exists in ledger")

    return anomalies
