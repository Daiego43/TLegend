import tkinter as tk
from tkinter.messagebox import askyesno


def confirm():
    root = tk.Tk()
    answer = askyesno(title='Continue', message='press "Yes" to continue')
    root.destroy()
    return answer
