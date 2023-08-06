"""
"""

import numpy as np
import librosa

def analyze(song_waveform, song_info):
    val = np.asarray(np.mean(librosa.feature.mfcc(y=song_waveform[0], sr=song_waveform[1], n_mfcc=20).T,axis=0).tolist())
    return val