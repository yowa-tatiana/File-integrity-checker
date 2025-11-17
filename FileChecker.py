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

#Function to calculate the hash value and returning the hash value
def hash_file(filepath):
    with open(filepath, "rb") as f: #Reading the file content
        file_hash = hashlib.sha256()
        while chunk := f.read(4096):
            file_hash.update(chunk)
    return file_hash.hexdigest()
#For the generate button , function to be used to write the hash value to the text area
def Generate():
    global selected_file
    if not selected_file:
        selected_file = upload_file()   # only ask if no file chosen

    hashvalue = hash_file(selected_file)
    open_area.insert("end", f"\nSHA-256 Hash:\n{hashvalue}\n")
    tk.Label.destroy(Right_frame)
    #tk.Label(Right_frame, text=f"Hash:\nGenerated)", bg="grey", justify="left").pack(pady=5)
    return hashvalue

####Doing the Gui
root = tk.Tk() #Creating the window
root.title("File Integrity Checker") #Setting the title
root.geometry("700x400") #Setting the size

#We will use a frame to set all our widgets
Top_frame = tk.Frame(root,bg='grey',height=50)
Top_frame.pack(side="top",fill="x")

#Left
left_frame = tk.Frame(root,bg='grey',height=150)
left_frame.pack(side="left",fill="y")

#Right
Right_frame=tk.Frame(root,bg='grey',height=150)
Right_frame.pack(side="right",fill="y")

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
tk.Label(Right_frame, text=f"Hash:\n(Not Generated Yet)", bg="grey", justify="left").pack(pady=5)

#Bottom status bar
status_label = tk.Label(bottom_frame, text="Ready", bg="#2c3e50", fg="white")
status_label.pack(fill="x")
#For the display
root.mainloop()