import pandas as pd 
df = pd.DataFrame({'Slonik':[0], 'Mishka':[0], 'Tigra':[0]})
df['Slonik'] += 1
df['Zayac'] = [0]
print(df)


df = pd.DataFrame({'Slonik':{'weight':0, 'power':0}, 
                   'Mishka':{'weight':0, 'power':0}, 
                   'Tigra':{'weight':0, 'power':0}})
if 'Zayac' not in df.columns:
    df['Zayac'] = {'weight':0, 'power':0}
print(df)