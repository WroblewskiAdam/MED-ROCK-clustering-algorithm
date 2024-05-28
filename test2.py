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
# print(clusters_points)
# print("dupa")