from tkinter import ttk, messagebox
import tkinter as tk
import requests
from ttkwidgets.autocomplete import AutocompleteCombobox

class Record(tk.Frame):
    def __init__(self, width, height, server):
        super().__init__()
        self.w = width
        self.h = height
        self.server = server
        self.create_widgets()

    def create_widgets(self):
        w, h = [225, 30]
        self.milage = ttk.Entry(self)
        mile_label = ttk.Label(self, text='Milage', anchor='e')
        save_btn = ttk.Button(self, text='Record', command=self.record_milage)
        self.milage.place(relx=115/self.w, rely=15/self.h, relwidth=200/self.w, relheight=h/self.h)
        mile_label.place(relx=15 / self.w, rely=15 / self.h, relwidth=100 / self.w, relheight=h / self.h)
        save_btn.place(relx=350/self.w, rely=15/self.h, relwidth=200/self.w, relheight=h/self.h)
        self.entries = []
        rollers = self.anilox_list()
        row1, row2, col1, col2, offset = [65, 95, 50, 325, 60]
        for i in range(10):
            label = ttk.Label(self, text=f'Unit {i + 1}', anchor='center')
            entry = AutocompleteCombobox(self, completevalues=rollers)
            if i % 2 == 0:
                label.place(relx=col1/self.w, rely=(row1 + (offset* (i//2)))/self.h, relwidth=w/self.w, relheight=h/self.h)
                entry.place(relx=col1/self.w, rely=(row2 + (offset* (i//2)))/self.h, relwidth=w/self.w, relheight=h/self.h)
            else:
                label.place(relx=col2 / self.w, rely=(row1 + (offset * (i // 2))) / self.h, relwidth=w / self.w, relheight=h / self.h)
                entry.place(relx=col2 / self.w, rely=(row2 + (offset * (i // 2))) / self.h, relwidth=w / self.w, relheight=h / self.h)
            entry.bind('<FocusOut>', self.verify_data)
            self.entries.append(entry)

    def on_resize(self, font_size):
        for entry in self.entries:
            entry.config(font=(None, font_size))
        self.milage.config(font=(None, font_size))

    def anilox_list(self) -> list:
        if self.server_check():
            endpoint = self.server + '/rollers'
            data = requests.get(endpoint).json()
            return data

    def server_check(self):
        try:
            r = requests.get(self.server)
            if r.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            messagebox.showerror(title='Connection Error',
                                 message=f'Connection timeout, could not connect to {self.server}')
            return False
        except Exception as e:
            messagebox.showerror(title='Uncaught Error', message=f'{e.__class__}\n{e}')
            return False

    def verify_data(self, event):
        roller = event.widget.get()
        if roller not in self.anilox_list() and roller != '':
            event.widget.delete(0, 'end')
            messagebox.showwarning(title='Invalid Anilox', message='Please select an anilox from the dropdown list.')

    def record_milage(self):
        rollers = []
        for unit in self.entries:
            if unit.get() != '':
                rollers.append(unit.get())
        if self.milage.get() == '':
            messagebox.showwarning('Invalid Milage', 'Please provide a milage.')
            return False
        data = {
            'milage' : self.milage.get(),
            'rollers' : rollers,
        }
        endpoint = self.server + '/add_milage'
        outcome = requests.post(endpoint, json=data)
        if outcome.status_code == 200:
            messagebox.showinfo(title='Milage Recorded', message='Milage has been updated for selected rollers.')
        else:
            messagebox.showerror(title=f'Error {outcome.status_code}', message=f'The following error occured:{outcome.json()['message']}')