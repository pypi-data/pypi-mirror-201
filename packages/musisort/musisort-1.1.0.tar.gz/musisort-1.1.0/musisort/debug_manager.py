import numpy as np
import matplotlib.pyplot as plt
from musisort import analysis_manager, classification_manager, file_manager, global_variables
import random
import os
import gc
import time
from progress.bar import Bar

def delete_section(x, perc):
    if random.randint(0, 99) < perc:
        return 0
    return x

def delete_percent(array, percent):
    changed = 0
    array_copy = np.copy(array)
    size = len(array)
    iter = 0 if percent == 0 else (10/percent)*10
    count = iter
    for index, val in enumerate(array):
        if index < count and (index + 1) >= count:
            changed = changed + 1
            count = count + iter
            array_copy[index] = 0
    return array_copy

def reduce_waveform(waveform, percentage):
    # 0 = 0% change, 100 = silent song
    #delete_v = np.vectorize(delete_section)
    #array2 = delete_v(waveform, percentage)
    array2 = delete_percent(waveform, percentage)
    return array2
    
def debug():
    # -> Make debug folder similar to all folder
    # -> Make new analyze_song in analysis_manager that just takes a waveform and song name info
    # Read single song in folder - if more than one, stop, print error
    songs = file_manager.get_songs("debug")
    if songs == None:
        exit()
    if len(songs) > 1 or len(songs) <= 0:
        print("Error! Only one song can be in the debug list at a time!")
        print("Detected", len(songs), "total songs... Cancelling Debug.")
        exit()
    # load song waveform
    song_path = os.path.join(file_manager.debug_song_list_dir, file_manager.list_song_folder, (songs[0][0] + "." + songs[0][1]))
    loaded_song_waveform = analysis_manager.load_song_waveform(song_path)
    # loop through x times (percentage_iterations) creating new waveform with percentage removed
    bar = Bar('Generating Debug Data', max=(global_variables.debug_remove_iterations-global_variables.debug_iteration_minus))
    
    for iteration in range(1, global_variables.debug_remove_iterations+1-global_variables.debug_iteration_minus, 1):
        percent = int(100/global_variables.debug_remove_iterations) * iteration
        modified_song_name = songs[0][0] + "debug" + str(percent)
        modified_song_waveform = (delete_percent(loaded_song_waveform[0], percent), loaded_song_waveform[1])
        #print("\n", percent, " - ", len(modified_song_waveform[0]), ":" , np.shape(modified_song_waveform[0]), " , " ,len(loaded_song_waveform[0]), ":" , np.shape(loaded_song_waveform[0]))
        # call analyze_song_waveform in analysis_manager with modified waveform
        analysis_manager.analyze_song_waveform(modified_song_name, songs[0][1], modified_song_waveform)
        # song name should be called "<original_song_name>debug<percentage>-flac"
        modified_song_waveform = None
        bar.next()
        gc.collect()
        time.sleep(1)
            
    bar.finish()
    
    # -> Make classify load these songs if debug set to True
    cluster_frequency = {}
    
    name = songs[0][0] + "." + songs[0][1]
    classification_amount = 100
    bar2 = Bar('Classifying Debug Data', max=classification_amount)
    for classification_current in range(classification_amount):
        classification_info = classification_manager.classify_songs("debug", 2, True)
        
        song_label_info = classification_info[0]
        centroids = classification_info[1]
        song_file_info = classification_info[2]
        
        song_label = song_label_info[name]
        for title in song_label_info.keys():
            label = song_label_info[title]
            if classification_current == 0:
                #print(title)
                if title != name:
                    cluster_frequency[title] = 0
            if label == song_label and title != name:
                cluster_frequency[title] = cluster_frequency[title] + 1
        bar2.next()
            
    bar2.finish()
    
    # data_type , {song_title, distance_from_original}
    distance_calculations = {}
    data_types_tested = ""
    
    for data_type in global_variables.data_types_enabled.keys():
        if global_variables.data_types_enabled[data_type]:
            data_types_tested = data_types_tested + data_type + ", "
            original_data = file_manager.load_song_data_file(data_type, songs[0][0], songs[0][1])
            distance_calculations[data_type] = {}
            for iteration in range(1, global_variables.debug_remove_iterations+1-global_variables.debug_iteration_minus, 1):
                percent = int(100/global_variables.debug_remove_iterations) * iteration
                modified_song_name = songs[0][0] + "debug" + str(percent)
                loaded_song = file_manager.load_song_data_file(data_type, modified_song_name, songs[0][1])
                distance_calculations[data_type][modified_song_name] = np.linalg.norm(original_data-loaded_song)
                loaded_song = None
                gc.collect()
                
    print(global_variables.header_seperator)
                
    print("\nAnalysis Methods Tested : " + data_types_tested + "\n")
    
    print(global_variables.header_seperator)
    
    print("\nChance to be in Same Cluster as Original Song Waveform:\n")
    for title in cluster_frequency.keys():
        percent_changed = int(title[title.rindex("debug")+5:title.rindex(".")])
        print(str(percent_changed) + " %" + " changed: " + str(cluster_frequency[title]) + "%")
        
    print(global_variables.header_seperator)
    
    distance_accuracies = {}
        
    print("\nModified Waveform Distances from Original Waveform by Analysis Method: ")
    for data_type in distance_calculations.keys():
        print("\nAnalysis Method Type =", data_type, ":")
        print("----------------------")
        distance_accuracies_inside = {}
        min = 999999
        for title in distance_calculations[data_type].keys():
            percent_changed = int(title[title.rindex("debug")+5:len(title)])
            if percent_changed < min:
                min = percent_changed
            distance = distance_calculations[data_type][title]
            print(percent_changed, "%","changed: distance = ", distance)
            distance_accuracies_inside[percent_changed] = distance
        in_place = 0
        for i in range(min, 100, min):
            #print(str(i))
            if i in distance_accuracies_inside.keys():
                distance = distance_accuracies_inside[i]
                below = -99999999
                above = 99999999
                if i != min:
                    below = distance_accuracies_inside[i-min]
                if (i+min) in distance_accuracies_inside.keys():
                    above = distance_accuracies_inside[i+min]
                if distance < above and distance > below:
                    in_place = in_place + 1
        distance_accuracies[data_type] = in_place
        print("\nIn place =", in_place)
            
    print("\n" + global_variables.header_seperator)
    #print("\nClassification Info Condensed: \n", classification_info)