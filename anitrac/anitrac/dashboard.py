from tkinter import ttk
import tkinter as tk

class Dashboard(tk.Frame):
    def __init__(self):
        super().__init__()
        self.create_table()
        self.create_widets()

    def create_table(self):
        self.table = ttk.Treeview(self)
        self.yscroll = ttk.Scrollbar(self, orient="vertical")
        self.yscroll.config(command=self.table.yview)
        self.table.config(yscrollcommand=self.yscroll.set, selectmode="extended")
        self.table['columns'] = ['Anilox','Milage', 'Clean Cycles']
         # Phantom Header
        self.table.column("#0", width=0, minwidth=0)
        self.table.heading("#0", text="PID")
        for index, col in enumerate(self.table["columns"]):
            self.table.column(col, anchor="center")
            self.table.heading(col, text=col, anchor="center")
        self.table["show"] = "headings"
        self.table.place(relx=(5/600), rely=(10/400), relheight=(325/400), relwidth=(580/600))
        self.yscroll.place(relx=(585/600), rely=(10/400), relheight=(325/400), relwidth=(15/600))

    def create_widets(self):
        clean = ttk.Button(self, text='Clean Anilox')
        clean.place(relx=(200/600), rely=(350/400), relheight=(40/400), relwidth=(200/600))

