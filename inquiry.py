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


def display_inquiries(tree):
    # Clear existing data
    tree.delete(*tree.get_children())

    # Fetch inquiry data from the database with email
    query = """
        SELECT i.inquiry, i.admission_number, u.email
        FROM inquiries i
        JOIN users u ON i.admission_number = u.admission_number
    """
    cursor.execute(query)
    inquiries = cursor.fetchall()

    # Insert inquiry data into the table
    for index, inquiry in enumerate(inquiries):
        admission_number = inquiry[1]
        email = inquiry[2]
        inquiry_text = inquiry[0]
        tree.insert("", "end", values=(index + 1, admission_number, email, inquiry_text))

def delete_inquiry():
    selected_item = inquiry_tree.selection()
    if selected_item:
        item_values = inquiry_tree.item(selected_item)["values"]
        index = item_values[0]
        admission_number = item_values[1]
        inquiry_text = item_values[3]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the inquiry with Index: {index}, Admission Number: {admission_number}, and Inquiry: {inquiry_text}?")
        if confirm:
            query = "DELETE FROM inquiries WHERE admission_number = %s AND inquiry = %s"
            cursor.execute(query, (admission_number, inquiry_text))
            conn.commit()
            messagebox.showinfo("Success", "Inquiry deleted successfully!")
            display_inquiries(inquiry_tree)
    else:
        messagebox.showerror("Error", "Please select an inquiry to delete.")

def intents():
    subprocess.Popen(["python", "intents.py"])
    root.withdraw()


def users():
    subprocess.Popen(["python", "admin.py"])
    root.withdraw()


def logout():
    root.withdraw()


# Create the main window
root = tk.Tk()
root.title("Manage Inquiries")
root.geometry("1800x1000+50+50")

# Create a treeview to display inquiry data
inquiry_tree = ttk.Treeview(root, columns=("index", "admission_number", "email", "inquiry"), show="headings")
inquiry_tree.heading("index", text="Index")
inquiry_tree.heading("admission_number", text="Admission Number")
inquiry_tree.heading("email", text="Email")
inquiry_tree.heading("inquiry", text="Inquiry")
# Add a scrollbar to the treeview
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=inquiry_tree.yview)
inquiry_tree.configure(yscrollcommand=scrollbar.set)

# Pack the treeview and scrollbar
inquiry_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Display inquiries
display_inquiries(inquiry_tree)

intent_button = tk.Button(root, text="Manage Intents", command=intents)
intent_button.pack(side=tk.BOTTOM)

user_button = tk.Button(root, text="Manage Users", command=users)
user_button.pack(side=tk.BOTTOM)

delete_button = tk.Button(root, text="Delete Inquiry", command=delete_inquiry)
delete_button.pack(side=tk.BOTTOM)

# Add a button to go back to the admin panel
logout_button = tk.Button(root, text="Logout", command=logout)
logout_button.pack(side=tk.BOTTOM, padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()

# Close the database connection
cursor.close()
conn.close()
