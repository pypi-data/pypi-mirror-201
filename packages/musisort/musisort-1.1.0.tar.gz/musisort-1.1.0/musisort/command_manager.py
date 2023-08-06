"""
"""

from musisort import classification_manager, configuration_data, file_manager, global_variables, debug_manager

command_descriptions = { \
    "help" : "Displays a list of all commands along with simple information about each one.", \
    "info" : "Displays more in-depth information about the command specified in the argument.", \
    "dir" :  "Displays a list of all directories the program uses.", \
    "config" : "Displays and modifies the configuration values for the program.", \
    "analyze" : "Will analyze the songs not analyzed yet within the /all/songs directory.", \
    "classify" : "Will sort songs in list based on musical similarity after analyzation.", \
    "debug" : "Used to view various results for debugging classification methods.", \
    "" : ""}

command_arguments = { \
    "help" : "", \
    "info" : "<command>", \
    "dir" :  "optional : <directory_name>", \
    "config" : "<config_key> optional : <new_value>", \
    "analyze" : "", \
    "classify" : "<list_folder> <category_count>", \
    "debug" : "<list_folder>", \
    "" : ""}

commands = {}

def parse_command(arguments):
    argument_count = len(arguments) - 1
    arguments.pop(0)
    if(argument_count == 0):
        print_help([])
        return
    if(arguments[0] in list(commands.keys())):
        commands[arguments[0]](arguments)
    
def print_help(arguments):
    print(global_variables.header_seperator)
    print(global_variables.header)
    print(global_variables.header_seperator)
    print("\n")
    for command in commands.keys():
        args = command_arguments[command]
        desc = command_descriptions[command]
        print("\t",command,"\t",args,"\n\n\t~",desc, "\n")
    print(global_variables.header_seperator)
    
def print_info(arguments):
    print("yo")
    
def print_dir(arguments):
    file_manager.print_directory_list()
    
def invoke_config(arguments):
    arguments.pop(0) # Remove config command argument 
    if len(arguments) <= 0:
        configuration_data.print_config_file()
    if len(arguments) == 2:
        key = arguments[0]
        value = arguments[1]
        if configuration_data.change_config_file(key, value) == False:
            print("The key '" + key + "' in the config file does not exist!")
            print("Type 'musisort config' to get the full list of keys...")
        else:
            print("Successfully set the key '" + key + "' to the value " + value + "!")
    
def invoke_analyze(arguments):
    file_manager.load_songs()
    return

def invoke_classify(arguments):
    classification_manager.classify_songs(arguments[1], int(arguments[2]))
    return

def invoke_debug(arguments):
    debug_manager.debug()
    return

def on_start():
    global commands
    commands = {"help": print_help, "info" : print_info, "dir" : print_dir, \
                "config" : invoke_config, "analyze" : invoke_analyze, \
                "classify" : invoke_classify, "debug" : invoke_debug}