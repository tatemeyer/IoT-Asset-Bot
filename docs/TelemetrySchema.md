| Field Name     | Data Type        | Requirement | Business Rule Mapping | Description                                           |
|----------------|-----------------|------------|---------------------|-------------------------------------------------------|
| asset_id       | Integer         | Mandatory  | N/A                 | Unique identifier for the remote hardware asset.     |
| timestamp      | ISO 8601 String | Mandatory  | BR-05               | For auditability and time-series tracking.          |
| mileage        | Float / Int     | Mandatory  | BR-01               | Used to ensure asset mileage does not decrease.     |
| battery_health | Integer (0-100)| Mandatory  | BR-02               | Used to trigger alerts if health falls below threshold. |
| usage_hours    | Float           | Mandatory  | BR-04               | Tracks total hours to flag anomalies above threshold. |
| error_code     | String          | Mandatory  | BR-03               | System status codes (e.g., "OK", "FAIL") for escalation. |
