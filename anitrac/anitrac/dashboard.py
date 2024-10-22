from tkinter import ttk, messagebox
import tkinter as tk
import requests
import json

class Dashboard(tk.Frame):
    def __init__(self, width, height, server):
        super().__init__()
        self.w = width
        self.h = height
        self.server = server
        self.create_table()
        self.create_widets()
        self.update_style()
        self.populate_table()

    def create_table(self):
        self.table = ttk.Treeview(self, show='headings')
        self.table['columns'] = ('Anilox','Milage', 'Clean Cycles')
        self.yscroll = ttk.Scrollbar(self, orient="vertical")
        self.yscroll.config(command=self.table.yview)
        self.table.config(yscrollcommand=self.yscroll.set, selectmode="extended")
        self.current_sort = 'roller'
        self.sort_type = 'asc'
        # Create headers so that each header can run a sort function
        self.table.heading('Anilox', text='Anilox', command= lambda: self.order_table('roller'))
        self.table.heading('Milage', text='Milage', command= lambda: self.order_table('milage'))
        self.table.heading('Clean Cycles', text='Clean Cycles', command= lambda: self.order_table('clean_cycles'))
        # Center aling data in rows
        for index, col in enumerate(self.table["columns"]):
            self.table.column(col, anchor="center")
        self.table.place(relx=(5/600), rely=(10/400), relheight=(325/400), relwidth=(580/600))
        self.yscroll.place(relx=(585/600), rely=(10/400), relheight=(325/400), relwidth=(15/600))

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
        clean = ttk.Button(self, text='Clean Anilox', command=self.clean_anilox)
        clean.place(relx=(50/self.w), rely=(350/self.h), relheight=(40/self.h), relwidth=(200/self.w))
        refresh = ttk.Button(self, text='Refresh Table', command=self.update_table)
        refresh.place(relx=(350/self.w), rely=(350/self.h), relheight=(40/self.h), relwidth=(200/self.w))
    
    def clean_anilox(self) -> None:
        try:
            record = self.table.item(self.table.focus())["values"][0]
            if messagebox.askokcancel(title='Clean anilox', message=f'Do you want to clean {record}'):
                if requests.post(self.server+'/clean', json={'roller': record}).status_code == 200:
                    messagebox.showinfo(title='Anilox Cleaned', message=f'Milage has been resert for anilox {record}')
                    self.update_table()
                else:
                    messagebox.showerror(title='Cleaning Error', message=f'Anilox {record} could not be cleaned.')
        except IndexError:
            messagebox.showwarning(title='Invalid Selection', message='Please select an anilox to clean.')

    def populate_table(self):
        if self.server_check():
            endpoint = self.server + f'/anilox_list?sort={self.current_sort}&method={self.sort_type}'
            data = requests.get(endpoint).json()
            self.get_limits()
            for index, record in enumerate(data):
                roller = record['roller']
                milage = record['milage']
                cycles = record['clean_cycles']
                if index % 2 == 0 and int(milage) < self.warning_limit:
                    tag = ('even',)
                elif index % 2 == 1 and int(milage) < self.warning_limit:
                    tag = ('odd',)
                elif self.warning_limit < int(milage) < self.limit:
                    tag = ('close',)
                else:
                    tag = ('over',)
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
        #self.table.config(columns=('Anilox','Footage', 'Clean Cycles'))
        for index, col in enumerate(self.table["columns"]):
            self.table.column(col, anchor="center")
            self.table.heading(col, text=col, anchor="center")

    def order_table(self, method):
        if method == self.current_sort and self.sort_type == 'asc':
            self.sort_type = 'desc'
        elif method == self.current_sort and self.sort_type == 'desc':
            self.sort_type = 'asc'
        else:
            self.sort_type = 'asc'
            self.current_sort = method
        self.update_table()

    def get_limits(self):
        with open('data\\config.json', 'r') as file:
            json_data = json.load(file)
            self.limit = int(json_data['milage_limit'])
            self.warning_limit = float(json_data['close_multiplier']) * self.limit
    
    def update_style(self):
        with open('data\\theme.json', 'r') as file:
            json_data = json.load(file)
            style = ttk.Style()
            self.table.tag_configure("even", background=json_data['even'])
            self.table.tag_configure("odd", background=json_data['odd'])
            self.table.tag_configure('close', background=json_data['close'])
            self.table.tag_configure('over', background=json_data['over'])
            style.map('Treeview', background=[('selected', json_data['selected'])])
