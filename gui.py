from tkinter import *
from tkinter.ttk import *
import threading


class Interface(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        self.progress_bar, self.progress_label, self.question, self.answer1, self.answer2, self.answer3, self.answer4, self.skip = (None,) * 8

    def run(self):
        # Create a new window
        window = Tk()
        # Set the title of the new window
        window.title("Sorteerhoed")
        # Remove the maximise button
        window.resizable(0, 0)

        # Upper part of GUI (header / progess)
        upper_frame = Frame(window)
        can = Canvas(upper_frame, height=100, width=100)
        can.place(x=200, y=200, anchor=NW)
        header = Label(can, text="De magische sorteerhoed(TM)", font=("Arial Bold", 20))
        self.progress_label = Label(can, text="Vraag: x van y", font=("Arial Bold", 12))
        print(self.progress_label)
        self.progress_bar = Progressbar(can, orient=HORIZONTAL, length=250, mode='determinate')

        # Frame seperator
        separator = Separator(window)

        # Lower part of GUI
        lower_frame = Frame(window)
        question = Label(lower_frame, text="Is dit een vraag?", anchor='w', font=("Arial Bold", 12))
        self.answer1 = Button(lower_frame, text="Antwoord1")
        self.answer2 = Button(lower_frame, text="Antwoord2")
        self.answer3 = Button(lower_frame, text="Antwoord3")
        self.answer4 = Button(lower_frame, text="Antwoord4")
        self.skip = Button(lower_frame, text="Sla over")

        # Pack all widgets in the right order
        header.pack(padx=10, pady=10)
        self.progress_label.pack(padx=15, pady=10)
        self.progress_bar.pack()
        can.pack()
        upper_frame.pack(side=TOP)
        separator.pack(pady=15, padx=35, fill='both')
        question.pack(anchor=W, fill='both', pady=(5, 15))
        self.answer1.pack(pady=5)
        self.answer2.pack(pady=5)
        self.answer3.pack(pady=5)
        self.answer4.pack(pady=5)
        self.skip.pack(pady=(5, 20))
        lower_frame.pack(side=TOP)

        # Start the window loop
        window.mainloop()

    def set_progress(self, current, total):
        progress = current / total * 100
        print(self.progress_label)
        self.progress_label = f"Vraag: {current} van de {total}"
        print(self.progress_label)
