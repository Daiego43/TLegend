from tkinter.messagebox import askyesno


def confirm():
    answer = askyesno(title='Continue', message='press "Yes" to continue')
    return answer
