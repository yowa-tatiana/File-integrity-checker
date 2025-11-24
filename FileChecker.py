#importing all the important libraries that will be used
import tkinter as tk #using it for a gui interaction
from importlib.resources import open_text
from tkinter import filedialog# for opening a file in the file explora
import os
import hashlib
import time
from datetime import datetime

selected_file = ""   # global variable to store the file path
#Method for selecting file and returning the absolute file path
def upload_file():
    global selected_file
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Text File", "*.txt"), ("All Files", "*.*")]
    )
    #If the file exist , return the file paths
    if file_path:
        selected_file = os.path.abspath(file_path)
    return selected_file
#Method for analyzing the file
def analyze_file():
    global selected_file
    if not selected_file:  # No file uploaded yet
        selected_file = upload_file()

    if not os.path.isfile(selected_file):
        raise FileNotFoundError(f"File not found: {selected_file}")

    stats = os.stat(selected_file)
    filename = os.path.basename(selected_file)
    file_size = stats.st_size
    file_created = datetime.fromtimestamp(stats.st_ctime).isoformat()
    file_modified = datetime.fromtimestamp(stats.st_mtime).isoformat()
#Appeninding the files to the text area
    open_area.delete("1.0", "end")
    open_area.insert("end", f"Filename:\t{filename}\n")
    open_area.insert("end", f"File Size:\t{file_size}\n")
    open_area.insert("end", f"File Created:\t{file_created}\n")
    open_area.insert("end", f"File Modified:\t{file_modified}\n")
    #hash = original_hash()



#Function to calculate the hash value and returning the hash value
def hash_file(filepath):
    with open(filepath, "rb") as f: #Reading the file content
        file_hash = hashlib.sha256()
        while chunk := f.read(4096):
            file_hash.update(chunk)
    return file_hash.hexdigest()

#Function to save the original hash value to a file
def saveHash():
    filename="hash.txt"
    #Checking if the file exist
    if os.path.isfile(filename):
        with open(filename, "a") as f: # appending the existig text if the file exist
            file_hash = hash_file(selected_file)
            f.write(f"{selected_file}\t{file_hash}\n")
    else:                                             #if it does not , it creates a new file
        with open(filename, "x") as f:
            file_hash = hash_file(selected_file)
            f.write(f"{selected_file}\t{file_hash}\n")


#A function for retrieving the hash value from the file and returning the original hash value
def original_hash():
    with open("hash.txt") as f:
       content= f.read()
       for line in content.split('\n'):
           if line.startswith(selected_file + '\t'):
               hash_value=line.split('\t', 1)[1]
               tk.Label(Right_frame, text=f"{hash_value}", bg="grey", justify="left").pack(pady=0.2, padx=10, expand=False)
               return hash_value


#For the generate button , function to be used to write the hash value to the text area
def Generate():
    global selected_file
    if not selected_file:
        selected_file = upload_file()   # only ask if no file chosen

    hashvalue = hash_file(selected_file)
    open_area.insert("end", f"\nSHA-256 Hash:\n{hashvalue}\n")
    saveHash()
    hash= original_hash()
   # tk.Label(Right_frame, text=f"{hash}", bg="grey", justify="left").pack(pady=0.2,padx=10,expand=False)
    if hash==hashvalue:
        open_area.insert("end","The hash values are the same , the file has not been corrupted")
    else:
        open_area.insert("end","The hash values aren't the same , the file has not been corrupted")

####Doing the Gui
root = tk.Tk() #Creating the window
root.title("File Integrity Checker") #Setting the title
root.geometry("7000x4000") #Setting the size

#We will use a frame to set all our widgets
Top_frame = tk.Frame(root,bg='grey',height=50)
Top_frame.pack(side="top",fill="x")

#Left
left_frame = tk.Frame(root,bg='grey',height=150)
left_frame.pack(side="left",fill="y")

#Right
Right_frame=tk.Frame(root,bg='grey',height=1500,width=450)
Right_frame.pack_propagate(False)
Right_frame.pack(side="right",fill="none")

#Bottom
bottom_frame = tk.Frame(root, bg="grey", height=30)
bottom_frame.pack(side="bottom", fill="x")
#Center
center_frame = tk.Frame(root, bg="white")
center_frame.pack(expand=True,fill="both")

#Add Widgets to frames

#Top bar
tk.Label(Top_frame, text="File Integrity Verification Tool", bg="grey",
         fg="white", font=("Arial", 14, "bold")).pack(pady=10)

# Left menu (buttons)
tk.Button(left_frame, text="Upload File &Analyze", command=analyze_file).pack(pady=10, fill="x", padx=10)
#tk.Button(left_frame, text="Analyze",command=analyze_file).pack(pady=5, fill="x", padx=10)
tk.Button(left_frame, text="Generate Report",command=Generate).pack(pady=5, fill="x", padx=10)

#Center area (Text box)
open_area = tk.Text(center_frame, wrap="word", font=("Consolas", 10))
open_area.pack(expand=True, fill="both", padx=10, pady=10)

#Right side (maybe for info or actions)
tk.Label(Right_frame, text="File Details", bg="grey", font=("Arial", 10, "bold")).pack(pady=5)
tk.Label(Right_frame, text=f"Hash:\n", bg="grey", justify="left").pack(pady=5)

#Bottom status bar
status_label = tk.Label(bottom_frame, text="Ready", bg="#2c3e50", fg="white")
status_label.pack(fill="x")
#For the display
root.mainloop()