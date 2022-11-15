import tkinter

import pyautogui as pg
from model.workaround_confirm import confirm
import pyperclip
import json
from sys import exit

config_file = "static/config.json"


def read_commands(file):
    commands = []
    with open(file, "r") as file:
        for command in file:
            command, wait = command.split(";")
            wait = int(wait)
            commands.append((command, wait))
    return commands


class TerminatorLaunch:

    def __init__(self, config_file):
        with open(config_file) as js:
            resol = json.load(js)
            self.native_resolution_x = resol['display_resolution'][0]
            self.native_resolution_y = resol['display_resolution'][1]

        self.eight_terminals = [[1, 1], [3, 1], [5, 1], [7, 1],
                                [1, 3], [3, 3], [5, 3], [7, 3]]

        self.five_terminals = [[1, 1], [3, 1], [6, 1],
                               [2, 3], [6, 3]]

        self.six_terminals = [[1, 1], [3, 1], [5, 1], [7, 1],
                              [2, 3], [6, 3]]

        self.four_terminals = [[2, 1], [6, 1],
                               [2, 3], [6, 3]]

        self.two_terminals = [[4, 1],
                              [4, 3]]

        self.x_step = self.native_resolution_x / 8
        self.y_step = self.native_resolution_y / 4

    def big_terminal(self):
        pg.moveTo(self.x_step, self.y_step)
        pg.hotkey("ctrl", "alt", "t")
        pg.sleep(0.5)
        pg.hotkey("winleft", "up")

    def open_horizontal(self):
        pg.hotkey("ctrl", "shift", "o")

    def open_vertical(self):
        pg.hotkey("ctrl", "shift", "e")

    def open_terminals(self, num_terminals=1):
        # Abrir una sola terminal por defecto
        self.big_terminal()
        final_pos = [[4, 1]]
        if num_terminals >= 2:  # Partirla en 2
            final_pos = self.two_terminals
            self.open_horizontal()
            if (2 < num_terminals <= 4) or num_terminals > 4:  # Partirla hasta en 4
                final_pos = self.four_terminals
                for i, j in self.two_terminals:
                    pg.moveTo(i * self.x_step, j * self.y_step)
                    pg.click()
                    self.open_vertical()

                if 4 < num_terminals <= 8:  # Partirla hasta en 8
                    self.four_terminals.reverse()
                    four_pos = self.four_terminals[(8 - num_terminals):]
                    for i, j in four_pos:
                        pg.moveTo(i * self.x_step, j * self.y_step)
                        pg.click()
                        self.open_vertical()
                    final_pos = self.eight_terminals[:num_terminals]
                    if num_terminals == 5:
                        final_pos = self.five_terminals
                    if num_terminals == 6:
                        final_pos = self.six_terminals
        return final_pos

    def workaround_write(self, text):
        pyperclip.copy(text)
        pg.rightClick()
        pg.press("down")
        pg.press("enter")
        pg.press("enter")

    def put_commands(self, pos, cmd):
        for i in range(len(cmd)):
            pg.moveTo(pos[i][0] * self.x_step, pos[i][1] * self.y_step)
            pg.click()
            text = cmd[i][0]
            self.workaround_write(text)
            if cmd[i][1]:
                ans = confirm()
                if not ans:
                    break
            pg.sleep(1)


def main_from_file(config_file, commands_file):
    term = TerminatorLaunch(config_file)
    commands = read_commands(commands_file)
    positions = term.open_terminals(len(commands))
    term.put_commands(positions, commands)
    del term


def main_from_list(config_file, commands):
    term = TerminatorLaunch(config_file)
    positions = term.open_terminals(len(commands))
    term.put_commands(positions, commands)
    del term
