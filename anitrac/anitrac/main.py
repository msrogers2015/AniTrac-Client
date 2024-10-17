from tkinter import ttk
import tkinter as tk
import dashboard

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        w = 600
        h = 400
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.minsize(w,h)
        self.geometry(f'{w}x{h}+{x}+{y}')
        self.title('AniTrac - Dashboard')
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.set_style()
        self.create_notebook()
        self.create_menu()
        self.bind('<Configure>', self.on_resize)
        self.mainloop()
    
    def on_resize(self, event):
        h = self.winfo_height()
        fontsize = h//40
        self.style.configure('.', font=(None, fontsize))
        self.style.configure('Treeview.Heading', font=(None, fontsize))

    def set_style(self) -> None:
        self.style = ttk.Style()
        #style.theme_use('alt')
        self.style.configure('TNotebook.Tab', width=self.winfo_screenwidth())
        self.style.configure('TNotebook.Tab', sticky='we')

    def create_notebook(self) -> None:
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', side='top', expand=True)
        self.dashboard = dashboard.Dashboard()
        frame2 = ttk.Frame(self.notebook)
        self.dashboard.pack()
        frame2.pack()
        self.notebook.add(self.dashboard, text='Dashboard')
        self.notebook.add(frame2, text='Record Job')

    def create_menu(self):
        menubar = tk.Menu(self)
        file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file)
        file.add_command(label='Check Server')
        file.add_cascade(label='Select Server')
        help = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=help)
        help.add_command(label="Help")
        help.add_command(label='About Anitrac')

        self.config(menu=menubar)


    def on_close(self) -> None:
        try:
            self.destroy()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = App()