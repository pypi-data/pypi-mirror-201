import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.neighbors import NearestNeighbors # importing the library
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from statistics import mean
from statistics import median


def full_scan(data, graph=False, kmeans_n_init=100, kmeans_max_iter=1000, kmeans_tol=0.0001):
    """
    The full end-to-end kscanner function

    Parameters
    ----------
    data : dataframe
        A dataframe/object to be used for unsupervised clustering

    graph : boolean
       A boolean set as Default=True that specifies if a graph should be plotted

    kmeans_n_init : int
       An argument to kmeans specifying how many random centroid initiations should be tried. Default is 100

    kmeans_max_iter : int
       An argument to kmeans specifying how many iterations should be tried. Default is 1000

    kmeans_tol : int
       An argument to kmeans specifying the tolerance. Default is 0.0001

    Returns
    -------
    out : list
        return [automated_eps, unique_clusters, kmeanModel_best, elapsed_time, fig1, fig2]
    """

    # Initialize time
    st = time.time()
    # Compute data proximity from each other using Nearest Neighbors
    neighb = NearestNeighbors(algorithm="brute")  # creating an object of the NearestNeighbors class
    nbrs = neighb.fit(data)  # fitting the data to the object
    distances, indices = nbrs.kneighbors(data)  # finding the nearest neighbours

    # Automate Approximation of Eps, remove 0 indices and distance values
    unlisted_distance = [item for sublist in distances for item in sublist if item != 0]
    sort_distances = sorted(unlisted_distance)


    dif1 = sorted(np.diff(sort_distances))
    sort_dif1 = sorted(list(dif1))
    dif2 = list(np.diff(sort_dif1))
    dif2 = sorted(dif2)

    # get rid of 0 values
    test = [x for x in dif2 if x != 0]

    # define quantiles and remove lowest 25% and highest 75%
    Q1 = np.quantile(test, .25)
    Q3 = np.quantile(test, .75)
    IQR = Q3 - Q1
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR
    test = [x for x in test if (x < upper_limit) and (x > lower_limit)]

    # determine metrics
    mean_test = mean(test)
    median_test = median(test)
    difference_test = median_test - mean_test

    # if > 0, median is greater than mean and there are more large changes to the right and we will use the 2nd quantile
    # if < 0, median is less than mean and there are more large changes to the left and we will use the 3rd quantile
    if difference_test < 0:
        best_pt = next((i for i in test if i >= (test[round(len(test) * 3 / 4)])), None)
    elif difference_test == 0:
        best_pt = mean_test
    else:
        best_pt = next((i for i in test if i >= test[round(len(test) * 1 / 4)]), None)


    # Epsilon
    automated_eps = (sort_distances[dif2.index(best_pt) + 2] + sort_distances[dif2.index(best_pt) + 1]) / 2

    if graph == True:
        # Sort and plot the distances results
        fig1 = plt.figure()
        distances = np.sort(distances, axis=0)  # sorting the distances
        distances = distances[:, 1]  # taking the second column of the sorted distances
        plt.rcParams['figure.figsize'] = (5, 3)  # setting the figure size
        plt.plot(distances)  # plotting the distances
        plt.show()  # showing the plot
    else:
        fig1="No graph"
        pass

    # Automate approximation of MinPts
    auto_dimension = data.shape[1]

    if auto_dimension <= 2:
        minpts = 4
    else:
        minpts = auto_dimension * 2

    # Cluster the data
    dbscan = DBSCAN(eps=automated_eps, min_samples=minpts).fit(data)  # fitting the model
    labels = dbscan.labels_  # getting the labels
    # Determine number of unique clusters
    unique_clusters = len(set(list(labels)))

    if graph == True:
        # Plot the clusters
        fig2 = plt.figure()
        plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=labels, cmap="plasma")  # plotting the clusters
        plt.xlabel("X")  # X-axis label
        plt.ylabel("Y")  # Y-axis label
        plt.show()  # showing the plot
    else:
        fig2="No graph"
        pass

    # run K-Means
    kmeanModel_best = KMeans(n_clusters=unique_clusters, n_init=kmeans_n_init, max_iter=kmeans_max_iter,
                             tol=kmeans_tol).fit(data)
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - st))
    return [automated_eps, unique_clusters, kmeanModel_best, elapsed_time, fig1, fig2]


def auto_epsilon(data, graph=False):
    """
    The helper function to approximate the determination of the Epsilon value for DBSCAN

    Parameters
    ----------
    data : dataframe
        A dataframe/object to be used for unsupervised clustering

    graph : boolean
       A boolean set as Default=True that specifies if a graph should be plotted

    Returns
    -------
    out : list
        return [automated_eps, distances, nbrs, elapsed_time, fig]

    """

    st = time.time()
    # Compute data proximity from each other using Nearest Neighbors
    neighb = NearestNeighbors(algorithm="brute")  # creating an object of the NearestNeighbors class
    nbrs = neighb.fit(data)  # fitting the data to the object
    distances, indices = nbrs.kneighbors(data)  # finding the nearest neighbours

    # Automate Approximation of Eps, remove 0 indices and distance values
    unlisted_distance = [item for sublist in distances for item in sublist if item != 0]
    sort_distances = sorted(unlisted_distance)

    dif1 = sorted(np.diff(sort_distances))
    sort_dif1 = sorted(list(dif1))
    dif2 = list(np.diff(sort_dif1))
    dif2 = sorted(dif2)

    # get rid of 0 values
    test = [x for x in dif2 if x != 0]

    # define quantiles and remove lowest 25% and highest 75%
    Q1 = np.quantile(test, .25)
    Q3 = np.quantile(test, .75)
    IQR = Q3 - Q1
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR
    test = [x for x in test if (x < upper_limit) and (x > lower_limit)]

    # determine metrics
    mean_test = mean(test)
    median_test = median(test)
    difference_test = median_test - mean_test

    # if > 0, median is greater than mean and there are more large changes to the right and we will use the 2nd quantile
    # if < 0, median is less than mean and there are more large changes to the left and we will use the 3rd quantile
    if difference_test < 0:
        best_pt = next((i for i in test if i >= (test[round(len(test) * 3 / 4)])), None)
    elif difference_test == 0:
        best_pt = mean_test
    else:
        best_pt = next((i for i in test if i >= test[round(len(test) * 1 / 4)]), None)

    # Epsilon
    automated_eps = (sort_distances[dif2.index(best_pt) + 2] + sort_distances[dif2.index(best_pt) + 1]) / 2

    if graph == True:
        # Sort and plot the distances results
        fig1 = plt.figure()
        distances = np.sort(distances, axis=0)  # sorting the distances
        distances = distances[:, 1]  # taking the second column of the sorted distances
        plt.rcParams['figure.figsize'] = (5, 3)  # setting the figure size
        plt.plot(distances)  # plotting the distances
        plt.show()  # showing the plot
    else:
        fig1="No graph"
        pass
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - st))
    return [automated_eps, distances, nbrs, elapsed_time, fig1]


def auto_minpts(data):
    """
    A helper function to approximate the MinPts value for DBSCAN

    Parameters
    ----------
    data : dataframe
        A dataframe/object to be used for unsupervised clustering

    Returns
    -------
    out : list
        return [minpts, elapsed_time]
    """

    st = time.time()
    auto_dimension = data.shape[1]
    if auto_dimension <= 2:
        minpts = 4
    else:
        minpts = auto_dimension * 2
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - st))
    return [minpts, elapsed_time]


def dbscanner(data, epsilon, minpts, graph=False):
    """
    A helper function that runs DBSCAN

    Parameters
    ----------
    data : dataframe
        A dataframe/object to be used for unsupervised clustering

    epsilon : float
        The approximated epsilon value which is an input for DBSCAN

    minpts : float
        The approximated minpts value which is an input for DBSCAN

    Returns
    -------
    out : list
        return [dbscan, unique_clusters, elapsed_time, fig]
    """
    st = time.time()
    # Cluster the data
    dbscan = DBSCAN(eps=epsilon, min_samples=minpts).fit(data)  # fitting the model
    labels = dbscan.labels_  # getting the labels
    # Determine number of unique clusters
    unique_clusters = len(set(list(labels)))

    if graph == True:
        # Plot the clusters
        fig2 = plt.figure()
        plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=labels, cmap="plasma")  # plotting the clusters
        plt.xlabel("X")  # X-axis label
        plt.ylabel("Y")  # Y-axis label
        plt.show()  # showing the plot
    else:
        fig2="No graph"
        pass
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - st))
    return [dbscan, unique_clusters, elapsed_time, fig2]


def kmeans_model(data, unique_clusters, kmeans_n_init=100, kmeans_max_iter=1000, kmeans_tol=0.0001):
    """
    A helper function that runs K-Means clustering

    Parameters
    ----------
    data : dataframe
        A dataframe/object to be used for unsupervised clustering

    unique_clusters : int
        The approximated unique clusters value which is an input for K-Means and is a returned value from DBSCAN

    kmeans_n_init : int
       An argument to kmeans specifying how many random centroid initiations should be tried. Default is 100

    kmeans_max_iter : int
       An argument to kmeans specifying how many iterations should be tried. Default is 1000

    kmeans_tol : int
       An argument to kmeans specifying the tolerance. Default is 0.0001

    Returns
    -------
    out : list
        return [kmeanModel_best, unique_clusters, elapsed_time]
    """
    st = time.time()
    # run K-Means
    kmeanModel_best = KMeans(n_clusters=unique_clusters, n_init=kmeans_n_init, max_iter=kmeans_max_iter, tol=kmeans_tol).fit(data)
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - st))
    return [kmeanModel_best, unique_clusters, elapsed_time]

