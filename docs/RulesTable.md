| Business Rule | Field           | Condition / Check                           | Action / Flag                                      |
|---------------|----------------|--------------------------------------------|---------------------------------------------------|
| BR-01         | mileage        | New telemetry mileage < existing ledger     | "BR-01: Mileage Decrease Detected"               |
| BR-02         | battery_health | Battery health < 20%                        | "BR-02: Low Battery Detected"                    |
| BR-03         | error_code     | Error code == "FAIL"                        | "BR-03: Error Code Detected"                     |
| BR-04         | usage_hours    | Usage hours > 5000                           | "BR-04: Usage Hours Anomaly Detected"            |
| BR-05         | timestamp      | New timestamp < last ledger timestamp       | "BR-05: Timestamp Anomaly Detected"             |
