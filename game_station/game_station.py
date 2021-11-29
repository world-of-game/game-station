import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import *
import subprocess
frame_styles = {"relief": "groove",
                "bd": 3, "bg": "#BEB2A7",
                "fg": "#073bb3", "font": ("Arial", 9, "bold")}

class LoginPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self, bg="#708090", height=431, width=626)  # this is the background
        main_frame.pack(fill="both", expand="true")

        self.geometry("626x431")  # Sets window size to 626w x 431h pixels
        self.resizable(0, 0)  # This prevents any resizing of the screen
        image1 = ImageTk.PhotoImage(file='Login.png', master=main_frame)
        panel1 = Label(main_frame, image=image1)
        panel1.image = image1  # keep a reference
        panel1.pack(side='top', fill='both', expand='yes')

        title_styles = {"font": ("Calibri", 16)}

        text_styles = {"font": ("Calibri", 14)}

        frame_login = tk.Frame(main_frame,  relief="groove", bd=2)  # this is the frame that holds all the login details and buttons
        frame_login.place(rely=0.30, relx=0.17, height=130, width=400)

        label_title = tk.Label(frame_login, title_styles, text="Login Page")
        label_title.grid(row=0, column=1, columnspan=1)

        label_user = tk.Label(frame_login, text_styles, text="Username:")
        label_user.grid(row=1, column=0)

        label_pw = tk.Label(frame_login, text_styles, text="Password:")
        label_pw.grid(row=2, column=0)

        entry_user = ttk.Entry(frame_login, width=45, cursor="xterm")
        entry_user.grid(row=1, column=1)

        entry_pw = ttk.Entry(frame_login, width=45, cursor="xterm", show="*")
        entry_pw.grid(row=2, column=1)

        button = ttk.Button(frame_login, text="Login", command=lambda: getlogin())
        button.place(rely=0.70, relx=0.35)

        signup_btn = ttk.Button(frame_login, text="Register", command=lambda: get_signup())
        signup_btn.place(rely=0.70, relx=0.55)

        def get_signup():
            SignupPage()

        def getlogin():
            username = entry_user.get()
            password = entry_pw.get()
            # if your want to run the script as it is set validation = True
            validation = validate(username, password)
            if validation:
                tk.messagebox.showinfo("Login Successful",
                                       "Welcome {}".format(username))
                root.deiconify()
                top.destroy()
            else:
                tk.messagebox.showerror("Information", "The Username or Password you have entered are incorrect ")

        def validate(username, password):
            # Checks the text file for a username/password combination.
            try:
                with open("credentials.txt", "r") as credentials:
                    for line in credentials:
                        line = line.split(",")
                        if line[1] == username and line[3] == password:
                            return True
                    return False
            except FileNotFoundError:
                print("You need to Register first or amend Line 71 to     if True:")
                return False

class SignupPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self, bg="#3F6BAA", height=150, width=250)
        # pack_propagate prevents the window resizing to match the widgets
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")

        self.geometry("250x150")
        self.resizable(0, 0)

        self.title("Registration")

        text_styles = {"font": ("Verdana", 10),
                       "background": "#3F6BAA",
                       "foreground": "#E1FFFF"}

        label_user = tk.Label(main_frame, text_styles, text="New Username:")
        label_user.grid(row=1, column=0)

        label_pw = tk.Label(main_frame, text_styles, text="New Password:")
        label_pw.grid(row=2, column=0)

        entry_user = ttk.Entry(main_frame, width=20, cursor="xterm")
        entry_user.grid(row=1, column=1)

        entry_pw = ttk.Entry(main_frame, width=20, cursor="xterm", show="*")
        entry_pw.grid(row=2, column=1)

        button = ttk.Button(main_frame, text="Create Account", command=lambda: signup())
        button.grid(row=4, column=1)

        def signup():
            # Creates a text file with the Username and password
            user = entry_user.get()
            pw = entry_pw.get()
            validation = validate_user(user)
            if not validation:
                tk.messagebox.showerror("Information", "That Username already exists")
            else:
                if len(pw) > 3:
                    credentials = open("credentials.txt", "a")
                    credentials.write(f"Username,{user},Password,{pw},\n")
                    credentials.close()
                    tk.messagebox.showinfo("Information", "Your account details have been stored.")
                    SignupPage.destroy(self)

                else:
                    tk.messagebox.showerror("Information", "Your password needs to be longer than 3 values.")

        def validate_user(username):
            # Checks the text file for a username/password combination.
            try:
                with open("credentials.txt", "r") as credentials:
                    for line in credentials:
                        line = line.split(",")
                        if line[1] == username:
                            return False
                return True
            except FileNotFoundError:
                return True

class MenuBar(tk.Menu):
    def carRacing(self):
        subprocess.call(["python", "Car_Race\car_race.py"])
    def Adventure(self):
        subprocess.call(["python", "adventure/adventure.py"])
    def Pong(self):
        subprocess.call(["python", "Pong Game\pong_game.py"])
    def Snake(self):
        subprocess.call(["python", "snake\main.py"])

    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        menu_home = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Home", menu=menu_home)
        menu_home.add_command(label="Home", command=lambda: parent.show_frame(HomePage))
        # menu_operations = tk.Menu(self, tearoff=0)
        # self.add_cascade(label="Our Games", menu=menu_operations)
        # menu_operations.add_command(label="Car Racing", command=self.carRacing)
        # menu_operations.add_command(label="Adventure", command=self.Adventure)
        # menu_operations.add_command(label="Pong", command=self.Pong)
        # menu_operations.add_command(label="Snake", command=self.Snake)


        menu_file = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Contact Us", menu=menu_file)
        menu_file.add_command(label="Our Staff", command=lambda: parent.show_frame(ContactPage))
        # menu_file.add_command(label="Our Staff", command=lambda: parent.OpenNewWindow())
        menu_file.add_separator()
        menu_file.add_command(label="Exit Application", command=lambda: parent.Quit_application())



class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        main_frame = tk.Frame(self, bg="#84CEEB", height=600, width=1024)
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        # self.resizable(0, 0) prevents the app from being resized
        # self.geometry("1024x600") fixes the applications size
        self.frames = {}
        pages = (ContactPage,HomePage)
        for F in pages:
            frame = F(main_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        menubar = MenuBar(self)
        tk.Tk.config(self, menu=menubar)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    # def OpenNewWindow(self):
    #     OpenNewWindow()

    def Quit_application(self):
        self.destroy()

class GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.main_frame = tk.Frame(self, bg="#BEB2A7", height=600, width=1024)
        # self.main_frame.pack_propagate(0)
        self.main_frame.pack(fill="both", expand="true")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

class ContactPage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        image1 = ImageTk.PhotoImage(file='staff.png', master=self.main_frame)
        panel1 = Label(self.main_frame, image=image1)
        panel1.image = image1  # keep a reference
        panel1.pack(side='top', fill='both', expand='yes')

class HomePage(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        image1 = ImageTk.PhotoImage(file='bg-2.png', master=self.main_frame)
        panel1 = Label(self.main_frame, image=image1)
        panel1.image = image1  # keep a reference
        panel1.pack(side='top', fill='both', expand='yes')

        B1 = tk.Button(panel1,text="Car Racing",
                      command=self.carRacing,
                      height=2,
                      width=10,
                      font="Arial 16 bold",
                      fg = 'white',
                      bg = '#FF0075',
                      bd =  10,
                      highlightthickness=4,
                      highlightcolor="#37d3ff",
                      highlightbackground="#37d3ff",
                      borderwidth=4).place(x=10, y=40)
        # B1.pack(side='top')
        B2 = tk.Button(panel1, text="Adventure", command=self.Adventure, height=2, width=10,font="Arial 16 bold",
                      fg = '#FFE300',
                      bg = '#753188',
                      bd =  10,
                      highlightthickness=4,
                      highlightcolor="#37d3ff",
                      highlightbackground="#37d3ff",
                      borderwidth=4).place(x=180, y=40)
        # B2.pack(side='top')
        B3 = tk.Button(panel1, text="Pong", command=self.Pong, height=2, width=10,font="Arial 16 bold",fg = '#090910',
                      bg = '#49FF00',
                      bd =  10,
                      highlightthickness=4,
                      highlightcolor="#37d3ff",
                      highlightbackground="#37d3ff",
                      borderwidth=4).place(x=10, y=140)
        # B3.pack(side='top')
        B4 = tk.Button(panel1, text="Snake", command=self.Snake,height=2, width=10,font="Arial 16 bold",
                      fg = '#0F044C',
                      bg = '#1DB9C3',
                      bd =  10,
                      highlightthickness=4,
                      highlightcolor="#37d3ff",
                      highlightbackground="#37d3ff",
                      borderwidth=4).place(x=180, y=140)
        # B4.pack(side="top")
        # self.main_frame.config(bg='systemTransparent')


    def carRacing(self):
            subprocess.call(["python", "Car_Race\car_race.py"])

    def Adventure(self):
            subprocess.call(["python", "adventure/adventure.py"])

    def Pong(self):
            subprocess.call(["python", "Pong Game\pong_game.py"])

    def Snake(self):
            subprocess.call(["python", "snake\main.py"])












top = LoginPage()
top.title("Game Station - Login Page")
root = MyApp()
root.withdraw()
root.title("Game Station")
root.geometry("1024x600")
root.resizable(0,0)
root.mainloop()