import sys
from time import sleep
from tkinter import *
from tkinter import ttk
from twilio.rest import Client

import RPi.GPIO as GPIO

from mfrc522 import SimpleMFRC522

import db as db



# Setup
reader = SimpleMFRC522()
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, GPIO.HIGH)

#twilio credentials
account_sid='ACabb9ae88371ff458f1c7384064e71fc1'
auth_token = 'bfd6eb4ee0132bc9e96984df6435c1ad'

client = Client(account_sid, auth_token)

def reminder_message():
    client.messages.create(
        to='+13529992461',
        body="Please remember to return your battery at the end of your shift",
        from_='++16419384623'
        
        )


#creating the window and creating the screen width and height of the display
root = Tk()
height = root.winfo_screenheight()
width = root.winfo_screenwidth()
root.columnconfigure(0, weight=1)
root.rowconfigure(0,weight=1)

# Declarations
employees = {770487949671 : 1, 938645028788 : 3, 428105086426 : 2}
admins = [838383016942, 0]
ID = -1
numBat = 0

#gui coding


#root.geometry(str(width)+"x"+str(height))
root.geometry("800x800")

#creating the title of the root window
root.title("TGH GUI test")


#creation of all available windows
WelcomeWindow = ttk.Frame(root, padding="3 3 15 15")
UserChoice = ttk.Frame(root, padding="3 3 15 15")    
UserNotFound = ttk.Frame(root, padding="3 3 15 15")
WithdrawWindow = ttk.Frame(root, padding="3 3 15 15")
RejectWithdraw = ttk.Frame(root,padding="3 3 15 15")
DepositWindow = ttk.Frame(root,padding="3 3 15 15")
ExitReject = ttk.Frame(root,padding="3 3 15 15")
ExitDeposit = ttk.Frame(root, padding="3 3 15 15")
ExitWithdraw = ttk.Frame(root, padding="3 3 15 15")
adminFrame = ttk.Frame(root, padding="3 3 15 15")
f = ttk.Frame(root, padding="3 3 15 15")


#gui functions
def WelcomeToUserFrame():
    WelcomeWindow.grid_forget()
    UserChoice.grid(row=0,column=0)
    statusLabel= ttk.Label(UserChoice, text="You have %s credits remaining" % (numBat))
    statusLabel.grid(row=1, columnspan=2)

def UserChoiceToWithdraw():
    UserChoice.grid_forget()
    WithdrawWindow.grid(row=0,column=0)
    
def UserChoiceToDeposit():
    UserChoice.grid_forget()
    DepositWindow.grid(row=0,column=0)
    
def UserChoiceToRejectWithdraw():
    UserChoice.grid_forget()
    RejectWithdraw.grid(row=0, column=0)
    
def WithdrawToExit():
    WithdrawWindow.grid_forget()
    ExitWithdraw.grid(row=0,column=0)
    
def DepositToExit():
    DepositWindow.grid_forget()
    ExitDeposit.grid(row=0,column=0)
    
def WExitToHome():
    ExitWithdraw.grid_forget()
    WelcomeWindow.grid(column=0,row=0)

def  DExitToMain():
    ExitDeposit.grid_forget()
    WelcomeWindow.grid(column=0,row=0)

def WelcomeToNotFound():
    WelcomeWindow.grid_forget()
    UserNotFound.grid(column=0,row=0)

def WelcomeToAdmin():
    WelcomeWindow.grid_forget()
    adminFrame.grid(column=0, row=0)

def NotFoundToHome():
    UserNotFound.grid_forget()
    WelcomeWindow.grid(row=0, column=0)
    

def RejectWithdrawToHome():
    RejectWithdraw.grid_forget()
    WelcomeWindow.grid(row=0, column=0)

def RexitToHome():
    ExitReject.grid_forget()
    WelcomeWindow.grid(column=0, row=0)

def adminToHome():
    adminFrame.grid_forget()
    WelcomeWindow.grid(column=0,row=0)
    
def admintoTransactionSheet():
    adminFrame.grid_forget()
    f.grid(column=0,row=0)

def adminToNewEmployee():
    adminFrame.grid_forget()
    NewEmployee.grid(column=0, row=0)
    
def NewEmployeeToAdminFrame():
    NewEmployee.grid_forget()
    adminFrame.grid(column=0,row=0)

def transactionSheetToAdminFrame():
    f.grid_forget()
    adminFrame.grid(column=0, row =0)

# Functions
def openSwitch(port):
    GPIO.output(port, GPIO.LOW)
    sleep(5)
    GPIO.output(port, GPIO.HIGH)

def openBoth(port1, port2):
    GPIO.output(port1, GPIO.LOW)
    GPIO.output(port2,GPIO.LOW)
    sleep(5)
    GPIO.output(port1,GPIO.HIGH)
    GPIO.output(port2,GPIO.HIGH)
    
def validateID(id): # Modify to return the user or something.
    if id in admins:
        return 2
    elif id in employees:
        return 1
    else:
        return 0

def checkWeight():
    return True
    
def checkBalance(ID):
    return employees[ID]
    
def updateBalance(ID, N):
    employees[ID] += N

def checkout():

    WithdrawToExit()
    openSwitch(16)
    root.update()
    
        
    
    

def checkin(ID):
    # User returning one or more batteries
    DepositToExit()

    openSwitch(18)
   
    root.update() 
    
def unauthorized():
    # Routine for unauthorized user
    print('Unauthorized')
    
def deposit(ID):
    UserChoiceToDeposit()
    root.update()
    credit = db.get_credit(ID)
    credit+=1
    print(credit)
    db.trig_credit(str(credit))
    db.record(ID,1)

    checkin(ID)
    
def withdraw(ID):
    credit = db.get_credit(ID)
    if db.get_credit(ID) >0:
        UserChoiceToWithdraw()
        root.update()
        db.record(ID,0)
        db.trig_credit(str(credit-1))
        checkout()
    elif db.get_credit(ID) ==0:
        UserChoiceToRejectWithdraw()
        root.update()
    else:
        UserChoiceToRejectWithdraw()
        root.update()
        
def show_no():
    i=0
    labels=['Date % time:', 'return:', 'First Name:', 'last name:', 'credit:' ,'email:', 'phone:']
    list.delete(0, END)
    for row in db.no_returns():
        list.insert(END,labels[i])
        list.insert(END,row)
        i+=1
        if i==len(labels):
            i=0

def show_all():
    i=0
    labels=['Date % time:', 'return:', 'First Name:', 'last name:', 'credit:' ,'email:', 'phone:']
    list.delete(0, END)
    for row in db.all_records():
        
        list.insert(END,labels[i])
        list.insert(END,row)
        i+=1
        if i==len(labels):
            i=0

        
         
    

def adminOpen():
    # Routine for admin badge
    print('Admin Authorized')
    openBoth(16, 18)

    

  
def StartScan():
    global ID
    ID,text = reader.read()
    
    print('ID:', ID)
    employee, admin = db.search("empid")
    
    aflag =1
    eflag =1
    for name in employee:
        if ID == name[0]:
            global numBat
            numBat = db.get_credit(ID)
            eflag=0
            WelcomeToUserFrame()
    for name in admin:
        if ID == name[0]:
            WelcomeToAdmin()
            root.update()
            aflag =0
    if aflag !=0 and eflag !=0:
        WelcomeToNotFound()    
        root.update()
        
    
def add_emp(): 
    if id_text.get == '' or fname_text.get == '' or lname_text.get =='' or email_text.get() == '' or phone_text.get() == '':
      messagebox.showerror('Required', "Please enclude all information")
      return
   
    db.insert(id_text.get(), fname_text.get(), lname_text.get(), 
            email_text.get(), phone_text.get())
    messagebox.showinfo('Message', "Employee Added!")
         
def rev_emp():
    if id_text.get == '':
      messagebox.showerror('Required', "Please provide employee ID")
    db.delete(id_text.get())
    messagebox.showinfo('Message', "Employee Deleted from Database!")

    if id_text.get == '' or fname_text.get == '' or lname_text.get =='':
         messagebox.showerror('Required', "Please provide employee name and ID")

def update_emp():
    db.update(id_text.get(), credit_text.get())
    messagebox.showinfo('Message', "Employee Infomation Updated!")
   
    if id_text.get == '' or fname_text.get == '' or lname_text.get =='':
         messagebox.showerror('Required', "Please provide employee name and ID")

def clear_text():
    fname_entry.delete(0,END)
    lname_entry.delete(0,END)
    id_entry.delete(0,END)
    email_entry.delete(0,END)
    phone_entry.delete(0,END)
    credit_entry.delete(0,END)


    






def close():
    GPIO.cleanup()
    root.destroy()






#home window that the user interacts with

welcome = ttk.Label(WelcomeWindow, text="press button to scan your card")
welcome.grid(column=0, row=0, columnspan=4)
ttk.Button(WelcomeWindow,text = "start to scan", command=StartScan).grid(row=1, columnspan=4, ipadx=20, ipady=20)


#if user is found in database move to user window

#User choosing between the option of either grabbing a battery or depositing a battery

depositButton = ttk.Button(UserChoice, text="Deposit", command=lambda:deposit(ID))
depositButton.grid(column=0, row=2, ipady=height/4, ipadx=width/8, sticky=(W))
withdrawButton= ttk.Button(UserChoice, text="Withdraw", command=lambda:withdraw(ID))
withdrawButton.grid(column=1,row=2, ipady=height/4, ipadx=width/8, sticky=(E))


#if user is not found
#
ttk.Label(UserNotFound, text="You were not found in the system").grid(row=0, ipady= 25)
ttk.Label(UserNotFound, text="If you should be in the system, please talk to an administrator to receive a battery and get entered into the system").grid(row=1)
ttk.Button(UserNotFound, text="return home", command= NotFoundToHome).grid(row=2)

#user hits withdraw
#
ttk.Label(WithdrawWindow, text="Please take a single battery from the right bin").grid(row=0,column=0)


#user unable to withdraw
#
ttk.Label(RejectWithdraw, text="You don't have any remaining credits to withdraw out any batteries").grid(row=0,column=0)
ttk.Label(RejectWithdraw, text="Please go see an administrator").grid(row=1,column=0)

ttk.Button(RejectWithdraw, text="Tap To End Transaction",command=RejectWithdrawToHome).grid(row=2)


#user hits deposit
#
ttk.Label(DepositWindow, text="please deposit a battery in the left bin").grid(row=0,column=0)

#exit window from reject
#

ttk.Label(ExitReject, text="Bye have a nice day").grid(row=0, column=0)
ttk.Button(ExitReject, text="Tap To End Transaction",command=RexitToHome).grid(row=1)


#exit window from deposit
#
ttk.Label(ExitDeposit, text="Bye have a nice day").grid(row=0, column=0)
ttk.Button(ExitDeposit, text="Tap To End Transaction",command=DExitToMain).grid(row=1)

#exit window from withdraw
#
ttk.Label(ExitWithdraw,text="By have a nice day and remember to return your battery at the end of your shift").grid(row=0, column=0)
ttk.Button(ExitWithdraw, text="Tap to End Transaction",command=WExitToHome).grid(row=1)


#if admin
#
ttk.Label(adminFrame, text="both bins are open please charge the old batteries and fill the right bin with newly charged batteries").grid(row=0, column=0, columnspan=4)
ttk.Button(adminFrame, text="Add New Employee", command=adminToNewEmployee).grid(row=1, column=0)
ttk.Button(adminFrame, text="View Transaction sheet", command=admintoTransactionSheet).grid(row=1,column=1)
ttk.Button(adminFrame, text="Open both bins", command=adminOpen).grid(row=1, column = 2)
ttk.Button(adminFrame, text="End admin access",command=adminToHome).grid(row=3, column=1, padx=20, ipadx=50, ipady=40, pady=30 )

#newEmployee additions
 #list box
list = Listbox(f, height=10, width=70, border=0,)
list.grid(row=3, column=1,columnspan= 6, rowspan=6, pady=20, padx=20)
#scroller
scroller = Scrollbar(f, orient="vertical", command=list.yview)
scroller.grid(row=3, column=7,rowspan=6, sticky='ns')
#set scoll to list box
list.configure(yscrollcommand=scroller.set)
# Button
all = Button(f, text='All Records', width=15, command= show_all)
all.grid(row=0, column=1, padx=20,pady=20)
no_ret = Button(f, text='No returns', width=15, command = show_no)
no_ret.grid(row=0, column=2, padx=20)
Button(f, text='return to admin screen', width=15 , command=transactionSheetToAdminFrame ).grid(row=0, column=3, padx=20)

 #adding a new employee to the database
 
NewEmployee = ttk.Frame(root, style = 'TFrame', padding="3 3 15 15")
 
 
 #First Name
fname_text = StringVar()
fname_label = Label(NewEmployee, text = 'First Name', font=('bold', 14), pady=20)
fname_label.grid(row=0, column=0, sticky=W)
fname_entry = Entry(NewEmployee, textvariable=fname_text)
fname_entry.grid(row=0, column=1)

 #Last Name
lname_text = StringVar()
lname_label = Label(NewEmployee, text = 'Last Name', font=('bold', 14), pady=20)
lname_label.grid(row=1, column=0, sticky=W)
lname_entry = Entry(NewEmployee, textvariable=lname_text)
lname_entry.grid(row=1, column=1)
 
 #Employee ID
id_text = StringVar()
id_label = Label(NewEmployee, text = 'ID Number', font=('bold', 14), pady=20)
id_label.grid(row=2, column=0, sticky=W)
id_entry = Entry(NewEmployee, textvariable=id_text)
id_entry.grid(row=2, column=1)
 
 #Email
email_text = StringVar()
email_label = Label(NewEmployee, text = 'Email', font=('bold', 14))
email_label.grid(row=0, column=3, sticky=W)
email_entry = Entry(NewEmployee, textvariable=email_text)
email_entry.grid(row=0, column=4)
# 
# #Phone
phone_text = StringVar()
phone_label = Label(NewEmployee, text = 'Phone Number', font=('bold', 14))
phone_label.grid(row=1, column=3, sticky=W)
phone_entry = Entry(NewEmployee, textvariable=phone_text)
phone_entry.grid(row=1, column=4)
# 
 #Credit 
credit_text = IntVar()
credit_label = Label(NewEmployee, text = 'Credit', font=('bold', 14))
credit_label.grid(row=2, column=3, sticky=W)
credit_entry = Entry(NewEmployee, textvariable=credit_text)
credit_entry.grid(row=2, column=4)
 
# #Buttons
add_btn = Button(NewEmployee, text='Add', width=12, command=add_emp)
add_btn.grid(row=3, column=0, pady=20)
rev_btn = Button(NewEmployee, text='Delete', width=12, command=rev_emp)
rev_btn.grid(row=3, column=1)
update_btn = Button(NewEmployee, text='Update', width=12, command=update_emp)
update_btn.grid(row=3, column=2)
clear_btn = Button(NewEmployee, text='Clear', width=12, command=clear_text)
clear_btn.grid(row=4, column=0)
done_btn = Button(NewEmployee, text='Done', width=12, command=NewEmployeeToAdminFrame)
done_btn.grid(row=4, column=1)




WelcomeWindow.grid(row=0,column=0)       


        
sleep(1)
        
        
root.protocol("WM_DELETE_WINDOW",close)
root.mainloop()
    



