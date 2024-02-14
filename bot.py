# import the required packages
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import mysql.connector
from PIL import ImageTk
import random
import mysql.connector

class Chatbot:
    def __init__(self, root, username):
        # Initialize the Chatbot class
        self.root = root
        self.root.title("University Customer Care Chatbot")
        self.root.geometry("800x600")

        # Create the chatbot's text area
        self.text_area = Text(root, bg="white", width=50, height=20)
        self.text_area.pack()

        # Create the user's input field
        self.input_field = Entry(root, width=50)
        self.input_field.pack()

        # Create the send button
        self.send_button = Button(root, text="Send", command=lambda: self.send_message())
        self.send_button.pack()

        self.username = username
        self.greet_user()
class Signup:

    def __init__(self, root):
        #initialize the signup class
        self.root = root
        self.root.title("University Customer Care Chatbot System")
        self.root.geometry("1000x600+100+50")
        self.root.resizable(width="False", height="False")

        # establish database connection
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="chatbot"
        )
        self.cursor = self.connection.cursor()


        # Background image
        self.bg = ImageTk.PhotoImage(file="images/nebula.jpg")
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=0, relheight=1)

        # Login frame
        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(x=250, y=150, width=500, height=400)

        # Title and subtitle
        title = Label(Frame_login, text="MTEJA AI", font=("Helevicta", 35, "bold"), fg="red", bg="white").place(x=90, y=30)
        subtitle = Label(Frame_login, text="Login Here", font=("Heelvicta", 15, "bold"), fg="blue", bg="white").place(x=90, y=100)

        # Username
        lbl_user = Label(Frame_login, text="Username", font=("Helvetica", 15), fg="black", bg="white").place(x=90, y=140)
        self.username_entry = Entry(Frame_login, font=("Helvetica", 10), bg="#E7E6E6")
        self.username_entry.place(x=90, y=170, width=320, height=35)

        # Password
        lbl_password = Label(Frame_login, text="Password", font=("Helvetica", 15), fg="black", bg="white").place(x=90, y=210)
        self.password_entry = Entry(Frame_login, font=("Helvetica", 10), bg="#E7E6E6", show="*")
        self.password_entry.place(x=90, y=240, width=320, height=35)

        # Button
        forget = Button(Frame_login, text="forgot password?", bd=0, font=("Helvetica", 12), fg="black", bg="white").place(x=90, y=280)
        submit = Button(Frame_login, text="Login", bd=1, font=("Helvetica", 12), fg="white", bg="red",command=self.check_funct)
        submit.place(x=90, y=320, width=180, height=40)

        login = Button(Frame_login, text="Sign Up", bd=1, font=("Helvetica", 12), fg="white", bg="red",command=self.check_funct)
        login.place(x=280, y=320, width=180, height=40)



    def check_funct(self):
        # Check the credentials against the database
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()

        if username == "" or password == "" or email == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            query = "SELECT * FROM users WHERE username = %s AND password = %s AND email = %s"
            values = (username,password,email)
            self.cursor.execute(query, values)
            user = self.cursor.fetchone()

            if user:
                messagebox.showinfo("Welcome", f"Welcome, {username}, New user created")
                self.open_chatbot(username)
            else:
                messagebox.showerror("Error", "Invalid username or password", parent=self.root)



class Login:
    def __init__(self, root):
        # Initialize the Login class
        self.root = root
        self.root.title("University Customer Care Chatbot")
        self.root.geometry("1000x600+100+50")
        self.root.resizable(width="False", height="False")

        # Establish database connection
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="chatbot",
        )
        self.cursor = self.connection.cursor()

        # Background image
        self.bg = ImageTk.PhotoImage(file="images/nebula.jpg")
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=0, relheight=1)

        # Login frame
        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(x=250, y=150, width=500, height=400)

        # Title and subtitle
        title = Label(Frame_login, text="MTEJA AI", font=("Helevicta", 35, "bold"), fg="red", bg="white").place(x=90, y=30)
        subtitle = Label(Frame_login, text="Login Here", font=("Heelvicta", 15, "bold"), fg="blue", bg="white").place(x=90, y=100)

        # Username
        lbl_user = Label(Frame_login, text="Username", font=("Helvetica", 15), fg="black", bg="white").place(x=90, y=140)
        self.username_entry = Entry(Frame_login, font=("Helvetica", 10), bg="#E7E6E6")
        self.username_entry.place(x=90, y=170, width=320, height=35)

        # Password
        lbl_password = Label(Frame_login, text="Password", font=("Helvetica", 15), fg="black", bg="white").place(x=90, y=210)
        self.password_entry = Entry(Frame_login, font=("Helvetica", 10), bg="#E7E6E6", show="*")
        self.password_entry.place(x=90, y=240, width=320, height=35)

        # Button
        forget = Button(Frame_login, text="forgot password?", bd=0, font=("Helvetica", 12), fg="black", bg="white").place(x=90, y=280)
        submit = Button(Frame_login, text="Login", bd=1, font=("Helvetica", 12), fg="white", bg="red",command=self.check_function)
        submit.place(x=90, y=320, width=180, height=40)

        signup = Button(Frame_login, text="Sign Up", bd=1, font=("Helvetica", 12), fg="white", bg="red",command=self.check_function)
        signup.place(x=280, y=320, width=180, height=40)

    def check_function(self):
        # Check the credentials against the database
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            values = (username,password)
            self.cursor.execute(query, values)
            user = self.cursor.fetchone()

            if user:
                messagebox.showinfo("Welcome", f"Welcome, {username}")
                self.open_chatbot(username)
            else:
                messagebox.showerror("Error", "Invalid username or password", parent=self.root)

    def open_chatbot(self, username):
        # Open the chatbot window
        self.root.destroy()  # Close the login window
        chatbot_root = Tk()
        chatbot_root.title("University Customer Care Chatbot")
        chatbot = Chatbot(chatbot_root, username)
        chatbot_root.mainloop()

if __name__ == "__main__":
    # Create and run the Tkinter main loop
    root = Tk()
    obj = Login(root)
    root.mainloop()
