import pandas as pd 
import datetime 
import re 

path = 'X:\\video_record\\old_comp\\test3.webm'
file_name = re.match(r'.+\\(.*)\.webm', path).group(1)
print("FILENAME: ", file_name)

columns=["date","from","to","class"]


row_list = []
values = (datetime.datetime.now(), 3,2,"car")
row_list.append(dict(zip(columns,values)))

df = pd.DataFrame(row_list, columns=columns)
print(df)