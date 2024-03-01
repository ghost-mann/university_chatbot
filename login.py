from tkinter import *
from PIL import ImageTk

#Functionality Part

def on_enter(event):
    if usernameEntry.get()=='Username':
        usernameEntry.delete(0,END)

#GUI
root = Tk()
root.geometry('990x660+50+50')
root.title("University Customer Care Chatbot")
root.resizable(0, 0)
bgImage=ImageTk.PhotoImage(file='./images/nebula.jpg')

bgLabel=Label(root,image=bgImage)
bgLabel.place(x=0,y=0)

heading=Label(root,text="USER LOGIN",font=("Helevicta", 22, 'bold'), fg="black")
heading.place(x=660,y=120)


#entry field
usernameEntry=Entry(root,width=25,font=("Helevicta", 13, 'bold'),bd=0, fg='black')
usernameEntry.place(x=620,y=200)
usernameEntry.insert(0, 'Username')

usernameEntry.bind('<FocusIn>',on_enter)

root.mainloop()