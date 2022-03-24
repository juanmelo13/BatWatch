
from tkinter import *
from tkinter import ttk


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

def switchFrame(newframe, oldframe):
    oldframe.grid_forget()
    newframe.grid(column=0,row=0)



    


#first window that the user interacts with
WelcomeWindow = ttk.Frame(root, padding="3 3 15 15")
WelcomeWindow.grid(column=0,row=0)
welcome = ttk.Label(WelcomeWindow, text="please scan your card")
welcome.grid(column=0, row=0)
buttonswitch = ttk.Button(WelcomeWindow, text="switch window", command=switchFrame)
buttonswitch.grid(row=1)

#if user is found in database move to user window


#numBat = 0
#UserChoice = ttk.Frame(root, padding="3 3 15 15")
#UserChoice.grid(row=0)
#statusLabel= ttk.Label(UserChoice, text = "you have "+str(numBat)+" credits left")
#statusLabel.grid(row=0, columnspan=2,sticky=(N))
#depositButton = ttk.Button(UserChoice, text="Deposit")
#depositButton.grid(column=0, row=1, ipady=height/4, ipadx=width/8, sticky=(W))
#withdrawButton= ttk.Button(UserChoice, text="Withdraw")
#withdrawButton.grid(column=1,row=1, ipady=height/4, ipadx=width/8, sticky=(E))


#if user is not found
#UserNotFound = ttk.Frame(root, padding="3 3 15 15")
#serNotFound.grid(column=0, row=0)
#ttk.Label(UserNotFound, text="You were not found in the system").grid(row=0, ipady= 25)
#ttk.Label(UserNotFound, text="If you should be in the system, please talk to an administrator to receive a battery and get entered into the system").grid(row=1)


#user hits withdraw
#WithdrawWindow = ttk.Frame(root, padding="3 3 15 15")
#WithdrawWindow.grid(column=0, row=0)
#ttk.Label(WithdrawWindow, text="Please take a single battery from the ")


#user unable to withdraw
#ejectWithdraw = ttk.Frame(root,padding="3 3 15 15")
#RejectWithdraw.grid(column=0, row=0)
#ttk.Label(RejectWithdraw, text="You have no available credits to take out any batteries")

#user hits deposit
#DepositWindow = ttk.Frame(root,padding="3 3 15 15")
#DepositWindow.grid(column=0, row=0 )
#ttk.Label(DepositWindow, text="please deposit a battery in the left bin").grid(row=0,column=0)

#exit window from reject
#xitReject = ttk.Frame(root,padding="3 3 15 15")
#ExitReject.grid(column=0, row=0 )
#ttk.Label(ExitReject, text="By have a nice day and remember to return your battery at the end of your shift").grid(row=0, column=0)


#exit window from deposit
#ExitDeposit = ttk.Frame(root, padding="3 3 15 15")
#ExitDeposit.grid(column=0,row=0)
#ttk.Label(ExitDeposit, text="By have a nice day and remember to return your battery at the end of your shift").grid(row=0, column=0)


#exit window from withdraw
#ExitWithdraw = ttk.Frame(root, padding="3 3 15 15")
#ExitWithdraw.grid(column=0, row=0)
#ttk.Label(ExitWithdraw,text="By have a nice day and remember to return your battery at the end of your shift").grid(row=0, column=0)


#if admin
#admin = ttk.Frame(root, padding="3 3 15 15")
#ttk.Label(admin, text="both bins are open please charge the old batteries and fill the right bin with newly charged batteries").grid(row=0, column=0)


root.mainloop()
