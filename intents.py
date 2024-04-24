import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from PIL import ImageTk, Image

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="austin",
    password="root",
    database="chatbot"
)
cursor = conn.cursor()


# Function to load intents from the database
def load_intents():
    intent_tree.delete(*intent_tree.get_children())
    query = "SELECT tag, patterns, responses FROM intents"
    cursor.execute(query)
    intents = cursor.fetchall()

    for intent in intents:
        tag, patterns, responses = intent
        intent_tree.insert("", "end", values=(tag, patterns, responses))


# Function to add a new intent
def add_intent():
    tag = tag_entry.get()
    patterns = patterns_entry.get()
    responses = responses_entry.get()

    if tag and patterns and responses:
        query = "INSERT INTO intents (tag, patterns, responses) VALUES (%s, %s, %s)"
        values = (tag, patterns, responses)
        cursor.execute(query, values)
        conn.commit()
        load_intents()
        tag_entry.delete(0, tk.END)
        patterns_entry.delete(0, tk.END)
        responses_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please fill in all fields.")


# Function to edit an existing intent
def edit_intent():
    selected_item = intent_tree.focus()
    if selected_item:
        tag = tag_entry.get()
        patterns = patterns_entry.get()
        responses = responses_entry.get()

        if tag and patterns and responses:
            values = (tag, patterns, responses, intent_tree.item(selected_item)["values"][0])
            query = "UPDATE intents SET tag = %s, patterns = %s, responses = %s WHERE tag = %s"
            cursor.execute(query, values)
            conn.commit()
            load_intents()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    else:
        messagebox.showerror("Error", "Please select an intent to edit.")


# Function to delete an intent
def delete_intent():
    selected_item = intent_tree.focus()
    if selected_item:
        tag = intent_tree.item(selected_item)["values"][0]
        query = "DELETE FROM intents WHERE tag = %s"
        cursor.execute(query, (tag,))
        conn.commit()
        load_intents()
    else:
        messagebox.showerror("Error", "Please select an intent to delete.")


# Create the main window
root = tk.Tk()
root.title("Manage Intents")
root.geometry("1800x1000+50+50")

# Create a canvas for the main window
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill=tk.BOTH, expand=True)

# Load the background image (you can replace this with your preferred image)
bg_image = ImageTk.PhotoImage(Image.open("./images/nebula.jpg"))
canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)

# Create a treeview to display intents
intent_tree = ttk.Treeview(root, columns=("Tag", "Patterns", "Responses"))
intent_tree.heading("#0", text="")
intent_tree.heading("Tag", text="Tag")
intent_tree.heading("Patterns", text="Patterns")
intent_tree.heading("Responses", text="Responses")
intent_tree.column("#0", width=0, stretch=tk.NO)
intent_tree.column("Tag", width=150)
intent_tree.column("Patterns", width=250)
intent_tree.column("Responses", width=250)
intent_tree.place(x=50, y=50)

# Load existing intents from the database
load_intents()

# Create input fields for adding/editing intents
tag_label = tk.Label(root, text="Tag:", font=("Helvetica", 12))
tag_label.place(x=50, y=350)
tag_entry = tk.Entry(root, font=("Helvetica", 12))
tag_entry.place(x=100, y=350, width=200)

patterns_label = tk.Label(root, text="Patterns:", font=("Helvetica", 12))
patterns_label.place(x=50, y=380)
patterns_entry = tk.Entry(root, font=("Helvetica", 12))
patterns_entry.place(x=100, y=380, width=400)

responses_label = tk.Label(root, text="Responses:", font=("Helvetica", 12))
responses_label.place(x=50, y=410)
responses_entry = tk.Entry(root, font=("Helvetica", 12))
responses_entry.place(x=100, y=410, width=400)

# Create buttons for managing intents
add_button = tk.Button(root, text="Add", command=add_intent, font=("Helvetica", 12))
add_button.place(x=550, y=350)

edit_button = tk.Button(root, text="Edit", command=edit_intent, font=("Helvetica", 12))
edit_button.place(x=550, y=380)

delete_button = tk.Button(root, text="Delete", command=delete_intent, font=("Helvetica", 12))
delete_button.place(x=550, y=410)

# Run the main loop
root.mainloop()

# Close the database connection
cursor.close()
conn.close()
