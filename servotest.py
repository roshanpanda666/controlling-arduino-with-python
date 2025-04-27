import time
from pyfirmata import Arduino, util

# Replace 'COM3' with your Arduino's port (e.g., '/dev/ttyACM0' for Linux)
board = Arduino('COM8')

# Use pin 9 for servo control
servo_pin = board.get_pin('d:10:s')  # d = digital, 9 = pin number, s = servo

# Move the servo from 0° to 180° and back
try:
    while True:
        for angle in range(0, 181, 10):  # Move from 0° to 180°
            servo_pin.write(angle)
            time.sleep(0.05)

        for angle in range(180, -1, -10):  # Move from 180° to 0°
            servo_pin.write(angle)
            time.sleep(0.05)

except KeyboardInterrupt:
    print("Stopped by user")
    board.exit()
