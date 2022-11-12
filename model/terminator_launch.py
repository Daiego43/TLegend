import tkinter

import pyautogui as pg
from model.workaround_confirm import confirm
import pyperclip
import json
from sys import exit
config_file = "static/config.json"

with open(config_file) as js:
    resol = json.load(js)
    resolucion_nativa_x = resol['display_resolution'][0]
    resolucion_nativa_y = resol['display_resolution'][1]

eight_terminal_positions = [[1, 1], [3, 1], [5, 1], [7, 1],
                            [1, 3], [3, 3], [5, 3], [7, 3]]
five_terminal_positions = [[1, 1], [3, 1], [6, 1],
                           [2, 3], [6, 3]]
six_terminal_positions = [[2, 1], [6, 1],
                          [1, 3], [3, 3], [5, 3], [7, 3]]
four_terminal_positions = [[2, 1], [6, 1],
                           [2, 3], [6, 3]]
two_terminal_positions = [[4, 1],
                          [4, 3]]
x = resolucion_nativa_x / 8
y = resolucion_nativa_y / 4


def big_terminal():
    pg.moveTo(x, y)
    pg.hotkey("ctrl", "alt", "t")
    pg.sleep(0.5)
    pg.hotkey("winleft", "up")


def open_horizontal(): pg.hotkey("ctrl", "shift", "o")


def open_vertical(): pg.hotkey("ctrl", "shift", "e")


def open_terminals(num_terminals=1):
    # Abrir una sola terminal por defecto
    big_terminal()
    final_pos = [[4, 1]]
    if num_terminals >= 2:  # Partirla en 2
        final_pos = two_terminal_positions
        open_horizontal()
        if (2 < num_terminals <= 4) or num_terminals > 4:  # Partirla hasta en 4
            final_pos = four_terminal_positions
            for i, j in two_terminal_positions:
                pg.moveTo(i * x, j * y)
                pg.click()
                open_vertical()

            if 4 < num_terminals <= 8:  # Partirla hasta en 8
                four_terminal_positions.reverse()
                four_pos = four_terminal_positions[(8 - num_terminals):]
                for i, j in four_pos:
                    pg.moveTo(i * x, j * y)
                    pg.click()
                    open_vertical()
                final_pos = eight_terminal_positions[:num_terminals]
                if num_terminals == 5:
                    final_pos = five_terminal_positions
                if num_terminals == 6:
                    final_pos = six_terminal_positions
    return final_pos


def read_commands(file):
    commands = []
    with open(file, "r") as file:
        for command in file:
            command, wait = command.split(";")
            wait = int(wait)
            commands.append((command, wait))
    return commands


def workaround_write(text):
    pyperclip.copy(text)
    pg.rightClick()
    pg.press("down")
    pg.press("enter")
    pg.press("enter")


def put_commands(pos, cmd):
    for i in range(len(cmd)):
        pg.moveTo(pos[i][0] * x, pos[i][1] * y)
        pg.click()
        text = cmd[i][0]
        workaround_write(text)
        if cmd[i][1]:
            ans = confirm()
            if not ans:
                break
        pg.sleep(1)


def main_from_file(file):
    commands = read_commands(file)
    positions = open_terminals(len(commands))
    put_commands(positions, commands)


def main_from_list(commands):
    positions = open_terminals(len(commands))
    put_commands(positions, commands)

