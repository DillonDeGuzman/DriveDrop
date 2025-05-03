import os
import shutil
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog, messagebox

def get_recent_photos(sd_card_path, days=1):
    now = datetime.now()
    cutoff = now - timedelta(days=days)
    recent_photos = []

    for root, _, files in os.walk(sd_card_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(root, file)
                modified_time = datetime.fromtimestamp(os.path.getmtime(full_path))
                if modified_time > cutoff:
                    recent_photos.append(full_path)

    return recent_photos

def copy_to_local(photo_paths, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    for path in photo_paths:
        shutil.copy2(path, destination_folder)

def browse_sd_card():
    path = filedialog.askdirectory(title="Select SD Card Folder")
    if path:
        sd_path_var.set(path)

def browse_dest_folder():
    path = filedialog.askdirectory(title="Select Destination Folder")
    if path:
        dest_path_var.set(path)

def process_photos():
    sd_path = sd_path_var.get()
    dest_path = dest_path_var.get()
    days = 1 if day_option.get() == "1" else 7

    if not sd_path or not dest_path:
        messagebox.showerror("Error", "Please select both SD card and destination folders.")
        return

    recent_photos = get_recent_photos(sd_path, days)

    if not recent_photos:
        messagebox.showinfo("No Photos", f"No recent photos found in the past {days} day(s).")
        return

    copy_to_local(recent_photos, dest_path)
    messagebox.showinfo("Success", f"Copied {len(recent_photos)} photo(s) to {dest_path}.")

# GUI Setup
root = tk.Tk()
root.title("DriveDrop")

sd_path_var = tk.StringVar()
dest_path_var = tk.StringVar()
day_option = tk.StringVar(value="1")

tk.Label(root, text="SD Card Folder:").grid(row=0, column=0, sticky='w')
tk.Entry(root, textvariable=sd_path_var, width=50).grid(row=0, column=1)
tk.Button(root, text="Browse", command=browse_sd_card).grid(row=0, column=2)

tk.Label(root, text="Destination Folder:").grid(row=1, column=0, sticky='w')
tk.Entry(root, textvariable=dest_path_var, width=50).grid(row=1, column=1)
tk.Button(root, text="Browse", command=browse_dest_folder).grid(row=1, column=2)

tk.Label(root, text="Time Range:").grid(row=2, column=0, sticky='w')
tk.Radiobutton(root, text="Past Day", variable=day_option, value="1").grid(row=2, column=1, sticky='w')
tk.Radiobutton(root, text="Past Week", variable=day_option, value="7").grid(row=2, column=1)

tk.Button(root, text="Copy Photos", command=process_photos, bg="lightblue").grid(row=3, column=1, pady=10)

root.mainloop()
