TCO Calculator

Overview
This project implements a Total Cost of Ownership (TCO) calculation framework for trucks and ships. The goal is to evaluate and compare different vehicle technologies (such as diesel and electric) by estimating their total economic impact over the full operational lifecycle.

What is TCO?
Total Cost of Ownership represents the complete cost of owning and operating an asset over a given period of time. Instead of focusing only on the purchase price, the TCO approach combines capital costs, operating costs, and residual value, while accounting for the time value of money through discounting.

Project Structure
The project is organized into independent calculation modules, each responsible for a specific cost component.

CAPEX Calculation
The CAPEX module computes all capital-related costs associated with acquiring and deploying a vehicle. This includes vehicle purchase cost, conversion and certification costs, infrastructure investments, registration taxes, financing costs, and possible subsidies. The output includes the total CAPEX, the Capital Recovery Factor (CRF), and a detailed cost breakdown.

OPEX Calculation
Operating expenditures are computed using dedicated OPEX calculators for trucks and ships. These modules estimate annual operating costs such as energy or fuel consumption, maintenance, insurance, and, in the case of ships, crew and port-related costs. The result is an annual OPEX value, optionally accompanied by a detailed breakdown.

Residual Value Calculation
The residual value module estimates the remaining value of the asset at the end of its operational period. This calculation accounts for depreciation, technology type, country-specific effects, maintenance levels, usage intensity, and external or health-related impacts. The residual value is later discounted and reintegrated into the TCO calculation.

Main Orchestrator
The core of the system is the function run_tco_scenario(user_inputs). This function acts as the main orchestrator: it reads all scenario inputs, runs the CAPEX, OPEX, and residual value calculations, and then computes the final TCO by combining discounted capital and operating costs. The function returns structured results that can be reused by command-line scripts, web interfaces, or APIs.

Input and Output Design
All calculations are driven by a single structured input dictionary that describes the scenario (asset type, powertrain, country, operation period, discount rate, and detailed parameters for each module). The outputs are returned as JSON-serializable dictionaries, making them easy to visualize, store, and compare across scenarios.

Design Philosophy
The TCO calculator is designed to be modular, transparent, and extensible. Each cost component is calculated independently, detailed breakdowns are preserved, and the overall structure allows easy integration into larger digital twin or decision-support systems.

Typical Use Cases
Typical applications include comparing diesel versus electric trucks, evaluating ship electrification scenarios, supporting long-term fleet planning, and analyzing the economic impact of sustainable transport strategies.