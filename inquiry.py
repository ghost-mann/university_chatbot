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


def display_inquiries(tree):
    # Clear existing data
    tree.delete(*tree.get_children())

    # Fetch inquiry data from the database
    query = 'SELECT inquiry, admission_number FROM inquiries'
    cursor.execute(query)
    inquiries = cursor.fetchall()

    # Insert inquiry data into the table
    for index, inquiry in enumerate(inquiries):
        admission_number = inquiry[1]
        inquiry_text = inquiry[0]
        tree.insert("", "end", values=(index + 1, admission_number, inquiry_text))


def back_to_admin_panel():
    root.withdraw()


# Create the main window
root = tk.Tk()
root.title("Manage Inquiries")
root.geometry("1250x660+50+50")

# Create a treeview to display inquiry data
inquiry_tree = ttk.Treeview(root, columns=("index", "admission_number", "inquiry"), show="headings")
inquiry_tree.heading("index", text="Index")
inquiry_tree.heading("admission_number", text="Admission Number")
inquiry_tree.heading("inquiry", text="Inquiry")

# Add a scrollbar to the treeview
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=inquiry_tree.yview)
inquiry_tree.configure(yscrollcommand=scrollbar.set)

# Pack the treeview and scrollbar
inquiry_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Display inquiries
display_inquiries(inquiry_tree)

# Add a button to go back to the admin panel
back_button = tk.Button(root, text="Back", command=back_to_admin_panel)
back_button.pack(side=tk.BOTTOM, padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()

# Close the database connection
cursor.close()
conn.close()
