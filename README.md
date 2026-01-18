# 🚚🚢 TCO Calculator Project

This repository contains a **Total Cost of Ownership (TCO) Calculator** designed to estimate the **full lifecycle cost of transportation assets**, with a focus on **trucks and ships**.

The project allows comparing different technologies (e.g. diesel vs electric) using **consistent financial, operational, and technical assumptions**, going far beyond a simple purchase-price comparison.

The goal is to make long-term cost behavior **transparent, reproducible, and explainable**.

---

## 🎯 What Is This Project?

This project answers a simple but important question:

**What does this vehicle or vessel really cost over its entire life?**

Instead of looking only at the purchase price, the calculator evaluates:

- How much it costs to buy and deploy the asset
- How much it costs to operate every year
- How much value it still has at the end of its life
- How money loses value over time (discounting)

All of this is combined into a single metric:

**Total Cost of Ownership (TCO)**

---

## 🧩 What Does the Calculator Compute?

The TCO is built from four main blocks.

### 1. CAPEX – Capital Expenditures

Upfront and investment-related costs:
- Vehicle or vessel purchase price
- Conversion or certification costs
- Charging or fueling infrastructure
- Registration and licensing taxes
- Financing costs
- Subsidies and incentives

Output:
- Total CAPEX
- Capital Recovery Factor (CRF)

---

### 2. OPEX – Operating Expenditures

Recurring yearly costs during operation.

Different calculators exist for each asset type.

For trucks:
- Energy or fuel consumption
- Maintenance
- Insurance
- Taxes

For ships:
- Energy or fuel consumption
- Maintenance
- Insurance
- Crew costs
- Port fees
- Operational taxes

Output:
- Annual OPEX
- Optional detailed breakdown

---

### 3. Residual Value (RV)

The Residual Value module estimates how much the asset is worth at the end of its operational life.

It accounts for:
- Asset age
- Usage intensity (distance traveled)
- Powertrain technology
- Maintenance assumptions
- Country-specific parameters
- External and health-related impacts

The residual value is discounted to present value and reintegrated into the TCO calculation.

---

### 4. Discounting and Aggregation

All costs are:
- Discounted using a chosen discount rate
- Aggregated over the full operational lifetime

Final outputs include:
- Total TCO (present value)
- Equivalent annual cost
- Cost per distance unit

---

## 🏗️ Code Architecture

The project follows a modular architecture.

Each cost block is computed independently and then combined.

TCO  
- CAPEX calculator  
- OPEX calculator (truck or ship)  
- Residual Value calculator  (truck or ship)
- Discounting and aggregation  

This structure makes the model:
- Easier to maintain
- Easier to extend
- Easier to test

---

## 🧠 Main Orchestration Logic

All calculations are coordinated by a central function:

**run_tco_scenario()**

This function:
1. Reads the scenario inputs
2. Runs the CAPEX calculation
3. Runs the Residual Value calculation
4. Runs the appropriate OPEX calculation (truck or ship)
5. Aggregates all components into a final TCO result

The orchestration logic is interface-agnostic and can be used from:
- Command-line scripts
- Jupyter notebooks
- Web dashboards
- APIs
- Decision-support tools

---

## 📥 Inputs

The model requires a single structured input defining the scenario, including:
- Asset type (truck or ship)
- Powertrain technology
- Country of operation
- Operational lifetime
- Discount rate
- Technical and operational assumptions

No internal code changes are required to run new scenarios.

---

## 📤 Outputs

The calculator returns a structured, JSON-serializable output containing:
- CAPEX breakdown
- Annual OPEX
- Residual Value
- Discounted cash flows
- Total TCO (present value)
- Equivalent annual cost
- Cost per distance unit

Outputs are ready to be visualized, compared, or integrated into other systems.

---

## 🧪 How to Run the Project (Beginner Friendly)

### Step 1 – Install Python

Python 3.9 or newer is required.

Check your version:

into the console (run as administrator Windows Powershell)

python --version


---

### Step 2 – Clone the Repository

git clone https://github.com/Mart1f/TCO_Calculator.git

---

cd TCO_Calculator\


---

### Step 3 – Install Dependencies

pip install -r requirements.txt


---

---

## Step 4 - Dashboard – How to Visualize the Results

In addition to running the calculations from Python, the project includes a **simple interactive dashboard** that allows users to **visualize and explore TCO results** without modifying the code.

The dashboard is intended for:
- Non-technical users
- Scenario comparison
- Result inspection and validation


Before running the dashboard, make sure the following Python packages are installed:

pip install streamlit pandas matplotlib


If you already installed the project dependencies using `requirements.txt`, these packages may already be included.

---

### ▶️ How to Launch the Dashboard

From the root folder of the project, run:

streamlit run dashboard/app.py


(Replace `dashboard/app.py` with the correct path if your dashboard file is located elsewhere.)

After running the command:
- A local web server will start automatically
- Your browser will open at:

http://localhost:8501


---

### 🖥️ What the Dashboard Shows

The dashboard allows you to:
- Load or select predefined TCO scenarios
- View CAPEX, OPEX, and Residual Value breakdowns
- Compare different technologies (e.g. DIESEL vs BEV)
- Inspect total TCO and equivalent annual cost
- Analyze cost per distance unit

All values shown in the dashboard are generated by the same calculation engine used in the Python scripts.


### 🛑 Troubleshooting

If the dashboard does not open:
- Make sure `streamlit` is installed
- Check that you are in the project root folder
- Verify the dashboard file path
- Ensure port `8501` is not blocked

You can stop the dashboard at any time by pressing:

CTRL + C (in the terminal)

## 📊 Typical Use Cases

- Comparing diesel vs electric trucks
- Evaluating ship electrification scenarios
- Supporting fleet investment decisions
- Long-term cost and sustainability analysis
- Feeding results into digital twins or simulations
- Academic or educational cost modeling

---

## 🧱 Design Philosophy

- Modular: each cost block is independent
- Transparent: calculations are explicit and traceable
- Extensible: easy to add new technologies or countries
- Robust: defensive programming to avoid crashes
- Research-friendly: formulas preserved, inputs adjustable

---

## 📌 Final Note

This project is a **decision-support tool**, not a forecasting oracle.

Results depend on:
- Input assumptions
- Quality of cost data
- Scenario definition

The real value of the model lies in **comparing scenarios consistently**, not in predicting exact future costs.




