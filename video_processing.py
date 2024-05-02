import cv2 
import base64
import supervision as sv
from ultralytics import YOLO
from lines_observer import LineObserver
from id_line_annotator import IdLineAnnotator
import torch
import re 
import datetime 
from pympler import muppy, summary


class VideoPlayer:
    def __init__(self,video_time, model='yolov8n.pt'):
        self.cap = cv2.VideoCapture()
        
        self.playlist = []
        self.playlist_cur = 0

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f'Using device: {device}')

        self.points = []
        
        self.cur_frame = 0

        self.model = YOLO(model).to(device)
        self.model.fuse()
        self.line_observer = LineObserver(delta_time = datetime.datetime.now() - video_time)


    def generate_frames(self):
        
        line_annotator = IdLineAnnotator(thickness=2, text_thickness=2, text_scale=1)
        tracker = sv.ByteTrack()

        if not self.cap.isOpened():
            return None    

        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if self.cur_frame%3000 == 0:
                all_objects = muppy.get_objects()
                sum1 = summary.summarize(all_objects)
                summary.print_(sum1)
            
            if ret and self.cur_frame % 1000 == 0:
                file_name = re.match(r'.+/(.*)\.mp4', self.playlist[self.playlist_cur-1]).group(1)
                self.line_observer.update_table()

                self.line_observer.target_objects.clear()
                self.line_observer.target_objects_size = 0

                self.line_observer.date_table.to_csv(f'/content/drive/MyDrive/may1csv/{file_name}.csv')

            if not ret:
                if self.playlist_cur > 0:
                   print("!!!!!!!!!!!!!!!!!!1!!!!!!!!!!"+self.playlist[self.playlist_cur-1])
                   file_name = re.match(r'.+/(.*)\.mp4', self.playlist[self.playlist_cur-1]).group(1)
                   self.line_observer.update_table()
                   self.line_observer.date_table.to_csv(f'/content/drive/MyDrive/may1csv/{file_name}.csv')
                if self.playlist_cur < len(self.playlist):
                    self.run_new_video()
                    continue
                else:
                    break
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


            compression_level = 50
            buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY, compression_level])[1]
            frame = buffer.tobytes()
            self.cur_frame += 1
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')    

    def run_new_video(self):
        if self.playlist_cur < len(self.playlist):
            self.cap = cv2.VideoCapture(self.playlist[self.playlist_cur])
            self.playlist_cur += 1
            self.cur_frame = 0
        
    
    def set_playlist(self,playlist):
        self.playlist = playlist
        self.playlist_cur = 0
        self.run_new_video()


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
    
    def add_line(self,x1,y1,x2,y2,width,height):
        self.add_point(x1,y1,width, height)
        self.add_point(x2,y2,width, height)

    def get_stat(self):
        return self.line_observer.date_table




    
    
