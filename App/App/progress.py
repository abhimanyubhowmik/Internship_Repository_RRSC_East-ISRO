    
from tkinter import *
import tkinter.ttk as ttk
import threading

class Progress():
    """ threaded progress bar for tkinter gui """
    def __init__(self, parent, row, column, columnspan):
        self.parent = parent
        self.progressbar = ttk.Progressbar(self.parent, orient=HORIZONTAL,
                                           mode="determinate",
                                           length= 100)
        self.progressbar.grid(row=row + 1, column=column,
                              columnspan=columnspan, sticky="we")
        self.progress_label = ttk.Label(self.parent, text='Initialising...')
        self.progress_label.grid(column=column, row=row, columnspan=columnspan)
        self.thread = threading.Thread()
        self.thread.__init__(target=self.progressbar)
        self.thread.start()

    def pb_stop(self):
        """ stops the progress bar """
        if not self.thread.is_alive():
            self.progressbar.stop()
            self.progressbar.grid_forget()
            self.progress_label.grid_forget()

    def pb_text(self,text):
        """ stops the progress bar """
        if not self.thread.is_alive():
            self.progress_label.config(text = text)

    def pb_value(self, value):
        """ stops the progress bar and fills it """
        if not self.thread.is_alive():
            self.progressbar['value'] = value
            self.parent.update_idletasks()
