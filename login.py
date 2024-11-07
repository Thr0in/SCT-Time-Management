"""
Created on Thu Nov  7 10:00:33 2024

@author: lpasd
"""


import tkinter as tk
from tkinter import messagebox


def login():
    username = entry_username.get()
    password = entry_password.get()

    with open("userdaten.txt", "r") as file:
        users = file.readlines()

    for user in users:
        user_data = user.strip().split(",")
        if len(user_data) == 3:
            file_username, file_password, role = user_data
            if username == file_username and password == file_password:
                
                
                messagebox.showinfo("Login Erfolgreich", f"Login Erfolgreich als {username}")
                return

                messagebox.showerror("Fehler", "Benutzername oder Passwort ist falsch!")



root = tk.Tk()
root.title("Login Screen")
root.geometry("300x200")


label_title = tk.Label(root, text="Bitte einloggen", font=("Arial", 14))
label_title.pack(pady=10)

label_username = tk.Label(root, text="Benutzername:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

label_password = tk.Label(root, text="Passwort:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

button_login = tk.Button(root, text="Login", command=login)
button_login.pack(pady=10)

# GUI ausführen
root.mainloop()
