import string #Imports the string library with
from tkinter import * #Imports tkinter in order to build the password manager GUI
from tkinter import messagebox #Imports the pop-up messagebox widget from tkinter
import pyperclip #Imports pyperclip for copy/paste clipboard function
import json #Imports json module to save passwords into a json file
import hashlib #Imports the hashlib module to hash our passwords
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
from random import choice, randint, shuffle #Imports various randomization functions

#First I define a function to generate our strong password
def generate_passwd():
    letters = string.ascii_lowercase + string.ascii_uppercase #This calls the letters in the string module
    numbers = string.digits #This calls the digits in the string module
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+'] #This defines the allowed passwords symbols

    #This next block defines the range of letters, symbols and numbers for our password using list comprehension
    passwd_letters = [choice(letters) for i in range(randint(8, 10))] #Randomly selects 8-10 letters
    passwd_symbols = [choice(symbols) for i in range(randint(2, 4))] #Randomly selects 2-4 symbols
    passwd_numbers = [choice(numbers) for i in range(randint(2, 4))] #Randomly selects 2-4 numbers

    password_list = passwd_letters + passwd_symbols + passwd_numbers #Combines the letters, symbols and numbers
    shuffle(password_list) #Randomizes/shuffles the randomly selected letters, numbers and symboles

    password = "".join(password_list) #Joins/concatenates the list of letters, symbols and numbers into a single string
    passwd_input.insert(0, password) #Inserts the generated password into the input password field
    pyperclip.copy(password) #Automatically copies the generated password to clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #
#This function will write the user-defined password into the passwords.json file when the button is clicked
def save_passwd():
    password = passwd_input.get() #Gets the password from the password input field
    hashed_passwd = hashlib.sha256(password.encode()).hexdigest() #Creates a sha256 hash of the password

    #Creates a nested dictionary of key/value pairs
    new_data = {website_input.get(): {
        "email": username_input.get(),
        "password": password,
        "hash": hashed_passwd,
    }}

    #Returns a pop-up dialog box with error description if the website or password fields are empty
    if len(website_input.get()) == 0 or len(passwd_input.get()) == 0:
        messagebox.showinfo(title="Oops", message="Entry field is empty")
    else: #opens up a message box to ask the user if it is ok to save the login credentials
        entry_check = messagebox.askokcancel(title=f"{website_input.get()}", message=f"Your details to be saved are:\n"
                                                                f"Email: {username_input.get()}\n"
                                                                f"Password: {passwd_input.get()}\n"
                                                                f"It it ok to save?")
        if entry_check:
            try: #First it will try to open and read the password file
                with open("passwords.json", "r") as password_file: #Opens the json file in read mode ("r")
                    data = json.load(password_file) #Loads the json file as the variable "data"
            except FileNotFoundError: #If the file does not exist, it will open and write to the file
                with open("passwords.json", "w") as password_file:
                    json.dump(new_data, password_file, indent=4) #Dumps the new data entry into the password file
            else:
                #Update the file data with the new website login credentials
                data.update(new_data)

                with open("passwords.json", "w") as password_file: #Next I open up the file in write ("w") mode
                    json.dump(data, password_file, indent=4) #Dumps the updated data into the file

            finally:
                website_input.delete(0, END) #Clears the website entry on the GUI when the "Add" button is pressed
                passwd_input.delete(0, END) #Clears the password entry on the GUI when the "Add" button is pressed

# ---------------------------- PASSWORD SEARCH ------------------------------- #
# This function will search the passwords.json file using an exception handling structure
def find_passwd():
    try: #First, it will try to open the password file
        with open("passwords.json", "r") as password_file: #Opens the json file in read mode
            data = json.load(password_file) #Defines the password file as data
    except FileNotFoundError: #If there is a File Not Found Error, a error message box pops up
        messagebox.showinfo(title="Error", message="No data file found")
    else: #If there is no exception, it continues through with this else condition to search the password file
        if website_input.get() in data: #If that website data exists, opens up a message box with the login credentials
            messagebox.showinfo(title=f"{website_input.get()}", message=f"Your login credentials are:\n"
                                                            f"Email: {data[website_input.get()]["email"]}\n"
                                                            f"Password: {data[website_input.get()]["password"]}\n"
                                                            f"Hash: {data[website_input.get()]["hash"]}")
        #Else condition for non-existent login credentials for the website that the user searched
        else:
            non_existent = messagebox.showinfo(title=f"{website_input.get()}", #pop-up box to display
                                               message="No credentials for this website exist")


# ---------------------------- GUI SETUP ------------------------------- #
window = Tk() #Define Tk as window
window.title("Password Manager") #Sets the GUI title
window.config(padx=50, pady=50, bg="white") #Configure a perimeter padding for the GUI canvas
canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0) #Sets the canvas size for the GUI image
manager_image = PhotoImage(file="GUI_logo.png") #Create a variable for the password logo using the PhotoImage class
canvas.create_image(100, 100, image=manager_image) #Places the image onto the blank canvas at (x=100 y=100)
canvas.grid(row=0, column=1) #Positions the canvas on the GUI

#The following variables define the website field label/button on the GUI
website_label = Label(text="Website:", bg="white")
website_label.grid(column=0, row=1)
website_label.focus()

#The following variables define the email/username field label on the GUI
user_label = Label(text="Email/Username:", bg="white")
user_label.grid(column=0, row=2)

#The following variables define the password field label/button on the GUI
passwd_label = Label(text="Password:", bg="white")
passwd_label.grid(column=0, row=3)

#The following variables define the user entry field's size/position on the GUI
website_input = Entry(width=21)
website_input.grid(column=1, row=1)
username_input = Entry(width=35)
username_input.insert(0, "cyber_anon@gmail.com") #Pre-populates the email/username with user's email
username_input.grid(column=1, row=2, columnspan=2)
passwd_input = Entry(width=21)
passwd_input.grid(column=1, row=3)

#The following define the clickable buttons size/position on the GUI and the commands that will run for each one
passwd_gen_button = Button(text="Generate Password", command=generate_passwd) #Clicking this button runs generate_passwd
passwd_gen_button.grid(column=2, row=3)
add_button = Button(text="Add", width=36, command=save_passwd) #Clicking this button runs save_passwd
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", width=14, command=find_passwd) #Clicking this button runs find_passwd
search_button.grid(column=2, row=1)


window.mainloop() #This maintains the GUI open until the user closes it
