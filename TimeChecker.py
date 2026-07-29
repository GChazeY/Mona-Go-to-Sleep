import datetime
import time
import os
import json
import random
import sys
import platform
import subprocess

system = platform.system()

if system == "Windows":
    from win11toast import toast

# Paths
if system == "Windows":
    appdata_dir = os.path.join(os.environ["APPDATA"], "Mona")
else:
    appdata_dir = os.path.join(os.path.expanduser("~"), ".mona")

os.makedirs(appdata_dir, exist_ok=True)
settings_path = os.path.join(appdata_dir, "settings.json")

# Load bed time settings
if not os.path.exists(settings_path):
    sys.exit()

with open(settings_path, "r") as f:
    data = json.load(f)

hour = data["hour"]
minute = data["minute"]
ampm = data["AMPM"]
shutdown = data["shutdown_enabled"]
shutdown_delay = data["shutdown_minutes"]
notify_frequency = data["notify_frequency"]

# Get current time
now = datetime.datetime.now()
current_minutes = now.hour * 60 + now.minute

# Convert saved bedtime to 24 hr form
if ampm == "PM" and hour != 12:
    hour24 = hour + 12
elif ampm == "AM" and hour == 12:
    hour24 = 0
else:
    hour24 = hour

bedtime_minutes = hour24 * 60 + minute
remainder_minutes = (bedtime_minutes - 5) % (24*60)
minutes_since_bedtime = (current_minutes - bedtime_minutes) % (24 * 60)
shutdown_minutes = (bedtime_minutes + shutdown_delay) % (24*60)

# Warning messages

five_minutes = ["Hey, let's wrap things up soon.", "You should save your progress today.", "Why not save your work for tomorrow?", "Are you almost done for the day?"]

bedtime_first = ["You must be tired after today. Let's go to sleep!", "You have a big day tomorrow. Let's go to sleep.", "Let's rest up and prepare for tomorrow.",
           "Let's call it a day and go to bed.", "Aren't you tired? Let's call it a day and go to sleep.", "Let's go to sleep for the day."]

bedtime_repeated = ["Hey, look. You need your rest to function tomorrow.", "Moe to peep... zzz...", "Do you really need to be doing that now?  You should rest for the day.", 
                    "Trust me, tomorrow morning, you won't be able to leave your bed.", "It's been " + str(minutes_since_bedtime) + " minutes already.  Can't we go to sleep already?"]

forced_shutdown = ["You left me with no other choice.  I'm shutting down your computer.",  "Hey! It's bedtime! If you won't listen, I'll make you!", 
                   "Your eyes are practically falling out. Shutting down!", "Look, I'm doing this for your own good. Go to bed!", "And the power cord slipped.  Bed time!"]


# Check and notify (Windows)
if system == "Windows":
    if current_minutes == remainder_minutes:
        message = random.randint(0, len(five_minutes)-1)
        toast("Mona", five_minutes[message], duration="short")
    elif current_minutes == bedtime_minutes:
        message = random.randint(0, len(bedtime_first)-1)
        toast("Mona", bedtime_first[message], duration="short")
    elif current_minutes > bedtime_minutes and minutes_since_bedtime < shutdown_delay and (minutes_since_bedtime % notify_frequency == 0):
        message = random.randint(0, len(bedtime_repeated)-1)
        toast("Mona", bedtime_repeated[message], duration="short")
    elif minutes_since_bedtime >= shutdown_delay and minutes_since_bedtime < shutdown_delay + (8*60) and shutdown:
        message = random.randint(0, len(forced_shutdown)-1)
        toast("Mona", forced_shutdown[message], duration="short")
        subprocess.run(["shutdown", "-s", "-t", "0"])

# Check and notify (Linux)
elif system == "Linux":
    if current_minutes == remainder_minutes:
        message = random.randint(0, len(five_minutes)-1)
        subprocess.run(["notify-send", "Mona", five_minutes[message]])
    elif current_minutes == bedtime_minutes:
        message = random.randint(0, len(bedtime_first)-1)
        subprocess.run(["notify-send", "Mona", bedtime_first[message]])
    elif current_minutes > bedtime_minutes and minutes_since_bedtime < shutdown_delay and (minutes_since_bedtime % notify_frequency == 0):
        message = random.randint(0, len(bedtime_repeated)-1)
        subprocess.run(["notify-send", "Mona", bedtime_repeated[message]])
    elif minutes_since_bedtime >= shutdown_delay and minutes_since_bedtime < shutdown_delay + (8*60) and shutdown:
        message = random.randint(0, len(forced_shutdown)-1)
        subprocess.run(["notify-send", "Mona", forced_shutdown[message]])
        subprocess.run(["sudo", "systemctl", "poweroff", "--force"])

# Check and notify (macOS)
elif system == "Darwin":
    if current_minutes == remainder_minutes:
        message = random.randint(0, len(five_minutes)-1)
        subprocess.run(["osascript", "-e", f'display notification "{five_minutes[message]}" with title "Mona"'])
    elif current_minutes == bedtime_minutes:
        message = random.randint(0, len(bedtime_first)-1)
        subprocess.run(["osascript", "-e", f'display notification "{bedtime_first[message]}" with title "Mona"'])
    elif current_minutes > bedtime_minutes and minutes_since_bedtime < shutdown_delay and (minutes_since_bedtime % notify_frequency == 0):
        message = random.randint(0, len(bedtime_repeated)-1)
        subprocess.run(["osascript", "-e", f'display notification "{bedtime_repeated[message]}" with title "Mona"'])
    elif minutes_since_bedtime >= shutdown_delay and minutes_since_bedtime < shutdown_delay + (8*60) and shutdown:
        message = random.randint(0, len(forced_shutdown)-1)
        subprocess.run(["osascript", "-e", f'display notification "{forced_shutdown[message]}" with title "Mona"'])
        subprocess.run(["sudo", "shutdown", "-h", "now"])

