from tkinter import *

def start_gui():
    window = Tk()
    window.title("Sorteerhoed")
    window.geometry("750x650")
    header = Label(window, text="De magische sorteerhoed(TM)", font=("Arial Bold", 50))
    header.grid(column=0, row=0)

    window.mainloop()

