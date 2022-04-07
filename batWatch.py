import sys
from time import sleep
from tkinter import *
from tkinter import ttk

import RPi.GPIO as GPIO

from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

# Declarations
employees = {770487949671 : 0, 938645028788 : 3, 428105086426 : 2}
admins = [838383016942, 0]

# Functions
def openSwitch(port):
    GPIO.setup(port, GPIO.OUT)
    GPIO.output(port, GPIO.LOW)
    sleep(5)
    GPIO.output(port, GPIO.HIGH)

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

def checkout(ID):
    # User taking a battery
    if checkBalance(ID) > 0:
        print('Sufficient funds, take a battery')
        openSwitch(18)
        updateBalance(ID, -1)
        return
    elif checkBalance(ID) == 0:
        print('Not enough funds, please contact an administrator')
        return
    else:
        print('Exception')
        return

def checkin(ID, N):
    # User returning one or more batteries
    print('Drop battery in container')
    openSwitch(18)
    # Check the balance to see if the batteries are dropped
    while(not checkWeight()):
        if (cancelOperation()):
            print('Operation Cancelled')
            return
            # Return to main menu
        pass
    # Batteries are sensed
    updateBalance(ID, N)
    
def unauthorized():
    # Routine for unauthorized user
    print('Unauthorized')

def employee(ID):
    # Routine for employee badge
    print('Employe Authorized')
    action = input('What do you want to do? (drop/pick)')
    if action == 'drop':
        N = int(input('How many batteries will you drop?'))
        checkin(ID, N)
        return
    elif action == 'pick':
        checkout(ID)
        return

def admin(ID):
    # Routine for admin badge
    print('Admin Authorized')
    openSwitch(18)

    
#gui coding
#creating the window and creating the screen width and height of the display
root = Tk()
height = root.winfo_screenheight()
width = root.winfo_screenwidth()
root.columnconfigure(0, weight=1)
root.rowconfigure(0,weight=1)


#root.geometry(str(width)+"x"+str(height))
root.geometry("400x400")

#creating the title of the root window
root.title("TGH GUI test")

def WelcomeToUserFrame(*args):
    WelcomeWindow.grid_forget()
    UserChoice.grid(row=0,column=0)

def UserChoiceToWithdraw(*args):
    UserChoice.grid_forget()
    WithdrawWindow.grid(row=0,column=0)

def UserChoiceToDeposit(*args):
    UserChoice.grid_forget()
    DepositWindow.grid(row=0,column=0)

def WithdrawToExit(*args):
    WithdrawWindow.grid_forget()
    ExitWithdraw.grid(row=0,column=0)

def DepositToExit(*args):
    DepositWindow.grid_forget()
    ExitDeposit.grid(row=0,column=0)    

def WExitToMain(*args):
    ExitWithdraw.grid_forget()
    WelcomeWindow.grid(column=0,row=0)

def  DExitToMain(*args):
    ExitDeposit.grid_forget()
    WelcomeWindow.grid(column=0,row=0)

def WelcomeToNotFound(*args):
    WelcomeWindow.grid_forget()
    UserNotFound.grid(column=0,row=0)

def WelcomeToAdmin(*args):
    WelcomeWindow.grid_forget()
    admin.grid(column=0, row=0)

def NotFoundToHome(*args):
    UserNotFound.grid_forget()
    WelcomeWindow.grid(row=0, column=0)

def RejectWithdrawToRexit(*args):
    RejectWithdraw.grid_forget()
    ExitReject.grid(row=0, column=0)


def RexitToHome(*args):
    ExitReject.grid_forget()
    WelcomeWindow.grid(column=0, row=0)

def adminToHome(*args):
    admin.grid_forget()
    WelcomeWindow.grid(column=0,row=0)



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
admin = ttk.Frame(root, padding="3 3 15 15")


#home window that the user interacts with

welcome = ttk.Label(WelcomeWindow, text="please scan your card")
welcome.grid(column=0, row=0, columnspan=4)
WelcomeToUser = ttk.Button(WelcomeWindow, text="switch window",command=WelcomeToUserFrame).grid(row=1,column=0)
ttk.Button(WelcomeWindow, text="not found window", command = WelcomeToNotFound).grid(row= 1, column=1)
ttk.Button(WelcomeWindow, text="Admin", command = WelcomeToAdmin).grid(row= 1, column=3)


#if user is found in database move to user window

#User choosing between the option of either grabbing a battery or depositing a battery
numBat = "x"
statusLabel= ttk.Label(UserChoice, text = "you have "+numBat+" credits left")
statusLabel.grid(row=1, columnspan=2)
depositButton = ttk.Button(UserChoice, text="Deposit", command=UserChoiceToDeposit )
depositButton.grid(column=0, row=2, ipady=height/4, ipadx=width/8, sticky=(W))
withdrawButton= ttk.Button(UserChoice, text="Withdraw", command=UserChoiceToWithdraw )
withdrawButton.grid(column=1,row=2, ipady=height/4, ipadx=width/8, sticky=(E))


#if user is not found
#
ttk.Label(UserNotFound, text="You were not found in the system").grid(row=0, ipady= 25)
ttk.Label(UserNotFound, text="If you should be in the system, please talk to an administrator to receive a battery and get entered into the system").grid(row=1)
ttk.Button(UserNotFound, text="return home", command= NotFoundToHome).grid(row=2)

#user hits withdraw
#
ttk.Label(WithdrawWindow, text="Please take a single battery from the right bin").grid(row=0,column=0)
ttk.Button(WithdrawWindow, text="switch window",command=WithdrawToExit).grid(row=1)


#user unable to withdraw
#
ttk.Label(RejectWithdraw, text="You have no available credits to take out any batteries")
ttk.Button(RejectWithdraw, text="switch window",command=RejectWithdrawToRexit).grid(row=1)


#user hits deposit
#
ttk.Label(DepositWindow, text="please deposit a battery in the left bin").grid(row=0,column=0)
ttk.Button(DepositWindow, text="switch window",command=DepositToExit).grid(row=1)

#exit window from reject
#

ttk.Label(ExitReject, text="Bye have a nice day").grid(row=0, column=0)
ttk.Button(ExitReject, text="switch window",command=RexitToHome).grid(row=1)


#exit window from deposit
#
ttk.Label(ExitDeposit, text="Bye have a nice day and remember to return your battery at the end of your shift").grid(row=0, column=0)
ttk.Button(ExitDeposit, text="switch window",command=DExitToMain).grid(row=1)

#exit window from withdraw
#
ttk.Label(ExitWithdraw,text="By have a nice day and remember to return your battery at the end of your shift").grid(row=0, column=0)
ttk.Button(WithdrawWindow, text="switch window",command=WithdrawToExit).grid(row=1)


#if admin
#
ttk.Label(admin, text="both bins are open please charge the old batteries and fill the right bin with newly charged batteries").grid(row=0, column=0)
ttk.Button(admin, text="switch window",command=adminToHome).grid(row=1)




try:
    while True:
        print('Scan your ID')
        WelcomeWindow.grid(column=0,row=0)
        ID, text = reader.read()

        print('ID:', ID)

        if validateID(ID) == 0:
            unauthorized()
            WelcomeToNotFound()
        elif validateID(ID) == 1:
            employee(ID)
            WelcomeToUserFrame()
        elif validateID(ID) == 2:
            admin(ID)
            WelcomeToAdmin()

        sleep(5)
        root.mainloop()
        
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
finally:
    GPIO.cleanup()
