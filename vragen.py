import codecs
import errno
import random
import os
import datetime

question_data = None
total_questions = 0
answered_questions = 0
points = {"SE": 0, "FICT": 0, "IOT": 0, "BDAM": 0}


def load_question_data():
    global total_questions
    # Vind alle bestanden in de map 'questions' en sla ze op als een lijst in het variabel files
    files = os.listdir('questions')
    # maak een lege dictionary en sla deze op in 'd'
    d = dict()
    # Voor elke file in files voer je de onderstaande code uit (BDAM, FICT etc)
    for file in files:
        # Sla de naam van het bestand - de laatste 4 karakters op in specialisatie. Bijv: BDAM.txt -> BDAM
        specialisation = file[:-4]
        # Open het bestand als f
        with codecs.open(f"questions/{file}", "r", "utf-8") as f:
            # Lees alle data in het bestand en split vervolgens het bestand op in regels. En sla deze lijst met regels op in 'lines'
            lines = f.read().split("\n")
            # Voeg deze specialisatie als key toe aan de 'd' dictionary, en als value een lege dictionary.
            d[specialisation] = dict()
            # Voor elke regel in de lijst met regels uit dit bestand voer de volgende code uit
            for line in lines:
                # Split een regel weer verder op, en sla dit op in 'splitted'. Hier komt een lijst uit met stukken van een regel gesplitst door een tab: \t
                splitted = line.split("\t")
                # Haal de eerste waarde uit de splitted lijst en sla deze op in 'vraag', vervolgens verwijder je deze waarde uit de lijst 'splitted'. Nu hebben we de vraag uit de regel gehaald, en hebben we alleen nog de antwoorden in 'splitted zitten'
                question = splitted.pop(0)
                total_questions += 1
                # Maak een lege lijst aan en sla deze op in 'tuples' (in dit geval een antwoord samen met het punten aantal)
                tuples = []
                # Voor elke waarde (split) in 'splitted' voer de volgende code uit. (Let op, in 'splitted' zitten nu nog alleen maar antwoorden, want de vraag hebben we er net uitgehaald.
                for split in splitted:
                    #Splits de vraag op bij het ';' teken en sla deze lijst op in answer
                    answer = split.split(';')
                    # Voeg aan tuples de eerste waarde en tweede waarde in answer toe (als een tuple)
                    tuples.append((answer[0], int(answer[1])))
                    # Voeg aan de dictionary bij de key 'specialisation' de dictionary toe met als key de vraag en als value de antwoorden die opgeslagen staan in tuples.
                    d[specialisation].update({question: tuples})
    # Return de dictionary die we net hebben gemaakt met alle questions
    return d


def get_question():
    global question_data
    #
    if question_data is None:
        question_data = load_question_data()
    for specialisation in question_data:
        if question_data[specialisation] == {}:
            del question_data[specialisation]
            break
    if not question_data:
        return None
    specialisation = random.choice(list(question_data))
    question = random.choice(list(question_data[specialisation]))
    answers = question_data[specialisation][question]
    return question, answers, specialisation


def question_answered(question, point, specialisation):
    global answered_questions
    del question_data[specialisation][question]
    points[specialisation] += point
    answered_questions += 1


def result_export(name):
    mkdir_p('uitslagen/')
    export_date = datetime.datetime.now()
    exportFile = open(f"uitslagen/Resultaten - {name} - {export_date.strftime('%d-%m-%Y %H:%M')}.txt", "w")
    exportFile.write("UITSLAG - TEST - ")
    exportFile.write(str(export_date.strftime("%d-%m-%Y %H:%M")) + "\n\nPunten\n")
    items = list(points.items())
    items.reverse()
    for x, y in items:
        exportFile.write(x + ": " + str(y) + "\n")
    
    exportFile.write("\nDe specalisatie met het hoogste aantal punten past het beste volgens onze test bij jou!")
    
    exportFile.close()


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
