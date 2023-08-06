"""
"""

# Strings
header_seperator = "-----------------------------------------------------------------------------"
header = """ __    __   __  __   ______   __   ______   ______   ______  ______  
/\\ \"-./  \\ /\\ \\/\\ \\ /\\  ___\\ /\\ \\ /\\  ___\\ /\\  __ \\ /\\  == \\/\\__  _\\ 
\\ \\ \\-./\\ \\\\ \\ \\_\\ \\\\ \\___  \\\\ \\ \\\\ \\___  \\\\ \\ \\/\\ \\\\ \\  __<\\/_/\\ \\/ 
 \\ \\_\\ \\ \\_\\\\ \\_____\\\\/\\_____\\\\ \\_\\\\/\\_____\\\\ \\_____\\\\ \\_\\ \\_\\ \\ \\_\\ 
  \\/_/  \\/_/ \\/_____/ \\/_____/ \\/_/ \\/_____/ \\/_____/ \\/_/ /_/  \\/_/ """


# Lists and Dictionaries
data_types = []
data_types_enabled = {}
data_types_cluster_algorithm = {} # if not in here, use default algorithm
audio_formats = ["mp3", "ogg", "wav", "flac", "m4a", "aac", "webm", "opus"]

# General values
debug_remove_iterations = 10
debug_iteration_minus = 1

def on_start():
    data_types.append("mel")
    data_types.append("pitch")
    data_types.append("bounds")
    data_types.append("4D")
    data_types_cluster_algorithm["pitch"] = 1
    
# Config Options
debug_mode = True