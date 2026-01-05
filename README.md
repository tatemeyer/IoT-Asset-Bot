# Intelligent IoT Asset Reconciliation System

## Overview

The Intelligent IoT Asset Reconciliation System is a fully automated, cross-platform pipeline that simulates how enterprises reconcile telemetry data from remote assets into centralized financial records using RPA-style UI automation and explainable intelligence.

The system intentionally avoids backend APIs and commercial RPA tools, instead implementing true UI-driven automation using Python and C++, mirroring real-world enterprise constraints where legacy systems, dashboards, and human-oriented interfaces dominate.

This project is considered feature-complete and stable as an MVP.

---

## High-Level Architecture

Edge Device (Raspberry Pi)
- Flask Dashboard (app.py)
- Human-readable Telemetry UI

(UI-only access)

Control Center (Windows / Python)
- Selenium UI Automation (RPA)
- Reconciliation Engine
- Intelligence Layer (Anomaly Detection)
- Excel-based Financial Ledgers
- Centralized Logging

Output
- Annotated Financial Output

---

## Core Design Principles

- Real RPA Behavior: Data is extracted exclusively through a UI designed for humans
- No API Shortcuts: Automation interacts with dashboards, not backend files
- Explainable Intelligence: Deterministic, auditable anomaly detection
- Enterprise Governance: Logging, retries, validation, and separation of concerns
- Cross-Platform Interoperability: Linux edge device and Windows control center

---

## Repository Structure

## Repository Structure

```text
.
├── control_center/
│   ├── intelligence/
│   │   └── anomaly_detection.py
│   ├── reconciliation/
│   │   └── reconcile.py
│   ├── ui_automation/
│   │   ├── selenium_bot.py
│   │   └── selectors.json
│   └── data/
│       ├── asset_ledger.xlsx
│       └── annotated_ledger.xlsx
│
├── edge_device/
│   └── app.py
│
├── logs/
│   └── automation.log
│
├── config.json
├── main.py
└── README.md
```

---

## Edge Device (Raspberry Pi)

Flask Dashboard (app.py)

- Hosts a human-readable telemetry dashboard
- Displays latest asset metrics in tabular form
- Serves as the only data source for the automation
- Designed explicitly to be scraped via UI automation
- No APIs are exposed for direct data access

---

## Control Center Components

UI Automation (RPA Core)

Module: selenium_bot.py

- Uses Selenium to launch a real browser session
- Navigates to the Raspberry Pi dashboard
- Extracts telemetry using DOM selectors
- Handles multiple failure modes:
  - Page load timeouts
  - Missing UI elements
  - Stale UI state
- Selector definitions are externalized in selectors.json to reduce fragility
- Mimics real human interaction patterns

---

Reconciliation Engine

Module: reconcile.py

Responsibilities:
- Validates incoming telemetry
- Evaluates new data against historical ledger entries
- Enforces predefined business rules
- Prevents duplicate or out-of-order records
- Persists reconciled data to Excel

Example rule types:
- Mileage must be monotonic
- Asset IDs must match known records
- Timestamps must be newer than previous entries

All financial data is stored in Excel spreadsheets under control_center/data.

---

Intelligence Layer (Anomaly Detection)

Module: anomaly_detection.py

The intelligence layer applies explainable, rule-based logic appropriate for financial and audit-sensitive environments.

Example logic:

def detect_anomalies(row):
    flags = []
    status = "CLEARED"

    if battery_health is missing:
        flag data error and escalate

    if battery health below threshold:
        flag low battery

    if usage exceeds threshold:
        flag high usage

    if error code equals FAIL:
        escalate immediately

    return final status and flags

Outputs:
- Annotated Excel ledger
- Status classifications: CLEARED, WARNING, ESCALATED
- Full audit trail via centralized logging

---

## Orchestration Pipeline

Entry Point: main.py

The entire system is orchestrated from a single control file.

Responsibilities:
- Configuration loading
- Centralized logging initialization
- Retry logic for UI automation
- Sequential execution of pipeline stages
- Graceful handling of critical failures

Pipeline Flow:
1. UI Extraction with retry logic
2. Telemetry validation and reconciliation
3. Intelligence layer annotation
4. Completion logging

All execution logs are written to:
logs/automation.log

---

## Logging and Auditability

- Single centralized log file
- Timestamped entries
- INFO, ERROR, and CRITICAL log levels
- UI failures, reconciliation decisions, and anomaly flags are logged

This enables:
- Post-run auditing
- Failure diagnosis
- Governance and compliance review

---

## Configuration

All runtime parameters are externalized in config.json, including:
- Retry attempts
- Retry delays
- Ledger paths
- Log file location
- Output file destinations

No environment-specific values are hardcoded.

---

## Why This Is Real RPA Without RPA Tools

- UI-only data access
- Fragile selector handling
- Human-oriented dashboards
- Retry and exception logic
- No backend integration shortcuts

This mirrors enterprise RPA use cases where APIs are unavailable, legacy systems dominate, and reliability matters more than raw speed.

---

## Current Status

- Feature complete
- Stable MVP
- End-to-end automation
- Enterprise-style architecture

---

## Potential Enhancements

- Multi-asset support
- Role-based access controls
- Message queue ingestion
- Reporting dashboards
- Containerized deployment

---

## License

This project is intended for educational, demonstration, and portfolio use.
