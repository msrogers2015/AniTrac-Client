from tkinter import ttk, messagebox
import tkinter as tk
import requests

class Dashboard(tk.Frame):
    def __init__(self, width, height, server):
        super().__init__()
        self.w = width
        self.h = height
        self.server = server
        self.create_table()
        self.create_widets()
        self.populate_table()

    def create_table(self):
        self.table = ttk.Treeview(self, columns=('Anilox','Milage', 'Clean Cycles'), show='headings')
        self.yscroll = ttk.Scrollbar(self, orient="vertical")
        self.yscroll.config(command=self.table.yview)
        self.table.config(yscrollcommand=self.yscroll.set, selectmode="extended")
         # Phantom Header
        self.table.column("#0", width=0, minwidth=0)
        self.table.heading("#0", text="PID")
        for index, col in enumerate(self.table["columns"]):
            self.table.column(col, anchor="center")
            self.table.heading(col, text=col, anchor="center")
        self.table.place(relx=(5/600), rely=(10/400), relheight=(325/400), relwidth=(580/600))
        self.yscroll.place(relx=(585/600), rely=(10/400), relheight=(325/400), relwidth=(15/600))

        self.table.tag_configure("even", background="#a7a8a9")
        self.table.tag_configure("odd", background="#ffffff")
        self.table.tag_configure('close', background='#fce300')
        self.table.tag_configure('over', background='#c8102e')

    def server_check(self):
        try:
            r = requests.get(self.server)
            if r.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            messagebox.showerror(title='Connection Error', message=f'Connection timeout, could not connect to {self.server}')
            return False
        except Exception as e:
            messagebox.showerror(title='Uncaught Error',message=f'{e.__class__}\n{e}')
            return False

    def create_widets(self):
        clean = ttk.Button(self, text='Clean Anilox')
        clean.place(relx=(50/self.w), rely=(350/self.h), relheight=(40/self.h), relwidth=(200/self.w))
        refresh = ttk.Button(self, text='Refresh Table', command=self.update_table)
        refresh.place(relx=(350/self.w), rely=(350/self.h), relheight=(40/self.h), relwidth=(200/self.w))

    def populate_table(self):
        if self.server_check():
            endpoint = self.server + '/anilox_list'
            data = requests.get(endpoint).json()
            for index, record in enumerate(data):
                if index % 2 == 0:
                    tag = ('even',)
                if index % 2 == 1:
                    tag = ('odd',)
                roller = record['roller']
                milage = record['milage']
                cycles = record['clean_cycles']
                self.table.insert(
                    parent='', index=index, values=[roller, f'{milage:,}', f'{cycles:,}'],tags=tag)
    
    def clear_table(self) -> None:
        """Delete all records from table"""
        for record in self.table.get_children():
            self.table.delete(record)

    def update_table(self) -> None:
        """Clean and repopulate table with search filters"""
        self.clear_table()
        self.populate_table()