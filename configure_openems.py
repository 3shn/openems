import requests
import json
import time

url = "http://admin:admin@localhost:8080/system/console/configMgr"

def configure(pid, properties):
    # Form data for OSGi config manager
    data = {
        "apply": "true",
        "factoryPid": pid,
        "action": "ajaxConfigManager",
    }
    data.update(properties)

    print(f"Configuring {pid}...")
    try:
        response = requests.post(url, data=data)
        print(response.status_code)
    except Exception as e:
        print(f"Failed to configure {pid}: {e}")

configs = [
    {
        "pid": "io.openems.edge.simulator.datasource.csv.direct",
        "properties": {
            "id": "datasource0",
            "source": open("load_profile.csv").read(),
            "timeDelta": 1,
            "factor": 1,
            "propertylist": "id,source,timeDelta,factor"
        }
    },
    {
        "pid": "io.openems.edge.simulator.meter.grid.acting",
        "properties": {
            "id": "meter0",
            "datasource.id": "datasource0",
            "propertylist": "id,datasource.id"
        }
    },
    {
        "pid": "io.openems.edge.simulator.ess.symmetric.reacting",
        "properties": {
            "id": "ess0",
            "capacity": 100000,
            "maxApparentPower": 50000,
            "initialSoc": 50,
            "propertylist": "id,capacity,maxApparentPower,initialSoc"
        }
    },
    {
        "pid": "io.openems.edge.controller.api.rest.readwrite",
        "properties": {
            "id": "ctrlApiRest0",
            "port": 8084,
            "apiTimeout": 60,
            "propertylist": "id,port,apiTimeout"
        }
    },
    {
        "pid": "io.openems.edge.controller.ess.fixactivepower",
        "properties": {
            "id": "ctrlFixActivePower0",
            "ess_id": "ess0",
            "mode": "MANUAL_ON",
            "power": 0, # Initial
            "propertylist": "id,ess_id,mode,power"
        }
    }
]

# Write out to be run later if we decide to
if __name__ == "__main__":
    for c in configs:
        configure(c["pid"], c["properties"])
