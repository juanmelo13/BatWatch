from tkinter import *
from tkinter import ttk
import db

root = Tk()
style = ttk.Style()
style.configure('TFrame', foreground = 'blue')
f = ttk.Frame(root, style = 'TFrame', padding="3 3 15 15")
f.grid(row = 0, column=0)

i = 0
def show_no():
    list.delete(0, END)
    for row in db.no_returns():
        list.insert(END, row)

def show_all():
    list.delete(0, END)
    for row in db.all_records():
        list.insert(END, row)

#list box
list = Listbox(f, height=10, width=70, border=0,)
list.grid(row=3, column=1, columnspan= 6, rowspan=6, pady=20, padx=20)
#scroller
scroller = Scrollbar(f, orient="vertical", command=list.yview)
scroller.grid(row=3, column=7, sticky='ns')
#set scoll to list box
list.configure(yscrollcommand=scroller.set)
# Button
all = Button(f, text='All Records', width=12, command= show_all)
all.grid(row=1, column=0, pady=20)
no_ret = Button(f, text='No returns', width=12, command = show_no)
no_ret.grid(row=1, column=1)

root.title('Records')
height = root.winfo_screenheight()
width = root.winfo_screenwidth()
root.columnconfigure(0, weight=1)
root.rowconfigure(0,weight=1)
#app.geometry(str(width)+"x"+str(height))
root.geometry('700x500')
root.mainloop()
