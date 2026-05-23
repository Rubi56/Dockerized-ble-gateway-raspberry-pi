# VREL BLE Gateway

This project implements a Dockerized Bluetooth Low Energy (BLE) gateway for the IoT VREL NextGen laboratory environment.

The application is designed to run on a Raspberry Pi with Docker. It performs BLE advertising and BLE scanning at the same time, and presents the captured BLE advertisement data on a web-based frontend.

## Main Functions

The gateway performs the following functions:

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

The advertised BLE gateway name is configured in `docker-compose.yml`:

```yaml
environment:
  - GATEWAY_NAME=VREL_BLE_Gateway
