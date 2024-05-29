from ROCK_algorithm import ROCK
import csv
from scipy.io import arff

import pandas as pd

zoo, meta = arff.loadarff('zoo.arff')
df = pd.DataFrame(zoo)
a = df.head()
print(a);
print(meta)
print(a.dtypes)
# print(df.shape[0])
# print(df)
# a.pop(a.columns[-1])
# print(a.iloc[2])


b = a.values.tolist()
print(b)


file = open('dataset3.csv')
reader = csv.reader(file)
data = list(reader)
# print(data)


# my_rock = ROCK()
# clusters = my_rock.get_clusters(data, 0.2, 2)
# print(clusters)

# clusters_points = my_rock.get_clusters_points(data,clusters)






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


list_data = df.values.tolist()
for i in range(10):
    print(list_data[i])
    
for i in range(len(list_data)):
    # print(list_data[i])
    # print(list_data[i][:-1])
    # print(list_data[i][-1])
    list_data[i] = [list_data[i][:-1], list_data[i][-1]]
    # print(list_data[i])

for i in range(len(list_data)):
    point_data = list_data[i][0]
    point_data_index = []
    for j in range(len(point_data)):
        if point_data[j] == 1: point_data_index.append(j)
    list_data[i][0] = point_data_index
    
for i in range(10):
    print(list_data[i])
# df.to_csv('zoo.csv', encoding='utf-8', index=False)



# print(clusters_points)
# print("dupa")
