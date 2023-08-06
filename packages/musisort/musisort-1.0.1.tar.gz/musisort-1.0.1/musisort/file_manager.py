"""
"""

from appdirs import AppDirs
import musisort.__init__ as init
import os
from musisort import analysis_manager, global_variables
import glob
import gc
import time
from progress.bar import Bar
import numpy as np

# Where song lists are stored that are categorized and analyzied
song_list_dir = "songlists"
all_song_list_dir = song_list_dir + os.sep + "all"
debug_song_list_dir = song_list_dir + os.sep + "debug"
custom_song_list_dir = song_list_dir + os.sep + "custom"
list_song_folder = "songs"
list_categories_folder = "categories"
custom_song_lists = {} # listname : custom_song_list_dir + sep + listname

# Where the data gathered from analysis methods are stored
song_data_dir = "songdata"
info_type_dir = "info"
data_type_dirs = {}

# Where configuration files are stored
configuration_dir = "config"

dirs = AppDirs(init.appname, init.appauthor)

'''
Functions that deal with the creation and management of directories.
'''

def on_start():
    user_data_dir = dirs.user_data_dir
        
    generate_path_variables(user_data_dir)
    
    confirm_paths_exist(user_data_dir)
    
def generate_path_variables(user_data_dir):
    global song_list_dir
    global all_song_list_dir
    global custom_song_list_dir
    global custom_song_lists
    global song_data_dir
    global data_type_dirs
    global configuration_dir
    global info_type_dir
    global debug_song_list_dir
    
    song_list_dir = os.path.join(user_data_dir, song_list_dir)
    all_song_list_dir = song_list_dir + os.sep + "all"
    debug_song_list_dir = song_list_dir + os.sep + "debug"
    custom_song_list_dir = song_list_dir + os.sep + "custom"
    
    song_data_dir = os.path.join(user_data_dir, song_data_dir)
    info_type_dir = os.path.join(song_data_dir, "info")
    
    configuration_dir = os.path.join(user_data_dir, configuration_dir)
    
    for data_type in global_variables.data_types:
        data_type_dirs[data_type] = song_data_dir + os.sep + data_type
        
def confirm_paths_exist(user_data_dir):
    # Top level folders in tree
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
    if not os.path.exists(song_list_dir):
        os.makedirs(song_list_dir)
        
    # Song data folder tree
    if not os.path.exists(song_data_dir):
        os.makedirs(song_data_dir)
    if not os.path.exists(info_type_dir):
        os.makedirs(info_type_dir)
    for data_type in data_type_dirs.keys():
        data_path = data_type_dirs[data_type]
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        
    # All songs list folder tree
    if not os.path.exists(all_song_list_dir):
        os.makedirs(all_song_list_dir)
    if not os.path.exists(os.path.join(all_song_list_dir, list_song_folder)):
        os.makedirs(os.path.join(all_song_list_dir, list_song_folder))
    if not os.path.exists(os.path.join(all_song_list_dir, list_categories_folder)):
        os.makedirs(os.path.join(all_song_list_dir, list_categories_folder))
        
    # Debug songs list folder tree
    if not os.path.exists(debug_song_list_dir):
        os.makedirs(debug_song_list_dir)
    if not os.path.exists(os.path.join(debug_song_list_dir, list_song_folder)):
        os.makedirs(os.path.join(debug_song_list_dir, list_song_folder))
    if not os.path.exists(os.path.join(debug_song_list_dir, list_categories_folder)):
        os.makedirs(os.path.join(debug_song_list_dir, list_categories_folder))
        
    # Custom song lists folder tree
    if not os.path.exists(custom_song_list_dir):
        os.makedirs(custom_song_list_dir)
    custom_lists = next(os.walk(custom_song_list_dir))[1]
    for custom_list in custom_lists:
        list_dir = os.path.join(custom_song_list_dir, custom_list)
        custom_song_lists[custom_list] = list_dir
        if not os.path.exists(os.path.join(list_dir, list_song_folder)):
            os.makedirs(os.path.join(list_dir, list_song_folder))
        if not os.path.exists(os.path.join(list_dir, list_categories_folder)):
            os.makedirs(os.path.join(list_dir, list_categories_folder))
            
    # Configuration folder tree
    if not os.path.exists(configuration_dir):
        os.makedirs(configuration_dir)
            
def print_directory_list():
    print(global_variables.header_seperator, "\n")
    print("MusiSort Folder : ", dirs.user_data_dir, "\n")
    
    # ---
    print("Config Folder : ", configuration_dir, "\n")
    
    # ---
    print("Song Lists Folder : ", song_list_dir, "\n")
    
    print("All Songs List Folder : ", all_song_list_dir, "\n")
    print("\tSongs Folder ::", os.path.join(all_song_list_dir, list_song_folder), "\n")
    
    
    print("Debug Songs List Folder : ", debug_song_list_dir, "\n")
    print("\tSongs Folder ::", os.path.join(debug_song_list_dir, list_song_folder), "\n")
    
    print("Custom Song Lists Folder : ", custom_song_list_dir, "\n")
    print("\tCustom Lists Song Folders : \n")
    for custom_list in custom_song_lists.keys():
        print("\t", custom_list, "::", os.path.join(custom_song_lists[custom_list], list_song_folder), "\n")
        
    # ---
    print("Song Data Folder : ",song_data_dir, "\n")
    print("\tData Types : \n")
    for data_type in data_type_dirs.keys():
        print("\t", data_type, "::", data_type_dirs[data_type], "\n")
    print(global_variables.header_seperator)
    
'''
Functions that deal with the loading of songs into python.
'''

loaded_songs_paths = {}
loaded_songs_names = {}
loaded_songs_ext = {}

def load_songs():
    global loaded_song_names
    
    song_count = 0
    song_max_count = len(glob.glob( os.path.join(all_song_list_dir, list_song_folder, "*.*")))
    bar = Bar('Processing Songs', max=song_max_count)
    
    for audio_format in global_variables.audio_formats:
        for song in sorted(glob.glob( os.path.join(all_song_list_dir, list_song_folder, ("*." + audio_format)) )):
            song_count += 1
            
            name = get_audio_name_from_path(song)
            loaded_songs_paths[song] = name[0]
            loaded_songs_names[name] = song
            loaded_songs_ext[song] = name[1]
            
            analysis_manager.analyze_song(song, name[0], name[1])
            
            # Asyncing for stopping crashes
            if song_count % 27 == 0:
                time.sleep(1)
            if song_count % 10 == 0:
                # Remove large leftover song data arrays before they fill up memory
                gc.collect()
                
            bar.next()
            
    bar.finish()
    
    # For debugging :
    #for index, element in enumerate(loaded_songs_paths.keys()):
    #    print(loaded_songs_paths[element] + "  :::  " + element)
    #    if index > 3:
    #        break
    return

def get_songs(list_name):
    global loaded_song_names
    
    song_count = 0
    song_dir_list = ""
    if list_name == "debug":
        song_dir_list = os.path.join(debug_song_list_dir, list_song_folder, ("*."))
    else:
        song_dir_list = os.path.join(all_song_list_dir, list_song_folder, ("*.")) if list_name == "all"\
            else os.path.join(custom_song_lists[list_name], list_song_folder, ("*."))
    song_max_count = len(glob.glob(song_dir_list + "*"))
    songs = []
    
    for audio_format in global_variables.audio_formats:
        for song in sorted(glob.glob( song_dir_list + audio_format )):
            song_count += 1
            
            name = get_audio_name_from_path(song)
            songs.append(name)
            #loaded_songs_paths[song] = name[0]
            #loaded_songs_names[name] = song
            #loaded_songs_ext[song] = name[1]
            
    return songs
    
def get_audio_name_from_path(path):
    file_name = path
    ext = ""
    if file_name.rfind("/") != -1:
        file_name = file_name[file_name.rfind("/")+1 : len(file_name)]
    if file_name.rfind(".") != -1:
        ext = file_name[file_name.rfind(".")+1 : len(file_name)]
        file_name = file_name[0 : file_name.rfind(".")]
    else:
        return None
    return (file_name, ext, (file_name + "-" + ext))

def load_song_data_file(data_type, song_file_name, song_file_ext):
    # Parse file name and file extension from file path
    data_file_path = os.path.join(song_data_dir, data_type, (song_file_name + "-" + song_file_ext + ".npy"))
    
    if os.path.exists(data_file_path):
        return np.load(data_file_path, allow_pickle=True)
    return None
         
def save_song_data_file(data_type, song_file_name, song_file_ext, data):
    data_file_path = os.path.join(song_data_dir, data_type, (song_file_name + "-" + song_file_ext + ".npy"))
    if os.path.exists(data_file_path):
        os.remove(data_file_path)
    np.save(data_file_path, data)
   
def load_info_data_file(song_file_name, song_file_ext, key):
    path_to_config = os.path.join(info_type_dir, (song_file_name + "-" + song_file_ext + ".txt"))
    
    if os.path.exists(path_to_config) == False:
        return None
        
    # If the info file does exist, replace the key's value with a new one
    f = open(path_to_config, "r")
    lines = f.readlines()
    f.close()
    
    value = None
    
    for line in lines:
        split_line = line.replace("\n", "").split(":")
        config_key = split_line[0]
        if config_key == key:
            value = split_line[1]
            break
            
    return value
 
def save_info_data_file(song_file_name, song_file_ext, key, value):
    path_to_config = os.path.join(info_type_dir, (song_file_name + "-" + song_file_ext + ".txt"))
    
    # If the info file does not exist, create a new file and exit function
    if os.path.exists(path_to_config) == False:
        f = open(path_to_config, "w")
        f.write(key + ":" + str(value))
        f.close()
        return
    
    # If the info file does exist, replace the key's value with a new one
    f = open(path_to_config, "r")
    lines = f.readlines()
    f.close()
    f = open(path_to_config, "w")
    new_lines = []
    changed = False
    
    for line in lines:
        split_line = line.replace("\n", "").split(":")
        config_key = split_line[0]
        if config_key == key:
            changed = True
            new_lines.append((config_key + ":" + str(value) + "\n"))
        else:
            new_lines.append(line)
    
    if changed == False:
        new_lines.append(key + ":" + str(value))
   
    f.writelines(new_lines)
    
    f.close()
    return changed
    
'''
Functions that deal with saving classification information.
'''

def save_song_labels(classification_info, list_name, category_count):
    list_path_dir = os.path.join(all_song_list_dir, list_categories_folder, ("labels_" + str(category_count) + ".txt"))
    if list_name != "all" and list_name != "debug":
        list_path_dir = os.path.join(custom_song_lists[list_name], list_categories_folder, ("labels_" + str(category_count) + ".txt"))
    elif list_name == "debug":
        list_path_dir = os.path.join(debug_song_list_dir, list_categories_folder, ("labels_" + str(category_count) + ".txt"))
    f = open(list_path_dir, "w")
    
    # Write new info to file
    for song in classification_info.keys():
        f.write(song + ":" + str(classification_info[song]))
        
    f.close()
    return
    
def load_song_labels(list_name, category_count):
    list_path_dir = os.path.join(all_song_list_dir, list_categories_folder, ("labels_" + str(category_count) + ".txt"))
    if list_name != "all" and list_name != "debug":
        list_path_dir = os.path.join(custom_song_lists[list_name], list_categories_folder, ("labels_" + str(category_count) + ".txt"))
    elif list_name == "debug":
        list_path_dir = os.path.join(all_song_list_dir, list_categories_folder, ("labels_" + str(category_count) + ".txt"))
    f = open(list_path_dir, "r")
    lines = f.readlines()
    
    song_dict = {}
    
    for index, line in enumerate(lines):
        split_line = line.split(":")
        song_dict[split_line[0]] = split_line[1]
    
    f.close()
    return song_dict
    
def save_song_centroids(centroid_info, list_name, category_count):
    list_path_dir = os.path.join(all_song_list_dir, list_categories_folder, ("centroids_" + str(category_count) + ".npy"))
    if list_name != "all"and list_name != "debug":
        list_path_dir = os.path.join(custom_song_lists[list_name], list_categories_folder, ("centroids_" + str(category_count) + ".npy"))
    elif list_name == "debug":
        list_path_dir = os.path.join(debug_song_list_dir, list_categories_folder, ("centroids_" + str(category_count) + ".npy"))
    
    if os.path.exists(list_path_dir):
        os.remove(list_path_dir)
    np.save(list_path_dir, centroid_info)
    
def load_song_centroids(list_name, category_count):
    # Parse file name and file extension from file path
    list_path_dir = os.path.join(all_song_list_dir, list_categories_folder, ("centroids_" + str(category_count) + ".npy"))
    if list_name != "all"and list_name != "debug":
        list_path_dir = os.path.join(custom_song_lists[list_name], list_categories_folder, ("centroids_" + str(category_count) + ".npy"))
    elif list_name == "debug":
        list_path_dir = os.path.join(debug_song_list_dir, list_categories_folder, ("centroids_" + str(category_count) + ".npy"))
        
    if os.path.exists(list_path_dir):
        return np.load(list_path_dir)
    return None