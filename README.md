# Intelligent IoT Asset Reconciliation System

## Overview

The **Intelligent IoT Asset Reconciliation System** is a cross-platform automation project that simulates how financial institutions reconcile telemetry data from remote assets into centralized financial systems.

This project demonstrates how **RPA-style automation principles** (UI interaction, fragile workflows, exception handling) can be implemented **purely using Python and C++**, without relying on commercial RPA tools. The goal is to bridge **embedded systems**, **enterprise automation**, and **financial reconciliation logic** in a realistic, production-inspired architecture.

---

## Problem Statement

In many enterprise environments—especially in finance—critical asset data originates from **remote or embedded devices** but must be manually reconciled into **legacy systems** such as Excel-based ledgers or ERP tools. These workflows are:

- Repetitive  
- Error-prone  
- UI-driven (no APIs available)  
- Fragile to system or network failures  

This project automates that reconciliation process end-to-end while preserving the real-world constraints that make RPA necessary.

---

## Solution Architecture

Raspberry Pi (Linux, C++)

└─ Telemetry Generator (C++)

└─ Local CSV / HTTP Exposure


Windows Control Center (Python)

├─ UI / Browser Automation (Selenium / PyAutoGUI)

├─ Reconciliation Engine

├─ Excel Ledger Interaction

├─ Anomaly Detection (Explainable Logic)

└─ Logging & Exception Handling

---

### Key Design Choices
- **C++ at the Edge:** Simulates embedded, long-running telemetry generation
- **Python Control Center:** Orchestrates automation, reconciliation, and intelligence
- **UI-Level Automation:** Mimics human interaction where APIs are unavailable
- **Explainable Intelligence:** Rule-based anomaly detection aligned with financial governance

---

## Features

- Simulated IoT telemetry generation on a Raspberry Pi
- Cross-platform automation between Linux and Windows
- UI-driven data extraction (browser / desktop automation)
- Automated reconciliation into an Excel-based financial ledger
- Anomaly and exception detection using deterministic rules
- Robust error handling (offline device, missing data, file locks)
- Audit-friendly logging

---

## Repository Structure

Intelligent-IoT-Asset-Reconciliation/

│ 

├── docs/ 

│ ├── PDD.md 

│ └── architecture.png 

│ 

├── edge-device-pi/

│ ├── telemetry_generator.cpp

│ ├── Makefile

│ └── telemetry.csv

│

├── control-center/

│ ├── ui_automation/

│ │ ├── selenium_bot.py

│ │ └── desktop_bot.py

│ │

│ ├── reconciliation/

│ │ ├── reconcile.py

│ │ └── rules.py

│ │

│ ├── intelligence/

│ │ └── anomaly_detection.py

│ │

│ ├── data/

│ │ └── mock_asset_ledger.xlsx

│ │

│ └── main.py

│

├── logs/

│ └── automation.log

│

└── README.md


---

## How It Works

### 1. Edge Telemetry Generation (C++)
A C++ program running on a Raspberry Pi simulates asset telemetry such as mileage, usage, and health indicators. Data is periodically written to a CSV file, representing a constrained embedded system with limited integration options.

### 2. UI-Based Data Extraction (Python)
On Windows, Python-based automation retrieves telemetry data using:
- Browser automation (Selenium), or
- Desktop UI automation (PyAutoGUI / PyWinAuto)

This mirrors RPA-style automation where backend APIs are unavailable.

### 3. Financial Reconciliation
Extracted telemetry is reconciled against a mock Excel ledger representing a financial system of record. Discrepancies are flagged automatically.

### 4. Intelligent Anomaly Detection
A lightweight intelligence layer evaluates telemetry using explainable, rule-based logic appropriate for financial environments where transparency is required.

### 5. Exception Handling & Logging
The system gracefully handles failures such as:
- Offline edge devices
- Missing or corrupted files
- Locked financial ledgers  

All exceptions are logged for auditability.

---

## Why No Commercial RPA Tool?

This project intentionally avoids tools like UiPath or Power Automate to demonstrate a **deep understanding of automation fundamentals** rather than vendor-specific implementations.

The same logic could be migrated to a commercial RPA platform with minimal changes.

> The focus is on **automation design, resilience, and governance**, not tool dependency.

---

## Key Skills Demonstrated

- Embedded systems (C++, Linux)
- Cross-platform automation
- RPA principles without vendor lock-in
- Financial reconciliation logic
- Explainable intelligent automation
- Exception handling and reliability engineering
- Enterprise-ready project structure and documentation

---

## Future Enhancements

- Add authentication and role-based access
- Replace CSV with message queues (MQTT / Kafka)
- Integrate a lightweight REST API
- Add dashboard-based reporting
- Package control center as a Windows service

---

## License

This project is provided for educational and demonstration purposes.
