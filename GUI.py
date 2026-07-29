import datetime
import time
import json
import os
import sys
import platform
import tkinter as tk

system = platform.system()

# Paths
if system == "Windows":
    appdata_dir = os.path.join(os.environ["APPDATA"], "Mona")
else:
    appdata_dir = os.path.join(os.path.expanduser("~"), ".mona")

os.makedirs(appdata_dir, exist_ok=True)
settings_path = os.path.join(appdata_dir, "settings.json")


# Create the page
root = tk.Tk()
root.title("Mona")
root.geometry("300x400")

if os.path.exists(settings_path):
    with open(settings_path, "r") as f:
        data = json.load(f)
else:
    data = {"hour": 0, "minute": 0, "AMPM": "", "shutdown_enabled": True, "shutdown_minutes": 30, "notify_frequency": 10}

# Functions
def save_clicked():
    global isSetUp
    hour = set_hour.get()
    minute = set_min.get()
    ampm = set_ampm.get()
    shutdown = set_shutdown.get()
    shutdown_minutes = shut_min.get()
    notify_frequency = frequency_min.get()


    data["hour"] = hour
    data["minute"] = minute
    data["AMPM"] = ampm
    data["shutdown_enabled"] = shutdown
    data["shutdown_minutes"] = shutdown_minutes
    data["notify_frequency"] = notify_frequency

    with open(settings_path, "w") as f:
        json.dump(data, f)

    saved_label = tk.Label(root, text = "Saved!")
    saved_label.grid(row = 3, column = 1, padx = 5, pady = 5)
    root.after(5000, saved_label.grid_forget)

# Set up / Change settings

# Build frames
time_frame = tk.Frame(root)
time_frame.grid(row = 0, column = 0, columnspan = 3, pady = 10)

shutdown_frame = tk.Frame(root)
shutdown_frame.grid(row = 1, column = 0, columnspan = 3, pady = 10)

# Bed time text
bedtime_text = tk.Label(time_frame, text = "Set Bed Time", width = 20)
    
# Create hour spinbox
set_hour = tk.IntVar(value = 12)
hour_spinbox = tk.Spinbox(
    time_frame, from_ = 1, to = 12, textvariable = set_hour, width = 5, wrap = True
)

# Create minute spinbox
set_min = tk.IntVar(value = 00)
min_spinbox = tk.Spinbox(
    time_frame, from_ = 0, to = 59, textvariable = set_min, format = "%02.0f", width = 5, wrap = True
)

# Create AM / PM spinbox
set_ampm = tk.StringVar(value = "AM")
ampm_spinbox = tk.Spinbox(
    time_frame, values = ("AM", "PM"), textvariable = set_ampm, width = 5, wrap = True
)

# Create shutdown checkbox
set_shutdown = tk.BooleanVar(value = True)
shutdown_checkbox = tk.Checkbutton(shutdown_frame, text = "Force shutdown if not asleep", variable = set_shutdown)

# Create shutdown minutes spinbox and label
shut_min_label = tk.Label(shutdown_frame, text = "Minutes until shutdown")

shut_min = tk.IntVar(value = 00)
shut_min_spinbox = tk.Spinbox(
    shutdown_frame, from_ = 0, to = 60, textvariable = shut_min, format = "%02.0f", width = 5, wrap = True
)

# Create frequency minutes spinbox and label
frequency_label = tk.Label(shutdown_frame, text = "Frequency of notifications past bedtime")

frequency_min = tk.IntVar(value = 00)
frequency_min_spinbox = tk.Spinbox(
    shutdown_frame, from_ = 0, to = 60, textvariable = frequency_min, format = "%02.0f", width = 5, wrap = True
)

# Create save button
save_button = tk.Button(
    root, text = "Save", command = save_clicked
)

# Place inside the grid
bedtime_text.grid(row = 0, column = 1, padx = 5,pady = 5)
hour_spinbox.grid(row = 1, column = 0, padx = 5, pady = 5)
min_spinbox.grid(row = 1, column = 1, padx = 5, pady = 5)
ampm_spinbox.grid(row = 1, column = 2, padx = 5, pady = 5)

shutdown_checkbox.pack(in_ = shutdown_frame)
shut_min_label.pack()
shut_min_spinbox.pack()
frequency_label.pack()
frequency_min_spinbox.pack()

save_button.grid(row = 2, column = 1, padx = 5, pady = 5)


root.mainloop()