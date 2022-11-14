import tkinter as tk
from tkinter.simpledialog import Dialog


answer = False


class DialogWindow(Dialog):
    def yes(self):
        global answer
        answer = True
        self.destroy()

    def no(self):
        global answer
        answer = False
        self.destroy()

    def buttonbox(self):
        box = tk.Frame(self)
        tk.Button(box, text="Yes", width=10, command=self.yes).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(box, text="No", width=10, command=self.no).pack(side=tk.LEFT, padx=5, pady=5)
        box.pack()


def confirm():
    global answer
    root = tk.Tk()
    root.withdraw()
    DialogWindow(root, title="Continue execution")
    root.destroy()
    return answer