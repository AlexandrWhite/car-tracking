import supervision as sv 
import pandas as pd
import datetime

class LineObserver:
    columns=["date","from","to","class"]

    def __init__(self,delta_time):
        self.lines = dict() #хрним каждую линию и её ID
        self.target_objects = dict()
        self.row_list = []
        self.date_table = pd.DataFrame()
        self.id = 0 

        self.row_list_size = 0
        self.target_objects_size = 0 
        self.delta_time = delta_time


    def add_line(self, line:sv.LineZone):
        self.id += 1
        self.lines[self.id] = line
    
    def upd_directions(self,obj_id):
        # Если линий две то делаем запись в таблицу
        if len(self.target_objects[obj_id]['lines'])==2:
            line_id1, line_id2 = self.target_objects[obj_id]['lines'][0], self.target_objects[obj_id]['lines'][1]
           
            class_id = self.target_objects[obj_id]['class_id']
            class_to_str = {2:'car',3:'motorcycle',5:'bus',7:'truck'}
            class_name = class_to_str[class_id]

            values = (datetime.datetime.now()-self.delta_time, line_id1, line_id2, class_name)
            self.row_list.append(dict(zip(LineObserver.columns, values)))
            self.row_list_size += 1

    def update(self, detections:sv.Detections):
        # Добавляем к объекту номер линии которую он пересек
        for lz_id, lz in self.lines.items():
            crossed_in, crossed_out = lz.trigger(detections)

            for direction in (crossed_in,crossed_out):
                try:
                    objects_id = detections[direction].tracker_id
                    classes_id = detections[direction].class_id
                except:
                    continue
                for obj_id, class_id in zip(objects_id, classes_id):
                    if obj_id not in self.target_objects.keys():
                        self.target_objects[obj_id] = {'lines':[lz_id], 'class_id':class_id}
                        self.target_objects_size += 1
                    else:
                        self.target_objects[obj_id]['lines'].append(lz_id)
                    self.upd_directions(obj_id)

    def update_table(self):
        self.date_table = pd.DataFrame(self.row_list, columns=LineObserver.columns)