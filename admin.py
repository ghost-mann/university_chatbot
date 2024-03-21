import tkinter as tk
from tkinter import ttk, messagebox
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
user_tree = ttk.Treeview(root, columns=("admission_number", "first_name", "last_name", "email", "department"), show="headings")
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
        # Open a new window to edit user details
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit User")
        edit_window.geometry("990x660+50+50")

        # Create input fields for first name
        first_name_label = tk.Label(edit_window, text="First Name:")
        first_name_label.pack()
        first_name_entry = tk.Entry(edit_window)
        first_name_entry.insert(0, first_name)
        first_name_entry.pack()

        # Create input fields for last name
        last_name_label = tk.Label(edit_window, text="Last Name:")
        last_name_label.pack()
        last_name_entry = tk.Entry(edit_window)
        last_name_entry.insert(0, last_name)
        last_name_entry.pack()

        # Create input fields for email
        email_label = tk.Label(edit_window, text="Email:")
        email_label.pack()
        email_entry = tk.Entry(edit_window)
        email_entry.insert(0, email)
        email_entry.pack()

        # Create input fields for department
        department_label = tk.Label(edit_window, text="Department:")
        department_label.pack()
        department_entry = tk.Entry(edit_window)
        department_entry.insert(0, department)
        department_entry.pack()

        def save_changes():
            new_first_name = first_name_entry.get()
            new_last_name = last_name_entry.get()
            new_email = email_entry.get()
            new_department = department_entry.get()

            # Update the user details in the database
            update_query = "UPDATE users SET first_name = %s, last_name = %s, email = %s, department = %s WHERE admission_number = %s"
            cursor.execute(update_query, (new_first_name, new_last_name, new_email, new_department, admission_number))
            conn.commit()
            messagebox.showinfo("Success", "User details updated successfully!")
            edit_window.destroy()
            display_users(user_tree)

        save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.pack()

def delete_user():
    selected_item = user_tree.selection()
    if selected_item:
        admission_number = user_tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the user with Admission Number: {admission_number}?")
        if confirm:
            # Delete the user from the database
            delete_query = "DELETE FROM users WHERE admission_number = %s"
            cursor.execute(delete_query, (admission_number,))
            conn.commit()
            messagebox.showinfo("Success", "User deleted successfully!")
            display_users(user_tree)

edit_button = tk.Button(button_frame, text="Edit User", command=edit_user)
edit_button.pack(side=tk.LEFT, padx=5, pady=5)

delete_button = tk.Button(button_frame, text="Delete User", command=delete_user)
delete_button.pack(side=tk.LEFT, padx=5, pady=5)

root.mainloop()

# Close the database connection
cursor.close()
conn.close()