import os 
print(os.getcwd)
file_name = "input.txt"

""" Generates an output .txt file. This file will be deleted if it exists!!!
"""
def init():
    if os.path.exists(file_name): 
        os.remove(file_name)

""" Appends content to .txt file automatically inserts new lines 
"""
def write(content): 
    with open(file_name, 'a') as file: 
        file.write(content + "\n")

""" Appends content to .txt file and displays a message to terminal
"""
def write_display(content, display): 
    with open(file_name, 'a') as file: 
        file.write(content + "\n")
    print(display)    
