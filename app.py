from flask import Flask, render_template, jsonify
import json

from services.matching import (
    rank_farmers,
    create_smart_pool
)

from services.forecast import (
    forecast_demand
)

from services.matching import rank_farmers, create_smart_pool

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/farmer")
def farmer():
    return render_template("farmer.html")


@app.route("/buyer")
def buyer():
    return render_template("buyer.html")


@app.route("/matching")
def matching():
    return render_template("matching.html")


@app.route("/deal")
def deal():
    return render_template("deal.html")


@app.route("/logistics")
def logistics():
    return render_template("logistics.html")


def load_demo_data():

    with open("data/demo_data.json", "r") as file:
        return json.load(file)
@app.route("/api/matches")
def api_matches():

    data = load_demo_data()

    demand = data["buyer_demand"]
    farmers = data["farmers"]

    matches = rank_farmers(
        farmers,
        demand
    )

    return jsonify({
        "demand": demand,
        "matches": matches
    })


@app.route("/api/pool")
def api_pool():

    data = load_demo_data()

    demand = data["buyer_demand"]
    farmers = data["farmers"]

    pool = create_smart_pool(
        farmers,
        demand
    )
@app.route("/api/forecast")
def api_forecast():

    forecast = forecast_demand(
        days=7
    )

    return jsonify({
        "product": "Tomato",
        "location": "Delhi NCR",
        "forecast": forecast
    })

    return jsonify(pool)
if __name__ == "__main__":
    app.run(debug=True)