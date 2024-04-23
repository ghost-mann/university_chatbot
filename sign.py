import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import ImageTk, Image
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
        user="austin",
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
        subprocess.Popen(["python", "bot_gui.py", "--admission-number", str(admission_number)])
        # close current window
        login_window.withdraw()

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
        user="austin",
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
            user="austin",
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

    # Function to resize the background image
    def resize_background_image(event):
        canvas_width = event.width
        canvas_height = event.height
        bg_image = ImageTk.PhotoImage(Image.open('./images/nebula.jpg').resize((canvas_width, canvas_height)))
        canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=tk.CENTER, image=bg_image)
        canvas.bg_image = bg_image

    def logout():
        # close admin panel window
        admin_panel_window.destroy()

    def launch_manage_users():
        subprocess.Popen(["python", "admin.py"])
        # destroy admin_panel after launching admin.py for managing users
        admin_panel_window.destroy()

    def launch_manage_inquiries():
        subprocess.Popen(["python", "inquiry.py"])
        admin_panel_window.destroy()

    # Create buttons for admin panel functions
    manage_users_button = tk.Button(admin_panel_window, text="Manage Users", command=launch_manage_users)
    manage_users_button.pack(pady=5)

    handle_inquiries_button = tk.Button(admin_panel_window, text="Handle Inquiries", command=launch_manage_inquiries)
    handle_inquiries_button.pack(pady=5)

    analytics_button = tk.Button(admin_panel_window, text="Analytics")
    analytics_button.pack(pady=5)

    logout_button = tk.Button(admin_panel_window, text="Log Out", command=logout)
    logout_button.pack(pady=5)

    # Show the admin panel window
    admin_panel_window.mainloop()


# Create the main window
root = tk.Tk()
root.title("Login and Sign Up Application")
# root.attributes("-fullscreen", True)
root.withdraw()  # Hide the main window

# Login Window
login_window = tk.Toplevel(root)
login_window.title("University Customer Care AI Chatbot")
login_window.geometry('1800x1000+50+50')

# Load and resize the logo image
logo_image = Image.open('images/mtejaai.png')
logo_image = logo_image.resize((500, 350))  # Adjust the dimensions as needed
logo_image = ImageTk.PhotoImage(logo_image)

# Load the background image
bgImage = ImageTk.PhotoImage(Image.open('./images/nebula.jpg'))

# Create a canvas
canvas = tk.Canvas(login_window, width=1800, height=1000)
canvas.pack(fill=tk.BOTH, expand=True)


# Function to resize the background image
def resize_background_image(event):
    canvas_width = event.width
    canvas_height = event.height
    bg_image = ImageTk.PhotoImage(Image.open('./images/nebula.jpg').resize((canvas_width, canvas_height)))
    canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=tk.CENTER, image=bg_image)
    canvas.bg_image = bg_image  # Keep a reference to prevent garbage collection


# Bind the <Configure> event to the canvas to resize the background image
canvas.bind('<Configure>', resize_background_image)

# Add the background image to the canvas
bg_image = ImageTk.PhotoImage(Image.open('./images/nebula.jpg'))
canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, anchor=tk.CENTER, image=bg_image)
canvas.bg_image = bg_image  # Keep a reference to prevent garbage collection

# Add the logo
logo_label = tk.Label(login_window, image=logo_image)
logo_label.place(x=650, y=150)

admission_number_label = tk.Label(login_window, text="Admission Number:", font=("Helvetica", 20), fg="white", bg="#7f1d1d")
admission_number_label.place(x=550, y=550)
admission_number_entry = tk.Entry(login_window, font=("Helvetica", 16), bg="white")
admission_number_entry.place(x=800, y=550, width=400, height=50)

password_label = tk.Label(login_window, text="Password:", font=("Helvetica", 20), fg="white", bg="#7f1d1d")
password_label.place(x=550, y=650)
password_entry = tk.Entry(login_window, show="*", font=("Helvetica", 16), bg="white")
password_entry.place(x=800, y=650, width=400, height=50)

login_button = tk.Button(login_window, text="Login", font=("Helvetica", 20), fg="white", bg="#7f1d1d", command=login)
login_button.place(x=600, y=750, width=200, height=60)

signup_button = tk.Button(login_window, text="Sign Up", font=("Helvetica", 20), fg="white", bg="#7f1d1d",
                          command=lambda: switch_window(login_window, signup_window))
signup_button.place(x=1000, y=750, width=200, height=60)

# Add a button to open the admin login window
admin_button = tk.Button(login_window, text="Admin Login", font=("Helvetica", 20), fg="white", bg="#7f1d1d",
                         command=admin_login)
admin_button.place(x=800, y=850, width=200, height=60)
# Signup Window
# Signup Window
signup_window = tk.Toplevel(root)
signup_window.title("Sign Up")
signup_window.geometry('1800x1000+50+50')

department_label = tk.Label(signup_window, text="Department:", font=("Helvetica", 16), fg="white", bg="#7f1d1d")
department_label.place(x=400, y=100)
department_entry = tk.Entry(signup_window, font=("Helvetica", 14))
department_entry.place(x=600, y=100, width=300, height=40)

gender_label = tk.Label(signup_window, text="Gender:", font=("Helvetica", 16), fg="white", bg="#7f1d1d")
gender_label.place(x=400, y=160)
gender_entry = tk.Entry(signup_window, font=("Helvetica", 14))
gender_entry.place(x=600, y=160, width=300, height=40)

first_name_label = tk.Label(signup_window, text="First Name:", font=("Helvetica", 16), fg="white", bg="#7f1d1d")
first_name_label.place(x=400, y=220)
first_name_entry = tk.Entry(signup_window, font=("Helvetica", 14))
first_name_entry.place(x=600, y=220, width=300, height=40)

last_name_label = tk.Label(signup_window, text="Last Name:", font=("Helvetica", 16), fg="white", bg="#7f1d1d")
last_name_label.place(x=400, y=280)
last_name_entry = tk.Entry(signup_window, font=("Helvetica", 14))
last_name_entry.place(x=600, y=280, width=300, height=40)

admission_number_signup_label = tk.Label(signup_window, text="Admission Number:", font=("Helvetica", 16), fg="white", bg="#7f1d1d")
admission_number_signup_label.place(x=400, y=340)
admission_number_signup_entry = tk.Entry(signup_window, font=("Helvetica", 14))
admission_number_signup_entry.place(x=600, y=340, width=300, height=40)

password_signup_label = tk.Label(signup_window, text="Password:", font=("Helvetica", 16), fg="white", bg="#7f1d1d")
password_signup_label.place(x=400, y=400)
password_signup_entry = tk.Entry(signup_window, show="*", font=("Helvetica", 14))
password_signup_entry.place(x=600, y=400, width=300, height=40)

retype_password_label = tk.Label(signup_window, text="Retype Password:", font=("Helvetica", 16), fg="white", bg="#7f1d1d")
retype_password_label.place(x=400, y=460)
retype_password_entry = tk.Entry(signup_window, show="*", font=("Helvetica", 14))
retype_password_entry.place(x=600, y=460, width=300, height=40)

email_label = tk.Label(signup_window, text="Email:", font=("Helvetica", 16), fg="white", bg="#7f1d1d")
email_label.place(x=400, y=520)
email_entry = tk.Entry(signup_window, font=("Helvetica", 14))
email_entry.place(x=600, y=520, width=300, height=40)

age_label = tk.Label(signup_window, text="Age:", font=("Helvetica", 16), fg="white", bg="#7f1d1d")
age_label.place(x=400, y=580)
age_entry = tk.Entry(signup_window, font=("Helvetica", 14))
age_entry.place(x=600, y=580, width=300, height=40)

signup_button = tk.Button(signup_window, text="Sign Up", font=("Helvetica", 18), fg="white", bg="#7f1d1d", command=signup)
signup_button.place(x=600, y=650, width=150, height=50)

back_button = tk.Button(signup_window, text="Back", font=("Helvetica", 18), fg="white", bg="#7f1d1d", command=lambda: switch_window(signup_window, login_window))
back_button.place(x=800, y=650, width=150, height=50)
# Show the login window initially
login_window.deiconify()

root.mainloop()
