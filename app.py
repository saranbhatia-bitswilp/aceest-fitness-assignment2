from flask import Flask, jsonify, request

app = Flask(__name__)

PROGRAMS = {
    "fat-loss": 22,
    "muscle-gain": 35,
    "beginner": 26,
    "mobility": 20
}

@app.route("/")
def home():
    return jsonify(message="ACEest Fitness and Gym")

@app.route("/health")
def health():
    return jsonify(status="ok", service="aceest-fitness")

@app.route("/programs")
def programs():
    return jsonify(programs=list(PROGRAMS.keys()))

@app.route("/release")
def release():
    return jsonify(version="1.1.0", application="ACEest Fitness")

@app.route("/calculate-calories", methods=["POST"])
def calculate_calories():
    data = request.get_json(silent=True) or {}

    try:
        weight = float(data.get("weight_kg", 0))
    except (TypeError, ValueError):
        return jsonify(error="Invalid weight"), 400

    program = data.get("program")

    if weight <= 0 or program not in PROGRAMS:
        return jsonify(error="Invalid weight or program"), 400

    calories = int(weight * PROGRAMS[program])

    return jsonify(estimated_kcal=calories)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
