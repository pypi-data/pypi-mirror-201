"""
"""

from musisort.analysis_methods import mel
from musisort.analysis_methods import pitch
from musisort.analysis_methods import bounds
from musisort.analysis_methods import fourdim

from musisort import file_manager, global_variables
import numpy as np
import librosa
import os

analysis_types = {"mel" : mel.analyze, "pitch" : pitch.analyze, "bounds" : bounds.analyze, \
                  "4D" : fourdim.analyze}

song_waveform = np.empty(0)

def on_start():
    return

def analyze_song(path_to_song, song_file_name, song_file_ext):
    global song_waveform
    song_loaded = False
    data_file_name = song_file_name + "-" + song_file_ext + ".npy"
    for data_type in global_variables.data_types:
        # If analysis type disabled, skip step
        if global_variables.data_types_enabled[data_type] == False:
            continue
        
        # Check if file has already been analyzed using this data type method
        path_to_data_file = os.path.join(file_manager.song_data_dir, data_type, data_file_name)
        if not os.path.exists(path_to_data_file):
            if song_loaded == False:
                song_loaded = True
                song_waveform = load_song_waveform(path_to_song)
                if song_waveform == None:
                    return
            analyzed_data = analysis_types[data_type](song_waveform, (song_file_name, song_file_ext))
            file_manager.save_song_data_file(data_type, song_file_name, song_file_ext, analyzed_data)
            
def analyze_song_waveform(song_file_name, song_file_ext, waveform):
    data_file_name = song_file_name + "-" + song_file_ext + ".npy"
    for data_type in global_variables.data_types:
        # If analysis type disabled, skip step
        if global_variables.data_types_enabled[data_type] == False:
            continue
        
        # Check if file has already been analyzed using this data type method
        path_to_data_file = os.path.join(file_manager.song_data_dir, data_type, data_file_name)
        if not os.path.exists(path_to_data_file):
            analyzed_data = analysis_types[data_type](waveform, (song_file_name, song_file_ext))
            file_manager.save_song_data_file(data_type, song_file_name, song_file_ext, analyzed_data)
        
def load_song_waveform(path_to_song):
    try:
        info = librosa.load(path_to_song)
        return info
    except Exception as e:
        print("An error occured in loading an audio file : \n", repr(e))
        return None