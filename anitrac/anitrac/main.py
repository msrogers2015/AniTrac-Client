from tkinter import ttk, messagebox
import tkinter as tk
import dashboard
import json
import requests

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.w = 600
        self.h = 400
        x = (self.winfo_screenwidth() // 2) - (self.w // 2)
        y = (self.winfo_screenheight() // 2) - (self.h // 2)
        self.minsize(self.w, self.h)
        self.geometry(f'{self.w}x{self.h}+{x}+{y}')
        self.title('AniTrac - Dashboard')
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.server = self.get_server()
        self.set_style()
        self.select_server()
        self.create_notebook()
        self.create_menu()
        self.bind('<Configure>', self.on_resize)
        self.mainloop()

    def get_server(self):
        with open('data\\config.json', 'r') as file:
            json_data = json.load(file)
            return json_data['server']

    def on_resize(self, event):
        h = self.winfo_height()
        fontsize = h//40
        self.style.configure('.', font=(None, fontsize))
        self.style.configure('Treeview.Heading', font=(None, fontsize))
        self.style.configure('Treeview', rowheight=h//20)

    def set_style(self) -> None:
        self.style = ttk.Style()
        #style.theme_use('alt')
        self.style.configure('TNotebook.Tab', width=self.winfo_screenwidth())
        self.style.configure('server.TButton', font=(None, 14))
        self.style.configure('Treeview', rowheight=50)

    def create_notebook(self) -> None:
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', side='top', expand=True)
        self.dashboard = dashboard.Dashboard(self.w, self.h, self.server)
        frame2 = ttk.Frame(self.notebook)
        self.dashboard.pack()
        frame2.pack()
        self.notebook.add(self.dashboard, text='Dashboard')
        self.notebook.add(frame2, text='Record Job')

    def create_menu(self):
        menubar = tk.Menu(self)
        file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file)
        file.add_command(label='Current Server', command=self.current_server)
        file.add_command(label='Check Server', command=self.check_server)
        file.add_cascade(label='Select Server', command=self.select_top.deiconify)
        help = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=help)
        help.add_command(label="Help")
        help.add_command(label='About Anitrac')
        self.config(menu=menubar)

    def current_server(self):
        messagebox.showinfo(title='Current Server', message=self.server)

    def select_server(self):
        self.select_top = tk.Toplevel(self)
        self.select_top.protocol("WM_DELETE_WINDOW", self.select_top.withdraw)
        w=400
        h=125
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.select_top.minsize(w,h)
        self.select_top.geometry(f'{w}x{h}+{x}+{y}')
        self.current = ttk.Label(self.select_top, text='Current Server: ' + self.server, font=(None, 14), anchor='center')
        self.current.pack(fill='x')
        self.new_server = ttk.Entry(self.select_top, font=(None, 14))
        self.new_server.pack(fill='x', padx=25, pady=5)
        save = ttk.Button(self.select_top, text='Save Server', style='server.TButton', command=lambda: self.save_server(self.new_server.get()))
        save.pack(fill='x', padx=100, pady=5, ipady=7)
        self.select_top.withdraw()

    def save_server(self, server):
        if server != '':
            if messagebox.askokcancel(title='Save Server', message=f'Save {server} as new server?'):
                self.server = server
                with open('data\\config.json', 'r') as file:
                    json_data = json.load(file)
                json_data['server'] = self.server
                with open('data\\config.json', 'w') as file:
                    file.write(json.dumps(json_data, indent=4))
                self.new_server.delete(0, 'end')
                self.current.config(text=f'Current Server: {self.server}')
                self.select_top.withdraw()
                self.dashboard.server = server
                return True
        self.select_top.focus_force()
        return False

    def check_server(self):
        try:
            r = requests.get(self.server)
            if r.status_code == 200:
                messagebox.showinfo(title='Valid Connection', message=f'You are connected to {self.server}')
        except requests.exceptions.ConnectionError:
            messagebox.showerror(title='Connection Error', message=f'Connection timeout, could not connect to {self.server}')
        except Exception as e:
            messagebox.showerror(title='Uncaught Error',message=f'{e.__class__}\n{e}')

    def on_close(self) -> None:
        try:
            self.destroy()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = App()