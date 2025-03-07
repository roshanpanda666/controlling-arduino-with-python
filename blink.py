from pyfirmata import Arduino, util
import time

# Define the port where your Arduino is connected
# On Windows, it might be something like 'COM3'
# On macOS or Linux, it might be something like '/dev/tty.usbmodem14101'
port = 'COM8'

# Create a new Arduino object
board = Arduino(port)

# Define the pin you want to control
led_pin = 13

# Blink the LED
try:
    while True:
        board.digital[led_pin].write(1)  # Turn the LED on
        time.sleep(1)                    # Wait for 1 second
        board.digital[led_pin].write(0)  # Turn the LED off
        time.sleep(1)                    # Wait for 1 second
except KeyboardInterrupt:
    # Exit the program when Ctrl+C is pressed
    board.exit()