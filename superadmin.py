import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import hashlib

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="chatbot"
)
cursor = conn.cursor()

# Create the main window
root = tk.Tk()
root.title("Super Admin Panel")
root.geometry("1800x1000+50+50")

# Create a canvas for the main window
canvas = tk.Canvas(root, width=1800, height=1000)
canvas.pack(fill=tk.BOTH, expand=True)

# # Load the background image
# bg_image = tk.PhotoImage(file="./images/nebula2.jpg")
# canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)


def show_user_logs():
    # Create a new window to display user logs
    user_logs_window = tk.Toplevel(root)
    user_logs_window.title("User Logs")
    user_logs_window.geometry("1200x800+300+100")

    # Create a treeview to display user logs
    user_logs_tree = ttk.Treeview(user_logs_window, columns=("Timestamp", "Admission Number", "Prompt"))
    user_logs_tree.heading("#0", text="")
    user_logs_tree.heading("Timestamp", text="Timestamp")
    user_logs_tree.heading("Admission Number", text="Admission Number")
    user_logs_tree.heading("Prompt", text="Prompt")
    user_logs_tree.column("#0", width=0, stretch=tk.NO)
    user_logs_tree.column("Timestamp", width=200)
    user_logs_tree.column("Admission Number", width=200)
    user_logs_tree.column("Prompt", width=800)
    user_logs_tree.pack(fill=tk.BOTH, expand=True)

    # Fetch user logs from the database
    query = "SELECT timestamp, admission_number, user_message,chatbot_response FROM user_logs"
    cursor.execute(query)
    user_logs = cursor.fetchall()

    # Insert user logs into the treeview
    for log in user_logs:
        timestamp, admission_number, prompt = log
        user_logs_tree.insert("", "end", values=(timestamp, admission_number, prompt))


def show_admin_logs():
    # Create a new window to display admin logs
    admin_logs_window = tk.Toplevel(root)
    admin_logs_window.title("Admin Logs")
    admin_logs_window.geometry("1200x800+300+100")

    # Create a treeview to display admin logs
    admin_logs_tree = ttk.Treeview(admin_logs_window,
                                   columns=("Timestamp", "Admin Username", "Operation", "Table", "Record"))
    admin_logs_tree.heading("#0", text="")
    admin_logs_tree.heading("Timestamp", text="Timestamp")
    admin_logs_tree.heading("Admin Username", text="Admin Username")
    admin_logs_tree.heading("Operation", text="Operation")
    admin_logs_tree.heading("Table", text="Table")
    admin_logs_tree.heading("Record", text="Record")
    admin_logs_tree.column("#0", width=0, stretch=tk.NO)
    admin_logs_tree.column("Timestamp", width=200)
    admin_logs_tree.column("Admin Username", width=200)
    admin_logs_tree.column("Operation", width=150)
    admin_logs_tree.column("Table", width=200)
    admin_logs_tree.column("Record", width=450)
    admin_logs_tree.pack(fill=tk.BOTH, expand=True)

    # Fetch admin logs from the database
    query = "SELECT timestamp, admin_username, operation, table_name, record FROM admin_logs"
    cursor.execute(query)
    admin_logs = cursor.fetchall()

    # Insert admin logs into the treeview
    for log in admin_logs:
        timestamp, admin_username, operation, table_name, record = log
        admin_logs_tree.insert("", "end", values=(timestamp, admin_username, operation, table_name, record))


# Create buttons for showing user logs and admin logs
users_button = tk.Button(root, text="Users", font=("Helvetica", 30, "bold"), fg="white", bg="#7f1d1d",
                         command=show_user_logs)
users_button.place(x=200, y=400, width=400, height=200)

admins_button = tk.Button(root, text="Admins", font=("Helvetica", 30, "bold"), fg="white", bg="#7f1d1d",
                          command=show_admin_logs)
admins_button.place(x=1200, y=400, width=400, height=200)

root.mainloop()

# Close the database connection
cursor.close()
conn.close()
