from pymongo import MongoClient
import pyfirmata
import time
from threading import Thread

# Replace the connection string with your own
connection_string = "mongodb+srv://roshan:roshanpwd@cluster0.uf1x9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Arduino setup
ARDUINO_PORT = 'COM8'  # Replace with your Arduino's port
LED_PIN = 13  # Pin where the LED is connected
SERVO_PIN = 10  # Pin where the servo motor is connected

# Initialize Arduino board
board = pyfirmata.Arduino(ARDUINO_PORT)
led = board.get_pin(f'd:{LED_PIN}:o')  # Set LED pin as output
servo = board.get_pin(f'd:{SERVO_PIN}:s')  # Set servo pin as PWM (servo)

# Function to control the LED and servo (non-blocking)
def control_led_and_servo():
    def run_sequence():
        # Blink the LED and move the servo
        for _ in range(3):  # Blink LED 3 times
            led.write(1)  # Turn LED on
            time.sleep(0.2)  # LED on for 0.2 seconds
            led.write(0)  # Turn LED off
            time.sleep(0.2)  # LED off for 0.2 seconds

        # Move servo to 90 degrees
        servo.write(90)
        time.sleep(1)  # Wait for 1 second

        # Move servo back to 0 degrees
        servo.write(0)
        time.sleep(1)  # Wait for 1 second

    # Run the sequence in a separate thread to avoid blocking
    Thread(target=run_sequence, daemon=True).start()

# Function to monitor MongoDB changes
def monitor_changes(db):
    # Monitor all collections in the database
    with db.watch() as change_stream:
        print("Monitoring changes in the database...")
        for change in change_stream:
            print("\nChange detected in the database!")
            print("Change details:", change)

            # Invoke the LED and servo control function
            control_led_and_servo()

# Function to fetch data periodically
def fetch_data_periodically(db):
    while True:
        print("\nFetching data from the database...")

        # List all collections in the database
        collections = db.list_collection_names()

        # Fetch and display all documents from each collection
        for collection_name in collections:
            print(f"\nFetching data from collection: {collection_name}")

            # Access the collection
            collection = db[collection_name]

            # Fetch all documents from the collection
            documents = collection.find()

            # Check if the collection is empty
            if collection.count_documents({}) == 0:
                print(f"The collection '{collection_name}' is empty.")
            else:
                # Iterate over the documents and print them
                for document in documents:
                    print("Document:", document)

        # Wait for 5 seconds before fetching data again
        time.sleep(5)

try:
    # Create a MongoClient object
    client = MongoClient(connection_string)

    # Access the 'test' database
    db = client.test
    print("Connected to database:", db.name)  # Debug: Confirm database name

    # Start monitoring changes in a separate thread
    Thread(target=monitor_changes, args=(db,), daemon=True).start()

    # Start periodic data fetching in the main thread
    fetch_data_periodically(db)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the Arduino connection
    board.exit()
    # Close the MongoDB connection
    client.close()