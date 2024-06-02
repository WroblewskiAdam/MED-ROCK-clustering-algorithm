from scipy.io import arff
import pandas as pd
from ROCK_algorithm import ROCK
from data_converter import Data_Converter
from pyclustering.cluster.rock import rock

data_converter = Data_Converter()

# with open('dataset3.csv', newline='') as f:
#     reader = csv.reader(f)
#     example_data = list(reader)
# for point in example_data:
#     for i in range(len(point)):
#         point[i] = int(point[i])
# example_data = data_converter.separate_class_from_data(example_data, -1)


zoo_data, meta = arff.loadarff('zoo.arff')
zoo_data = pd.DataFrame(zoo_data)
zoo_data = data_converter.split_multi_arg_attribute(zoo_data, "LEGS", [0,1,2,3,4,5,6,7,8])
zoo_data = data_converter.convert_data_types(zoo_data)
zoo_data = zoo_data.values.tolist()
zoo_data = data_converter.separate_class_from_data(zoo_data, -1)


votes_data =  pd.read_csv('votes.data', sep=",", header = None)
# print(votes_data.head())

for i in range(1,17):
    votes_data = data_converter.split_multi_arg_attribute(votes_data,i,['y','n'], True)
    # print(votes_data.head())
# print(votes_data.head())

votes_data = votes_data.values.tolist()
votes_data = data_converter.separate_class_from_data(votes_data, 0)


my_rock = ROCK(votes_data)

jaccard = "jaccard"
sorensen = "sorensen"
euclidean = "euclidean"


# clusters = my_rock.get_clusters(0.75 ,7, jaccard)
# clusters_as_classes = my_rock.get_clusters_as_classes()

# for cluster in clusters_as_classes:
#     print(cluster)
#     print("No. republican", cluster.count('republican'))
#     print("No. democrat", cluster.count('democrat'))
i = 0.05
while i < 1:
    clusters = my_rock.get_clusters(i ,2, euclidean)
    score = my_rock.get_score()
    print("theta=" , round(i,2) , "score=" , round(score*100,1), "num_of_clusters" , len(my_rock.clusters))
    
    clusters_as_classes = my_rock.get_clusters_as_classes()
    # for cluster in clusters_as_classes:
    #     print(cluster)

    for cluster in clusters_as_classes:
        # print(cluster)
        print("No. republican", cluster.count('republican'))
        print("No. democrat", cluster.count('democrat'))

    i = i + 0.05
# score = my_rock.get_score()
# print(score)

