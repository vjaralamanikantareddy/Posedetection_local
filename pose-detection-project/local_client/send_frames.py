import cv2
import requests

url = "http://<your-render-server>/process_frame"  # Replace with your Render server URL

# Capture video from webcam
cap = cv2.VideoCapture(0)  

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    _, img_encoded = cv2.imencode('.jpg', frame)
    
    # Send frame to server
    response = requests.post(url, data=img_encoded.tobytes(), headers={'Content-Type': 'image/jpeg'})
    
    if response.status_code == 200:
        print("Frame sent successfully")
    else:
        print("Failed to send frame")

cap.release()
