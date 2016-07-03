import os
import threading
import webbrowser

from supplychainpy.reporting.views import app, db
import tkinter as tk
from tkinter import ttk


class ReportsLauncher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.message = "launching reports"
        self.name = "reports"
        self.port = 5000

    def print_message(self):
        print(self.message)

    def run(self):
        print(self.port)
        app.run(port=self.port)


def exit_report():
    exit()


def launch_browser(event, url: str):
    webbrowser.open_new(str(url))


class SupplychainpyReporting:
    """Creates report launcher gui, to launch browser and using flask local server. Allows port number to be
        changed.
    """

    def __init__(self, master):
        master.title('Supplychainpy')
        master.resizable(False,False)

        self.spawn = ReportsLauncher()
        self.parent = master
        self.hyperlink = ''
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/reporting/static/logo.gif'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
        logo = tk.PhotoImage(file=abs_file_path)

        # set supplychainpy logo for report launcher gui
        self.image = ttk.Label(master, image=logo)
        self.image.image = logo
        self.image.config(background='black')
        self.image.grid(row=0, column=1, columnspan=2)

        self.instruction_label = ttk.Label(master, text='Launch supplychainpy reports')
        self.instruction_label.grid(row=1, column=1, columnspan=6)
        self.instruction_label.config(background='black', foreground='white')

        self.hyperlink_label = ttk.Label(master)
        self.hyperlink_label.config(background='black', foreground='#8dc53e', text='click to open browser:',
                                    font=('system', 10, 'bold'))

        self.validation_label = ttk.Label(master)
        self.validation_label.config(background='black', foreground='red',
                                     text='Incorrect port! Please enter correct port number',
                                     font=('system', 10, 'bold'))

        self.runtime_validation_label = ttk.Label(master)
        self.runtime_validation_label.config(background='black', foreground='red',
                                             text='The reports are already running @ {}'.format(self.hyperlink),
                                             font=('system', 10, 'bold'))

        self.port_label = ttk.Label(master, text='Change port (default :5000):')
        self.port_label.config(background='black', foreground='white', justify=tk.RIGHT)

        self.port_text = ttk.Entry(master, width=10)

        self.change_port = tk.BooleanVar()
        self.change_port.set(False)

        self.change_port_checkbutton = tk.Checkbutton(master, variable=self.change_port, activebackground='black',
                                                      activeforeground='white',
                                                      bg='black', fg='white', relief='solid', selectcolor='blue',
                                                      text='Change default port (default :5000)',
                                                      command=lambda: self.show_port_entry())

        self.change_port_checkbutton.config(onvalue=True)
        self.change_port_checkbutton.grid(row=2, column=1, columnspan=2, pady=(0, 10))

        self.hyperlink_text = ttk.Label(master)
        self.hyperlink_text.config(background='black', foreground='lightblue', font=('courier', 11, 'underline'))
        self.hyperlink_text.bind("<Button-1>", lambda e, url=str(self.hyperlink): launch_browser(e, url))

        ttk.Button(master, text='Launch Reporting', command=lambda: self.spawn_reports()).grid(row=6, column=1,
                                                                                               padx=(15, 5))
        ttk.Button(master, text='Exit Reporting', command=lambda: exit_report()).grid(row=6, column=2, padx=(5, 15))

    def spawn_reports(self):
        """Checks if port number is specified, then validates port number."""

        # if port specified check port is numeric
        try:

            if self.port_text.get() is not '' and isinstance(int(self.port_text.get()), int) and self.hyperlink == '':
                self.hyperlink = 'http://127.0.0.1:{}'.format(self.port_text.get())
                self.validation_label.grid_forget()
                self.hyperlink_text.config(text=self.hyperlink)
                self.hyperlink_text.bind("<Button-1>", lambda e, url=str(self.hyperlink): launch_browser(e, url))
                self.hyperlink_text.grid(row=4, column=1, columnspan=2)
                self.hyperlink_label.grid(row=3, column=1, columnspan=2)
                self.spawn.daemon = True
                self.spawn.port = self.port_text.get()
                self.spawn.start()
            elif self.port_text.get() is '':
                self.validation_label.grid_forget()
                self.hyperlink = 'http://127.0.0.1:5000'
                self.hyperlink_text.config(text=self.hyperlink)
                self.hyperlink_text.bind("<Button-1>", lambda e, url=str(self.hyperlink): launch_browser(e, url))
                self.hyperlink_text.grid(row=4, column=1, columnspan=2)
                self.hyperlink_label.grid(row=3, column=1, columnspan=2)
                self.spawn.daemon = True
                self.spawn.start()
            else:
                self.hyperlink_label.grid_forget()

        except ValueError:
            self.validation_label.grid(row=3, column=1, columnspan=2)
            self.hyperlink_label.grid_forget()
        except RuntimeError:
            self.runtime_validation_label.grid(row=3, column=1, columnspan=2)

    def show_port_entry(self):
        if self.change_port.get():
            self.port_label.grid(row=5, column=1, columnspan=1, padx=(15, 0), pady=(10, 10))
            self.port_text.grid(row=5, column=2, columnspan=1, padx=(0, 15), pady=(10, 10))
        else:
            self.port_text.forget()
            self.port_label.forget()


def launch_report():
    from supplychainpy.reporting import load
    # db.create_all()
    # load.load()
    launcher = tk.Tk()
    app = SupplychainpyReporting(launcher)
    app.parent.configure(background='black')
    launcher.mainloop()