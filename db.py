from dataclasses import dataclass
from tkinter import messagebox, ttk
from tkinter import *

from psycopg2 import connect
#from db import Databse
import db

def add_emp(): 
   if id_text.get == '' or fname_text.get == '' or lname_text.get =='' or email_text.get() == '' or phone_text.get() == '':
      messagebox.showerror('Required', "Please enclude all information")
      return
   
   db.insert(id_text.get(), fname_text.get(), lname_text.get(), 
            email_text.get(), phone_text.get())
   messagebox.showinfo('Message', "Employee Added!")
         
def rev_emp():
   if id_text.get == '' or fname_text.get == '' or lname_text.get =='':
      messagebox.showerror('Required', "Please provide employee name and ID")
   db.delete(id_text.get())
   messagebox.showinfo('Message', "Employee Deleted from Database!")

def update_emp():
   if id_text.get == '' or fname_text.get == '' or lname_text.get =='':
      messagebox.showerror('Required', "Please provide employee name and ID")
   db.update(id_text.get(), credit_text.get())
   messagebox.showinfo('Message', "Employee Infomation Updated!")

def clear_text():
   fname_entry.delete(0,END)
   lname_entry.delete(0,END)
   id_entry.delete(0,END)
   email_entry.delete(0,END)
   phone_entry.delete(0,END)
   credit_entry.delete(0,END)

def done():
   db.close()
   app.quit()

app = Tk()
style = ttk.Style()
style.configure('TFrame', foreground = 'blue')
f = ttk.Frame(app, style = 'TFrame', padding="3 3 15 15")
f.grid(row = 0, column=0)

#First Name
fname_text = StringVar()
fname_label = Label(f, text = 'First Name', font=('bold', 14), pady=20)
fname_label.grid(row=0, column=0, sticky=W)
fname_entry = Entry(f, textvariable=fname_text)
fname_entry.grid(row=0, column=1)

#Last Name
lname_text = StringVar()
lname_label = Label(f, text = 'Last Name', font=('bold', 14), pady=20)
lname_label.grid(row=1, column=0, sticky=W)
lname_entry = Entry(f, textvariable=lname_text)
lname_entry.grid(row=1, column=1)

#Employee ID
id_text = StringVar()
id_label = Label(f, text = 'ID Number', font=('bold', 14), pady=20)
id_label.grid(row=2, column=0, sticky=W)
id_entry = Entry(f, textvariable=id_text)
id_entry.grid(row=2, column=1)

#Email
email_text = StringVar()
email_label = Label(f, text = 'Email', font=('bold', 14))
email_label.grid(row=0, column=3, sticky=W)
email_entry = Entry(f, textvariable=email_text)
email_entry.grid(row=0, column=4)

#Phone
phone_text = StringVar()
phone_label = Label(f, text = 'Phone Number', font=('bold', 14))
phone_label.grid(row=1, column=3, sticky=W)
phone_entry = Entry(f, textvariable=phone_text)
phone_entry.grid(row=1, column=4)

#Credit 
credit_text = IntVar()
credit_label = Label(f, text = 'Credit', font=('bold', 14))
credit_label.grid(row=2, column=3, sticky=W)
credit_entry = Entry(f, textvariable=credit_text)
credit_entry.grid(row=2, column=4)

#Buttons
add_btn = Button(f, text='Add', width=12, command=add_emp)
add_btn.grid(row=3, column=0, pady=20)
rev_btn = Button(f, text='Delete', width=12, command=rev_emp)
rev_btn.grid(row=3, column=1)
update_btn = Button(f, text='Update', width=12, command=update_emp)
update_btn.grid(row=3, column=2)
clear_btn = Button(f, text='Clear', width=12, command=clear_text)
clear_btn.grid(row=4, column=0)
done_btn = Button(f, text='Done', width=12, command=done)
done_btn.grid(row=4, column=1)

app.title('Update Database')
#with and height of the app
height = app.winfo_screenheight()
width = app.winfo_screenwidth()
app.columnconfigure(0, weight=1)
app.rowconfigure(0,weight=1)
#app.geometry(str(width)+"x"+str(height))
app.geometry("700x400") 

#start program
app.mainloop()
