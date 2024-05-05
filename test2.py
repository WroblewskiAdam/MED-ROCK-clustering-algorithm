from ROCK_algorithm import ROCK
import csv


file = open('dataset.csv')
reader = csv.reader(file)
data = list(reader)


my_rock = ROCK()
clusters = my_rock.get_clusters(data, 0.2, 2)
print(clusters)
