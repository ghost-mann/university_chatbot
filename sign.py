import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import ImageTk

# Function to switch between windows
def switch_window(window, new_window):
    window.withdraw()
    new_window.deiconify()

# Function to handle login
def login():
    admission_number = int(admission_number_entry.get())
    password = password_entry.get()

    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="chatbot"
    )
    cursor = conn.cursor()

    # Check if the user exists in the database
    query = "SELECT * FROM users WHERE admission_number = %s AND password = %s"
    cursor.execute(query, (admission_number, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login Successful", "Welcome!")
        # Launch the bot_gui.py script
        # subprocess.Popen(["python", "bot_gui.py"])
    else:
        messagebox.showerror("Login Failed", "Invalid admission number or password.")

    # Close the database connection
    cursor.close()
    conn.close()

# Function to handle signup
def signup():
    department = department_entry.get()
    gender = gender_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    admission_number = int(admission_number_signup_entry.get())
    password = password_signup_entry.get()
    retype_password = retype_password_entry.get()
    email = email_entry.get()
    age = int(age_entry.get())  # Convert age to integer

    if password != retype_password:
        messagebox.showerror("Sign Up Failed", "Passwords do not match.")
        return

    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="chatbot"
    )
    cursor = conn.cursor()

    # Check if the admission number already exists

    # The %s is a placeholder for a parameterized query.This is a security measure to prevent SQL injection attacks.

    query = "SELECT * FROM users WHERE admission_number = %s"

    # The cursor is an object that allows Python code to execute SQL commands. The second argument (admission_number,
    # ) is a tuple containing the values to substitute into the %s placeholders in the query.
    cursor.execute(query, (admission_number,))

    # fetches the first matching user (if any) from the database.
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Sign Up Failed", "Admission number already exists.")
    else:
        # Insert the new user into the database
        query = "INSERT INTO users (department, gender, first_name, last_name, admission_number, password, email, age) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (department, gender, first_name, last_name, admission_number, password, email, age)
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Sign Up Successful", "You can now log in.")
        switch_window(signup_window, login_window)

    # Close the database connection
    cursor.close()
    conn.close()

# Function to display the admin panel
def admin_panel():
    # Create the admin panel window
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Panel")
    admin_window.geometry("990x600+50+50")

    # Function to fetch and display user data
    def display_users():
        # Clear the existing data.Setting it to 'normal' allows modifications to its contents.
        user_data_text.config(state='normal')
        user_data_text.delete('1.0', tk.END)

        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="chatbot"
        )
        cursor = conn.cursor()

        # Fetch user data from the database
        query = "SELECT * FROM users"
        cursor.execute(query)
        users = cursor.fetchall()

        # Display user data in the text widget
        for user in users:
            user_data_text.insert(tk.END, str(user) + "\n")

        # Close the database connection
        cursor.close()
        conn.close()

        user_data_text.config(state='disabled')

    # Create a button to display user data
    display_users_button = tk.Button(admin_window, text="Display Users", command=display_users)
    display_users_button.pack(pady=10)

    # Create a text widget to display user data
    user_data_text = tk.Text(admin_window, height=10, width=50)
    user_data_text.pack()
    user_data_text.config(state='disabled')

    # Add any additional functionality for the admin panel here

    # Show the admin panel window
    admin_window.mainloop()

# Create the main window
root = tk.Tk()
root.title("Login and Sign Up Application")
root.withdraw()  # Hide the main window

# Login Window
login_window = tk.Toplevel(root)
login_window.title("Login")
login_window.geometry('990x660+50+50')
login_window.resizable(0, 0)
bgImage = ImageTk.PhotoImage(file='./images/nebula.jpg')

admission_number_label = tk.Label(login_window, text="Admission Number:")
admission_number_label.pack()
admission_number_entry = tk.Entry(login_window)
admission_number_entry.pack()

password_label = tk.Label(login_window, text="Password:")
password_label.pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

login_button = tk.Button(login_window, text="Login", command=login)
login_button.pack()

signup_button = tk.Button(login_window, text="Sign Up", command=lambda: switch_window(login_window, signup_window))
signup_button.pack()

# Add a button or menu item to open the admin panel
admin_button = tk.Button(login_window, text="Admin Panel", command=admin_panel)
admin_button.pack()

# Signup Window
signup_window = tk.Toplevel(root)
signup_window.title("Sign Up")
signup_window.resizable(0, 0)
signup_window.geometry('990x660+50+50')

signup_window.withdraw()  # Hide the signup window initially

department_label = tk.Label(signup_window, text="Department:")
department_label.pack()
department_entry = tk.Entry(signup_window)
department_entry.pack()

gender_label = tk.Label(signup_window, text="Gender:")
gender_label.pack()
gender_entry = tk.Entry(signup_window)
gender_entry.pack()

first_name_label = tk.Label(signup_window, text="First Name:")
first_name_label.pack()
first_name_entry = tk.Entry(signup_window)
first_name_entry.pack()

last_name_label = tk.Label(signup_window, text="Last Name:")
last_name_label.pack()
last_name_entry = tk.Entry(signup_window)
last_name_entry.pack()

admission_number_signup_label = tk.Label(signup_window, text="Admission Number:")
admission_number_signup_label.pack()
admission_number_signup_entry = tk.Entry(signup_window)
admission_number_signup_entry.pack()

password_signup_label = tk.Label(signup_window, text="Password:")
password_signup_label.pack()
password_signup_entry = tk.Entry(signup_window, show="*")
password_signup_entry.pack()

retype_password_label = tk.Label(signup_window, text="Retype Password:")
retype_password_label.pack()
retype_password_entry = tk.Entry(signup_window, show="*")
retype_password_entry.pack()

email_label = tk.Label(signup_window, text="Email:")
email_label.pack()
email_entry = tk.Entry(signup_window)
email_entry.pack()

age_label = tk.Label(signup_window, text="Age:")
age_label.pack()
age_entry = tk.Entry(signup_window)
age_entry.pack()

signup_button = tk.Button(signup_window, text="Sign Up", command=signup)
signup_button.pack()

back_button = tk.Button(signup_window, text="Back", command=lambda: switch_window(signup_window, login_window))
back_button.pack()

# Show the login window initially
login_window.deiconify()

root.mainloop()