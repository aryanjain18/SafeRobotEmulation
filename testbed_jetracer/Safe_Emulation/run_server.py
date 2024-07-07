import keyboard
import socket

# Define the IP address and port of the JetRacer
JETRACER_IP = '10.10.10.108'  # Replace with your JetRacer's IP address
JETRACER_PORT = 3078       # You can choose any port number

def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((JETRACER_IP, JETRACER_PORT))
        s.sendall(command.encode())

def on_press(event):
    if event.name == 'up':
        print("up")
        send_command('forward')
    elif event.name == 'down':
        send_command('backward')
    elif event.name == 'left':
        send_command('left')
    elif event.name == 'right':
        send_command('right')

keyboard.on_press(on_press)
print("Use the arrow keys to control the JetRacer. Press 'esc' to quit.")

keyboard.wait('esc')
