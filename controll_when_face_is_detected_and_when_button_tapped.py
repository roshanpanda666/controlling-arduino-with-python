from pymongo import MongoClient
import pyfirmata
import time
from threading import Thread
import cv2
import winsound

# Load Haar cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# MongoDB connection details
connection_string = "mongodb+srv://roshan:roshanpwd@cluster0.uf1x9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Arduino setup
ARDUINO_PORT = 'COM8'  # Replace with your Arduino's port
LED_PIN = 13  # Pin where the LED is connected
SERVO_PIN = 10  # Pin where the servo motor is connected

# Initialize Arduino board
board = pyfirmata.Arduino(ARDUINO_PORT)
led = board.get_pin(f'd:{LED_PIN}:o')  # Set LED pin as output
servo = board.get_pin(f'd:{SERVO_PIN}:s')  # Set servo pin as PWM (servo)

# Flag to ensure the servo only moves once when a face is detected
servo_triggered = False

# Function to control the LED and servo once (non-blocking)
def control_led_and_servo_once():
    led.write(1)
    servo.write(90)  # Move servo to 90 degrees
    time.sleep(1)
    servo.write(0)   # Move servo back to 0 degrees
    time.sleep(1)
    led.write(0)

# Face detection function
def detect(gray, frame):
    global servo_triggered

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0 and not servo_triggered:
        servo_triggered = True
        winsound.Beep(2000, 200)
        Thread(target=control_led_and_servo_once, daemon=True).start()

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return frame

# Function to monitor MongoDB changes
def monitor_changes(db):
    with db.watch() as change_stream:
        print("Monitoring changes in the database...")
        for change in change_stream:
            print("\nChange detected in the database!")
            print("Change details:", change)

            # Trigger the servo and LED when new data is detected
            control_led_and_servo_once()

# Function to fetch data periodically from MongoDB
def fetch_data_periodically(db):
    while True:
        print("\nFetching data from the database...")

        collections = db.list_collection_names()

        for collection_name in collections:
            print(f"\nFetching data from collection: {collection_name}")
            collection = db[collection_name]
            documents = collection.find()

            if collection.count_documents({}) == 0:
                print(f"The collection '{collection_name}' is empty.")
            else:
                for document in documents:
                    print("Document:", document)

        time.sleep(5)  # Wait 5 seconds before fetching data again

try:
    # Create a MongoClient object
    client = MongoClient(connection_string)

    # Access the 'test' database
    db = client.test
    print("Connected to database:", db.name)  # Debug: Confirm database name

    # Start monitoring changes in a separate thread
    Thread(target=monitor_changes, args=(db,), daemon=True).start()

    # Start periodic data fetching in the main thread
    Thread(target=fetch_data_periodically, args=(db,), daemon=True).start()

    # Start video capture for face detection
    video_capture = cv2.VideoCapture(1)  # Use 0 if 1 doesn't work

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture frame")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        canvas = detect(gray, frame)
        cv2.imshow('Face Detection', canvas)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Error: {e}")

finally:
    # Release resources and close connections
    video_capture.release()
    cv2.destroyAllWindows()
    board.exit()
    client.close()
    print("Resources released.")
