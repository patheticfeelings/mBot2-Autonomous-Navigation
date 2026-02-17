import socket, json, math, threading, tkinter as tk
from queue import Queue

# Server Configuration
HOST = "0.0.0.0" 
PORT = 5000
CELL_SIZE = 20
WIDTH, HEIGHT = 600, 600

class RobotServer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("mBot2 Telemetry & Mapping Server")
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="#ffffff")
        self.canvas.pack()
        
        self.queue = Queue()
        self.x, self.y = WIDTH//2, HEIGHT//2
        self.angle = 90 # Facing North
        
        self.draw_grid()
        self.robot_marker = self.canvas.create_oval(self.x-10, self.y-10, self.x+10, self.y+10, fill="red")
        
    def draw_grid(self):
        for i in range(0, WIDTH, CELL_SIZE):
            self.canvas.create_line(i, 0, i, HEIGHT, fill="#f0f0f0")
            self.canvas.create_line(0, i, WIDTH, i, fill="#f0f0f0")

    def process_data(self):
        while not self.queue.empty():
            data = self.queue.get()
            action = data.get('action')
            dist = data.get('distance', 0)
            
            if action == 'forward':
                # Scale: 1cm = 2 pixels
                step = 2 
                dx = step * math.cos(math.radians(self.angle))
                dy = -step * math.sin(math.radians(self.angle))
                
                new_x, new_y = self.x + dx, self.y + dy
                self.canvas.create_line(self.x, self.y, new_x, new_y, fill="blue", width=2)
                self.x, self.y = new_x, new_y
                
            elif action == 'stop':
                self.canvas.create_oval(self.x-3, self.y-3, self.x+3, self.y+3, fill="orange")
                
            self.canvas.coords(self.robot_marker, self.x-10, self.y-10, self.x+10, self.y+10)
            
        self.root.after(100, self.process_data)

    def start_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Server listening on port {PORT}...")
        
        conn, addr = s.accept()
        print(f"Connected by: {addr}")
        
        buffer = ""
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data: break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.queue.put(json.loads(line))
            except:
                break
        conn.close()

    def run(self):
        threading.Thread(target=self.start_socket, daemon=True).start()
        self.process_data()
        self.root.mainloop()

if __name__ == "__main__":
    app = RobotServer()
    app.run()