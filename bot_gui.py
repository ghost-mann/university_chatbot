# Import necessary libraries and modules
from tkinter import *
from tkinter import messagebox
import subprocess
from botapp import ChatApp as cA
import mysql.connector
import sys

admission_number = sys.argv[2]

# Define the function to send messages
def send():
    # Get the message from the EntryBox
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)

    # Check if the message is not empty
    if msg != '':
        # Update ChatLog with user's message
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12))

        # Get chatbot response and update ChatLog
        res = cA().chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)

        # Log the user's message and chatbot's response into the database
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="chatbot"
            )
            cursor = conn.cursor()

            # Insert the user's message and chatbot's response into the database
            query = "INSERT INTO user_logs (admission_number, user_message, chatbot_response) VALUES (%s, %s, %s)"
            values = (admission_number, msg, res)
            cursor.execute(query, values)
            conn.commit()

            # Close the database connection
            cursor.close()
            conn.close()

        except mysql.connector.Error as error:
            print("Error logging user message and chatbot response:", error)

# function to submit inquiry into the database
def submit_inquiry():
    inquiry_text = InquiryBox.get("1.0", 'end-1c').strip()
    InquiryBox.delete("0.0", END)

    if inquiry_text:
        try:
            # connect to the database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="chatbot"
            )
            cursor = conn.cursor()

            # insert the inquiry into the database
            query = "INSERT INTO inquiries (inquiry, admission_number) VALUES (%s, %s)"
            values = (inquiry_text, admission_number)
            cursor.execute(query, values)
            conn.commit()

            # close the database connection
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Inquiry submitted successfully!")
        except mysql.connector.Error as error:
            print("Error submitting inquiry:", error)
            messagebox.showerror("Error", "Failed to submit inquiry! Please try again.")

# Function to get the logged-in user's admission number
def get_logged_in_user_admission_number():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="chatbot"
        )
        cursor = conn.cursor()

        logged_in_user_identifier = "example_user"
        query = "SELECT * FROM users WHERE admission_number = %s"
        cursor.execute(query, (logged_in_user_identifier,))
        result = cursor.fetchone()

        # Close the database connection
        cursor.close()
        conn.close()

        # Return the admission number if found, otherwise return None
        if result:
            return result[0]
        else:
            return None
    except mysql.connector.Error as error:
        print("Error connecting to the database:", error)
        return None

def logout():
    subprocess.Popen(["python", "sign.py"])
    base.withdraw()

# Create the main GUI window
base = Tk()
base.title("ChatBot - SL")
base.geometry("1200x800+50+50")
base.resizable(width=FALSE, height=FALSE)

# Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="10", font="Arial")
ChatLog.config(state=DISABLED)

# Vertical scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="arrow", width=20)
ChatLog['yscrollcommand'] = scrollbar.set

# Horizontal scrollbar
h_scrollbar = Scrollbar(base, orient='horizontal', command=ChatLog.xview, width=20, cursor="arrow")
ChatLog['xscrollcommand'] = h_scrollbar.set

# Create Button to send message
SendButton = Button(base, font=("Verdana", 12, 'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                    command=send)

# Create the box to enter message
EntryBox = Text(base, bd=0, bg="white", height="5", font="Arial")

# Create a label to display the admission number
admission_number_label = Label(base, text=f"Admission Number:", font=("Arial", 12, 'bold'))

# create an inquiry submission box
InquiryBox = Text(base, bd=0, bg="white", height="5", font="Arial")

# create a inquire button
inquiry_button = Button(base, font=("Verdana", 12, 'bold'), text="Submit Inquiry", width="12", height=5,
                        bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff', command=submit_inquiry)

# create a logout button
logout_button = Button(base, font=("Verdana", 12, 'bold'), text="Logout", width="12", height=5,
                       bd=0, bg="#32de97", activebackground="#3c9d9b", fg='white', command=logout)

# Get the logged-in user's admission number and update the label
logged_in_user_admission_number = get_logged_in_user_admission_number()
admission_number_label.config(text=f"Admission Number : {admission_number}")

# Place all components on the screen
scrollbar.place(x=680, y=10, height=460)
h_scrollbar.place(x=5, y=475, width=685)
ChatLog.place(x=10, y=10, height=460, width=680)
EntryBox.place(x=160, y=550, height=120, width=550)
SendButton.place(x=10, y=550, height=120)
admission_number_label.place(x=900, y=20)
InquiryBox.place(x=800, y=150, width=380)
inquiry_button.place(x=900, y=350, height=120)
logout_button.place(x=900, y=550, height=120)

# Start the GUI main loop
base.mainloop()