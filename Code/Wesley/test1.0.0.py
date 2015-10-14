__author__ = 'Wesley'
import tkinter as tk
root = tk.Tk()
root.title("Actuele Vertrektijden")
root.geometry("1360x700")
root.configure(background='yellow')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

top_frame = tk.Frame(root)
top_frame.configure(background='yellow')
top_frame.grid(row=1, column=0)
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_rowconfigure(1, weight=1)

welkom = tk.Label(top_frame, text="Welkom bij NS", bg="yellow", font=("Helvetica", 20), fg="blue")
welkom.grid(row=0, column=0, sticky=tk.N+tk.E+tk.W)

huidige_button = tk.Button(top_frame, text="Huidige Trajecten", fg="white", bg="blue", font=("Helvetica", 12), command=top_frame.destroy)
huidige_button.grid(row=1, column=0, sticky=tk.N+tk.W)
andere_button = tk.Button(top_frame, text="Ander Traject", fg="white", bg="blue", font=("Helvetica", 12), width=2, height=1, command=top_frame.destroy)
andere_button.grid(row=1, column=1, sticky=tk.N+tk.E)

root.mainloop()