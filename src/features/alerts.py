import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "..", "config", "alert_config.json")

with open(config_path, "r") as f:
    alert_config = json.load(f)


def check_alerts(stats):
    alerts = []
    if stats["cpu_usage"] > alert_config["cpu_threshold"]:
        alerts.append("CPU alto!")
    if stats["cpu_temp"] and stats["cpu_temp"] > alert_config["temp_threshold"]:
        alerts.append("Temperatura alta!")
    if stats["ram_used"] / stats["ram_total"] * 100 > alert_config["ram_threshold"]:
        alerts.append("RAM alta!")
    return alerts if alerts else None
