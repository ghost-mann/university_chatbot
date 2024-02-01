from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import mysql.connector
import random

responses = [
    "Hello! How can I help you today?",
    "What's on your mind?",
    "I'm here to assist you. What do you need?",
    "How can I assist you?",
    "What can I help you with?",
]

class Chatbot:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Chatbot Program")
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

    def greet_user(self):
        greeting = f"Hello, {self.username}! How can I assist you today?"
        self.display_response(greeting)

    def chatbot_response(self, user_input):
        # Normalize the user's input
        user_input = user_input.lower()

        # Check for specific keywords in the user's input
        if "movie" in user_input:
            return "I recommend checking out the IMDb website for movie recommendations. They have a wide variety of genres and ratings to choose from."
        elif "weather" in user_input:
            return "You can check the weather by using a weather website or app. Some popular ones include Weather.com and The Weather Channel app."
        elif "news" in user_input:
            return "There are many websites and apps that offer the latest news updates, such as CNN, Fox News, and NBC News."
        elif "joke" in user_input:
            return "Why couldn't the bicycle stand up by itself? Because it was two-tired!"
        else:
            # If no keywords are detected, select a random response from the list
            return random.choice(responses)

    def send_message(self):
        # Get the user's input
        user_input = self.input_field.get()

        # Clear the input field
        self.input_field.delete(0, END)

        # Generate a response from the chatbot
        response = self.chatbot_response(user_input)

        # Display the response in the chatbot's text area
        self.display_response(f"User: {user_input}")
        self.display_response(f"Chatbot: {response}")

    def display_response(self, message):
        self.text_area.insert(END, message + "\n")

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chatbot")
        self.root.geometry("1000x600+100+50")
        self.root.resizable(False, False)

        # Database connection
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="chatbot"
        )
        self.cursor = self.connection.cursor()

        # background image
        self.bg = ImageTk.PhotoImage(file="images/nebula.jpg")
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        # Login frame
        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(x=250, y=150, width=500, height=400)

        # title and subtitle
        title = Label(Frame_login, text="MTEJA AI", font=("Helvetica", 35, "bold"), fg="red", bg="white").place(x=90, y=30)
        subtitle = Label(Frame_login, text="Login Here", font=("Helvetica", 15, "bold"), fg="blue", bg="white").place(x=90, y=100)

        # username
        lbl_user = Label(Frame_login, text="Username", font=("Helvetica", 15), fg="black", bg="white").place(x=90, y=140)
        self.username_entry = Entry(Frame_login, font=("Helvetica", 10), bg="#E7E6E6")
        self.username_entry.place(x=90, y=170, width=320, height=35)

        # password
        lbl_password = Label(Frame_login, text="Password", font=("Helvetica", 15), fg="black", bg="white").place(x=90, y=210)
        self.password_entry = Entry(Frame_login, font=("Helvetica", 10), bg="#E7E6E6", show="*")
        self.password_entry.place(x=90, y=240, width=320, height=35)

        # button
        forget = Button(Frame_login, text="forgot password?", bd=0, font=("Helvetica", 12), fg="black", bg="white").place(x=90, y=280)
        submit = Button(Frame_login, text="Login", bd=1, font=("Helvetica", 12), fg="white", bg="red", command=self.check_function).place(x=90, y=320, width=180, height=40)

    def check_function(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            # Check the credentials against the database
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            values = (username, password)
            self.cursor.execute(query, values)
            user = self.cursor.fetchone()

            if user:
                messagebox.showinfo("Welcome", f"Welcome, {username}")
                self.open_chatbot(username)
            else:
                messagebox.showerror("Error", "Invalid username or password", parent=self.root)

    def open_chatbot(self, username):
        self.root.destroy()  # Close the login window
        chatbot_root = Tk()
        chatbot_root.title("Chatbot Program")
        chatbot = Chatbot(chatbot_root, username)
        chatbot_root.mainloop()

if __name__ == "__main__":
    root = Tk()
    obj = Login(root)
    root.mainloop()
