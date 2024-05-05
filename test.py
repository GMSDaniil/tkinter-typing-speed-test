from tkinter import *
import datetime
import requests

GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
PINK = "#e2979c"
PURPLE = "#A020F0"




class MainWindow():
    def __init__(self, main) -> None:
        self.main = main

        self.label = Label(self.main, text='Welcome to the Typing-speed test app!', background=YELLOW, padx=50, pady=30)
        self.label.grid(row=0, column=1)

        self.text = "Text"
        self.start_btn = Button(self.main, text='Start', command=self.start)
        self.start_btn.grid(row=1, column=1)


    def generate_text(self):
        response = requests.get('http://metaphorpsum.com/paragraphs/1/4')
        self.text = response.text

    def start(self):
        top = Toplevel(self.main)
        top.config(background=YELLOW)
        top.title("Testing")
        self.main.eval(f'tk::PlaceWindow {str(top)} center')
        top_text = Label(top, text="Type text:", background=YELLOW, padx=50)
        top_text.grid(row=0, column=1)
        text = Label(top, pady=30, width=20, background=YELLOW)
        text.grid(row=1, column=1)
        
        current = Label(top, pady=10, background=YELLOW)
        current.grid(row=2, column=1)
        self.generate_text()
        self.listen_keys(text, current, top, top_text)
        

        

    def listen_keys(self, text, current, top, top_text):
        self.l = 0
        self.r = 20
        self.r = self.change_text(text, current, self.l, self.r)

        temp_time = datetime.datetime.now()
        self.start_time = temp_time.minute*60 + temp_time.second
        
        def keydown(e):
            if e.char == current.cget("text"):
                self.l += 1
                self.r += 1
                if self.l == len(self.text):
                    
                    temp_time = datetime.datetime.now()
                    end_time = temp_time.minute*60 + temp_time.second
                    top_text.config(text='Results:')
                    diff = end_time-self.start_time
                    text.config(text=f'{diff//60} minutes, {diff%60} seconds.')
                    wpm = round(((self.text.count(' ')+1)/diff)*60, 2)
                    sps = len(self.text)//(diff)
                    current.config(text=f'{wpm} words per minute.\n {sps} symbols per second.')
                    
                    exit_btn = Button(top, text='Exit', command=top.destroy)
                    exit_btn.grid(row=3, column=1)
                    return
                self.change_text(text,current, self.l, self.r)
                



        top.bind("<KeyPress>", keydown)
    
    def change_text(self, text, current, l, r):
        if r+1 >= len(self.text):
            r = len(self.text)
            
        text.config(text=self.text[l:r+1])
        current.config(text=self.text[l], fg=PURPLE)


        return r


        

window = Tk()
window.title('Typing Speed')
window.config(background=YELLOW)
window.eval('tk::PlaceWindow . center')
MainWindow(window)


window.mainloop()