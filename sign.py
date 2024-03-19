import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import ImageTk
import subprocess


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
    query = "SELECT * FROM users WHERE admission_number = %s"
    cursor.execute(query, (admission_number,))
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


# Function to handle admin login
def admin_login():
    # Create the admin login window
    admin_login_window = tk.Toplevel(root)
    admin_login_window.title("Admin Login")
    admin_login_window.geometry("300x150")

    # Function to validate admin credentials
    def validate_admin():
        admin_username = admin_username_entry.get()
        admin_password = admin_password_entry.get()

        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="chatbot"
        )
        cursor = conn.cursor()

        # Check if the admin credentials are valid
        query = "SELECT * FROM administrators WHERE admin_username = %s AND admin_password = %s"
        cursor.execute(query, (admin_username, admin_password))
        admin = cursor.fetchone()

        if admin:
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            admin_login_window.withdraw()
            open_admin_panel()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

        # Close the database connection
        cursor.close()
        conn.close()

    # Admin username label and entry
    admin_username_label = tk.Label(admin_login_window, text="Username:")
    admin_username_label.pack()
    admin_username_entry = tk.Entry(admin_login_window)
    admin_username_entry.pack()

    # Admin password label and entry
    admin_password_label = tk.Label(admin_login_window, text="Password:")
    admin_password_label.pack()
    admin_password_entry = tk.Entry(admin_login_window, show="*")
    admin_password_entry.pack()

    # Login button
    login_button = tk.Button(admin_login_window, text="Login", command=validate_admin)
    login_button.pack(pady=10)

    # Show the admin login window
    admin_login_window.mainloop()


# Function to open the admin panel
def open_admin_panel():
    # Close the login window
    login_window.withdraw()

    # Create the admin panel window
    admin_panel_window = tk.Toplevel(root)
    admin_panel_window.title("Admin Panel")
    admin_panel_window.geometry("990x660+50+50")

    # Function to fetch and display user data
    def display_users():
        # Clear the existing data
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

    def logout():
        # close admin panel window
        admin_panel_window.destroy()

    def launch_manage_users():
        subprocess.Popen(["python", "admin.py"])
        # destroy admin_panel after launching admin.py for managing users
        admin_panel_window.destroy()

    # Create buttons for admin panel functions
    manage_users_button = tk.Button(admin_panel_window, text="Manage Users", command=launch_manage_users)
    manage_users_button.pack(pady=5)

    handle_inquiries_button = tk.Button(admin_panel_window, text="Handle Inquiries")
    handle_inquiries_button.pack(pady=5)

    analytics_button = tk.Button(admin_panel_window, text="Analytics")
    analytics_button.pack(pady=5)

    logout_button = tk.Button(admin_panel_window, text="Log Out", command=logout)
    logout_button.pack(pady=5)

    # Create a text widget to display user data
    user_data_text = tk.Text(admin_panel_window, height=10, width=50)
    user_data_text.pack()
    user_data_text.config(state='disabled')

    # Show the admin panel window
    admin_panel_window.mainloop()


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

# Add a button to open the admin login window
admin_button = tk.Button(login_window, text="Admin Login", command=admin_login)
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
