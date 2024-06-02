import numpy as np
import csv


def jaccard_coefficient(a, b):
    A = set(a)
    B = set(b)
    intersection = A.intersection(B)
    sum = A.union(B)

    if len(A) == 0 or len(B) == 0:
        return 0
    else:
        return len(intersection)/len(sum)


def get_similiarity_matrix(data):
    points_num = len(data)
    matrix = np.zeros((points_num,points_num))
    for i in range(0, points_num):
        a = data[i]
        for j in range(i+1,points_num):
            b = data[j]
            matrix[i][j] = jaccard_coefficient(a,b)
            matrix[j][i] = jaccard_coefficient(a,b)
        matrix[i][i] = 1
    return matrix


def get_adjacency_matrix(data, phi):
    points_num = len(data)
    matrix = np.zeros((points_num,points_num))
    similiarity_matrix = get_similiarity_matrix(data)
    for i in range(0, points_num):
        for j in range(i+1,points_num):
            if similiarity_matrix[i][j] >= phi:
                matrix[i][j] = 1
                matrix[j][i] = 1
        matrix[i][i] = 1
    return matrix


def get_links_matrix(adjacency_matrix):
    links_matrix = np.matmul(adjacency_matrix, adjacency_matrix)
    np.fill_diagonal(links_matrix,0)
    return links_matrix


def get_link_for_clusters(cluster_a, cluster_b, link_matrix):
    links = 0
    for point_a_index in cluster_a:
        for point_b_index in cluster_b:
            links += link_matrix[point_a_index][point_b_index]
    return links


def clusters_goodness(cluster_a, cluster_b, link_matrix, theta):
    link_num = get_link_for_clusters(cluster_a, cluster_b, link_matrix)
    n_a = len(cluster_a)
    n_b = len(cluster_b)
    f = (1-theta)/(1+theta)
    a = pow((n_a + n_b), (1+2*f))
    b = pow(n_a, 1+2*f)
    c = pow(n_b, 1+2*f)
    goodness = link_num / (pow((n_a + n_b), (1+2*f)) - pow(n_a, 1+2*f) - pow(n_b, 1+2*f)) 
    return goodness


def get_clusters_to_merge(all_clusters, link_matrix, theta):
    max_goodness = 0
    a_cluster_to_merge = None
    b_cluster_to_merge = None 
    for i in range(len(all_clusters)):
        a = all_clusters[i]
        for j in range(i+1, len(all_clusters)):
            b = all_clusters[j]
            goodness = clusters_goodness(a, b, link_matrix, theta)
            if(goodness > max_goodness):
                max_goodness = goodness
                a_cluster_to_merge = i
                b_cluster_to_merge = j
    return (a_cluster_to_merge, b_cluster_to_merge)


def rock(data, phi, cluster_num, theta = 0.5):
    theta = phi
    adjacency_matrix = get_adjacency_matrix(data, phi)
    links_matrix = get_links_matrix(adjacency_matrix)
    clusters = []
    for i in range(len(data)):
        clusters.append([i])

    while (len(clusters) > cluster_num):
        clusters_to_merge = get_clusters_to_merge(clusters, links_matrix, theta)
        if clusters_to_merge != (None, None):
            a = clusters_to_merge[0]
            b = clusters_to_merge[1]
            clusters[a] += clusters[b]
            clusters.pop(b)
        else:
            break
    return clusters


def run():
    with open('dataset.csv') as file:
        reader = csv.reader(file)
        data = list(reader)
        clusters = rock(data, 0.5, 2)
        print(clusters)
run()
