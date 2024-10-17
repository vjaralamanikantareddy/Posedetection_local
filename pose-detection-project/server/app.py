from flask import Flask, request, Response
import cv2
import numpy as np
import mediapipe as mp

app = Flask(__name__)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

@app.route('/process_frame', methods=['POST'])
def process_frame():
    file_bytes = np.frombuffer(request.data, np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    # Pose detection
    with mp_pose.Pose(static_image_mode=False) as pose:
        results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    # Encode the frame and send it back (optional)
    _, img_encoded = cv2.imencode('.jpg', img)
    return Response(img_encoded.tobytes(), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
