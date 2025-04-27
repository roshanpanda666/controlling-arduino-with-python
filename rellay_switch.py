import pyfirmata
import time

# Connect to Arduino (change the port accordingly)
board = pyfirmata.Arduino('COM8')  # Example: 'COM3' for Windows, '/dev/ttyUSB0' for Linux

# Define the relay pin
relay_pin = board.get_pin('d:8:o')  # d = digital, 7 = pin number, o = output

# Blink the relay ON and OFF
while True:
    relay_pin.write(1)  # Relay ON
    print("Relay ON 🔥")
    time.sleep(1)       # Wait 1 second

    relay_pin.write(0)  # Relay OFF
    print("Relay OFF 💤")
    time.sleep(1)       # Wait 1 second
