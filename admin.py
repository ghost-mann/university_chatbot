import subprocess
import tkinter as tk
from datetime import datetime

# Connect to MySQL database
from tkinter import ttk, messagebox
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="chatbot"
)
cursor = conn.cursor()

# Admin name (replace with your logic to get the actual admin name)
admin_name = "austin"


def log_operation(operation_type, user_details, table_name):
    insert_query = "INSERT INTO admin_logs (operation, record, table_name, admin_username) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (operation_type, user_details, table_name, admin_name))
    conn.commit()


def display_users(tree):
    # Clear existing data
    tree.delete(*tree.get_children())

    # Fetch user data from the database
    query = 'SELECT admission_number, first_name, last_name, email, department, dob FROM users'
    cursor.execute(query)
    users = cursor.fetchall()

    # Insert user data into the table
    for user in users:
        admission_number, first_name, last_name, email, department, dob = user
        tree.insert("", "end", values=(admission_number, first_name, last_name, email, department, dob))


def edit_user(tree):
    selected_item = tree.selection()
    if selected_item:
        admission_number, first_name, last_name, email, department, dob = tree.item(selected_item)["values"]
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit User")
        edit_window.geometry("1000x660+50+50")

        # First Name
        first_name_label = tk.Label(edit_window, text="First Name:")
        first_name_label.pack()
        first_name_entry = tk.Entry(edit_window)
        first_name_entry.insert(0, first_name)
        first_name_entry.pack()

        # Last Name
        last_name_label = tk.Label(edit_window, text="Last Name:")
        last_name_label.pack()
        last_name_entry = tk.Entry(edit_window)
        last_name_entry.insert(0, last_name)
        last_name_entry.pack()

        # Email
        email_label = tk.Label(edit_window, text="Email:")
        email_label.pack()
        email_entry = tk.Entry(edit_window)
        email_entry.insert(0, email)
        email_entry.pack()

        # Department
        department_label = tk.Label(edit_window, text="Department:")
        department_label.pack()
        department_entry = tk.Entry(edit_window)
        department_entry.insert(0, department)
        department_entry.pack()

        # date of birth
        dob_label = tk.Label(edit_window, text="Date of Birth:")
        dob_label.pack()
        dob_entry = tk.Entry(edit_window)
        dob_entry.insert(0, dob)
        dob_entry.pack()

        def save_changes():
            new_first_name = first_name_entry.get()
            new_last_name = last_name_entry.get()
            new_email = email_entry.get()
            new_department = department_entry.get()
            new_dob = dob_entry.get()

            update_query = "UPDATE users SET first_name = %s, last_name = %s, email = %s, department = %s, dob = %s WHERE admission_number = %s"
            cursor.execute(update_query,
                           (new_first_name, new_last_name, new_email, new_department, new_dob, admission_number))
            conn.commit()
            user_details = f"Admission Number: {admission_number}, First Name: {new_first_name}, Last Name: {new_last_name}, Email: {new_email}, Department: {new_department}, DOB: {new_dob}"
            log_operation("Update", user_details, "users")
            messagebox.showinfo("Success", "User details updated successfully!")
            edit_window.destroy()
            display_users(user_tree)

        save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.pack()


def delete_user(tree):
    selected_item = tree.selection()
    if selected_item:
        admission_number, first_name, last_name, email, department, dob = tree.item(selected_item)["values"]
        confirm = messagebox.askyesno("Confirm Deletion",
                                      f"Are you sure you want to delete the user with Admission Number: {admission_number}?")
        if confirm:
            delete_query = "DELETE FROM users WHERE admission_number = %s"
            cursor.execute(delete_query, (admission_number,))
            conn.commit()
            user_details = f"Admission Number: {admission_number}, First Name: {first_name}, Last Name: {last_name}, Email: {email}, Department: {department}, DOB: {dob}"
            log_operation("Delete", user_details, "users")
            messagebox.showinfo("Success", "User deleted successfully!")
            display_users(user_tree)


def inquiries():
    subprocess.Popen(["python", "inquiry.py"])
    root.withdraw()


def intents():
    subprocess.Popen(["python", "intents.py"])
    root.withdraw()


def back_to_admin_panel():
    root.withdraw()


# Create the main window
root = tk.Tk()
root.title("Manage Users")
root.geometry("1800x1000+50+50")

# Create a treeview to display user data
user_tree = ttk.Treeview(root, columns=(
    "admission_number", "first_name", "last_name", "email", "department", "date of birth"),
                         show="headings")
user_tree.heading("admission_number", text="Admission Number")
user_tree.heading("first_name", text="First Name")
user_tree.heading("last_name", text="Last Name")
user_tree.heading("email", text="Email")
user_tree.heading("department", text="Department")
user_tree.heading("date of birth", text="Date of Birth")

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

edit_button = tk.Button(button_frame, text="Edit User", command=lambda: edit_user(user_tree))
edit_button.pack(side=tk.LEFT, padx=5, pady=5)

delete_button = tk.Button(button_frame, text="Delete User", command=lambda: delete_user(user_tree))
delete_button.pack(side=tk.LEFT, padx=5, pady=5)

inquiry_button = tk.Button(button_frame, text="Inquiries", command=inquiries)
inquiry_button.pack(side=tk.LEFT, padx=5, pady=5)

intents_button = tk.Button(button_frame, text="Intents", command=intents)
intents_button.pack(side=tk.LEFT, padx=5, pady=5)

logout_button = tk.Button(button_frame, text="Logout", command=back_to_admin_panel)
logout_button.pack(side=tk.LEFT, padx=1, pady=5)

root.mainloop()

# Close the database connection
cursor.close()
conn.close()
