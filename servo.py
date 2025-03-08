import pyfirmata
from pynput.mouse import Listener
import time

# Arduino setup
ARDUINO_PORT = 'COM8'  # Replace with your Arduino's port
SERVO_PIN = 10  # Pin where the servo motor is connected

# Initialize Arduino board
board = pyfirmata.Arduino(ARDUINO_PORT)
servo = board.get_pin(f'd:{SERVO_PIN}:s')  # Set servo pin as PWM (servo)

# Function to move the servo
def move_servo(angle):
    servo.write(angle)
    print(f"Servo moved to {angle} degrees")

# Function to handle mouse click events
def on_click(x, y, button, pressed):
    if pressed:  # Only trigger on mouse button press (not release)
        print(f"Mouse clicked at ({x}, {y})")
        move_servo(90)  # Move servo to 90 degrees
        time.sleep(1)  # Wait for 1 second
        move_servo(0)  # Move servo back to 0 degrees

# Start listening for mouse clicks
print("Listening for mouse clicks... Press Ctrl+C to exit.")
with Listener(on_click=on_click) as listener:
    try:
        listener.join()  # Keep the script running
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Reset servo to 0 degrees and close the Arduino connection
        move_servo(0)
        board.exit()