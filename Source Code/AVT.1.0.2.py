__author__ = 'mostafa'

import requests
import datetime
import xmltodict
import tkinter as tk

class NSAPI():
    def __init__(self):

        self.auth_details = ('wesley.cool@live.nl', '3yWaal5WME4-i1Lx31gAxDe_coUrKYJvr9e7fqofdz1ilOEsO4DQuQ')
        self.details = ('wesley.cool@live.nl', '3yWaal5WME4-i1Lx31gAxDe_coUrKYJvr9e7fqofdz1ilOEsO4DQuQ')

    def get_stations(self):
        """   return stations """
        tmp_lijst = []
        try:
            response = requests.get('http://webservices.ns.nl/ns-api-stations', auth=self.auth_details)
            data = xmltodict.parse(response.text)
            for station in data['stations']['station']:
                tmp_lijst += [station['name']]
        except:
            print("Error! There is no response from network!")
        return tmp_lijst

    def get_avt(self, statoin='Utrecht'):
        """      return actuele vertrek tijden   """

        # een verbinding maken met ns server
        tmp_dict = {}
        try:
            response = requests.get('http://webservices.ns.nl/ns-api-avt?station=' + statoin, auth=self.auth_details)
            data = xmltodict.parse(response.text)
            tmp_dict = data['ActueleVertrekTijden']['VertrekkendeTrein']
        except:
            print('Error! There is no response from network')
        return tmp_dict


class GuiAVT(tk.Frame):
    def __init__(self, root):

        self.root = root
        self.bc = '#FFFF00'
        self.fg = 'white'

        self.root.configure(background=self.bc)
        self.top_frame = tk.Frame(root, background=self.bc)
        self.button_frame = tk.Frame(root, background=self.bc)
        self.canvas = tk.Canvas(self.top_frame, background=self.bc)
        self.avt_frame = tk.Frame(self.canvas, background=self.bc)
        self.vsb = tk.Scrollbar(self.top_frame, orient='vertical', command=self.canvas.yview)


        self.top_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.button_frame.grid(row=1, column=0, sticky=tk.NE)
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.avt_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.vsb.grid(row=0, column=1, sticky=tk.NSEW)

        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.avt_frame.grid_rowconfigure(0, weight=1)
        self.avt_frame.grid_columnconfigure(0, weight=1)
        self.vsb.grid_rowconfigure(0, weight=1)
        self.vsb.grid_columnconfigure(1, weight=1)


        self.canvas.create_window((0,0), window=self.avt_frame, anchor='nw', tag='self.avt_frame')
        self.avt_frame.bind('<Configure>', self.onFrameConfigure)


    def show(self, station='Utrecht'):
        self.add_to_button_frame()
        self.show_avt(station)


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def make_row(self, row, column, text, bc, fg='black'):
        font = ("Helvetica", 12)
        label = tk.Label(self.avt_frame, text=text, font=font,padx=10, foreground=fg,
                          wraplength=250, justify=tk.LEFT, background=bc, pady=5,anchor='w')
        label.grid(row=row, column=column, sticky=tk.NSEW)

    def show_avt(self, station):
        ns = NSAPI()
        avt = ns.get_avt(station)
        # Add labels to the canvas frame [=topframe]
        # The items we need to show
        dict_details = ['VertrekTijd', 'VertrekVertragingTekst', 'EindBestemming', 'VertrekSpoor',
                        'RouteTekst', 'TreinSoort', 'Vervoerder']
        headers = ['Tijd', 'Vertraging', 'Naar', 'Spoor', 'Via', 'Reisdetails', 'Vervoerder']
        # create the headers
        for c, item in enumerate(headers):
            self.make_row(0, c, item, "orange")
        # Create the Train items
        even = False
        for r, value in enumerate(avt):
            if even:
                even = False
                bc = 'lightgreen'
            else:
                even = True
                bc = 'lightblue'
            for c, item in enumerate(dict_details):
                if item in value:
                    if item == 'VertrekTijd':
                        try:
                            tijd = datetime.datetime.strptime(value[item].split("+")[0], "%Y-%m-%dT%H:%M:%S")
                            text = tijd.strftime("%H:%M")
                        except:
                            print('Hmm...Error for VertrekTijd!')
                            text = ""
                        self.make_row(r+1, c, text, bc)
                    elif item == 'VertrekVertragingTekst':
                        self.make_row(r+1, c, value[item], bc, 'red')
                    elif item == 'VertrekSpoor' :
                        try:
                            if value[item]['@wijziging'] == 'true':
                                fg = 'red'
                            else:
                                fg = 'black'
                            text = value[item]['#text']
                        except:
                            print("Hmm..Error for VertrekSpoor!")
                            text = ""
                            fg = 'black'

                        self.make_row(r+1, c, text,bc, fg)
                    elif item == 'TreinSoort':
                        text = value[item]
                        if 'ReisTip' in value:
                            text += ', ' + value['ReisTip']
                        if 'Opmerkingen' in value:
                            text += ', ' + value['Opmerkingen']['Opmerking']
                        self.make_row(r+1, c, text, bc)
                    else:
                        self.make_row(r+1, c, value[item], bc)
                else:
                    self.make_row(r+1, c, ' ', bc)

    def add_to_button_frame(self):
        button = {0: self.return_to_start, 1: self.search_another, 2: self.stop}
        button_text = ['Terug naar het begin scherm', 'Ander station opvragen', 'Stoppen']
        # default Font
        font = ("Helvetica", 12, 'bold')
        bc = 'blue'
        for i, item in enumerate(button_text):
            if item == 'Stoppen': bc = 'red'
            b = tk.Button(self.button_frame, text=item, font=font,
                               background=bc, foreground=self.fg, height=2, command=button[i])
            b.grid(row=0, column=i, padx=10, pady=20)

    def return_to_start(self):
        self.destroy_me()
        start = StartScreen(self.root)
        start.show()

    def search_another(self):
        self.destroy_me()
        andere = GuiAndere(self.root)
        andere.show()

    def stop(self):
        self.root.destroy()

    def destroy_me(self):
        self.top_frame.destroy()
        self.button_frame.destroy()


class SearchStation():
    def __init__(self, text):
        global stations_lijst

        # self.text = text
        self.stations = []
        self.letters = set()
        for station in stations_lijst:
            if station[0:len(text)].lower() == text.lower():
                if station not in self.stations:
                    # self.stations.add(station)
                    self.stations += [station]
                if len(text) < len(station):
                    self.letters.add(station[len(text)].lower())

    def resterende_stations(self):
        self.stations.sort()
        return self.stations

    def resterende_letters(self):
        return self.letters


class GuiAndere(tk.Frame):
    def __init__(self, root):

        # content of the textbox
        self.entry_content = tk.StringVar()
        # content of the Error Label (look add_entry function)
        global error_content
        error_content = tk.StringVar()
        self.root = root
        # set the background color
        self.bc = '#3333FF'
        # set the foreground color (text colors)
        self.fg = 'white'
        root.configure(background=self.bc)

        self.keyboard_frame = tk.Frame(root, background='purple')
        self.top_fram = tk.Frame(root, background=self.bc)
        self.entry_frame = tk.Frame(self.top_fram, backgroun=self.bc,
                                    padx=40, pady=5)
        self.list_frame = tk.Frame(self.top_fram, backgroun=self.bc, padx=30, pady=5)

        self.top_fram.grid(row=0, column=0, sticky=tk.NSEW)
        self.entry_frame.grid(row=0, column=0, sticky=tk.N+tk.W, pady=20)
        self.list_frame.grid(row=0, column=1, sticky=tk.N+tk.W, pady=20)
        self.keyboard_frame.grid(row=1, column=0, pady=40, sticky=tk.NS)

        self.top_fram.grid_rowconfigure(0, weight=1)
        self.top_fram.grid_columnconfigure(0, weight=1)
        self.entry_frame.grid_rowconfigure(0, weight=1)
        self.entry_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(1, weight=1)
        self.keyboard_frame.grid_rowconfigure(1, weight=1)
        self.keyboard_frame.grid_columnconfigure(0, weight=1)

    def show(self):
        self.add_entry()
        self.add_keyboard()

    def on_keyboard_click(self, name):
        # if keypress is %R remove the last char
        if name == '%R':
            self.entry_content.set(self.entry_content.get()[:-1])
        # if keypress is %T destroy the frames and show main page
        elif name == '%T':
            # Return to first page
            self.show_start()
        # else enter the keypress into the textbox
        else:
            self.entry_content.set(self.entry_content.get() + name)

    def on_result_click(self, text):
        self.destroy_me()
        avt = GuiAVT(self.root)
        avt.show(text)

    def on_text_change(self, *args):
        # Search for stations
        # if textbox is not empty: search the station
        if len(self.entry_content.get()) > 0:
            # make the text to all uppercase
            self.entry_content.set(self.entry_content.get().upper())
            search = SearchStation(self.entry_content.get())
            # show the stations
            self.add_stations(search.resterende_stations())
            # disable unsuported keys on the keyboard
            letters = search.resterende_letters()
            # special characters in ascii and their button index as dict key
            sp = {26:39, 27:45, 28: 47, 29:32}
            for index, button in enumerate(self.keyboard_frame.winfo_children()[0:30]):
                # Get the button char using ascii code
                # index 0 t/m 25 are A t/m Z
                if index < 26 and not chr(index+97) in letters:
                    button.config(state='disable')
                # index 26 t/m 29 are speciale characters
                elif index >= 26 and not chr(sp[index]) in letters:
                        button.config(state='disable')
                else:
                    button.config(state='normal')
        # if texbox is empty remove oud search results (buttons) from list_frame
        else:
            for button in self.list_frame.grid_slaves():
                button.destroy()
            # enable all keys
            for button in self.keyboard_frame.winfo_children()[0:30]:
                button.config(state='normal')

    def add_stations(self, stations):
        # default Font
        font = ("Helvetica", 14)
        # First remove all buttons from this frame
        for button in self.list_frame.grid_slaves():
            button.destroy()
        # Add Buttons (stations) to the list_frame
        for index, station in enumerate(stations):
            button = tk.Button(self.list_frame, text=station, width=30, height=2,
                               font=font, background=self.bc, foreground=self.fg,
                               command=lambda name=station: self.on_result_click(name))
            button.grid(row=index+1, column=0, sticky=tk.NSEW, pady=5)

    def add_entry(self):
        global error_content
        # default Font
        font = ("Helvetica", 16)
        # Add a label
        label1 = tk.Label(self.entry_frame, text='Station:', font=font,
                          background=self.bc, foreground=self.fg)
        label1.grid(row=0, column=0, sticky=tk.NW, pady=20)
        # Use trace methode to check if the text in the texbox is changed
        self.entry_content.trace('w', self.on_text_change)
        # Add a entry(Text Box)
        textbox1 = tk.Entry(self.entry_frame, font=font, width=20, background='lightgreen',
                            textvariable=self.entry_content)
        textbox1.grid(row=1, column=0, sticky=tk.NW + tk.E)

        # # Add a lable for showing Error's in the App
        # label2 = tk.Label(self.entry_frame, text='Station2', font=font,
        #                   background=self.bc, foreground=self.fg)
        # label2.grid(row=2, column=0, sticky=tk.NW, pady=20)

    def add_keyboard(self):
        # default Font
        font = ("Helvetica", 12, 'bold')
        # default column and row
        c = 0
        r = 0
        # Add A t/m Z
        for i in range(65, 91):
            if c > 11:
                c = 0
                r += 1
            button = tk.Button(self.keyboard_frame, text=chr(i), width=4, height=2, disabledforeground='white',
                               background='yellow', font=font, command=lambda name=chr(i): self.on_keyboard_click(name))
            button.grid(row=r, column=c, sticky=tk.NSEW, padx=10, pady=10)
            c += 1
        # Add " ' "
        button = tk.Button(self.keyboard_frame, text="'", width=4, height=2, disabledforeground='white',
                           background='yellow', font=font, command=lambda name="'": self.on_keyboard_click(name))
        button.grid(row=r, column=c, sticky=tk.NSEW, padx=10, pady=10)
        c += 1
        # Add " - "
        button = tk.Button(self.keyboard_frame, text='-', width=4, height=2, disabledforeground='white',
                           background='yellow', font=font, command=lambda name='-': self.on_keyboard_click(name))
        button.grid(row=r, column=c, sticky=tk.NSEW, padx=10, pady=10)
        c += 1
        # Add " / "
        button = tk.Button(self.keyboard_frame, text='/', width=4, height=2, disabledforeground='white',
                           background='yellow', font=font, command=lambda name='/': self.on_keyboard_click(name))
        button.grid(row=r, column=c, sticky=tk.NSEW, padx=10, pady=10)
        c += 1
        # Add Space
        button = tk.Button(self.keyboard_frame, text='Space', width=12, height=2, disabledforeground='white',
                           background='yellow', font=font, command=lambda name=' ': self.on_keyboard_click(name))
        button.grid(row=r, column=c, columnspan=3, sticky=tk.NSEW, padx=10, pady=10)
        c += 3
        # Add "Clear"
        button = tk.Button(self.keyboard_frame, text='Clear', width=12, height=2,
                           background='yellow', font=font, command=lambda name='%R': self.on_keyboard_click(name))
        button.grid(row=r, column=c, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)
        c += 2
        # Add "terug"
        button = tk.Button(self.keyboard_frame, text='Treug', width=12, height=2,
                           background='red', font=font, command=lambda name='%T': self.on_keyboard_click(name))
        button.grid(row=r, column=c, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)

    def show_start(self):
        self.destroy_me()
        start = StartScreen(self.root)
        start.show()

    def destroy_me(self):
        self.keyboard_frame.destroy()
        self.top_fram.destroy()


class StartScreen(tk.Frame):
    def __init__(self, root):

        self.root = root
        root.configure(background='yellow')

        self.top_frame = tk.Frame(root, background='yellow')
        self.top_frame.grid(row=0, column=0, sticky=tk.E+tk.W)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(0, weight=1)

        self.button_frame = tk.Frame(root, background='yellow')
        self.button_frame.grid(row=1, column=0, pady=40)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)

    def show_huidige(self):
        self.destroy_me()
        avt = GuiAVT(self.root)
        avt.show()

    def search_andere(self):
        self.destroy_me()
        andere = GuiAndere(self.root)
        andere.show()

    def show(self):
        welkom = tk.Label(self.top_frame, text="Welkom bij NS", bg="yellow", font=("Helvetica", 30), fg="blue", anchor='center')
        welkom.grid(row=0, column=0, pady=0, sticky=tk.EW)

        huidige_button = tk.Button(self.button_frame, text="HUIDIGE TRAJECTEN", fg="white", bg="blue",
                                   font=("Helvetica", 15, 'bold'), width=30, height=5, command=self.show_huidige)
        huidige_button.grid(row=0, column=0, pady=20, padx=50)
        andere_button = tk.Button(self.button_frame, text="ANDER TRAJECT", fg="white", bg="blue",
                                  font=("Helvetica", 15, 'bold'), width=30, height=5, command=self.search_andere)
        andere_button.grid(row=0, column=1, pady=20, padx=50)

        stop_button = tk.Button(self.button_frame, text="STOPPEN", fg="white", bg="red",
                                  font=("Helvetica", 15, 'bold'), width=30, height=5, command=self.root.destroy)
        stop_button.grid(row=1, column=0, columnspan=2, pady=20, padx=50)

    def destroy_me(self):
        self.top_frame.destroy()
        self.button_frame.destroy()


def main():
    ns = NSAPI()
    global stations_lijst
    stations_lijst = ns.get_stations()
    root = tk.Tk()
    root.title("Actuele Vertrektijden")
    root.geometry('1024x768')
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    start = StartScreen(root)
    start.show()
    root.mainloop()

if __name__ == "__main__":
    main()
