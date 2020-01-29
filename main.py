from pynput.keyboard import Key, Controller
import time
import configparser
import random

keyboard = Controller()
config = configparser.ConfigParser()
config.read('config.cfg')

cps = float(config['DEFAULT']['typeSpeedInCPM']) / 60 if config['DEFAULT']['typeSpeedInCPM'] else 0.5
baseWait = float(config['DEFAULT']['baseEnterDelay']) if config['DEFAULT']['baseEnterDelay'] else 2
countdown = int(config['DEFAULT']['countdownInSeconds']) if config['DEFAULT']['countdownInSeconds'] else 5 
jitter = float(config['DEFAULT']['typeJitter']) if config['DEFAULT']['typeJitter'] else 0.0
print("cps: {}\nbaseWait: {}\ncountdown: {}\n".format(cps, baseWait, countdown))
print("Move cursor where you want to input text. Running in ")
for i in range(countdown, 0, -1):
    print(i)
    time.sleep(1)

with open('commandscript', 'r') as scriptfile:
    line = scriptfile.readline()
    linewait_multiplier = 1
    while line:
        print("Got: ", end="")
        for c in line:
            print(c, end="")
            if c == "\n":
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                time.sleep(baseWait * linewait_multiplier)
            elif c == "=":
                linewait_multiplier = float(line[1:])
                break
            elif c == "#":
                break
            elif c == "\\":
                keyboard.press(Key.ctrl)
                keyboard.press(line[1])
                keyboard.release(Key.ctrl)
                keyboard.release(line[1])
            else:
                keyboard.press(c)
                keyboard.release(c)
                time.sleep(1 / cps * (1 + random.uniform(-jitter, jitter)))
        line = scriptfile.readline()
        print("Typing next line:\n\t{}".format(line))

print("Typing completed.")
