from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import vragen


class Interface:
    def __init__(self):
        self.current_question = None
        self.current_answers = None
        self.current_specialisation = None
        # Create a new window
        self.window = Tk()
        # Set the title of the new window
        self.window.title("Sorteerhoed")
        # Set fixed window size
        self.window.geometry("600x450")
        # Set window icon
        self.window.iconbitmap("magichat.ico")
        # Remove the maximise button
        self.window.resizable(0, 0)

        # Upper part of GUI (header / progess)
        upper_frame = Frame(self.window)
        can = Canvas(upper_frame, height=100, width=100)
        can.place(x=200, y=200, anchor=NW)
        header = Label(can, text="De magische sorteerhoed(TM)", font=("Arial Bold", 20))
        self.progress_label = Label(can, text="Vraag: x van y", font=("Arial Bold", 12))
        self.progress_bar = Progressbar(can, orient=HORIZONTAL, length=250, mode='determinate')

        # Frame seperator
        separator = Separator(self.window)

        # Lower part of GUI
        self.lower_frame = Frame(self.window)
        self.question = Label(self.lower_frame, wrap=500, text="Is dit een vraag?", anchor='center', font=("Arial Bold", 12))
        self.answer1 = Button(self.lower_frame, text="Antwoord1", command=lambda: self.submit_answer(self.answer1))
        self.answer2 = Button(self.lower_frame, text="Antwoord2", command=lambda: self.submit_answer(self.answer2))
        self.answer3 = Button(self.lower_frame, text="Antwoord3", command=lambda: self.submit_answer(self.answer3))
        self.answer4 = Button(self.lower_frame, text="Antwoord4", command=lambda: self.submit_answer(self.answer4))
        self.skip = Button(self.lower_frame, text="Sla over", command=lambda: self.load_question())
        self.start = Button(self.lower_frame, text="Starten", command=lambda: self.start_test())
        # Results part of GUI
        self.top_result = Label(self.lower_frame, text="De specialisatie die het beste bij jou past is: #ERROR#")
        self.description = Label(self.lower_frame, wrap=400, text="Beschrijving..........................................Beschrijving..........................................Beschrijving..........................................Beschrijving", anchor='center')
        self.result_tree = Treeview(self.lower_frame, height=4, selectmode="none", columns=("points", "percent"))
        self.result_tree['columns'] = ("points", "percent")

        self.result_tree.column("#0", width=90, anchor='center')
        self.result_tree.heading("#0", text="Specialisatie")

        self.result_tree.column("points", width=60, anchor='center')
        self.result_tree.heading("points", text="Punten")

        self.result_tree.column("percent", width=240, anchor='center')
        self.result_tree.heading("percent", text="Hoeveel % past deze specialisatie bij mij?")

        self.name_frame = Frame(self.lower_frame)
        self.name_label = Label(self.name_frame, text="Vul je naam in om deze uitslag op te slaan:")
        self.name_entry = Entry(self.name_frame)
        self.name_button = Button(self.name_frame, text="Opslaan", command=lambda: self.save_results())
        self.save_confirm = Label(self.lower_frame, text="Je uitslag is opgeslagen!")

        #INIT
        header.pack(padx=10, pady=10)
        self.progress_label.pack(padx=15, pady=10)
        self.progress_bar.pack()
        self.question.pack(anchor=W, fill='both', pady=(5, 15), padx=35)
        can.pack()
        upper_frame.pack(side=TOP)
        separator.pack(pady=15, padx=35, fill='both')
        self.lower_frame.pack(side=TOP)

        #Welcome screen
        self.start.pack()
        self.skip.pack_forget()
        self.question["text"] = "Je krijgt verschillende vragen, met 3 of 4 antwoorden. Kies het antwoord dat het beste bij jouw past!"
        self.progress_label["text"] = "Ben je ready? Je kan starten met de test!"
        self.answer1.pack_forget()
        self.answer2.pack_forget()
        self.answer3.pack_forget()
        self.answer4.pack_forget()

        # Start the window loop
        self.window.mainloop()

    def set_progress(self):
        current = vragen.answered_questions
        total = vragen.total_questions
        progress = current / total * 100
        self.progress_label['text'] = f"Vraag: {current} van de {total}"
        self.progress_bar['value'] = progress
        self.progress_bar.update()

    def show_results(self, points):
        self.question.pack_forget()
        self.answer1.pack_forget()
        self.answer2.pack_forget()
        self.answer3.pack_forget()
        self.answer4.pack_forget()
        self.skip.pack_forget()

        points = {k: v for k, v in sorted(points.items(), key=lambda item: item[1])}
        for specialisatie in points:
            percent = round((points[specialisatie] / 15) * 100, 2)
            self.result_tree.insert('', '0', text=specialisatie, iid=specialisatie, values=(points[specialisatie], str(percent) + "%"))

        self.top_result['text'] = f"De specialisatie die het beste bij jou past is: {list(points.keys())[-1]}"
        self.description['text'] = "Beschrijving..........................................Beschrijving..........................................Beschrijving..........................................Beschrijving" # TODO Automatically show the right description for every specialisation
        self.result_tree.selection_set(list(points.keys())[-1])
        self.progress_label['text'] = "Alle vragen zijn afgerond"
        self.progress_bar['value'] = 100

        self.top_result.pack(pady=(0, 15))
        self.description.pack(pady=(0, 15))
        self.result_tree.pack()

        self.name_frame.pack(side=LEFT, expand=True)
        self.name_label.pack(side=LEFT, padx=5)
        self.name_entry.pack(side=LEFT, fill=X, padx=5)
        self.name_button.pack(in_=self.name_frame, side=LEFT, padx=5, pady=15)


    def start_test(self):
        self.start.pack_forget()
        
        # Pack all widgets in the right order
        self.answer1.pack(pady=5)
        self.answer2.pack(pady=5)
        self.answer3.pack(pady=5)
        self.answer4.pack(pady=5)
        self.skip.pack(pady=(5, 20))

        # Show the first random question
        self.load_question()

        # Set the initial progress
        self.set_progress()

    def load_question(self):
        question_tuple = vragen.get_question()
        if question_tuple is None:
            print("Finished", vragen.points)
            self.show_results(vragen.points)
            return
        question = question_tuple[0]
        answers = question_tuple[1]
        self.current_specialisation = question_tuple[2]
        self.current_answers = answers
        self.current_question = question
        self.answer1['text'] = answers[0][0]
        self.answer2['text'] = answers[1][0]
        if len(answers) > 2:
            self.answer3['text'] = answers[2][0]
            if not self.answer3.winfo_ismapped():
                self.answer3.pack(after=self.answer2, pady=5)
        else:
            self.answer3.pack_forget()
        if len(answers) > 3:
            self.answer4['text'] = answers[3][0]
            if not self.answer4.winfo_ismapped():
                self.answer4.pack(after=self.answer3, pady=5)
        else:
            self.answer4.pack_forget()
        self.question['text'] = question

    def save_results(self):
        vragen.result_export(self.name_entry.get())
        messagebox.showinfo(master=self.window, title="All set!", message="Je resultaten zijn opgeslagen!")

    def submit_answer(self, button):
        answer = button['text']
        for answer_tuple in self.current_answers:
            if answer_tuple[0] == answer:
                vragen.question_answered(self.question['text'], answer_tuple[1], self.current_specialisation)
                self.set_progress()
                self.load_question()
                return
