import cv2 
import base64
import supervision as sv
from ultralytics import YOLO
import torch

class VideoPlayer:
    def __init__(self, model='yolov8n.pt'):
        self.cap = cv2.VideoCapture()
        self.on_pause = False 
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f'Using device: {device}')

        self.model = YOLO(model).to(device)
        self.model.fuse()

    def generate_frames(self):
        previous_frame = None

        if not self.cap.isOpened():
            frame = cv2.imread('flask_test/static/default_video.png')
            buffer = cv2.imencode('.jpg',frame)[1]
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')    

        while self.cap.isOpened():
            if self.on_pause:
                ret, frame = True, previous_frame
            else:
                ret, frame = self.cap.read()
                previous_frame = frame

            if not ret:
                frame = cv2.imencode('.jpg',self.default_frame)[1]
            else:
                results = self.model.predict(frame, verbose=False)
                frame = results[0].plot()
            
            compression_level = 30
            buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY, compression_level])[1]
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')    
 

    def run_new_video(self, path):
        self.cap = cv2.VideoCapture(path)
    
    def pause(self):
        if not self.on_pause:
            self.on_pause = True 
    
    def play(self):
        if self.on_pause:
            self.on_pause = False
    




    
    
