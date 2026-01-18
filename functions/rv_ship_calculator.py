import os
import json
import math
from cosapp.base import System
from models.vehicle_port import VehiclePropertiesPort
from models.country_port import CountryPropertiesPort

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENERGY_ALIASES = {
    "fcet": "FCET",
    "fcev": "FCET",
    "hice": "HICE",
    "hev": "HEV",
    "bev": "BEV",
    "biodiesel": "BIODIESEL",
    "bio_diesel": "BIODIESEL",
    "e_diesel": "E_DIESEL",
    "ediesel": "E_DIESEL",
    "hvo": "HVO",
    "lng": "LNG",
    "diesel": "DIESEL",
}

def norm_energy(x: str) -> str:
    if not x:
        return "DIESEL"
    s = str(x).strip()
    low = s.lower()
    if low in ENERGY_ALIASES:
        return ENERGY_ALIASES[low]
    return s.upper()

class ResidualValueShipCalculator(System):
    def setup(self, ship_class: str = "ro_pax_medium", db_path: str = None):
        if db_path is None:
            db_folder = os.path.abspath(os.path.join(BASE_DIR, "..", "database"))
            db_path = os.path.join(db_folder, "db_ships.json")

        with open(db_path, "r") as f:
            db = json.load(f)

        object.__setattr__(self, "_countries", {c["country"]: c for c in db.get("countries", [])})
        object.__setattr__(self, "_ship_class", str(ship_class))

        self.add_input(VehiclePropertiesPort, "in_vehicle_properties")
        self.add_input(CountryPropertiesPort, "in_country_properties")

        self.add_outward("rv", 0.0)
        self.add_outward("depreciated_value", 0.0)
        self.add_outward("health_factor", 1.0)
        self.add_outward("external_factor", 1.0)

        self.add_outward("dep_year_component", 0.0)
        self.add_outward("dep_use_component", 0.0)
        self.add_outward("dep_maint_component", 0.0)

    def compute(self):
        vp = self.in_vehicle_properties
        country = str(vp.registration_country)
        e = norm_energy(getattr(vp, "type_energy", "DIESEL"))

        if country not in self._countries:
            raise KeyError(f"Country '{country}' not found in db_ships.json")

        c = self._countries[country]

        if "rv_ship" not in c:
            raise KeyError(f"Missing 'rv_ship' in db_ships.json for country '{country}'")

        if self._ship_class not in c["rv_ship"]:
            raise KeyError(f"Missing rv_ship['{self._ship_class}'] for country '{country}'")

        p = c["rv_ship"][self._ship_class]

        purchase = float(getattr(vp, "purchase_cost", 0.0))
        if purchase <= 0:
            self.rv = 0.0
            self.depreciated_value = 0.0
            self.health_factor = 1.0
            self.external_factor = 1.0
            return

        age = int(getattr(vp, "current_year", 0) - getattr(vp, "year_purchase", 0))
        age = max(0, age)

        usage = float(getattr(vp, "travel_measure", 0.0))
        maint = float(getattr(vp, "maintenance_cost", 0.0))
        maint_ratio = (maint / purchase) if purchase > 0 else 0.0

        r_year = float(p["depr_rate_per_year"].get(e, p["depr_rate_per_year"].get("DEFAULT", 0.06)))
        r_use = float(p["depr_rate_per_unit"].get(e, p["depr_rate_per_unit"].get("DEFAULT", 0.0)))
        k_maint = float(p.get("maint_penalty_coef", 2.0))
        floor_frac = float(p.get("min_floor_fraction", 0.10))
        cap_frac = float(p.get("max_total_depr_fraction", 0.85))
        min_health = float(p.get("min_health_factor", 0.35))

        dep_year = purchase * r_year * age
        dep_use = purchase * r_use * usage
        dep_maint = purchase * 0.0

        self.dep_year_component = dep_year
        self.dep_use_component = dep_use
        self.dep_maint_component = dep_maint

        dep_total = dep_year + dep_use + dep_maint
        dep_total = min(dep_total, purchase * cap_frac)

        floor_value = purchase * floor_frac
        self.depreciated_value = max(floor_value, purchase - dep_total)

        ob_rate = float(p["obsolescence_rate"].get(e, p["obsolescence_rate"].get("DEFAULT", 0.02)))
        health = math.exp(-ob_rate * age) * math.exp(-k_maint * maint_ratio)
        self.health_factor = min(1.0, max(min_health, health))

        ef = c.get("external_factors_ship", None)
        if ef is None:
            ef = {
                "energy_growth_rate": 0.04,
                "energy_price_factor": {},
                "co2_factor": {},
                "subsidy_factor": 0.30,
                "min_external_factor": 0.85,
                "max_external_factor": 1.15
            }

        growth = float(ef.get("energy_growth_rate", 0.04))
        energy_factor = float(ef.get("energy_price_factor", {}).get(e, 0.0))
        co2_factor = float(ef.get("co2_factor", {}).get(e, 0.0))
        subsidy_factor = float(ef.get("subsidy_factor", 0.30))
        min_ext = float(ef.get("min_external_factor", 0.85))
        max_ext = float(ef.get("max_external_factor", 1.15))

        P_ref = float(c.get("energy", {}).get("energy_price_c_e", {}).get(e, 0.0))
        if P_ref > 0:
            P_t = P_ref * ((1.0 + growth) ** age)
            delta = (P_t - P_ref) / P_ref
        else:
            delta = 0.0

        subsidy_eur = 0.0
        try:
            subsidy_eur = float(c["subsidies"]["2025"]["medium"]["vehicle_subsidies"].get(e, 0.0))
        except Exception:
            subsidy_eur = 0.0

        incentive = (subsidy_eur / purchase) if purchase > 0 else 0.0

        ext = 1.0 + energy_factor * delta + co2_factor + subsidy_factor * incentive
        self.external_factor = min(max_ext, max(min_ext, ext))

        self.rv = self.depreciated_value * self.health_factor * self.external_factor
