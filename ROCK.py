import numpy as np
import math
import copy

class ROCK:
    def __init__(self, data_binary):
        self.data_binary = copy.deepcopy(data_binary)
        self.similarity_matrix = None
        self.adjacency_matrix = None
        self.links_matrix = None
        self.clusters = None
        self.clusters_points = None
        self.clusters_classes = None
        self.function = None

    def get_intersection_sum_len(self, a, b):
        intersection_len = 0
        sum_len = 0
        for i in range(len(a)):
            if a[i] == b[i] and a[i] != 0 and b[i] != 0:
                intersection_len += 1
            if a[i] == 1 or b[i] == 1:
                sum_len += 1
        return (intersection_len, sum_len)
    
    def calculate_jaccard_coefficient(self, a, b):
        if len(b) == 0 or len(a) == 0:
            return 0
        else:
            intersection, sum = self.get_intersection_sum_len(a,b)
            return intersection/sum
        
    def calculate_soresen_coefficient(self, a, b):
        if len(b) == 0 or len(a) == 0:
            return 0
        else:
            intersection, sum = self.get_intersection_sum_len(a,b)
            sum_a = 0
            sum_b = 0
            
            for i in range(len(a)):
                sum_a += a[i]
                sum_b += b[i] 
            return 2*(intersection)/(sum_a+sum_b)
        
    def calculate_euclidean_distance(self, a, b):
        sum = 0
        for i in range(len(a)):
            sum = sum + (int(a[i]) - int(b[i]))**2
        euclidean_distance = math.sqrt(sum)
        return euclidean_distance

    def calculate_similiarity_matrix(self):
        points_num = len(self.data_binary)
        matrix = np.zeros((points_num,points_num))
        for i in range(0, points_num):
            for j in range(i+1,points_num):
                if self.function == "jaccard":
                    matrix[i][j] = self.calculate_jaccard_coefficient(self.data_binary[i][0], self.data_binary[j][0])
                    matrix[j][i] = matrix[i][j]
                elif self.function == "sorensen":
                    matrix[i][j] = self.calculate_soresen_coefficient(self.data_binary[i][0], self.data_binary[j][0])
                    matrix[j][i] = matrix[i][j]
                elif self.function == "euclidean":
                    matrix[i][j] = self.calculate_euclidean_distance(self.data_binary[i][0], self.data_binary[j][0])
                    matrix[j][i] = matrix[i][j]
            matrix[i][i] = 1

        self.similarity_matrix = matrix

    def calculate_adjacency_matrix(self, phi):
        points_num = len(self.data_binary)
        matrix = np.zeros((points_num,points_num))
        self.calculate_similiarity_matrix()
        for i in range(0, points_num):
            for j in range(i+1,points_num):
                if self.similarity_matrix[i][j] >= phi:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
            matrix[i][i] = 1
        self.adjacency_matrix = matrix

    def get_links_matrix(self, adjacency_matrix):
        links_matrix = np.matmul(adjacency_matrix, adjacency_matrix)
        np.fill_diagonal(links_matrix,0)
        self.links_matrix = links_matrix
   
    def get_link_for_clusters(self, cluster_a, cluster_b):
        links = 0
        for point_a_index in cluster_a:
            for point_b_index in cluster_b:
                links += self.links_matrix[point_a_index][point_b_index]
        return links

    def clusters_goodness(self, cluster_a, cluster_b, theta):
        link_num = self.get_link_for_clusters(cluster_a, cluster_b)
        n_a = len(cluster_a)
        n_b = len(cluster_b)
        f = (1-theta)/(1+theta)
        goodness = link_num / (pow((n_a + n_b), (1+2*f)) - pow(n_a, 1+2*f) - pow(n_b, 1+2*f)) 
        return abs(goodness)

    def get_clusters_to_merge(self, theta):
        max_goodness = 0
        a_cluster_to_merge = None
        b_cluster_to_merge = None 
        for i in range(len(self.clusters)):
            a = self.clusters[i]
            for j in range(i+1, len(self.clusters)):
                b = self.clusters[j]
                goodness = self.clusters_goodness(a, b, theta)
                if(goodness >= max_goodness):
                    max_goodness = goodness
                    a_cluster_to_merge = i
                    b_cluster_to_merge = j
        return (a_cluster_to_merge, b_cluster_to_merge)

    def get_clusters(self, theta, cluster_num, function = "jaccard", data = None):
        if data: self.data_binary = data;
        self.function = function

        self.calculate_adjacency_matrix(theta)
        self.get_links_matrix(self.adjacency_matrix)
        self.clusters = []
        for i in range(len(self.data_binary)):
            self.clusters.append([i])

        while (len(self.clusters) > cluster_num):
            clusters_to_merge = self.get_clusters_to_merge(theta)
            if clusters_to_merge != (None, None):
                a = clusters_to_merge[0]
                b = clusters_to_merge[1]
                self.clusters[a] += self.clusters[b]
                self.clusters.pop(b)
            else:
                break

        for cluster in self.clusters:
            cluster.sort()

        self.get_clusters_points()
        self.get_clusters_as_classes()
        return self.clusters
    
    def get_clusters_points(self):
        clusters_points = []
        for cluster in self.clusters:
            cluster_list = []
            for point_index in cluster:
                cluster_list.append(tuple(self.data_binary[point_index]))
            clusters_points.append(cluster_list)
        self.clusters_points = clusters_points

    def get_clusters_as_classes(self):
        clusters = []
        for cluster in self.clusters_points:
            cluster_classes = []
            for point in cluster:
                cluster_classes.append(point[1])
            cluster_classes.sort()
            clusters.append(cluster_classes)
        self.clusters_classes = clusters
        return clusters
         
    def get_score(self):
        correctly_classified = 0
        for cluster in self.clusters_classes:
            most_frequent = max(set(cluster), key=cluster.count)
            num_of_most_frequent = cluster.count(most_frequent)
            correctly_classified += num_of_most_frequent
        
        return correctly_classified / len(self.data_binary)



