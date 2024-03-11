from tkinter import *
from PIL import ImageTk

def login(window):
    if window == "login":
        print("Logged in successfully")
    elif window == "signup":
        print("Signed up successfully")

# Functionality Part (clearing of text boxes while being clicked)
def on_enter(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, END)

# code for signup window
def open_sign_up_window():
    # Close the current window (hides main login window doesn't destroy it)
    root.withdraw()

    # Toplevel() constructor creates a new window distinct from the main window
    signup_window = Toplevel()
    signup_window.title("Sign Up")
    # width x height+x position+y position
    signup_window.geometry('990x660+50+50')
    # This line makes the signup_window non-resizable either in horizontal or vertical direction
    signup_window.resizable(0, 0)
    # loads image file and converts it to make it compatible using ImageTk.PhotoImage() function
    signup_bg_image = ImageTk.PhotoImage(file='./images/nebula2.jpg')

    # create a label and set the background image
    signup_bg_label = Label(signup_window, image=signup_bg_image)
    signup_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Add entry fields on top of the background image
    admission_label = Label(signup_window, text="Admission No.:", font=("Helvetica", 12), bg="black", fg="white")
    admission_label.place(x=20, y=20)
    admission_entry = Entry(signup_window, font=("Helvetica", 12))
    admission_entry.place(x=150, y=20)

    gender_label = Label(signup_window, text="Gender:", font=("Helvetica", 12), bg="black", fg="white")
    gender_label.place(x=20, y=60)
    gender_entry = Entry(signup_window, font=("Helvetica", 12))
    gender_entry.place(x=150, y=60)

    department_label = Label(signup_window, text="Department:", font=("Helvetica", 12), bg="black", fg="white")
    department_label.place(x=20, y=100)
    department_entry = Entry(signup_window, font=("Helvetica", 12))
    department_entry.place(x=150, y=100)

    first_name_label = Label(signup_window, text="First Name:", font=("Helvetica", 12), bg="black", fg="white")
    first_name_label.place(x=20, y=140)
    first_name_entry = Entry(signup_window, font=("Helvetica", 12))
    first_name_entry.place(x=150, y=140)

    last_name_label = Label(signup_window, text="Last Name:", font=("Helvetica", 12), bg="black", fg="white")
    last_name_label.place(x=20, y=180)
    last_name_entry = Entry(signup_window, font=("Helvetica", 12))
    last_name_entry.place(x=150, y=180)

    password_label = Label(signup_window, text="Password:", font=("Helvetica", 12), bg="black", fg="white")
    password_label.place(x=20, y=220)
    password_entry = Entry(signup_window, show="*", font=("Helvetica", 12))
    password_entry.place(x=150, y=220)

    retype_password_label = Label(signup_window, text="Retype Password:", font=("Helvetica", 12), bg="black",
                                  fg="white")
    retype_password_label.place(x=20, y=260)
    retype_password_entry = Entry(signup_window, show="*", font=("Helvetica", 12))
    retype_password_entry.place(x=150, y=260)

    user_type_label = Label(signup_window, text="User Type:", font=("Helvetica", 12), bg="black", fg="white")
    user_type_label.place(x=20, y=300)
    user_type_var = StringVar()
    student_radiobutton = Radiobutton(signup_window, text="Student", variable=user_type_var, value="student",
                                      font=("Helvetica", 12), bg="black", fg="white")
    student_radiobutton.place(x=150, y=300)
    staff_radiobutton = Radiobutton(signup_window, text="Staff", variable=user_type_var, value="staff",
                                    font=("Helvetica", 12), bg="black", fg="white")
    staff_radiobutton.place(x=250, y=300)

    # Add a sign-up button
    # The lambda keyword allows you to define a function inline without needing to assign it a name
    # TBR
    signup_button = Button(signup_window, text="Sign Up", command=lambda: login("signup"), font=("Helvetica", 14))
    signup_button.place(x=100, y=350)

    # add a login button
    # root.deiconify() brings main window bak into view
    login_button = Button(signup_window, text="Login", command=root.deiconify, font=("Helvetica", 14))
    login_button.place(x=200, y=350)

    # Keep a reference to the background image
    signup_bg_label.image = signup_bg_image

# code for login window
def open_login_window():
    # Close the current window
    root.withdraw()

    # create a new window for login
    login_window = Toplevel()
    login_window.title("Login")
    login_window.geometry('990x660+50+50')
    login_window.resizable(0, 0)
    login_bg_image = ImageTk.PhotoImage(file='./images/nebula.jpg')

    # create a label and set the background image
    login_bg_label = Label(login_window, image=login_bg_image)
    login_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Add entry fields on top of the background image
    username_label = Label(login_window, text="Username:", font=("Helvetica", 12), bg="black", fg="white")
    username_label.place(x=20, y=20)
    username_entry = Entry(login_window, font=("Helvetica", 12))
    username_entry.place(x=150, y=20)

    password_label = Label(login_window, text="Password:", font=("Helvetica", 12), bg="black", fg="white")
    password_label.place(x=20, y=60)
    password_entry = Entry(login_window, show="*", font=("Helvetica", 12))
    password_entry.place(x=150, y=60)

    # Add a login button
    login_button = Button(login_window, text="Login", command=lambda: login("login"), font=("Helvetica", 14))
    login_button.place(x=100, y=100)

    # Add a sign-up button
    # The lambda keyword allows you to define a function inline without needing to assign it a name
    # TBR
    signup_button = Button(login_window, text="Sign Up", command=lambda: login("signup"), font=("Helvetica", 14))
    signup_button.place(x=100, y=350)

    # Keep a reference to the background image
    login_bg_label.image = login_bg_image

# GUI
root = Tk()
root.geometry('990x660+50+50')
root.title("University Customer Care Chatbot")
root.resizable(0, 0)
bgImage = ImageTk.PhotoImage(file='./images/nebula.jpg')

bgLabel = Label(root, image=bgImage)
bgLabel.place(x=0, y=0)

heading = Label(root, text="USER LOGIN", font=("Helevicta", 22, 'bold'), fg="black")
heading.place(x=660, y=120)

# entry field (USERNAME)
usernameEntry = Entry(root, width=25, font=("Helevicta", 13, 'bold'), bd=0, fg='black')
usernameEntry.place(x=620, y=200)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', lambda event: on_enter(event, usernameEntry, 'Username'))

# password
passwordEntry = Entry(root, width=25, font=("Helevicta", 13, 'bold'), bd=0, fg='black')
passwordEntry.place(x=620, y=250)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', lambda event: on_enter(event, passwordEntry, 'Password'))

# buttons(Login)
loginButton = Button(root, text="LOGIN", width=10, bd=0, fg='black', command=open_login_window)
loginButton.place(x=620, y=300)

# sign up
signupButton = Button(root, text="SIGN UP", width=10, bd=0, fg="black", command=open_sign_up_window)
signupButton.place(x=760, y=300)

root.mainloop()
