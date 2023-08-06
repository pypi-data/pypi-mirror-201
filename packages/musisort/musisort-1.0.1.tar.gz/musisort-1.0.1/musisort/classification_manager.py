import numpy as np
from sklearn import cluster
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.utils.multiclass import unique_labels
import scipy.interpolate as interp

import glob
import gc
import time
from musisort import global_variables
from musisort import file_manager, debug_manager

def classify_songs(list_path, category_count, debug=False):
    """Function used to classify list of songs into their own categories.
    Calls the categorization functions below according to the data type being read.
    
    Basic Logic of function is as follows:
    1. Read necessary data
    2. Load data from files and call classify functions using it
    3. Unify the labels in the individual label lists into one single label for each song
    4. Save labels for songs into a file as well as the centroids created
    """
    # 1. Load enabled data types for processing
    data_types_enabled = []
    for data_type in global_variables.data_types_enabled.keys():
        #print(data_type, " : ", global_variables.data_types_enabled[data_type])
        if global_variables.data_types_enabled[data_type]:
            data_types_enabled.append(data_type)
            
    if len(data_types_enabled) <= 0:
        print("No data types are enabled in the config! Cannot classify...")
        return
    # If category count == -1, perform silhouette clustering.  Else, use category count for k
    songs = file_manager.get_songs(list_path)
    if debug:
        song_name = songs[0][0]
        for i in range(1, global_variables.debug_remove_iterations+1-global_variables.debug_iteration_minus, 1):
            percent = int(100/global_variables.debug_remove_iterations) * i
            songs.append(((song_name + "debug" + str(percent)), songs[0][1]))
    
    # 2. Cluster data for each data type
    clustering_algorithm = get_nonsilo_labels if category_count != -1 else get_silo_labels
    clustering_simple_category_count = category_count if category_count != -1 else 10
    
    data_type_labels = np.zeros(shape=(len(data_types_enabled), len(songs)))
    #data_type_clusters = {}
    
    for index, data_type in enumerate(data_types_enabled):
        # Decide on which clustering algorithm to use for data type
        # Used for performance handling
        
        clustering_algorithm_type = 0
        if data_type in global_variables.data_types_cluster_algorithm.keys():
            clustering_algorithm_type = global_variables.data_types_cluster_algorithm[data_type]
        
        # Ensure all dimensions are equal in size, and resize if not
        sizeInfo = ensure_dimensions(songs, data_type)
        shapeOfData = None
            
        # Gather song data to single array
        song_data = None
        for index2, song in enumerate(songs):
            loaded_song = file_manager.load_song_data_file(data_type, song[0], song[1])
            if shapeOfData == None:
                shapeOfData = get_dimensions_shape(loaded_song, sizeInfo)
            if song_data is None:
                song_data = np.zeros(shape=(len(songs), np.prod(shapeOfData)))
            if loaded_song is None:
                loaded_song = np.zeros(shape=shapeOfData)
                
            song_data[index2] = np.resize(resize_array(loaded_song, shapeOfData), np.prod(shapeOfData))

        # Call clustering algorithms for data type using loaded song data
        if clustering_algorithm_type == 1:
            data_type_labels[index] = get_labels_simple(song_data, clustering_simple_category_count)[0]
            continue
        
        clustering_data = clustering_algorithm(song_data, category_count)
        data_type_labels[index] = clustering_data[0]
        
        # Clear song_data array to save space
        song_data = None
        gc.collect()
        
    # 3. Combine values of label arrays into one single 2D array
    # Values of each index is a array of labels for each data type for a song (ex:) [1, 5, 2, 3]
    
    data_type_labels_tuple = ()
    for index in range(len(data_type_labels)):
        data_type_labels_tuple = data_type_labels_tuple + (data_type_labels[index],)
    condensed_labels = np.vstack(data_type_labels_tuple).T

    # Perform clustering on combined label array to get how close overall labels are
    final_combined_data = clustering_algorithm(condensed_labels, category_count)

    final_combined_labels = final_combined_data[0]
    final_combined_clusters = final_combined_data[1]
    
    # Unique the labels so they aren't random numbers but equal in distance (1, 7, 3) -> (1, 3, 2)
    #final_combined_labels = unique_labels(final_combined_labels)
    
    # Create dictionary of song name and label value
    song_values = {}
    song_values_sorted = {}
    
    for label in np.sort(np.unique(final_combined_labels)):
        song_values_sorted[label] = []

    for index, label in enumerate(final_combined_labels):
        song = (songs[index][0] + "." + songs[index][1])
        song_values_sorted[label].append(song)
        song_values[song] = label
        
    if debug != True:
        index_song = 1
        for label in song_values_sorted.keys():
            for song in song_values_sorted[label]:
                print(index_song, ":", song, ":", label)
                index_song = index_song + 1
                
        file_manager.save_song_labels(song_values, list_path, category_count)
        file_manager.save_song_centroids(final_combined_clusters, list_path, category_count)

    return (song_values, final_combined_clusters, songs)
    
def get_silo_labels(data, n):
    # n does nothing, just for parameter consistency
    # Takes a 2d array with each element being a vector
    # (50, 100) , 50 100 element vectors
    k = 30
    
    sil_score_max = 9999
    best_labels = None
    best_clusters = None
    
    if len(np.unique(data)) == 1:
        return get_labels_simple(data, 1)

    for n_cluster in range(2,k):
        model = KMeans(n_clusters = n_cluster, n_init=5).fit(data)
        labels = model.labels_
        sil_score = silhouette_score(data, labels)
        if sil_score < sil_score_max:
            sil_score_max = sil_score
            best_labels = labels
            best_clusters = model.cluster_centers_
    return (best_labels, best_clusters)

def get_nonsilo_labels(data, k):
    model = KMeans(n_clusters = k, n_init=5).fit(data)
    return (model.labels_, model.cluster_centers_)

def get_labels_simple(data, k):
    model = KMeans(n_clusters = k, n_init=1).fit(data)
    return (model.labels_, model.cluster_centers_)

##############################################################################
# Functional Methods

def get_dimensions_shape(song, size_info):
    if size_info[1] == True:
        shape = (size_info[0], ) if song.ndim == 1 else (len(song), size_info[0])
        return shape
    return np.shape(song)

def ensure_dimensions(songs, data_type):
    maxSize = -1
    wasChanged = False
    for song in songs:
        size = file_manager.load_info_data_file(song[0], song[1], (data_type + "size"))
        if size is None:
            continue
        size = int(size)
        if maxSize < size:
            if not wasChanged and maxSize != -1:
                wasChanged = True
            maxSize = size
    return maxSize, wasChanged

def resize_array(array, shapeNeeded):
    if shapeNeeded != np.shape(array):
        if array.ndim == 1:
            return resize_1Darray(array, shapeNeeded[-1])
        else:
            return resize_2Darray(array, shapeNeeded[-1])
    return array

def resize_2Darray(array, n):
    """
    Takes a m-dimensional array and resizes its 1D endpoints to n indexes
    """
    new_array = np.zeros(shape=(len(array), n))
    for index, x in enumerate(array):
        new_array[index] = resize_1Darray(x, n)
    return new_array

def resize_1Darray(array, n):
    """
    Function resizes a 1D array of x-count values to n-count values.
    """
    return interp.interp1d(np.arange(len(array)),np.copy(array))(np.linspace(0,array.size-1,n))