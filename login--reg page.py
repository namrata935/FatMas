import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
import mysql.connector

class mainform:
    def __init__(self, master):
        self.master = master
        w = 1200
        h = 650
        self.master.geometry(f"{w}x{h}")
        self.master.title("Main Form")


root = Tk()
connection = mysql.connector.connect(host='localhost', user='root', port='3306', password='password', database='pyproj')


c = connection.cursor()

# Define the SQL query to create the users table
create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE,
        password VARCHAR(255),
        vehicle_num VARCHAR(20),
        vehicle_type VARCHAR(10)
    )
'''

# Execute the SQL query to create the table
c.execute(create_table_query)

# Commit the changes
connection.commit()

w = 450
h = 525
bgcolor = "#E0FFFF"


root.overrideredirect(1) 
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws-w)/2
y = (hs-h)/2
root.geometry("%dx%d+%d+%d" % (w, h, x, y))



headerframe = tk.Frame(root, highlightbackgroun='cadetblue', highlightcolor='cadetblue', highlightthickness=2, bg='#E0FFFF', width=w, height=70)

titleframe = tk.Frame(headerframe, bg='cadetblue', padx=1, pady=1)

title_label = tk.Label(text = "LOGIN", padx = 200, pady = 10, bg='cadetblue3', fg='#fff', font=('Tahoma',24))

close_button = tk.Button(headerframe, text='x', borderwidth=1, relief='solid', font=('Verdana',12))

headerframe.pack()
titleframe.pack()
title_label.pack()
close_button.pack()

titleframe.place(y=26, relx=0.5, anchor=CENTER)
close_button.place(x=410, y=10)


def close_win():
    root.destroy()

close_button['command'] = close_win


mainframe = tk.Frame(root, width=w, height=h)

# ----------- Login Page ------------- #
loginframe = tk.Frame(mainframe, width=w, height=h)
login_contentframe = tk.Frame(loginframe, padx=30, pady=100, highlightbackgroun='yellow', highlightcolor='yellow', highlightthickness=2, bg=bgcolor)

username_label = tk.Label(login_contentframe, text='Username:', font=('Verdana',16), bg=bgcolor)

password_label = tk.Label(login_contentframe, text='Password:', font=('Verdana',16), bg=bgcolor)

username_entry = tk.Entry(login_contentframe, font=('Verdana',16))

password_entry = tk.Entry(login_contentframe, font=('Verdana',16), show='*')

login_button = tk.Button(login_contentframe,text="Login", font=('Verdana',16), bg='#2980b9',fg='#fff', padx=25, pady=10, width=25)

go_register_label = tk.Label(login_contentframe, text="Don't have an account? create one" ,font=('Verdana',15), bg=bgcolor, fg='firebrick')

mainframe.pack(fill='both', expand=1)
loginframe.pack(fill='both', expand=1)
login_contentframe.pack(fill='both', expand=1)

username_label.grid(row=0, column=0, pady=10)
username_entry.grid(row=0, column=1)

password_label.grid(row=1, column=0, pady=10)
password_entry.grid(row=1, column=1)

login_button.grid(row=2, column=0, columnspan=2, pady=40)

go_register_label.grid(row=3, column=0, columnspan=2, pady=(5, 20))


#function to take user to register page
def go_to_register():
    loginframe.forget()
    registerframe.pack(fill="both", expand=1)
    title_label['text'] = 'REGISTER'
    title_label['bg'] = '#27ae60'


go_register_label.bind("<Button-1>", lambda page: go_to_register())


#function to login
def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    vals = (username, password,)
    select_query = "SELECT * FROM `users` WHERE `username` = %s and `password` = %s"
    c.execute(select_query, vals)
    user = c.fetchone()
    if user is not None:
        #messagebox.showinfo('Test','Test')
        messagebox.showinfo('Login Successful', 'Welcome, ' + username + '!')
        mainformwindow = tk.Toplevel()
        app = mainform(mainformwindow)
        root.withdraw() # hide the root
        mainformwindow.protocol("WM_DELETE_WINDOW", close_win) # close the app

    else:
        messagebox.showwarning('Error','wrong username or password')



login_button['command'] = login


# ----------- Register Page ------------- #

registerframe = tk.Frame(mainframe, width=w, height=h)

register_contentframe = tk.Frame(registerframe, padx=15, pady=15, highlightbackgroun='yellow', highlightcolor='yellow', highlightthickness=2, bg=bgcolor)

username_label_rg = tk.Label(register_contentframe, text='Username:',font=('Verdana',14), bg=bgcolor)

password_label_rg = tk.Label(register_contentframe, text='Password:', font=('Verdana',14), bg=bgcolor)

confirmpass_label_rg = tk.Label(register_contentframe, text='Repeat Password:', font=('Verdana',14), bg=bgcolor)

vehicle_num_label_rg = tk.Label(register_contentframe, text='Enter license no:', font=('Verdana',14), bg=bgcolor)

vehicletype_label_rg = tk.Label(register_contentframe, text='Vehicle type:', font=('Verdana',14), bg=bgcolor)



username_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22)

password_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22, show='*')

confirmpass_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22, show='*')

vehicle_num_entry_rg = tk.Entry(register_contentframe, font=('Verdana',14), width=22)

radiosframe = tk.Frame(register_contentframe)
vehicletype = StringVar()
vehicletype.set('car')
car_radiobutton = tk.Radiobutton(radiosframe, text='car', font=('Verdana',14), bg=bgcolor, variable=vehicletype, value='car')
truck_radiobutton = tk.Radiobutton(radiosframe, text='truck', font=('Verdana',14), bg=bgcolor, variable=vehicletype, value='truck')
lmc_radiobutton = tk.Radiobutton(radiosframe, text = 'LMC', font =('Verdana',14), bg=bgcolor, variable=vehicletype, value='LMC') 



register_button = tk.Button(register_contentframe,text="Register", font=('Verdana',16), bg='#3CB371',fg='#fff', padx=25, pady=10, width=25)
go_login_label = tk.Label(register_contentframe, text=" already have an account? sign in" , font=('Verdana',15), bg=bgcolor, fg='firebrick')

#mainframe.pack(fill='both', expand=1)
#registerframe.pack(fill='both', expand=1)
register_contentframe.pack(fill='both', expand=1)

username_label_rg.grid(row=1, column=0, pady=5, sticky='e')
username_entry_rg.grid(row=1, column=1)

password_label_rg.grid(row=2, column=0, pady=5, sticky='e')
password_entry_rg.grid(row=2, column=1)

confirmpass_label_rg.grid(row=3, column=0, pady=5, sticky='e')
confirmpass_entry_rg.grid(row=3, column=1)

vehicle_num_label_rg.grid(row=4, column=0, pady=5, sticky='e')
vehicle_num_entry_rg.grid(row=4, column=1)

vehicletype_label_rg.grid(row=5, column=0, pady=5, sticky='e')
radiosframe.grid(row=5, column=1)
car_radiobutton.grid(row=0, column=0)
truck_radiobutton.grid(row=0, column=1)
lmc_radiobutton.grid(row=0, column=2)




register_button.grid(row=7, column=0, columnspan=2, pady=20)

go_login_label.grid(row=8, column=0, columnspan=2, pady=40)




# --------------------------------------- #


#to display login frame
def go_to_login():
    registerframe.forget()
    loginframe.pack(fill="both", expand=1)
    title_label['text'] = 'LOGIN'
    title_label['bg'] = '#2980b9'


go_login_label.bind("<Button-1>", lambda page: go_to_login())
# --------------------------------------- #

# cheicking if username already exists
def check_username(username):
    username = username_entry_rg.get().strip()
    vals = (username,)
    select_query = "SELECT * FROM `users` WHERE `username` = %s"
    c.execute(select_query, vals)
    user = c.fetchone()
    if user is not None:
        return True
    else:
        return False



# --------------------------------------- #


#register function
def register():

    username = username_entry_rg.get().strip()
    password = password_entry_rg.get().strip()
    confirm_password = confirmpass_entry_rg.get().strip()
    vehicle_num = vehicle_num_entry_rg.get().strip()
    gdr = vehicletype.get()
   
    
    

    if len(username) > 0 and len(password) > 0 and len(vehicle_num) > 0:
        if check_username(username) == False: 
            if password == confirm_password:
                vals = (username, password, vehicle_num, gdr)
                insert_query = "INSERT INTO `users`(`username`, `password`, `vehicle_num`, `vehicle_type`) VALUES (%s,%s,%s,%s)"
                c.execute(insert_query, vals)
                connection.commit()
                messagebox.showinfo('Register','your account has been created successfully')
            else:
                messagebox.showwarning('Password','incorrect password confirmation')
        else:
            messagebox.showwarning('Duplicate Username','This Username Already Exists,try another one')
    else:
        messagebox.showwarning('Empty Fields','make sure to enter all the information')

register_button['command'] = register

# --------------------------------------- #

root.mainloop()


