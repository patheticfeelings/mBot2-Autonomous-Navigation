import mbuild, mbot2, event, time, cyberpi, socket, json

# --- Network Configuration ---
WIFI_SSID = "YOUR_WIFI_NAME"
WIFI_PASS = "YOUR_WIFI_PASSWORD"
SERVER_HOST = "192.168.1.XXX" # Your PC's IP Address
SERVER_PORT = 5000

# --- Global Variables ---
mode = 'autonomous' # Modes: 'autonomous' or 'gripper'
sock = None
steps = []

def init_socket():
    global sock
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_HOST, SERVER_PORT))
        sock.settimeout(0.1)
        cyberpi.console.println("Socket: Connected")
    except Exception as e:
        cyberpi.console.println("Socket Error: " + str(e))
        sock = None

def send_step_to_server(step_dict):
    global sock
    if sock is None:
        init_socket()
        if sock is None: return
    try:
        msg = json.dumps(step_dict) + "\n"
        sock.sendall(msg.encode("utf-8"))
    except:
        sock = None 

def connect_wifi():
    cyberpi.console.println("Connecting to WiFi...")
    try:
        cyberpi.wifi.connect(WIFI_SSID, WIFI_PASS)
        for _ in range(20):
            if cyberpi.wifi.is_connect():
                cyberpi.console.println("WiFi: Connected")
                return True
            time.sleep(0.5)
    except:
        pass
    return False

def get_distance_cm():
    # Odometry calculation based on motor angles
    angl = mbot2.EM_get_angle('em1')
    return round(((angl / 360) * (6.4 * 3.1415)), 2)

@event.start
def on_start():
    cyberpi.console.println("System Ready")
    if connect_wifi():
        init_socket()
    cyberpi.console.println('Press B to Start')

@event.is_press('a')
def switch_mode():
    global mode
    mode = 'gripper' if mode == 'autonomous' else 'autonomous'
    cyberpi.console.println('Mode: ' + mode)

@event.is_press('b')
def execute():
    mbot2.servo_set(90, 3) # Reset Gripper
    mbot2.servo_set(90, 4)
    
    while True:
        dist_sensor = mbuild.ultrasonic2.get(1)
        
        if mode == 'gripper':
            if dist_sensor <= 15:
                mbot2.drive_power(0, 0)
                # Gripper Logic
                for _ in range(20): mbot2.servo_add(1, 3); time.sleep(0.01)
                mbot2.straight(7, 20)
                for _ in range(60): mbot2.servo_add(1, 4); time.sleep(0.01)
                time.sleep(1)
                mbot2.turn(180)
                mbot2.forward(30)
                while not mbuild.quad_rgb_sensor.is_color("green", "any"):
                    pass
                mbot2.drive_power(0, 0)
                mbot2.servo_set(90, 4) # Release object
                break
        else:
            # Autonomous Mode
            if dist_sensor > 15:
                mbot2.forward(30)
                send_step_to_server({'action': 'forward', 'distance': get_distance_cm(), 'reason': 'normal_move'})
            else:
                mbot2.drive_power(0,0)
                send_step_to_server({'action': 'stop', 'distance': 0, 'reason': 'obstacle_detected'})
                mbot2.turn(90)
                mbot2.EM_reset_angle('em1')
            time.sleep(0.1)