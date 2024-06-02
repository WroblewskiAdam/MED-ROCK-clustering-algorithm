import csv
from scipy.io import arff
import pandas as pd
from ROCK_algorithm import ROCK


def convert(df, column_name, attribures_list):
    # rozbicie kolumny wieloatrybutowej
    column = df[column_name]
    column_index = df.columns.tolist().index(column_name)
    df = df.drop(columns = [column_name])
    for i in range(len(attribures_list)):
        values = []
        attribute_value = attribures_list[i]
        for point in column:
            values.append(1) if point == attribute_value else values.append(0)
        df.insert(column_index + i, column_name + str(attribute_value), values)

    # zmiana typu kolumny klasy
    df_mod = df.select_dtypes([object]).stack().str.decode('utf-8').unstack()
    df["class"] = df_mod["class"]
    # konwersja danych do int
    df = df.astype(int)
    return df
    
def split_data_class(list_data):
    # print("dupa")
    # for i in list_data:
    #     print(i)
    for i in range(len(list_data)):
        list_data[i] = [list_data[i][:-1], list_data[i][-1]]

    return list_data
    
def convert_data_to_index(list_data):
    for i in range(len(list_data)):
        point_data = list_data[i][0]
        point_data_index = []
        for j in range(len(point_data)):
            if int(point_data[j]) == 1: point_data_index.append(j)
        list_data[i][0] = point_data_index
    return list_data



zoo, meta = arff.loadarff('zoo.arff')
print(type(zoo))
print(zoo)
df = pd.DataFrame(zoo)

df = pd.read_csv('dataset3.csv')

with open('dataset3.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
for i in data :
    print(i)

# df = convert(df, "LEGS", [0,1,2,3,4,5,6,7,8])
data = split_data_class(data)
for i in data :
    print(i)
data = convert_data_to_index(data)

for i in data :
    print(i)


my_rock = ROCK()

data_without_indexes = []
for point in data:
    data_without_indexes.append(point[0])

clusters = my_rock.get_clusters(data_without_indexes, 0.2, 2)
for cluster in clusters:
    cluster.sort()
print(clusters)

clusters_points = my_rock.get_clusters_points(data,clusters)
# print(clusters_points)

