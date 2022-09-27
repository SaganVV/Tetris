from tkinter import *
from tkinter import messagebox

class Menu(Tk):
    def __init__(self, width_window, height_window):
        super().__init__()
        self.geometry(f'{width_window}x{height_window}')

        self.but_play_one = Button(self, text="Нажми!",
                       bg='red', command= lambda: self.destroy())
        self.but_play_one.place(relx=0.5,y=100)

    def say_hello(self):
        print("Привет, Tkinter!")
if __name__=='__main__':
    app = Menu(600,600)
    #app.geometry('600x600')
    app.mainloop()
