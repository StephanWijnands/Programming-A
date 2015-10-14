__author__ = 'Wesley'
import tkinter as tk
import xmltodict
root = tk.Tk()
root.title("Actuele Vertrektijden")
root.geometry("1360x700")
root.configure(background='yellow')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

def raise_frame(frame):
    frame.tkraise()

def verwerk_xml():
    """Hier word de XML stations.xml ingelezen"""
    bestand = open('stations.xml', 'r')
    xml_string = bestand.read()
    return xmltodict.parse(xml_string)

def vertrektijden(stations_dict):
    """Hier worden alle vertrektijden opgehaald vauit het XML bestand stations.xml"""
    for actuele_vertrek_tijd in stations_dict['ActueleVertrekTijden']['VertrekkendeTrein']:
        vertrektijd = actuele_vertrek_tijd['VertrekTijd']
        uur_minuten = (vertrektijd.split('T')[1].split(':')[0:2])
        print(uur_minuten[0] + ':' + uur_minuten[1])

def vertrekspoor(stations_dict):
    """Hier worden alle sporen van vertrek opgehaald vauit het XML bestand stations.xml"""
    for spoor in stations_dict['ActueleVertrekTijden']['VertrekkendeTrein']:
        spoortje = str(spoor['VertrekSpoor'])
        vertrek_zonder_wijziging = (spoortje.split('\'')[7])
        print(vertrek_zonder_wijziging)

def tijd_vertraging(stations_dict):
    for vertraging in stations_dict['ActueleVertrekTijden']['VertrekkendeTrein']:
        if str(vertraging['VertrekVertragingBoolean'] == True):
            tijd = str(vertraging['VertrekVertragingTekst'])
            print(tijd)

stations_dict = verwerk_xml()
test2 = vertrektijden(stations_dict)

f2 = tk.Frame(root)
f2.configure(background='yellow')
f2.grid(row=0, column=0, stick=tk.NSEW)
f2.grid_columnconfigure(0, weight=1)
f2.grid_rowconfigure(0, weight=1)

top_frame = tk.Frame(root)
top_frame.configure(background='yellow')
top_frame.grid(row=0, column=0, stick=tk.NSEW)
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_rowconfigure(0, weight=1)

welkom = tk.Label(top_frame, text="Welkom bij NS", bg="yellow", font=("Helvetica", 20), fg="blue")
welkom.grid(row=0, sticky=tk.E+tk.N+tk.W, pady=100)

huidige_button = tk.Button(top_frame, text="Huidige Trajecten", fg="white", bg="blue", font=("Helvetica", 12), width=20, height=50, command=lambda:raise_frame(f2))
huidige_button.grid(row=0, column=0, sticky=tk.N+tk.W, pady=300, padx=400)
ga_terug = tk.Button(f2, text="Ga Terug", fg="white", bg="blue", font=("Helvetica", 12), width=20, height=50, command=lambda:raise_frame(top_frame))
ga_terug.grid(row=0, column=0, sticky=tk.S+tk.W, pady=300, padx=400)
andere_button = tk.Button(top_frame, text="Ander Traject", fg="white", bg="blue", font=("Helvetica", 12), width=20, height=50,)
andere_button.grid(row=0, column=0, sticky=tk.N+tk.E, pady=300, padx=400)
test = tk.Label(f2, text=test2, fg="blue", bg="yellow", font=("Helevetica", 20))
test.grid(row=0, column=0, sticky=tk.N)

raise_frame(top_frame)
root.mainloop()