"""
"""

import os

from musisort import file_manager, global_variables

total_config_keys = 4

def on_start():
    generate_config_file(False)
    read_config_file()
    return

def change_config_file(key, value):
    path_to_config = os.path.join(file_manager.configuration_dir, "config.txt")
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
                
    f.writelines(new_lines)
    
    f.close()
    return changed

def read_config_file():
    path_to_config = os.path.join(file_manager.configuration_dir, "config.txt")
    f = open(path_to_config, "r")
    lines = f.readlines()
    
    for index, line in enumerate(lines):
        lineReplaced = line.replace("\n", "")
        # Analysis methods enabled check
        if(index < 4):
            split_line = lineReplaced.split(":")
            data_type = split_line[0]
            enabled = (split_line[1] == 'True')
            global_variables.data_types_enabled[data_type] = enabled
        else:
            split_line = lineReplaced.split(":")
            if index == 4:
                global_variables.debug_mode = bool(split_line[1] == 'True')
    
    f.close()

def generate_config_file(create_new):
    path_to_config = os.path.join(file_manager.configuration_dir, "config.txt")
    if os.path.exists(path_to_config) and create_new == False:
        f2 = open(path_to_config, "r")
        if len(f2.readlines()) != total_config_keys:
            generate_config_file(True)
        f2.close()
        return
    
    file_action = "a" if create_new == False else "w"
    f = open(path_to_config, file_action)
    
    # Write new info to file
    for data_type in global_variables.data_types:
        f.write(data_type + ":" + str("True") + "\n")
    # Write debug mode to file
    f.write("debug-mode:" + str("True") + "\n")
        
    f.close()
    return

def print_config_file():
    path_to_config = os.path.join(file_manager.configuration_dir, "config.txt")
    f = open(path_to_config, "r")
    lines = f.readlines()

    print(global_variables.header_seperator, "\n")
    
    for index, line in enumerate(lines):
        if index == 0:
            print("Analysis Methods Enabled : \n")
        split_line = line.split(":")
        key = split_line[0]
        value = split_line[1]
        if index < 4:
            print("\t" + key + " = " + value)
        else:
            print(key + " = " + value)
        
    print(global_variables.header_seperator) 
    
    f.close()