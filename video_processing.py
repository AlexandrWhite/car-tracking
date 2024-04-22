import cv2 
import base64
import supervision 
import ultralytics

class VideoPlayer:
    def __init__(self):
        self.cap = cv2.VideoCapture()
        self.on_pause = False 

    def generate_frames(self):
        previous_frame = None

        if not self.cap.isOpened():
            frame = cv2.imread('flask_test\\static\\default_video.png')
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
    




    
    
