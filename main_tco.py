from cosapp.drivers import RunOnce

from functions.Opex_Calculator import TruckOPEXCalculator, ShipOPEXCalculator
from functions.rv_calculator import ResidualValueCalculator
from functions.capex_calculator import VehicleCAPEXCalculator


def run_capex(capex_inputs: dict, asset_type: str, verbose: bool = False) -> dict:
    capex_data = capex_inputs.get("capex", {})
    sys_capex = VehicleCAPEXCalculator("capex_global", vehicle_type=asset_type)

    # MAIN INPUTS
    sys_capex.in_vehicle_properties.type_vehicle = capex_data.get("powertrain_type", "DIESEL")
    sys_capex.in_vehicle_properties.type_energy = capex_data.get("powertrain_type", "DIESEL")
    sys_capex.in_vehicle_properties.vehicle_number = capex_data.get("vehicle_number", 1)
    sys_capex.in_vehicle_properties.vehicle_id = capex_data.get("vehicle_id", 1)
    sys_capex.in_vehicle_properties.vehicle_weight_class = capex_data.get("vehicle_weight_class", "light")
    sys_capex.in_vehicle_properties.registration_country = capex_data.get("country", "France")
    sys_capex.in_vehicle_properties.year = capex_data.get("year", 2025)

    # ACQUISITION
    sys_capex.in_vehicle_properties.is_new = capex_data.get("is_new", True)
    sys_capex.in_vehicle_properties.owns_vehicle = capex_data.get("owns_vehicle", False)
    sys_capex.in_vehicle_properties.purchase_cost = capex_data.get("purchase_price", 0.0)
    sys_capex.in_vehicle_properties.conversion_cost = capex_data.get("conversion_cost", 0.0)
    sys_capex.in_vehicle_properties.certification_cost = capex_data.get("certification_cost", 0.0)
    sys_capex.in_vehicle_properties.vehicle_dict = capex_data.get("vehicle_dict", {})

    # INFRA
    sys_capex.in_vehicle_properties.n_slow = capex_data.get("n_slow")
    sys_capex.in_vehicle_properties.n_fast = capex_data.get("n_fast")
    sys_capex.in_vehicle_properties.n_ultra = capex_data.get("n_ultra")
    sys_capex.in_vehicle_properties.n_stations = capex_data.get("n_stations", 0)
    sys_capex.in_vehicle_properties.smart_charging_enabled = capex_data.get("smart_charging_enabled", False)

    # FINANCING
    sys_capex.in_vehicle_properties.loan_years = capex_data.get("loan_years", 10)

    sys_capex.add_driver(RunOnce("run_capex"))
    sys_capex.run_drivers()

    return {
        "total": float(sys_capex.c_capex_total),
        "crf": float(sys_capex.c_crf),
        "vehicle_cost": float(sys_capex.c_vehicle_cost),
        "infrastructure_cost": float(sys_capex.c_infrastructure_cost),
        "infrastructure_hardware": float(sys_capex.c_infrastructure_hardware),
        "infrastructure_grid": float(sys_capex.c_infrastructure_grid),
        "infrastructure_installation": float(sys_capex.c_infrastructure_installation),
        "taxes": float(sys_capex.c_taxes),
        "financing_cost": float(sys_capex.c_financing_cost),
        "subsidies": float(sys_capex.c_subsidies),
        "meta": {
            "asset_type": asset_type,
            "powertrain": sys_capex.in_vehicle_properties.type_energy,
            "weight_class": sys_capex.in_vehicle_properties.vehicle_weight_class,
            "country": sys_capex.in_vehicle_properties.registration_country,
            "fleet_size": int(sys_capex.in_vehicle_properties.vehicle_number),
            "purchase_price": float(sys_capex.in_vehicle_properties.purchase_cost),
            "is_new": bool(sys_capex.in_vehicle_properties.is_new),
            "loan_years": int(sys_capex.in_vehicle_properties.loan_years),
        }
    }


def run_opex_truck(opex_inputs: dict, verbose: bool = False) -> dict:
    sys_opex = TruckOPEXCalculator("opex_truck")

    for key, value in opex_inputs.items():
        if hasattr(sys_opex, key):
            setattr(sys_opex, key, value)

    sys_opex.in_vehicle_properties.purchase_cost = float(opex_inputs.get("purchase_price", 0.0))

    sys_opex.add_driver(RunOnce("run_truck"))
    sys_opex.run_drivers()

    # Si tu TruckOPEXCalculator tiene más atributos de breakdown, agrégalos aquí
    out = {"opex_total": float(sys_opex.o_opex_total)}

    # Ejemplo: si existen, los incluimos sin romper nada
    for attr in ["o_taxes", "o_insurance", "o_maintenance", "o_energy", "o_tolls", "o_driver"]:
        if hasattr(sys_opex, attr):
            out[attr.replace("o_", "")] = float(getattr(sys_opex, attr))

    return out


def run_opex_ship(opex_inputs: dict, rv_value: float, verbose: bool = False) -> dict:
    sys_ship = ShipOPEXCalculator("ship_opex_case")
    vp = sys_ship.in_vehicle_properties
    cp = sys_ship.in_country_properties

    vp.purchase_cost = float(opex_inputs.get("purchase_price", 0.0))
    vp.GT = float(opex_inputs.get("GT", 0.0))
    vp.annual_energy_consumption_kWh = float(opex_inputs.get("consumption_energy", 0.0))
    vp.maintenance_cost_annual = float(opex_inputs.get("maintenance_cost", 0.0))
    vp.crew_count = float(opex_inputs.get("crew_count", 0.0))
    cp.crew_monthly_total = float(opex_inputs.get("crew_monthly_total", 0.0))
    vp.fuel_mass_kg = float(opex_inputs.get("fuel_mass_kg", 0.0))
    vp.days_in_port = float(opex_inputs.get("days_in_port_per_year", 0.0))

    vp.ship_class = str(opex_inputs.get("ship_class", "fishing_small"))
    vp.registration_country = str(opex_inputs.get("registration_country", "France"))
    vp.country_oper = str(opex_inputs.get("country_oper", vp.registration_country))
    vp.type_energy = str(opex_inputs.get("type_energy", "DIESEL"))

    # Inyecta RV (ya calculado afuera)
    sys_ship.in_residual_value = float(rv_value)

    sys_ship.add_driver(RunOnce("run_ship"))
    sys_ship.run_drivers()

    return {
        "opex_total": float(sys_ship.o_opex_total),
        "taxes": float(sys_ship.o_taxes),
        "ports": float(sys_ship.o_ports),
        "insurance": float(sys_ship.o_insurance),
        "crew": float(sys_ship.o_crew),
        "maintenance": float(sys_ship.o_maintenance),
        "energy": float(sys_ship.o_energy),
        "meta": {
            "ship_class": vp.ship_class,
            "country": vp.registration_country,
            "type_energy": vp.type_energy,
        }
    }


def run_rv(rv_inputs: dict, verbose: bool = False) -> dict:
    rv_sys = ResidualValueCalculator("rv_global", type_vehicle=rv_inputs["type_vehicle"])

    rv_sys.in_vehicle_properties.type_vehicle = rv_inputs["type_vehicle"]
    rv_sys.in_vehicle_properties.type_energy = rv_inputs["type_energy"]
    rv_sys.in_vehicle_properties.registration_country = rv_inputs["registration_country"]
    rv_sys.in_vehicle_properties.purchase_cost = rv_inputs["purchase_cost"]
    rv_sys.in_vehicle_properties.year_purchase = rv_inputs["year_purchase"]
    rv_sys.in_vehicle_properties.current_year = rv_inputs["current_year"]
    rv_sys.in_vehicle_properties.travel_measure = rv_inputs["travel_measure"]

    rv_sys.in_vehicle_properties.minimum_fuel_consumption = rv_inputs["minimum_fuel_consumption"]
    rv_sys.in_vehicle_properties.powertrain_model_year = rv_inputs["powertrain_model_year"]
    rv_sys.in_vehicle_properties.warranty = rv_inputs["warranty"]
    rv_sys.in_vehicle_properties.type_warranty = rv_inputs["type_warranty"]
    rv_sys.in_vehicle_properties.maintenance_cost = float(rv_inputs["maintenance_cost"])

    rv_sys.add_driver(RunOnce("run_rv"))
    rv_sys.run_drivers()

    return {
        "rv": float(rv_sys.rv),
        "total_depreciation": float(rv_sys.total_depreciation),
        "total_impact_health": float(rv_sys.total_impact_health),
        "total_external_factors": float(rv_sys.total_external_factors),
        "meta": {
            "type_vehicle": rv_inputs["type_vehicle"],
            "type_energy": rv_inputs["type_energy"],
            "registration_country": rv_inputs["registration_country"],
            "year_purchase": rv_inputs["year_purchase"],
            "current_year": rv_inputs["current_year"],
            "purchase_cost": float(rv_inputs["purchase_cost"]),
        }
    }



# ======================================================================
# GLOBAL FUNCTION: RUN_TCO_SCENARIO
# ======================================================================

def run_tco_scenario(user_inputs: dict, verbose: bool = False) -> dict:
    asset_type = user_inputs["asset_type"]

    # 1) CAPEX (dict)
    capex = run_capex(dict(user_inputs), asset_type, verbose=verbose)
    capex_total = float(capex["total"])
    crf = float(capex["crf"])

    # 2) RV (dict)
    rv = run_rv(user_inputs["rv"], verbose=verbose)
    rv_value = float(rv["rv"])

    # 3) OPEX (dict)
    if asset_type == "truck":
        opex = run_opex_truck(user_inputs["opex_truck"], verbose=verbose)
    elif asset_type == "ship":
        opex = run_opex_ship(user_inputs["opex_ship"], rv_value, verbose=verbose)
    else:
        raise ValueError(f"Unknown asset_type: {asset_type}")

    opex_annual = float(opex["opex_total"])

    # 4) Params
    N = int(user_inputs["operation_years"])
    interest_rate = float(user_inputs.get("discount_rate", 0.04))
    annual_distance = float(user_inputs.get("annual_distance_travel", 80000))

    # (fallback CRF if something weird happens)
    if crf == 0.0:
        if interest_rate == 0.0:
            crf = 1.0 / N
        else:
            r = interest_rate
            crf = (r * (1 + r) ** N) / (((1 + r) ** N) - 1)

    # 5) TCO
    rv_discounted = rv_value / ((1 + interest_rate) ** N)
    capex_component = (capex_total - rv_discounted) * crf

    opex_component = 0.0
    opex_pv_details = []
    for n in range(1, N + 1):
        pv = opex_annual / ((1 + interest_rate) ** n)
        opex_component += pv
        opex_pv_details.append({"year": n, "pv": float(pv)})

    tco_total = capex_component + opex_component

    tco_per_distance_unit = None
    if annual_distance > 0:
        tco_per_distance_unit = float(tco_total / (N * annual_distance))

    return {
        "meta": {
            "description": user_inputs.get("description", "No description"),
            "asset_type": asset_type,
            "powertrain_type": user_inputs.get("powertrain_type", ""),
            "country": user_inputs.get("country", ""),
            "operation_years": N,
            "discount_rate": interest_rate,
            "annual_distance_travel": annual_distance,
        },
        "inputs": user_inputs,   # útil para debug en dashboard
        "capex": capex,
        "rv": rv,
        "opex": opex,
        "tco": {
            "capex_total": float(capex_total),
            "rv_value": float(rv_value),
            "rv_discounted": float(rv_discounted),
            "crf": float(crf),
            "capex_component": float(capex_component),
            "opex_annual": float(opex_annual),
            "opex_component_pv": float(opex_component),
            "tco_total": float(tco_total),
            "equivalent_annual_cost": float(tco_total / N),
            "tco_per_distance_unit": tco_per_distance_unit,
            "opex_pv_details": opex_pv_details,
        }
    }


# ======================================================================
# MAIN
# ======================================================================

if __name__ == "__main__":
    print("\n" + "#"*80)
    print("#" + " "*78 + "#")
    print("#" + " "*20 + "TCO CALCULATION SYSTEM" + " "*37 + "#")
    print("#" + " "*78 + "#")
    print("#"*80)
    
    # Run single scenario - Choose one: "truck" or "ship"
    # Uncomment the scenario you want to run:
    
    # TRUCK SCENARIO
    scenario_inputs_truck_elec = make_example_truck_electric_fleet()
    scenario_inputs_truck_diesel = make_example_truck_diesel()
    scenario_inputs_ship_elec = make_example_ship_electric()
    scenario_inputs_ship_diesel = make_example_ship_diesel()
    
   
    # Run TCO calculation
    #results = run_tco_scenario(scenario_inputs_truck_elec)
    #results = run_tco_scenario(scenario_inputs_truck_diesel)
    #results = run_tco_scenario(scenario_inputs_ship_elec)       
    results = run_tco_scenario(scenario_inputs_ship_diesel)
    
    print("\n" + "#"*80)
    print("# TCO CALCULATION COMPLETED")
    print("#"*80)