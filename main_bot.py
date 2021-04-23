import tkinter as tk
import betting as bet
from tkinter import messagebox
import threading as t


class Main:

    def __init__(self):
        self.bot = bet.Bot()

    def quitBot(self, canvas):
        self.bot.stopBot()
        canvas.quit()

    def startBot(self, lossStreak=8):

        if str.isdigit(lossStreak):
            if int(lossStreak) <= 0:
                tk.messagebox.showwarning(title="Warning", message="Please Enter an Integer Higher than 0")
            else:
                tk.messagebox.showwarning(title="Reminder", message="Don't Forget To Log In")
                botThread = t.Thread(target=(self.bot.runBot), args=(int(lossStreak), ))
                botThread.start()

        else:
            tk.messagebox.showwarning(title="Warning", message="Please Enter an Integer")

        
    def draw(self, canvas): 
            
        #Set up Canvas
        canvas.title("Crash Bot")
        canvas.minsize(width=250, height=250)
        canvas.resizable(0, 0)

        #Make bottom frame
        bottomFrame = tk.Frame(canvas,width=100, height=100)
        bottomFrame.grid(row=1, column=0)

        #Description
        tk.Label(canvas, text=" Enter the Desired Loss Streak ").grid(row=0, column=0, padx=5, pady=5)

        #Entry Field
        desiredLossField = tk.Entry(bottomFrame, width=10)
        desiredLossField.grid(row=0, column=0, padx=5, pady=5)

        #Button
        tk.Button(bottomFrame, text="Submit",
                command=lambda: self.startBot(desiredLossField.get())).grid(row=0, column=1)
        tk.Button(bottomFrame, text="Quit",
                command=lambda: self.quitBot(canvas)).grid(row=1, column=1, pady=5)


#Set Up

canvas = tk.Tk()
program = Main()

program.draw(canvas)
canvas.mainloop()
