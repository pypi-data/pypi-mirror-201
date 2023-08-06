"""
"""

import numpy as np
import librosa.display
import matplotlib.pyplot as plt

f_v = None

def create_grid(arrays):
    grid = np.asarray([1])
    for array in arrays:
        grid = np.multiply.outer(grid, array)
    if np.max(grid) == 0 and np.min(grid) == 0:
        return np.squeeze(grid)
    grid = grid / grid.sum() # May cause issues if grid.sum == 0
    return np.squeeze(grid)

def get_peaks(song_waveform):
    peaks = [] # distance (frequency), difference (amplitude)
    length = song_waveform.size
    previous_peak_time = -1
    previous_peak_amplitude = -1
    for index in range(1, length-1):
        sample = song_waveform[index]
        if song_waveform[index-1] < sample and sample > song_waveform[index+1]:
            if previous_peak_time != -1:
                distance = abs(previous_peak_time - index)
                difference = abs(previous_peak_amplitude - sample)
                peaks.append([distance, difference])
            previous_peak_time = index
            previous_peak_amplitude = sample
    if len(peaks) == 0:
        max = np.max(song_waveform)
        m = [0, 0]
        peaks = [m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m]
    return np.asarray(peaks)

def function(x, n, upper):
    max = x if x >= n else n
    min = n if x >= n else x
    if max == 0 and min == 0:
        return 0
    exponent = upper + (upper * -1 * (min / max))
    return x + ((n-x) * (1 - (1/((abs(n-x)+1)**(exponent)))))

def get_centered_mean(data):
    n = np.median(data)
    upper = 1/2
    return np.mean(f_v(data, n, upper))

def analyze(song_waveform, song_info):
    global f_v
    f_v = np.vectorize(function)
    split_count = 10
    song_data = song_waveform[0]

    """y = song_waveform[0]
    sr = song_waveform[1]
    fig, ax = plt.subplots(nrows=3, sharex=True)
    librosa.display.waveshow(y, sr=sr, ax=ax[0])
    ax[0].set(title='Envelope view, mono')
    ax[0].label_outer()
    plt.show()"""
    
    min_value = np.min(song_data)
    if min_value < 0:
        song_data = song_data + abs(min_value)
    song_peaks = np.array_split(get_peaks(song_data), split_count)
    distances_mean = []
    differences_mean = []
    distances_max = []
    differences_max = []
    for i in range(split_count):
        current_splice = song_peaks[i]
        distances = current_splice[:, 0]
        differences = current_splice[:, 1]
        distances_mean.append(get_centered_mean(distances))
        differences_mean.append(get_centered_mean(differences))
        distances_max.append(np.max(distances))
        differences_max.append(np.max(differences))
    arrays = (np.asarray(distances_mean),np.asarray(differences_mean),\
        np.asarray(distances_max),np.asarray(differences_max))
    arr_return = np.ravel(create_grid(arrays))
    return arr_return