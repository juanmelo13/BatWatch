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

    




try:
    while True:
        print('Scan your ID')
        ID, text = reader.read()

        print('ID:', ID)

        if validateID(ID) == 0:
            unauthorized()
        elif validateID(ID) == 1:
            employee(ID)
        elif validateID(ID) == 2:
            admin(ID)

        sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
finally:
    GPIO.cleanup()
