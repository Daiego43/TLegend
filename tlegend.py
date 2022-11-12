import os
from model.terminator_launch import main_from_list, read_commands, main_from_file
from flask import *
import webview
import threading

tlegend = Flask(__name__)
command_files_folder = "command_files"


@tlegend.route('/', methods=['GET', 'POST'])
def home():  # put tlegendlication's code here
    return render_template("main_menu.html")


########################################################################################################################
# URLS RELATIVAS AL MENU DE GESTION DE ARCHIVOS DE COMANDOS                                                            #
########################################################################################################################
@tlegend.route('/command_files/<selected>', methods=['GET', 'POST'])
def load_files(selected):
    command_files = {}
    for file in os.listdir(command_files_folder):
        command_files[file] = read_commands(os.path.join(command_files_folder, file))
    sel = selected
    if selected == "0":
        sel = next(iter(command_files))
    return render_template("command_files/command_files.html", command_files=command_files, selected=sel)


@tlegend.route('/command_files/option', methods=['GET', 'POST'])
def manage_option():
    selected = request.form['command_file_name']
    option = request.form["submit"]
    if option == "delete":
        os.remove(os.path.join(command_files_folder, selected))
        return load_files(0)
    if option == "edit":
        commands = read_commands(os.path.join(command_files_folder, selected))
        return render_template("command_file_editor/command_editor.html", num_of_cmds=len(commands), commands=commands, filename=selected)
    if option == "run":
        main_from_file(os.path.join(command_files_folder, selected))
        return load_files(selected)


########################################################################################################################
# URLS RELATIVAS AL EDITOR DE COMANDOS                                                                                 #
########################################################################################################################

def determine_num_cmds():
    n = 1
    r = request.form
    if request.form.get("num_of_cmds") is not None:
        n = int(request.form.get("num_of_cmds"))

    if request.form.get("submit") == 'add':
        if request.form.get("num_of_cmds") is not None:
            n = int(request.form.get("num_of_cmds")) + 1
            if n > 8:
                n = 8

    if request.form.get("submit") == "remove":
        if request.form.get("num_of_cmds") is not None:
            n = int(request.form.get("num_of_cmds")) - 1
            if n < 1:
                n = 1
    return n


def save_file():
    pass


def test_commands(commands):
    main_from_list(commands)


def get_commands(num_of_cmds):
    terminator_input = []
    for i in range(num_of_cmds):
        cmd = ""
        cmd_wait = 0
        if request.form.get(f"command{i}") is not None:
            cmd = request.form.get(f"command{i}")
        if request.form.get(f"command{i}_wait") is not None:
            cmd_wait = int(request.form.get(f"command{i}_wait"))
        terminator_input.append((cmd, cmd_wait))
    return terminator_input


@tlegend.route('/command_editor', methods=['GET', 'POST'])
def command_editor():
    filename = request.form.get("filename")
    num_of_cmds = determine_num_cmds()
    commands = get_commands(num_of_cmds)
    if request.form.get("submit") == "test":
        test_commands(commands)
    if request.form.get("submit") == "save":
        with open(os.path.join(command_files_folder, filename), "x") as f:
            for c in commands:
                f.write(str(c[0]) + ";" + str(c[1]) + "\n")
        return load_files("0")
    return render_template("command_file_editor/command_editor.html", num_of_cmds=num_of_cmds, commands=commands, filename=filename)


###################################################################################################################
###################################################################################################################
###################################################################################################################

if __name__ == '__main__':
    def start_server():
        tlegend.run()
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    webview.create_window("Terminator Launcher", "http://127.0.0.1:5000/", width=1225, height=800, resizable=False)
    webview.start()
