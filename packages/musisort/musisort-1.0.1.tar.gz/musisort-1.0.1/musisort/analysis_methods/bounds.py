"""
"""

import numpy as np

def analyze(song_waveform, song_info):
    split_count = 10
    song_data = song_waveform[0]
    min_value = np.min(song_data)
    if min_value < 0:
        song_data = song_data + abs(min_value)
    waveform_sections = np.array_split(song_data, split_count)
    min_max_values = []
    for i in range(split_count):
        min_max_values.append(np.max(waveform_sections[i]))
        min_max_values.append(np.min(waveform_sections[i]))
    return np.asarray(min_max_values)