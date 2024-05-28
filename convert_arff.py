import csv
from scipy.io import arff

import pandas as pd



def convert(df, column_name, attribures_list):
    column = df[column_name]
    column_index = df.columns.tolist().index(column_name)
    df = df.drop(columns = [column_name])
    for i in range(len(attribures_list)):
        values = []
        attribute_value = attribures_list[i]
        for point in column:
            values.append(1) if point == attribute_value else values.append(0)
        df.insert(column_index + i, column_name + str(attribute_value), values)    
    return df
        
        

        
zoo, meta = arff.loadarff('zoo.arff')
df = pd.DataFrame(zoo)

df = convert(df, "LEGS", [0,1,2,3,4,5,6,7,8])
print(df.head());
df_mod = df.select_dtypes([object]).stack().str.decode('utf-8').unstack()
df["class"] = df_mod["class"]
df = df.astype(int)
print(df.head());
print(df.dtypes)



df.to_csv('zoo.csv', encoding='utf-8', index=False)


