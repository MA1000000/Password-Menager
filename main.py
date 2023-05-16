from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# -------PASSWORD GENERATOR----------------


def password_generate():  # function
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_numbers + password_symbols + password_letters
    random.shuffle(password_list)  # shuffle the password_list

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)  # copying the password from the entry


# ----------SAVE PASSWORD------------------

def save():  # saving the org from entry by button
    website = website_entry.get()  # saving the website name
    email = email_entry.get()  # saving the email
    password = password_entry.get()  # saving the password
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)  # reading old data
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)  # updating old data

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)  # saving updating data
        finally:
            website_entry.delete(0, END)  # dilate website entry
            password_entry.delete(0, END)  # dilate password entry


# --------find password--------


def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email:\t{email}\nPassword:\t{password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists")


# -------------UI SETUP--------------------

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_lebal = Label(text="Website")
website_lebal.grid(row=1, column=0)
email_label = Label(text="Email/Username")
email_label.grid(row=2, column=0)
password_label = Label(text="Password")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=33)
website_entry.grid(row=1, column=1)
email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "menashearad@gmail.com")  # default email
password_entry = Entry(width=33)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(row=1, column=2)
generate_password_button = Button(text="Generate Password", command=password_generate)
generate_password_button.grid(row=3, column=2, columnspan=2)
add_button = Button(text="Add", width=26, command=save)  # calling the save func
add_button.grid(row=6, column=1)

window.mainloop()  # hold the window
