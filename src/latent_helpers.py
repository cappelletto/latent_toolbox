import numpy as np

# Sure, here's a pseudo code for implementing silhouette analysis:

# Inputs:

#     Data matrix X of size N x D
#     Cluster assignments vector C of size N x 1

# Outputs:

#     Silhouette score vector S of size N x 1

#     For each data point i in range(N):
#         Calculate the average distance from point i to all other points in its assigned cluster
#         Assign it as a value of "a[i]"

#     For each data point i in range(N):
#         Calculate the average distance from point i to all other points in each of the other clusters
#         Assign the minimum of these distances as a value of "b[i]"
#         If the assigned cluster has only one point, assign a value of 0 to "b[i]"

#     For each data point i in range(N):
#         Calculate the silhouette score as:
#         s[i] = (b[i] - a[i]) / max(a[i], b[i])

#     Return the silhouette score vector S

# In this pseudo code, the silhouette score for each data point is calculated by comparing its distance to the other points in its assigned cluster (a[i]) and its distance to the points in each of the other clusters (b[i]). The silhouette score ranges from -1 to 1, where a score close to 1 indicates a well-separated cluster, a score close to 0 indicates a borderline case, and a score close to -1 indicates that the data point may be assigned to the wrong cluster.

# This pseudo code assumes that the data points are represented as a matrix X of size N x D, where N is the number of data points and D is the number of dimensions, and that the cluster assignments are stored in a vector C of size N x 1. The output of the algorithm is a vector S of size N x 1, containing the silhouette score for each data point.

def silhouette_analysis(X, C):
    """
    Compute the silhouette score for each data point.
    
    Inputs:
    - X: Data matrix of size N x D, where N is the number of data points and D is the number of dimensions.
    - C: Cluster assignments vector of size N x 1, where each element is an integer representing the cluster assignment of the corresponding data point.
    
    Outputs:
    - S: Silhouette score vector of size N x 1, where each element is the silhouette score of the corresponding data point.
    """
    
    N = X.shape[0]  # Number of data points
    S = np.zeros((N,))  # Initialize silhouette score vector
    
    for i in range(N):
        # Compute average distance from point i to all other points in its assigned cluster
        a_i = np.mean(np.linalg.norm(X[C == C[i]] - X[i], axis=1))
        
        # Compute average distance from point i to all other points in each of the other clusters
        b_i = np.min([np.mean(np.linalg.norm(X[C == j] - X[i], axis=1)) for j in set(C) - {C[i]}])
        
        # Compute silhouette score for point i
        S[i] = (b_i - a_i) / max(a_i, b_i)
    
    return S


def k_means(X, K, max_iter=100):
    """
    Compute K-means clustering on the data matrix X.
    
    Inputs:
    - X: Data matrix of size N x D, where N is the number of data points and D is the number of dimensions.
    - K: Number of clusters.
    - max_iter: Maximum number of iterations.
    
    Outputs:
    - C: Cluster assignments vector of size N x 1, where each element is an integer representing the cluster assignment of the corresponding data point.
    - mu: Cluster centroid matrix of size K x D, where each row is a cluster centroid.
    """
    
    N = X.shape[0]  # Number of data points
    D = X.shape[1]  # Number of dimensions
    mu = X[np.random.choice(N, K, replace=False), :]  # Randomly initialize cluster centroids
    C = np.zeros((N,), dtype=int)  # Initialize cluster assignments
    iter_count = 0
    
    while iter_count < max_iter:
        # Assign each data point to the nearest centroid
        for i in range(N):
            C[i] = np.argmin(np.linalg.norm(X[i] - mu, axis=1))
        
        # Update each centroid as the mean of the assigned data points
        for k in range(K):
            mu[k] = np.mean(X[C == k], axis=0)
        
        iter_count += 1
    
    return C, mu


# Function that reads a npy file containing a numpy array and exports it as a csv file.
def convert_to_csv(filename):
    array = np.load(filename)
    np.savetxt(filename[:-4] + ".csv", array, delimiter=",")
    return    


# Function that reads a numpy array from a file and exports it as a csv file
def export_csv(filename, array):
    np.savetxt(filename, array, delimiter=",")
    return