# mBot2 Autonomous Navigation & Real-time Data Visualization

## Project Overview

This project demonstrates an advanced practical application of autonomous robotics using an **mBot2**, programmed in **Python**. The system integrates multiple sensors and network communication to enable the robot to navigate intelligently, interact with its environment, and send real-time telemetry data to a server. The server then graphically visualizes the robot's path through a GUI.

A key feature is its ability to operate in two distinct modes: **Self-Guided** (navigation and obstacle avoidance) and **Gripper** (object detection and manipulation), showcasing skills in low-level programming, network communication, and data processing.

## Key Features

- **Robot-Server Communication:** Uses TCP/IP sockets for bidirectional communication and data exchange in **JSON** format.
- **Dynamic Operating Modes:**
- **Self-Guided Mode:** Autonomous navigation with obstacle detection (ultrasonic sensor) and floor marking identification (color sensor). Logs and transmits navigation events.
- **Gripper Mode:** Object detection, manipulation using gripper servomotors, and precise deposition at specific locations (identified by color).

- **Real-time Data Acquisition:** Continuous collection of sensor data (light, sound, distance, color) for decision-making.
- **Graphical Visualization:** Python server using the **Tkinter** library to dynamically map the robot's movements and actions in real-time.
- **Hardware:** mBot2, CyberPi, Ultrasonic Sensors, Quad RGB Sensor, Gripper Module.
- **Software:** Python (mBuild, mbot2, socket, json, tkinter).

## How It Works

1. **Initialization:** The mBot2 establishes a Wi-Fi connection and connects to the TCP server.
2. **Mode Selection:** The user toggles between "Self-Guided" and "Gripper" modes using the robot's physical buttons.
3. **Execution:**

- In **Self-Guided** mode, the robot avoids obstacles and reacts to colors, sending its status and actions to the server.
- In **Gripper** mode, it detects an object, grabs it, and transports it to a green floor marking.

4. **Server-side:** Receives JSON data, processes coordinates, and updates the visual map of the path and events.

## Setup and Execution

### On mBot2 (File: `mbot2_client.py`)

1. **Wi-Fi Configuration:**

- Update `WIFI_SSID` and `WIFI_PASS` with your network credentials.
- Update `SERVER_HOST` with the IP address of the machine running the server.

2. **Upload:** Deploy `mbot2_client.py` to the mBot2 using the CyberPi interface.

### On Computer (File: `server_map_gui.py`)

1. **Dependencies:** Ensure Python is installed along with the `tkinter` library (standard in most Python distributions).
2. **Run:** Open a terminal in the project folder and execute:

```bash
python server_map_gui.py
```

The server will start and open a window, waiting for the mBot2 to connect.

## Challenges and Learning Outcomes

- **Wi-Fi Stability:** Required code adjustments and reconnection logic to ensure a robust link.
- **Gripper Calibration:** Precise control of servomotors required fine-tuning and iterative testing.
- **Robot-Server Synchronization:** The main challenge was matching physical movement with the graphical representation due to slight variations in movement precision and data frequency. This highlighted the importance of **state management** in distributed systems.

## Future Perspectives (Opportunities for Improvement)

- Implementation of a more robust communication protocol (e.g., **MQTT**) with authentication and encryption for better security.
- Integration of a more precise positioning system (e.g., visual odometry or IMU) to improve map accuracy.
- Addition of a remote control interface via the server for the gripper mode.
