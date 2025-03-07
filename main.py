from pymongo import MongoClient
import pyfirmata
import time
from threading import Thread

# Replace the connection string with your own
connection_string = "mongodb+srv://roshan:roshanpwd@cluster0.tskix.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Arduino setup
ARDUINO_PORT = 'COM8'  # Replace with your Arduino's port
LED_PIN = 13  # Pin where the LED is connected

# Initialize Arduino board
board = pyfirmata.Arduino(ARDUINO_PORT)
led = board.get_pin(f'd:{LED_PIN}:o')  # Set LED pin as output

# Function to control the LED
def control_led():
    # Rapid blinking for 3 seconds
    end_time = time.time() + 3
    while time.time() < end_time:
        led.write(1)  # Turn LED on
        time.sleep(0.1)  # Rapid blink
        led.write(0)  # Turn LED off
        time.sleep(0.1)

    # Slow blinking for 4 seconds
    end_time = time.time() + 4
    while time.time() < end_time:
        led.write(1)  # Turn LED on
        time.sleep(0.5)  # Slow blink
        led.write(0)  # Turn LED off
        time.sleep(0.5)

    # Turn LED off
    led.write(0)

# Function to monitor MongoDB changes
def monitor_changes(db):
    # Monitor all collections in the database
    with db.watch() as change_stream:
        print("Monitoring changes in the database...")
        for change in change_stream:
            print("\nChange detected in the database!")
            print("Change details:", change)

            # Invoke the LED control function
            control_led()

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