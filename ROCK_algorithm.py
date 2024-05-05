import numpy as np

class ROCK:
    def __init__(self):
        self.similarity_matrix = None
        self.adjacency_matrix = None
        self.links_matrix = None
        self.clusters = None
    

    def calculate_jaccard_coefficient(self, a, b):
        A = set(a)
        B = set(b)
        intersection = A.intersection(B)
        sum = A.union(B)

        if len(A) == 0 or len(B) == 0:
            return 0
        else:
            return len(intersection)/len(sum)


    def calculate_similiarity_matrix(self, data):
        points_num = len(data)
        matrix = np.zeros((points_num,points_num))
        for i in range(0, points_num):
            a = data[i]
            for j in range(i+1,points_num):
                b = data[j]
                matrix[i][j] = self.calculate_jaccard_coefficient(a,b)
                matrix[j][i] = self.calculate_jaccard_coefficient(a,b)
            matrix[i][i] = 1
        self.similarity_matrix = matrix

    def calculate_adjacency_matrix(self, data, phi):
        points_num = len(data)
        matrix = np.zeros((points_num,points_num))
        self.calculate_similiarity_matrix(data)
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
        # return links_matrix


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
        a = pow((n_a + n_b), (1+2*f))
        b = pow(n_a, 1+2*f)
        c = pow(n_b, 1+2*f)
        goodness = link_num / (pow((n_a + n_b), (1+2*f)) - pow(n_a, 1+2*f) - pow(n_b, 1+2*f)) 
        return goodness


    def get_clusters_to_merge(self, theta):
        max_goodness = 0
        a_cluster_to_merge = None
        b_cluster_to_merge = None 
        for i in range(len(self.clusters)):
            a = self.clusters[i]
            for j in range(i+1, len(self.clusters)):
                b = self.clusters[j]
                goodness = self.clusters_goodness(a, b, theta)
                if(goodness > max_goodness):
                    max_goodness = goodness
                    a_cluster_to_merge = i
                    b_cluster_to_merge = j
        return (a_cluster_to_merge, b_cluster_to_merge)


    def get_clusters(self, data, phi, cluster_num, theta = 0.5):
        theta = phi
        self.calculate_adjacency_matrix(data, phi)
        self.get_links_matrix(self.adjacency_matrix)
        self.clusters = []
        for i in range(len(data)):
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
        return self.clusters
    
    def get_clusters_points(self, data, clusters):
        clusters_points = []
        for cluster in clusters:
            cluster_list = []
            for point_index in cluster:
                cluster_list.append(tuple(data[point_index]))
            clusters_points.append(cluster_list)
        return clusters_points