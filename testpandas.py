import pandas as pd 
import datetime 
import re 

path = '/content/drive/MyDrive/video1may3/test1.mp4'
file_name = re.match(r'.+/(.*)\.mp4', path).group(1)
print("FILENAME: ", file_name)

columns=["date","from","to","class"]


row_list = []
values = (datetime.datetime.now(), 3,2,"car")
row_list.append(dict(zip(columns,values)))

df = pd.DataFrame(row_list, columns=columns)
print(df)