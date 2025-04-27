import cv2
import winsound
# Loading the cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


#step 2 detecting 
def detect(gray, frame):
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #step 3 drawing the rectangle
    for (x, y, w, h) in faces:
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        if rectangle.any() == True:
            winsound.Beep(5000, 200)
    
    return frame


# showing the camera
video_capture = cv2.VideoCapture(1)  # Change the index to 1 for cam1
while True:
    _, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canvas = detect(gray, frame)
    cv2.imshow('Video', canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()