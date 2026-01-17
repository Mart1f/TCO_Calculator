## 🚚🚢 TCO Calculator Project

This repository contains a **Total Cost of Ownership (TCO) calculator** designed to estimate the **full lifecycle cost of transportation assets**, with a focus on **trucks and ships**. The tool allows comparing different technologies, such as **diesel and electric powertrains**, using consistent technical and financial assumptions.

The project is intended to provide a clear and transparent view of **long-term costs**, going beyond simple purchase price analysis.

---

## 🎯 Project Purpose

The main objective of this project is to understand how different cost components interact over time and to identify the **real cost drivers** of a vehicle or vessel during its operational life.

The calculator combines:

* **Capital Expenditures (CAPEX)**
* **Operating Expenditures (OPEX)**
* **Residual Value (RV)**
* **Discounting over time** (time value of money)

All these elements are integrated into a single **Total Cost of Ownership** metric.

---

## 🧩 Architecture Overview

The system follows a **modular architecture**, where each cost component is computed independently.

### CAPEX Module

The CAPEX module computes all capital-related costs associated with acquiring and deploying an asset, including:

* Vehicle purchase cost
* Conversion and certification costs
* Infrastructure investments
* Registration taxes
* Financing costs
* Subsidies

The output includes the **total CAPEX**, the **Capital Recovery Factor (CRF)**, and a detailed breakdown of capital costs.

---

### OPEX Modules

Operating expenditures are computed using dedicated OPEX calculators for each asset type:

* **Truck OPEX Calculator**
* **Ship OPEX Calculator**

These modules estimate **annual operating costs**, such as:

* Energy or fuel consumption
* Maintenance
* Insurance
* Crew costs (ships only)
* Port fees and operational taxes (ships only)

The result is an **annual OPEX value**, with optional detailed breakdowns depending on the asset.

---

### Residual Value Module

The **Residual Value (RV) module** estimates the remaining value of the asset at the end of its operational lifetime.

The calculation accounts for:

* Depreciation
* Usage intensity
* Powertrain technology
* Country-specific effects
* Maintenance assumptions
* External and health-related impacts

The residual value is then **discounted to present value** and reintegrated into the TCO calculation.

---

## ⚙️ How It Works

* A **single structured input** defines the scenario
  (asset type, technology, country, operational lifetime, discount rate, etc.)

* **CAPEX**, **OPEX**, and **Residual Value** are calculated **independently**

* All costs are **discounted over time**

* The **final Total Cost of Ownership** is computed

* Results are returned as **structured data**, ready to be reused

---

## 🧠 Main Orchestration Logic

All calculations are coordinated by a central function called **`run_tco_scenario`**.

This function:

1. Reads all scenario inputs
2. Runs the CAPEX calculation
3. Runs the Residual Value calculation
4. Runs the appropriate OPEX calculation (truck or ship)
5. Combines all components into a final TCO result

The orchestration logic is **interface-agnostic**, meaning it can be used from:

* Command-line scripts
* Web dashboards
* APIs
* Decision-support or simulation tools

---

## 📥 Inputs

The model requires the following inputs:

* Asset type (**truck** or **ship**)
* Powertrain technology
* Country of operation
* Operational lifetime
* Financial parameters (e.g. **discount rate**)
* Detailed **CAPEX**, **OPEX**, and **Residual Value** assumptions

All inputs are provided through a **single structured input dictionary**.

---

## 📤 Outputs

The calculator produces the following outputs:

* Total CAPEX
* Annual OPEX
* Residual Value
* Discounted cash flows
* **Total TCO (present value)**
* Equivalent annual cost

All outputs are returned in a **structured and JSON-serializable format**, making them easy to visualize, compare across scenarios, or integrate into other systems.

---

## 🧱 Design Philosophy

The project follows a few key design principles:

* **Modular** – each cost block is independent
* **Transparent** – detailed breakdowns are preserved
* **Extensible** – easy to add new technologies or asset types
* **UI-ready** – outputs are structured for dashboards or APIs
* **Engineering-oriented** – suitable for technical and analytical use

---

## 📊 Typical Use Cases

* Comparing **diesel vs. electric trucks**
* Evaluating **ship electrification scenarios**
* Supporting **fleet investment decisions**
* Performing **long-term cost and sustainability analysis**
* Feeding results into **digital twins or decision-support tools**


