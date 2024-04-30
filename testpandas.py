import pandas as pd 
import datetime 

columns=["date","from","to","class"]


row_list = []
values = (datetime.datetime.now(), 3,2,"car")
row_list.append(dict(zip(columns,values)))

df = pd.DataFrame(row_list, columns=columns)
print(df)