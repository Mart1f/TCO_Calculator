from flask import Flask, render_template, request, redirect, url_for

from main_tco import run_tco_scenario
from inputs.gen_truck_in import make_example_truck_electric_fleet, make_example_truck_diesel
from inputs.gen_ship_in import make_example_ship_electric, make_example_ship_diesel

app = Flask(__name__)

SCENARIOS = {
    "truck_electric": make_example_truck_electric_fleet,
    "truck_diesel": make_example_truck_diesel,
    "ship_electric": make_example_ship_electric,
    "ship_diesel": make_example_ship_diesel,
}


@app.get("/")
def home():
    return redirect(url_for("dashboard", scenario="ship_diesel"))


@app.get("/dashboard")
def dashboard():
    scenario = request.args.get("scenario", "ship_diesel")
    if scenario not in SCENARIOS:
        scenario = "ship_diesel"

    user_inputs = SCENARIOS[scenario]()
    results = run_tco_scenario(user_inputs, verbose=False)

    return render_template(
        "dashboard.html",
        scenario=scenario,
        scenarios=list(SCENARIOS.keys()),
        results=results
    )


if __name__ == "__main__":
    print("Starting Flask on http://127.0.0.1:8000/dashboard")
    app.run(host="127.0.0.1", port=8000, debug=True)
