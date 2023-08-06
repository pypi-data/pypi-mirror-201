"""This is a docstring
"""

import sys
from musisort import configuration_data, global_variables
import musisort.command_manager as cmd_manager
import musisort.file_manager as file_manager

def main():
    on_start()
    
    cmd_manager.parse_command(sys.argv)
    
    exit()

def on_start():
    global_variables.on_start()
    cmd_manager.on_start()
    file_manager.on_start()
    configuration_data.on_start()

if __name__ == "__main__":
    main()