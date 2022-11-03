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
    """
    Enseña los archivos de comandos disponibles y su contenido.
    Desde aqui se permite crear, editar, borrar y ejecutar archivos de comandos
    :param selected:
    :return:
    """
    command_files = {}
    for file in os.listdir(command_files_folder):
        command_files[file] = read_commands(os.path.join(command_files_folder, file))

    sel = selected
    if selected == "0":
        sel = next(iter(command_files))
    return render_template("command_files/command_files.html", command_files=command_files, selected=sel)


@tlegend.route('/command_files/option', methods=['GET', 'POST'])
def manage_option():
    command_files = {}
    print(request.form)
    selected = request.form['command_file_name']
    option = request.form["submit"]
    for file in os.listdir(command_files_folder):
        command_files[file] = read_commands(os.path.join(command_files_folder, file))

    print(option)
    if option == "delete":
        # TODO: Borrar el archivo que se selecciono
        return load_files(selected)
    if option == "edit":
        # TODO: Abrir el editor de comandos para un archivo
        return load_files(selected)
    if option == "run":
        main_from_file(os.path.join(command_files_folder, selected))
        return load_files(selected)

########################################################################################################################
# URLS RELATIVAS AL EDITOR DE COMANDOS                                                                                 #
########################################################################################################################


@tlegend.route('/command_editor/<num>', methods=['GET', 'POST'])
def command_editor(num):
    # define the number of commands
    num = int(num)
    nums = [i for i in range(1, num + 1)]
    add = num + 1 if num < 8 else 8
    dec = num - 1 if num > 1 else 1

    return render_template("command_file_editor/command_editor_v2.html", numcommands=nums, add=add, dec=dec, num=num)


@tlegend.route('/processing_commands', methods=['GET', 'POST'])
def process_form():
    try:
        result = ''
        maxcmds = int(request.form['numcmds']) + 1
        commands = []
        for i in range(1, maxcmds):
            command = request.form[f'command_{i}']
            command_opt = request.form[f'command_{i}_wait']
            commands.append((command, int(command_opt)))
        main_from_list(commands)
    except Exception as e:
        print(e)
    return command_editor('1')


if __name__ == '__main__':
    def start_server():
        tlegend.run()


    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    webview.create_window("Terminator Launcher", "http://127.0.0.1:5000/", width=1225, height=800, resizable=False)
    webview.start()
