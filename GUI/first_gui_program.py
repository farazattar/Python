import tkinter as tk
window = tk.Tk()
window.title("My First GUI Program with Python")
window.geometry("600x400")
newlabel = tk.Label(text = " Visit My First GUI Program with Python ")
newlabel.grid(column=0,row=0)
window.mainloop()