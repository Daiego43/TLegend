# TLegend
A scripting framework used to launch multi-pane terminator sessions with separate apps/processes running

## User guide
### Step 1
Open the config.json file and write the resolution of your main display.
If you have more than two monitors, note that the programme will always run on the monitor you have designated as the primary monitor.

### Step 2
Create a new file called **commands.txt** with the commands you want to execute in different terminals, followed by a semicolon(;) and a 0 or 1, example:

```
echo "hello world";0
source ~/.bashrc;1
```
Writing 0 or 1 is a flag for a confirmation window to show up and wait for the user to click on it to resume or cancel execution

### Step 3
Execute terminator_launch.py and let the magic happen.

## Requirements
Software requirements:
* Python3.8
* GNOME Terminator

Package dependencies:
* PyAutoGUI==0.9.53
* pyperclip==1.8.2

## Upgrades (Coming soon!)
* Using python3.10 will allow the contributors to rewrite a big chunk of code in a more readable way since keywords `match` and `case` are introduced

* The project should be clone and play. Make an executable release friendly to use
