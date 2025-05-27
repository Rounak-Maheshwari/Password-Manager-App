from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    # password_list = []
    password_list = [random.choice(letters) for char in range(nr_letters)]
    password_list += [random.choice(symbols) for c in range(nr_symbols)]
    password_list += [random.choice(numbers) for ar in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)                #Copies the password to the clipboard.


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any field empty!")

    else:
        try:
            with open("data.json", "r") as password_file:
                # Reading Old Data
                data = json.load(password_file)
        except FileNotFoundError:
            with open("data.json", "w") as password_file:
                json.dump(new_data, password_file, indent=4)
        else:
            # Updating old data with new Data.
            data.update(new_data)

            with open("data.json", "w") as password_file:
                # Saving updated Data.
                json.dump(data, password_file, indent=4)
        finally:
            # Deleting the contents from the entries of website and password after the add button is called.
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().title()
    try:
        with open("data.json") as password_file:
            data = json.load(password_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:   
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Creating the Canvas Widget
canvas = Canvas(width=200, height=200)
password_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=password_image)
canvas.grid(row=0, column=1)


# Creating the website label
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

# Creating the email/Username label
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

# Creating the Password Label
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)



# Creating the website entry
website_entry = Entry(width=24)
website_entry.grid(row=1, column=1)
website_entry.focus()

# Creating the email entry
email_entry = Entry(width=43)
email_entry.insert(0, "myofficialgmail.com")
email_entry.grid(row=2, column=1, columnspan=2)

# Creating the Password entry
password_entry = Entry(width=24)
password_entry.grid(row=3, column=1)

# Creating search button
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(row=1, column=2)
# Creating the Generate Password button
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)


# Creating the Add button
add_button = Button(text="Add", width=37, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
