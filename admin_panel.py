import tkinter as tk
import subprocess
from PIL import Image, ImageTk


def open_admin_panel(root, login_window):
    # Close the login window
    login_window.withdraw()

    # Create the admin panel window
    admin_panel_window = tk.Toplevel(root)
    admin_panel_window.title("Admin Panel")
    admin_panel_window.geometry("1800x1000+50+50")

    # Create a canvas for the admin panel window
    admin_panel_canvas = tk.Canvas(admin_panel_window, width=1800, height=1000)
    admin_panel_canvas.pack(fill=tk.BOTH, expand=True)

    # Function to resize the background image
    def resize_background_image(event):
        canvas_width = event.width
        canvas_height = event.height
        bg_image = ImageTk.PhotoImage(Image.open('./images/nebula.jpg').resize((canvas_width, canvas_height)))
        admin_panel_canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=tk.CENTER, image=bg_image)
        admin_panel_canvas.bg_image = bg_image

    # Bind the <Configure> event to the admin panel canvas to resize the background image
    admin_panel_canvas.bind('<Configure>', resize_background_image)

    # Load the initial background image for the admin panel window
    bg_image = ImageTk.PhotoImage(Image.open('./images/nebula.jpg'))
    admin_panel_canvas.create_image(admin_panel_canvas.winfo_width() // 2, admin_panel_canvas.winfo_height() // 2,
                                    anchor=tk.CENTER, image=bg_image)
    admin_panel_canvas.bg_image = bg_image  # Keep a reference to prevent garbage collection

    def logout():
        # Close the admin panel window
        admin_panel_window.destroy()

    def launch_manage_users():
        subprocess.Popen(["python", "admin.py"])
        # Destroy the admin panel after launching admin.py for managing users
        admin_panel_window.destroy()

    def launch_manage_inquiries():
        subprocess.Popen(["python", "inquiry.py"])
        admin_panel_window.destroy()

    def launch_manage_intents():
        subprocess.Popen(["python", "intents.py"])
        admin_panel_window.destroy()

    # Create buttons for admin panel functions
    manage_users_button = tk.Button(admin_panel_window, text="Manage Users", command=launch_manage_users,
                                    font=("Helvetica", 16), fg="white", bg="#7f1d1d")
    manage_users_button.place(x=800, y=200, width=250, height=70)

    handle_inquiries_button = tk.Button(admin_panel_window, text="Handle Inquiries", command=launch_manage_inquiries,
                                        font=("Helvetica", 16), fg="white", bg="#7f1d1d")
    handle_inquiries_button.place(x=800, y=280, width=250, height=70)

    intents_button = tk.Button(admin_panel_window, text="Manage Intents", command=launch_manage_intents,
                               font=("Helvetica", 16), fg="white", bg="#7f1d1d")
    intents_button.place(x=800, y=360, width=250, height=70)

    logout_button = tk.Button(admin_panel_window, text="Log Out", command=logout, font=("Helvetica", 16), fg="white",
                              bg="#7f1d1d")
    logout_button.place(x=800, y=440, width=250, height=70)

    # Show the admin panel window
    admin_panel_window.mainloop()
