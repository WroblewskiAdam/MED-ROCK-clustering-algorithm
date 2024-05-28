from pyclustering.cluster import cluster_visualizer,cluster_visualizer_multidim
from pyclustering.cluster.rock import rock;
from pyclustering.utils import read_sample;
from random import random;
import csv


file1 = open('dataset.csv')
reader1 = csv.reader(file1)
data = list(reader1)

# file2 = open('obce_point_neighbour_matrix.csv')
# reader2 = csv.reader(file2)
# data2 = list(reader2)

# print(data1 == data2)



# # print(data)

rock_instance = rock(data, 0.5, 2, 0.2)

rock_instance.process()

clusters = rock_instance.get_clusters()

print(clusters)