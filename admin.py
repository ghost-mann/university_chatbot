import subprocess
import tkinter as tk
from tkinter import ttk
import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="chatbot"
)
cursor = conn.cursor()


# Function to display users
def display_users(tree):
    # Clear existing data
    for item in tree.get_children():
        tree.delete(item)

    # Fetch user data from the database
    query = 'SELECT admission_number, first_name, last_name, email, department FROM users'
    cursor.execute(query)
    users = cursor.fetchall()

    # Insert user data into the table
    for user in users:
        admission_number, first_name, last_name, email, department = user
        tree.insert("", "end", values=(admission_number, first_name, last_name, email, department))


# Create the main window
root = tk.Tk()
root.title("Manage Users")
root.geometry("1250x660+50+50")

# Create a treeview to display user data
user_tree = ttk.Treeview(root, columns=("admission_number", "first_name", "last_name", "email", "department"),
                         show="headings")
user_tree.heading("admission_number", text="Admission Number")
user_tree.heading("first_name", text="First Name")
user_tree.heading("last_name", text="Last Name")
user_tree.heading("email", text="Email")
user_tree.heading("department", text="Department")

# Add a scrollbar to the treeview
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=user_tree.yview)
user_tree.configure(yscrollcommand=scrollbar.set)

# Pack the treeview and scrollbar
user_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Display users
display_users(user_tree)

# Add buttons for editing, viewing, and deleting users
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X)


def edit_user():
    selected_item = user_tree.selection()
    if selected_item:
        admission_number, first_name, last_name, email, department = user_tree.item(selected_item)["values"]
        # Implement your logic for editing the user here
        print(
            f"Editing user with Admission Number: {admission_number}, First Name: {first_name}, Last Name: {last_name}, Email: {email}, Department: {department}")


edit_button = tk.Button(button_frame, text="Edit User", command=edit_user)
edit_button.pack(side=tk.LEFT, padx=5, pady=5)


def back_button():
    root.destroy()
    subprocess.Popen(["python", "sign.py", "open_admin_panel"])


back_button = tk.Button(button_frame, text="Back", command=back_button)
back_button.pack(side=tk.LEFT, padx=5, pady=5)


def delete_user():
    selected_item = user_tree.selection()
    if selected_item:
        admission_number = user_tree.item(selected_item)["values"][0]
        # Implement your logic for deleting the user here
        print(f"Deleting user with Admission Number: {admission_number}")


delete_button = tk.Button(button_frame, text="Delete User", command=delete_user)
delete_button.pack(side=tk.LEFT, padx=5, pady=5)

root.mainloop()

# Close the database connection
cursor.close()
conn.close()
