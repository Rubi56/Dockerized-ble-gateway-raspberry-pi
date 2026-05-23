# VREL BLE Gateway

This project implements a Dockerized Bluetooth Low Energy (BLE) gateway for the IoT VREL NextGen laboratory environment.

The gateway runs on a Raspberry Pi with Docker. It advertises the Raspberry Pi as a BLE gateway, scans nearby BLE advertising frames, and displays captured BLE data on a web-based frontend.

## Main Functions

1. Advertises the Raspberry Pi as a BLE gateway device.
2. Scans nearby BLE advertising frames from SUT/VREL laboratory devices.
3. Displays gateway status and captured BLE advertisement data on a webpage.

## Implementation Range

The current implementation includes:

- BLE advertising using the configured gateway name.
- BLE scanning of nearby advertising devices.
- Web frontend for live monitoring.
- Display of detected BLE device information:
  - Device name
  - MAC address
  - RSSI
  - Last seen timestamp
  - Local name
  - Service UUIDs
  - Manufacturer data
- Docker Compose configuration for Raspberry Pi deployment.

The current version displays live BLE advertisement data. It does not yet decode project-specific sensor payloads from SUT/VREL devices because the final advertisement format, UUIDs, and manufacturer data structure must be confirmed in the laboratory environment.

## Configuration

The advertised BLE gateway name is configured in docker-compose.yml:

GATEWAY_NAME=VREL_BLE_Gateway

This name is visible in BLE scanner applications such as nRF Connect.

## Docker Configuration

The project uses a lightweight Python base image:

FROM python:3.12-slim

The container requires access to the host Raspberry Pi Bluetooth service. For this reason, docker-compose.yml uses:

- host networking
- privileged mode
- DBus socket mounts

The DBus mounts are required for communication with the host Bluetooth/BlueZ service.

## Persistence and Volumes

No persistent application data volume is required in the current implementation.

Captured BLE data is displayed live on the webpage and stored only in memory. When the container restarts, the detected device list is reset.

The DBus mounts in docker-compose.yml are not used for data persistence. They are required only for Bluetooth access from inside the container.

## Installation and Running

1. Clone the repository on Raspberry Pi:

git clone <repository-url>
cd <repository-folder>

2. Check Docker installation:

docker --version
docker compose version

If Docker is not installed:

sudo apt update
sudo apt install -y docker.io docker-compose-v2

3. Run the gateway:

sudo docker compose up --build

4. Open the webpage:

http://RASPBERRY_PI_IP:5000

Example:

http://10.42.0.205:5000

## Verification

The running system can be verified in two ways:

1. Open the webpage and confirm:
   - Advertising status is running
   - Scanner status is running
   - Detected BLE devices are displayed

2. Open nRF Connect on a phone and confirm that the advertised gateway name appears:

VREL_BLE_Gateway

## Laboratory Deployment Notes

The Raspberry Pi must be physically close to the SUT/VREL BLE devices in order to capture their BLE advertisements.

The same containerized implementation was tested on Raspberry Pi 4. Final validation should be performed on the laboratory Raspberry Pi 5 with the target VREL/SUT devices.

## Contributors

- Rubi Thapa

## Supervisor / Project Context

This work is part of the AIH project for the IoT VREL NextGen laboratory ecosystem at Silesian University of Technology.
