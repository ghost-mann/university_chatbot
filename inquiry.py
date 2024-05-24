import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import subprocess

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="chatbot"
)
cursor = conn.cursor()

# Assume this variable is set after a successful admin login
logged_in_admin_username = "austin"  # Replace with the actual admin username


# Function to log admin operations
def log_admin_operation(operation, table_name, record):
    try:
        # Insert the admin operation into the database
        query = "INSERT INTO admin_logs (admin_username, operation, table_name, record) VALUES (%s, %s, %s, %s)"
        values = (logged_in_admin_username, operation, table_name, str(record))
        cursor.execute(query, values)
        conn.commit()

    except mysql.connector.Error as error:
        print("Error logging admin operation:", error)


def display_inquiries(tree):
    # Clear existing data
    tree.delete(*tree.get_children())

    # Fetch inquiry data from the database with email and is_resolved
    query = """
        SELECT i.inquiry, i.admission_number, u.email, i.is_resolved
        FROM inquiries i
        JOIN users u ON i.admission_number = u.admission_number
    """
    cursor.execute(query)
    inquiries = cursor.fetchall()  # Fetch the result set

    # Insert inquiry data into the table
    for index, inquiry in enumerate(inquiries):
        admission_number = inquiry[1]
        email = inquiry[2]
        inquiry_text = inquiry[0]
        is_resolved = inquiry[3]
        resolved_status = "Resolved" if is_resolved else "Unresolved"
        tree.insert("", "end", values=(index + 1, admission_number, email, inquiry_text, resolved_status))


def mark_inquiry_resolved():
    selected_item = inquiry_tree.selection()
    if selected_item:
        item_values = inquiry_tree.item(selected_item)["values"]
        index = item_values[0]
        admission_number = item_values[1]
        inquiry_text = item_values[3]

        query = "UPDATE inquiries SET is_resolved = TRUE WHERE admission_number = %s AND inquiry = %s"
        cursor.execute(query, (admission_number, inquiry_text))
        conn.commit()
        cursor.fetchall()  # Consume the result set
        messagebox.showinfo("Success", "Inquiry marked as resolved!")
        display_inquiries(inquiry_tree)

        # Log the admin operation
        log_admin_operation("Mark Inquiry Resolved", "inquiries", (admission_number, inquiry_text))
    else:
        messagebox.showerror("Error", "Please select an inquiry to mark as resolved.")


def mark_inquiry_unresolved():
    selected_item = inquiry_tree.selection()
    if selected_item:
        item_values = inquiry_tree.item(selected_item)["values"]
        index = item_values[0]
        admission_number = item_values[1]
        inquiry_text = item_values[3]

        query = "UPDATE inquiries SET is_resolved = FALSE WHERE admission_number = %s AND inquiry = %s"
        cursor.execute(query, (admission_number, inquiry_text))
        conn.commit()
        cursor.fetchall()  # Consume the result set
        messagebox.showinfo("Success", "Inquiry marked as unresolved!")
        display_inquiries(inquiry_tree)

        # log admin operation
        log_admin_operation("Mark Inquiry Unresolved", "inquiries", (admission_number, inquiry_text))
    else:
        messagebox.showerror("Error", "Please select an inquiry to mark as unresolved.")


def delete_inquiry():
    selected_item = inquiry_tree.selection()
    if selected_item:
        item_values = inquiry_tree.item(selected_item)["values"]
        index = item_values[0]
        admission_number = item_values[1]
        inquiry_text = item_values[3]

        confirm = messagebox.askyesno("Confirm Deletion",
                                      f"Are you sure you want to delete the inquiry with Index: {index}, Admission "
                                      f"Number: {admission_number}, and Inquiry: {inquiry_text}?")
        if confirm:
            query = "DELETE FROM inquiries WHERE admission_number = %s AND inquiry = %s"
            cursor.execute(query, (admission_number, inquiry_text))
            conn.commit()
            messagebox.showinfo("Success", "Inquiry deleted successfully!")
            display_inquiries(inquiry_tree)
            log_admin_operation("Delete Inquiry", "inquiries", (admission_number, inquiry_text))
    else:
        messagebox.showerror("Error", "Please select an inquiry to delete.")


def intents():
    subprocess.Popen(["python", "intents.py"])
    root.withdraw()
    log_admin_operation("Open Intents", "admin_logs", "-")


def users():
    subprocess.Popen(["python", "admin.py"])
    root.withdraw()
    log_admin_operation("Open Users", "admin_logs", "-")


def logout():
    root.withdraw()
    log_admin_operation("Logout", "admin_logs", "-")


# Create the main window
root = tk.Tk()
root.title("Manage Inquiries")
root.geometry("1800x1000+50+50")

# Create a treeview to display inquiry data
inquiry_tree = ttk.Treeview(root, columns=("index", "admission_number", "email", "inquiry", "status"), show="headings")
inquiry_tree.heading("index", text="Index")
inquiry_tree.heading("admission_number", text="Admission Number")
inquiry_tree.heading("email", text="Email")
inquiry_tree.heading("inquiry", text="Inquiry")
inquiry_tree.heading("status", text="Status")

# Add a scrollbar to the treeview
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=inquiry_tree.yview)
inquiry_tree.configure(yscrollcommand=scrollbar.set)

# Pack the treeview and scrollbar
inquiry_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Display inquiries
display_inquiries(inquiry_tree)

intent_button = tk.Button(root, text="Manage Intents", command=lambda: intents())
intent_button.pack(side=tk.BOTTOM)

user_button = tk.Button(root, text="Manage Users", command=lambda: users())
user_button.pack(side=tk.BOTTOM)

delete_button = tk.Button(root, text="Delete Inquiry", command=lambda: delete_inquiry())
delete_button.pack(side=tk.BOTTOM)

resolve_button = tk.Button(root, text="Mark as Resolved", command=lambda: mark_inquiry_resolved())
resolve_button.pack(side=tk.BOTTOM)

unresolved_button = tk.Button(root, text="Mark as Unresolved", command=lambda: mark_inquiry_unresolved())
unresolved_button.pack(side=tk.BOTTOM)

logout_button = tk.Button(root, text="Logout", command=lambda: logout())
logout_button.pack(side=tk.BOTTOM, padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()

# Close the database connection
cursor.close()
conn.close()
