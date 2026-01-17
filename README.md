🚚🚢 TCO Calculator Project

This repository contains a Total Cost of Ownership (TCO) calculator designed to estimate the full lifecycle cost of transportation assets, with a focus on trucks and ships.

The tool allows you to compare different technologies (such as diesel vs. electric powertrains) by analyzing how costs evolve over time instead of looking only at the initial purchase price.

🎯 Purpose of the Project

The main goal of this project is to provide a clear and structured understanding of long-term costs by combining:

Capital Expenditures (CAPEX) – acquisition, infrastructure, financing, taxes

Operating Expenditures (OPEX) – energy, maintenance, insurance, crew, ports

Residual Value (RV) – remaining value at the end of the operational life

Discounting – time value of money over the operation period

By integrating all these components, the calculator highlights the real cost drivers of each scenario.

🧩 Architecture Overview

The system follows a modular architecture, where each cost component is calculated independently:

CAPEX module
Computes all upfront and investment-related costs and derives the Capital Recovery Factor (CRF).

OPEX modules
Dedicated calculators for trucks and ships, adapted to their specific cost structures.

Residual Value module
Estimates the remaining value of the asset based on depreciation, usage, technology, and external factors.

All modules are coordinated by a central orchestration function, which combines the results into a final TCO value.

⚙️ How It Works

A single structured input defines the scenario
(asset type, technology, country, lifetime, discount rate, etc.)

CAPEX, OPEX, and Residual Value are calculated separately

Costs are discounted over time

The final Total Cost of Ownership is computed

Results are returned as structured data, ready to be reused

📤 Inputs & Outputs
Inputs

Asset type (truck or ship)

Powertrain technology

Country of operation

Operational lifetime

Financial parameters (discount rate)

Detailed CAPEX, OPEX, and RV assumptions

Outputs

Total CAPEX

Annual OPEX

Residual Value

Discounted cash flows

Total TCO (present value)

Equivalent annual cost

All outputs are JSON-serializable, making them easy to visualize, store, or compare.

🧠 Design Philosophy

Modular – each cost block is independent

Transparent – detailed breakdowns are preserved

Extensible – easy to add new technologies or asset types

UI-ready – designed to work with dashboards or APIs

Engineering-oriented – suitable for technical and analytical use

📊 Typical Use Cases

Comparing diesel vs. electric trucks

Evaluating ship electrification scenarios

Supporting fleet investment decisions

Performing long-term cost and sustainability analysis

Feeding results into digital twins or decision tools
