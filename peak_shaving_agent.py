import requests
import time
import base64
from requests.auth import HTTPBasicAuth

# OpenEMS REST API Configuration
OPENEMS_URL = "http://localhost:8084/rest/channel"
AUTH = HTTPBasicAuth('user', 'password') # Default read/write user if configured, else admin/admin

MAX_GRID_W = 80000 # 80 kW limit

def get_channel_value(component_id, channel_id):
    try:
        response = requests.get(f"{OPENEMS_URL}/{component_id}/{channel_id}", auth=AUTH, timeout=2)
        if response.status_code == 200:
            data = response.json()
            return data.get('value')
    except Exception as e:
        print(f"Error reading {component_id}/{channel_id}: {e}")
    return None

def set_channel_value(component_id, channel_id, value):
    try:
        payload = {"value": value}
        response = requests.post(f"{OPENEMS_URL}/{component_id}/{channel_id}", json=payload, auth=AUTH, timeout=2)
        if response.status_code == 200:
            print(f"Successfully set {component_id}/{channel_id} to {value}")
        else:
            print(f"Failed to set {component_id}/{channel_id}. Status: {response.status_code}")
    except Exception as e:
        print(f"Error setting {component_id}/{channel_id}: {e}")

def run_agent():
    print(f"Starting Peak Shaving Agent. Target Max Grid: {MAX_GRID_W} W")
    while True:
        # 1. Read Grid Power
        grid_w = get_channel_value("meter0", "ActivePower")

        # 2. Read ESS State of Charge
        soc = get_channel_value("ess0", "Soc")

        if grid_w is not None and soc is not None:
            print(f"Current Grid Power: {grid_w} W, ESS SoC: {soc} %")

            # 3. Calculate Target Power for ESS
            # Positive power means discharge (provide energy to the grid/loads)
            # Negative power means charge
            if grid_w > MAX_GRID_W:
                required_discharge_w = grid_w - MAX_GRID_W
                # Protect battery from over-discharging (simple logic)
                if soc > 10:
                    target_power = int(required_discharge_w)
                    print(f"Peak detected! Requesting ESS discharge of {target_power} W")
                else:
                    target_power = 0
                    print("Peak detected, but ESS SoC is too low! Cannot discharge.")
            else:
                # Normal operation, perhaps charge if low, but keep simple for now
                target_power = 0
                print("Grid power within limits.")

            # 4. Send command to OpenEMS
            # We configured the FixActivePower controller to be our target
            # However, directly writing to ess0/SetActivePowerEquals is the standard way for external controllers
            # Let's write to ess0/SetActivePowerEquals
            set_channel_value("ess0", "SetActivePowerEquals", target_power)

        else:
            print("Failed to read telemetry from OpenEMS. Retrying...")

        # Run loop every 5 seconds (simulating 1-second control loop with some buffer)
        time.sleep(5)

if __name__ == "__main__":
    run_agent()
