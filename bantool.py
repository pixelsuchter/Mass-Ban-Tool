import json
import os
import subprocess
import sys
import time

try:
    import pyautogui
except ImportError:
    # installs pyautogui module if it is missing, needed for pressing buttons
    print('Installing pyautogui')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
    import pyautogui


pyautogui.PAUSE = 0.001
pyautogui.FAILSAFE = True

try:
    with open("config.json", "r") as f:
        config = json.load(f)
except (OSError, json.JSONDecodeError):
    print("Config file does not exist or corrupt, creating default config\n")
    with open("config.json", "w") as f:
        config = {"command_delay": 0.05, "delay_every_n_commands": (5, 100), "commands": ["/ban", "/block", "/unban", "/unblock"]}
        json.dump(config, f)


cmd_delay = config["command_delay"]
cmd_pause, batch_size = config["delay_every_n_commands"]

commandlist = config["commands"]


def execute_command(command: str):
    if os.path.isfile("unban.txt"):
        start = time.time()
        amount = 0
        with open("namelist.txt", "r") as f:
            for name in f:
                pyautogui.write("{cmd} {name}".format(cmd=command, name=name))
                amount += 1
                time.sleep(cmd_delay)
                time.sleep(cmd_pause if not amount % batch_size else 0.00001)
            pyautogui.press("enter")
            pyautogui.write("-DONE-")
        print("command took {time} seconds for {num} names".format(num=amount, time=time.time() - start))
    else:
        print("namelist.txt does not exist!")


while True:
    for num, cmd in enumerate(commandlist):
        print("{command}  ({number})".format(command=cmd, number=num))

    try:
        decision = int(input("\n"))
        print("You have 10 seconds to click into the chat window!")
        time.sleep(10)
        execute_command(commandlist[decision])

    except (IndexError, ValueError):
        sys.exit(0)
