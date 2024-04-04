# Import necessary libraries and modules

from tkinter import *
from botapp import ChatApp as cA
import nltk
# nltk.download('punkt')
# nltk.download('wordnet')

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


# Create the main GUI window
base = Tk()
base.title("ChatBot - SL")
base.geometry("990x660+50+50")
base.resizable(width=FALSE, height=FALSE)

# Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial", )
ChatLog.config(state=DISABLED)

# vertical scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="arrow", width=20)
ChatLog['yscrollcommand'] = scrollbar.set

# horizontal scrollbar
h_scrollbar = Scrollbar(base, orient='horizontal', command=ChatLog.xview, width=20, cursor="arrow")
ChatLog['xscrollcommand'] = h_scrollbar.set
# Create Button to send message
SendButton = Button(base, font=("Verdana", 12, 'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                    command=send)

# Create the box to enter message
EntryBox = Text(base, bd=0, bg="white", width="29", height="5", font="Arial")

# Place all components on the screen
scrollbar.place(x=545, y=6, height=386)
h_scrollbar.place(x=2, y=395, width=550)
ChatLog.place(x=6, y=6, height=386, width=550)
EntryBox.place(x=128, y=450, height=90, width=440)
SendButton.place(x=6, y=450, height=90)

# Start the GUI main loop
base.mainloop()
