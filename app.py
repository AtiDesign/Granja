from flask import Flask, jsonify, render_template, request
from arduino import Arduino
import pyfirmata

app = Flask(__name__)

arduino = Arduino(port="COM3")
it = pyfirmata.util.Iterator(arduino.board)
it.start()

state = {
    "automatic": True,
    "loteStart": None,
    "readings": {"temp": None, "hum": None, "nh3": None, "lux": None, "ts": None},
    "actuators": {"fan": False, "exh": False, "heat": False, "light": False},
    "thresholds": {"nh3Max": 25, "luxTarget": 30}
}

@app.route("/api/state")
def api_state():
    state["readings"] = {
        "temp": arduino.read_temp(),
        "hum": arduino.read_hum(),
        "nh3": arduino.read_nh3(),
        "lux": arduino.read_lux(),
        "ts": None
    }
    return jsonify(state)

@app.route("/api/mode", methods=["POST"])
def api_mode():
    data = request.get_json()
    state["automatic"] = bool(data.get("automatic", True))
    return jsonify({"automatic": state["automatic"]})

@app.route("/api/actuators", methods=["POST"])
def api_actuators():
    data = request.get_json()
    fan   = bool(data.get("fan"))
    exh   = bool(data.get("exh"))
    heat  = bool(data.get("heat"))
    light = bool(data.get("light"))

    arduino.set_fan(fan)
    arduino.set_exhaust(exh)
    arduino.set_heat(heat)
    arduino.set_light(light)

    state["actuators"] = {"fan": fan, "exh": exh, "heat": heat, "light": light}
    return jsonify(state["actuators"])

@app.route("/api/thresholds", methods=["POST"])
def api_thresholds():
    data = request.get_json()
    state["thresholds"]["nh3Max"] = data.get("nh3Max", 25)
    state["thresholds"]["luxTarget"] = data.get("luxTarget", 30)
    state["loteStart"] = data.get("loteStart", None)
    return jsonify(state["thresholds"])

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
