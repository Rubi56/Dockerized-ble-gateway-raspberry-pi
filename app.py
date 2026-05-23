from flask import Flask, render_template, jsonify
import asyncio
import threading
import time
import os
import subprocess
import atexit
from bleak import BleakScanner

ADVERTISED_NAME = os.getenv("GATEWAY_NAME", "VREL_BLE_Gateway")

app = Flask(__name__)

devices_data = {}

gateway_status = {
    "scanner": "starting",
    "advertising": "starting",
    "advertised_name": ADVERTISED_NAME,
    "gateway_role": "BLE advertiser + BLE scanner",
    "web_server": "running",
    "detected_devices": 0
}

advertiser_process = None


def bluetoothctl_reader(process):
    try:
        for line in process.stdout:
            print("[bluetoothctl]", line.strip())

            if "Advertising object registered" in line:
                gateway_status["advertising"] = "running"

            if "Failed" in line or "failed" in line:
                gateway_status["advertising"] = "error"

    except Exception as error:
        print("Bluetoothctl reader error:", error)


def start_ble_advertising():
    global advertiser_process

    try:
        gateway_status["advertising"] = "starting"

        advertiser_process = subprocess.Popen(
            ["bluetoothctl"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        reader_thread = threading.Thread(
            target=bluetoothctl_reader,
            args=(advertiser_process,),
            daemon=True
        )
        reader_thread.start()

        commands = [
            "power on\n",
            "menu advertise\n",
            f"name {ADVERTISED_NAME}\n",
            "back\n",
            "advertise on\n"
        ]

        for command in commands:
            advertiser_process.stdin.write(command)
            advertiser_process.stdin.flush()
            time.sleep(0.7)

        gateway_status["advertising"] = "running"
        print(f"BLE advertising started as: {ADVERTISED_NAME}")

    except Exception as error:
        gateway_status["advertising"] = "error"
        print("BLE advertising error:", error)


def stop_ble_advertising():
    global advertiser_process

    try:
        if advertiser_process and advertiser_process.stdin:
            advertiser_process.stdin.write("advertise off\n")
            advertiser_process.stdin.write("exit\n")
            advertiser_process.stdin.flush()
            advertiser_process.terminate()
            print("BLE advertising stopped.")
    except Exception as error:
        print("Error while stopping advertising:", error)


def detection_callback(device, advertisement_data):
    devices_data[device.address] = {
        "name": device.name or "Unknown",
        "address": device.address,
        "rssi": advertisement_data.rssi,
        "last_seen": time.strftime("%Y-%m-%d %H:%M:%S"),
        "local_name": advertisement_data.local_name or "Unknown",
        "service_uuids": list(advertisement_data.service_uuids),
        "manufacturer_data": str(advertisement_data.manufacturer_data)
    }


async def scan_loop():
    try:
        gateway_status["scanner"] = "starting"

        scanner = BleakScanner(detection_callback)
        await scanner.start()

        gateway_status["scanner"] = "running"
        print("BLE scanner started.")

        while True:
            await asyncio.sleep(1)

    except Exception as error:
        gateway_status["scanner"] = "error"
        print("BLE scanner error:", error)


def start_scanner():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(scan_loop())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def api_status():
    gateway_status["detected_devices"] = len(devices_data)
    return jsonify(gateway_status)


@app.route("/api/devices")
def api_devices():
    return jsonify(list(devices_data.values()))


if __name__ == "__main__":
    atexit.register(stop_ble_advertising)

    advertising_thread = threading.Thread(
        target=start_ble_advertising,
        daemon=True
    )
    advertising_thread.start()

    scanner_thread = threading.Thread(
        target=start_scanner,
        daemon=True
    )
    scanner_thread.start()

    print("Web server started.")
    app.run(host="0.0.0.0", port=5000, debug=False)
