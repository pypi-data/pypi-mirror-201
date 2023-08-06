"""
"""

import numpy as np
import librosa
from musisort import file_manager

def analyze(song_waveform, song_info):
    val = librosa.feature.chroma_stft(y=song_waveform[0], sr=song_waveform[1])
    file_manager.save_info_data_file(song_info[0], song_info[1], "pitchsize", len(val[0]))
    return val