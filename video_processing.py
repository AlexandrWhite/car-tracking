import cv2 
import base64
import supervision as sv
from ultralytics import YOLO
from lines_observer import LineObserver
from id_line_annotator import IdLineAnnotator
import torch

class VideoPlayer:
    def __init__(self, model='yolov8n.pt'):
        self.cap = cv2.VideoCapture()

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f'Using device: {device}')

        self.points = []

        self.model = YOLO(model).to(device)
        self.model.fuse()
        self.line_observer = LineObserver()


    def generate_frames(self):
        
        line_annotator = IdLineAnnotator(thickness=2, text_thickness=2, text_scale=1)
        tracker = sv.ByteTrack()

       

        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if not ret:
                frame = cv2.imencode('.jpg',self.default_frame)[1]
            else:
                for point in self.points:
                    frame = cv2.circle(frame, (point.x, point.y), radius=4, color=(0, 0, 255), thickness=-1)    

                results = self.model.track(source=frame,
                                        persist = True, 
                                        verbose=False,
                                        show=False,
                                        classes = [2,3,5,7], #car,motorcycle, bus, truck
                                        tracker='bytetrack.yaml')

                frame = results[0].plot()
                detections = sv.Detections.from_ultralytics(results[0])
                detections = tracker.update_with_detections(detections)

                self.line_observer.update(detections=detections)

                for line_id in self.line_observer.lines.keys():
                    frame = line_annotator.annotate(frame=frame, 
                            line_counter = self.line_observer.lines[line_id], id=line_id)


            compression_level = 10
            buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY, compression_level])[1]
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')    
 

    def run_new_video(self, path):
        self.cap = cv2.VideoCapture(path)
    
    def add_point(self,x,y,width,height):
        orig_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        orig_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        Sx = orig_width/width
        Sy = orig_height/height

        point = sv.Point(x,y)
        point.x = round(Sx * point.x)
        point.y = round(Sy * point.y)
        
        self.points.append(point)

        if len(self.points) == 2:
            lz = sv.LineZone(start=self.points[0], end=self.points[1])
            self.line_observer.add_line(lz)
            self.points.clear()
    
    def get_stat(self):
        return self.line_observer.info_table





    
    
