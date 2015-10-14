import requests
import xmltodict
from tkinter import *
auth_details = ('wesley.cool@live.nl', '3yWaal5WME4-i1Lx31gAxDe_coUrKYJvr9e7fqofdz1ilOEsO4DQuQ')
response = requests.get('http://webservices.ns.nl/ns-api-avt?station=Utrecht', auth=auth_details)
root = Tk()
root.title("Actuele Vertrektijden")
root.geometry("1360x700")
root.configure(background='yellow')

def schrijf_xml(reponse):
    bestand = open('stations.xml', 'w')
    bestand.write(str(response.text))
    bestand.close()

def verwerk_xml():
    bestand = open('stations.xml', 'r')
    xml_string = bestand.read()
    return xmltodict.parse(xml_string)

def print_stationsnamen(stations_dict):
    for actuele_vertrek_tijd in stations_dict['ActueleVertrekTijden'] ['VertrekkendeTrein']:
        print(actuele_vertrek_tijd['RitNummer'], actuele_vertrek_tijd['VertrekTijd'])

stations_dict = verwerk_xml()
#print_stationsnamen(stations_dict)
label1 = Label(root, text="Welkom bij NS", bg="yellow", font=("Helvetica", 20), fg="blue")
label1.pack()
huidige_button = Button(text="Huidige Trajecten", fg="white", bg="blue", font=("Helvetica", 12), padx=20)
#button = Button(insert, text="10p").grid(row=2, column=1)
huidige_button.pack()
#if huidige_button is pressed:
    #root.destroy()
root.mainloop()
