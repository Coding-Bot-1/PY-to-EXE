# Made by person569
# https://github.com/person569/PY-to-EXE

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import shutil
import threading
from time import sleep


class PythonToEXE:
    def __init__(self):
        self.converting = False
        self.set_up_tkinter()
        self.disable_enable()

    def set_up_tkinter(self):
        # Label for the PYTHON file name
        self.label_python_file = Label(root, width=142, height=4, fg="blue")
        self.label_python_file.place(x=1, y=1)

        # Label for the ICON file name
        self.label_icon_file = Label(root, width=142, height=4, fg="blue")

        # Button to browse the Icon file
        self.browse_icon_files_button = Label(root, text='Browse Icon File', relief=SUNKEN, fg='white', bg='#1B365D',
                                              font=('Roboto,sans-serif', '15'), width=20, height=2,
                                              state='disabled')
        self.browse_icon_files_button.place(x=270, y=240)
        self.browse_icon_files_button.bind("<Enter>", self.browse_icon_files_button_hover)

        # Button to browse the Python file
        self.browse_python_files_button = Label(root, text='Browse Python File',
                                                relief=SUNKEN, borderwidth=0, fg='white', bg='#1B365D',
                                                font=('Roboto,sans-serif', '15'), width=20, height=2)
        self.browse_python_files_button.place(x=510, y=242)
        self.browse_python_files_button.bind("<Button-1>", self.browse_python_file)
        self.browse_python_files_button.bind("<Enter>", self.browse_python_files_button_hover)

        # Convert to EXE button
        self.convert_to_exe_button = Button(root, text='Convert to EXE', state="disabled", relief=SUNKEN, borderwidth=0,
                                            command=self.set_up_pyinstaller_command, fg='white', bg='#1B365D',
                                            font=('Roboto,sans-serif', '18'), width=30, height=5)
        self.convert_to_exe_button.place(x=290, y=320)
        self.convert_to_exe_button.bind("<Enter>", self.convert_to_exe_button_hover)
        self.convert_to_exe_button.bind("<Leave>", self.convert_to_exe_button_unhover)

        # Console button
        self.console_check = IntVar(value=0)
        self.console = Checkbutton(root, text='Console', variable=self.console_check)
        self.console.config(bg='white', relief=SUNKEN, borderwidth=0, activebackground="white")
        self.console.select()
        self.console.bind("<Enter>", self.console_checkbox_hover)
        self.console.place(x=420, y=180)

        # Icon button
        self.icon_check = IntVar(value=0)
        self.icon = Checkbutton(root, text='icon', variable=self.icon_check)
        self.icon.config(bg='white', activebackground="white")
        self.icon.bind("<Enter>", self.icon_checkbox_hover)
        self.icon.place(x=530, y=179)

    def console_checkbox_hover(self, argument):
        self.console.config(cursor="hand2")

    def icon_checkbox_hover(self, argument):
        self.icon.config(cursor="hand2")

    def browse_python_files_button_hover(self, argument):
        if not self.converting:
            self.browse_python_files_button.config(cursor='hand2')

    def browse_icon_files_button_hover(self, argument):
        if not self.converting:
            if self.browse_icon_files_button["state"] == 'normal' and self.icon_check.get():
                self.browse_icon_files_button.config(cursor='hand2')
            else:
                self.browse_icon_files_button.config(cursor='arrow')

    def convert_to_exe_button_hover(self, argument):
        # if not self.converting:
        if self.convert_to_exe_button["state"] == 'normal':
            self.convert_to_exe_button.config(bg='#1B466D')
            self.convert_to_exe_button.config(cursor='hand2')

    def convert_to_exe_button_unhover(self, argument):
        if self.convert_to_exe_button["state"] == 'normal':
            self.convert_to_exe_button.config(bg='#1B365D')
            self.convert_to_exe_button.config(cursor='arrow')

    def browse_python_file(self, x):
        self.filename = filedialog.askopenfilename(initialdir="/",
                                                   title="Select a File",
                                                   filetypes=(("Python Files",
                                                               "*.py*"),
                                                              ("All Files",
                                                               "*.*")))

        if self.filename != '':
            self.label_python_file.configure(text="Python File: " + self.filename)
            self.file_directory = self.filename

    def browse_icon_file(self, x):
        self.filename = filedialog.askopenfilename(initialdir="/",
                                                   title="Select a File",
                                                   filetypes=(("Icon Files",
                                                               "*.ico*"),
                                                              ("All Files",
                                                               "*.*")))

        if self.filename != '':
            self.label_icon_file.configure(text="Icon File: " + self.filename)
            self.icon_directory = self.filename

    def set_up_pyinstaller_command(self):
        # Run the command
        os.chdir(self.remove_file_name(self.file_directory))
        command = "pyinstaller"

        command = command + ' --onefile'

        if not self.console_check.get():
            command = command + ' --windowed'

        if self.icon_check.get():
            command = command + f' --icon="{self.get_file_name(self.icon_directory)}"'

        print(f'{command} "{self.get_file_name(self.file_directory)}"')
        threading.Thread(
            target=lambda: self.convert_to_exe(f"{command} {self.get_file_name(self.file_directory)}")).start()

    def convert_to_exe(self, command):
        # Disable all the widgets
        self.browse_icon_files_button["state"] = "disabled"
        self.browse_python_files_button["state"] = "disabled"
        self.convert_to_exe_button["state"] = "disabled"
        self.console["state"] = "disabled"
        self.icon["state"] = "disabled"

        sleep(1)

        # Change cursor to loading cursor
        root.config(cursor="wait")

        self.browse_icon_files_button.config(cursor="wait")
        self.browse_python_files_button.config(cursor="wait")
        self.convert_to_exe_button.config(cursor="wait")

        self.converting = True
        self.run_command(f"{command} {self.get_file_name(self.file_directory)}")

        try:
            # Remove useless files
            os.remove(
                self.remove_file_name(self.file_directory) + f"/{self.get_file_name(self.file_directory)[:-3]}.spec")
            shutil.rmtree(self.remove_file_name(self.file_directory) + "/__pycache__", ignore_errors=True)
            shutil.rmtree(self.remove_file_name(self.file_directory) + "/build", ignore_errors=True)

            # Move the exe from the dist folder to the folder of the Python file
            TO = self.remove_file_name(self.file_directory)
            shutil.move(self.remove_file_name(self.file_directory) + '/dist/' +
                        self.get_file_name(self.file_directory)[:-3] + '.exe', TO)

            shutil.rmtree(self.remove_file_name(self.file_directory) + '/dist')

            print("Finished Converting Python to EXE")

            self.browse_icon_files_button["state"] = "normal"
            self.browse_python_files_button["state"] = "normal"
            self.convert_to_exe_button.place(x=290, y=320)
            self.console["state"] = "normal"
            self.icon["state"] = "normal"
            messagebox.showinfo("Completed", "Successfully converted PY to EXE")
            self.converting = False
        except:
            messagebox.showerror("Error", "Something went wrong")

            self.browse_icon_files_button["state"] = "normal"
            self.browse_python_files_button["state"] = "normal"
            self.convert_to_exe_button.place(x=290, y=320)
            self.console["state"] = "normal"
            self.icon["state"] = "normal"
            self.converting = False

        root.config(cursor="arrow")

    def disable_enable(self):
        # Check if Python file is chosen, if yes set the state to normal
        if self.label_python_file.cget('text') != '' and not self.converting:
            self.convert_to_exe_button["state"] = "normal"
        else:
            self.convert_to_exe_button["state"] = "disabled"

        if self.icon_check.get():
            self.browse_icon_files_button['state'] = 'normal'
            self.browse_icon_files_button.bind("<Button-1>", self.browse_icon_file)
            self.label_icon_file.place(x=0, y=75)

            if self.label_icon_file.cget('text') == '':
                self.convert_to_exe_button["state"] = 'disabled'
        else:
            self.browse_icon_files_button.bind("<Button-1>", lambda *args: None)
            self.browse_icon_files_button['state'] = 'disable'
            self.label_icon_file.place_forget()

        root.after(1, self.disable_enable)

    def run_command(self, command):
        os.system(f'cmd /c "{command}"')

    def remove_file_name(self, directory):
        count = 0
        for index in range(len(directory)):
            if directory[index] == '/':
                count += 1
                if count == directory.count('/'):
                    return directory[:index]

    def get_file_name(self, directory):
        count = 0
        for index in range(len(directory)):
            if directory[index] == '/':
                count += 1
                if count == directory.count('/'):
                    return directory[index + 1:]


root = Tk()
root.title('Python to EXE')
root.geometry("1000x500+130+50")
root.config(background="white")

icon = PhotoImage(file="icon.png")
root.iconphoto(False, icon)
PythonToEXE()
root.mainloop()
