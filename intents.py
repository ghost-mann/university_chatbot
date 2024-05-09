import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from PIL import ImageTk, Image

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="admin",
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
        tag, patterns, responses = intent_tree.item(selected_item)["values"]
        edit_intent_window(tag, patterns, responses)
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


# Function to go back to the main menu
def logout():
    # Close the current window
    root.destroy()

# Function to open the edit intent window
def edit_intent_window(tag, patterns, responses):
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Intent")

    # Create input fields for editing the intent
    tag_label = tk.Label(edit_window, text="Tag:", font=("Helvetica", 12))
    tag_label.grid(row=0, column=0, padx=10, pady=10)
    tag_entry = tk.Entry(edit_window, font=("Helvetica", 12))
    tag_entry.grid(row=0, column=1, padx=10, pady=10)
    tag_entry.insert(0, tag)

    patterns_label = tk.Label(edit_window, text="Patterns:", font=("Helvetica", 12))
    patterns_label.grid(row=1, column=0, padx=10, pady=10)
    patterns_entry = tk.Entry(edit_window, font=("Helvetica", 12))
    patterns_entry.grid(row=1, column=1, padx=10, pady=10)
    patterns_entry.insert(0, patterns)

    responses_label = tk.Label(edit_window, text="Responses:", font=("Helvetica", 12))
    responses_label.grid(row=2, column=0, padx=10, pady=10)
    responses_entry = tk.Entry(edit_window, font=("Helvetica", 12))
    responses_entry.grid(row=2, column=1, padx=10, pady=10)
    responses_entry.insert(0, responses)

    # Create a save button to update the intent
    def save_intent():
        new_tag = tag_entry.get()
        new_patterns = patterns_entry.get()
        new_responses = responses_entry.get()

        if new_tag and new_patterns and new_responses:
            values = (new_tag, new_patterns, new_responses, tag)
            query = "UPDATE intents SET tag = %s, patterns = %s, responses = %s WHERE tag = %s"
            cursor.execute(query, values)
            conn.commit()
            load_intents()
            edit_window.destroy()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    save_button = tk.Button(edit_window, text="Save", command=save_intent, font=("Helvetica", 12))
    save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


# Create the main window
root = tk.Tk()
root.title("Manage Intents")
root.geometry("1800x1000+50+50")

# Create a canvas for the main window
canvas = tk.Canvas(root, width=1800, height=1000)
canvas.pack(fill=tk.BOTH, expand=True)

# Load the background image (you can replace this with your preferred image)
bg_image = ImageTk.PhotoImage(Image.open("./images/nebula.jpg").resize((1800, 1000)))
canvas.create_image(900, 500, image=bg_image)

# Create a treeview to display intents
intent_tree = ttk.Treeview(root, columns=("Tag", "Patterns", "Responses"), height=20)
intent_tree.heading("#0", text="")
intent_tree.heading("Tag", text="Tag")
intent_tree.heading("Patterns", text="Patterns")
intent_tree.heading("Responses", text="Responses")
intent_tree.column("#0", width=0, stretch=tk.NO)
intent_tree.column("Tag", width=200)
intent_tree.column("Patterns", width=400)
intent_tree.column("Responses", width=400)
intent_tree.place(x=350, y=100)

# Load existing intents from the database
load_intents()

# Create input fields for adding/editing intents
tag_label = tk.Label(root, text="Tag:", font=("Helvetica", 16), bg="#431407", fg="#f8fafc")
tag_label.place(x=200, y=600)
tag_entry = tk.Entry(root, font=("Helvetica", 16))
tag_entry.place(x=300, y=600, width=300)

patterns_label = tk.Label(root, text="Patterns:", font=("Helvetica", 16), bg="#431407", fg="#f8fafc")
patterns_label.place(x=200, y=700)
patterns_entry = tk.Entry(root, font=("Helvetica", 16))
patterns_entry.place(x=320, y=700, width=600)

responses_label = tk.Label(root, text="Responses:", font=("Helvetica", 16), bg="#431407", fg="#f8fafc")
responses_label.place(x=200, y=800)
responses_entry = tk.Entry(root, font=("Helvetica", 16))
responses_entry.place(x=320, y=800, width=600)

# Create buttons for managing intents
add_button = tk.Button(root, text="Add", command=add_intent, font=("Helvetica", 16), bg="#431407", fg="#f8fafc",
                       width=10, height=2)
add_button.place(x=1200, y=600)

edit_button = tk.Button(root, text="Edit", command=edit_intent, font=("Helvetica", 16), bg="#431407", fg="#f8fafc",
                        width=10, height=2)
edit_button.place(x=1200, y=700)

delete_button = tk.Button(root, text="Delete", command=delete_intent, font=("Helvetica", 16), bg="#431407",fg="#f8fafc", width=10, height=2)
delete_button.place(x=1200, y=800)

logout_button = tk.Button(root, text="Logout", command=logout, font=("Helvetica", 16), bg="#431407",fg="#f8fafc" ,width=10, height=2)
logout_button.place(x=200, y=900)

# Run the main loop
root.mainloop()

# Close the database connection
cursor.close()
conn.close()