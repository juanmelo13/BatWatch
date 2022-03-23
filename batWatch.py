import sys
from time import sleep

import RPi.GPIO as GPIO

from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

# Declarations
admins = [770487949671, 0, 0]
employees = [0, 0]

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
    
def checkout():
    # User taking a battery
    '''
    if checkBalance() == enough funds:
        print('Sufficient funds, take a battery')
        openSwitch()
        updateBalance(-1)
        return
    elif checkBalance() == not enough funds:
        print('Not enough funds, please contact an administrator')
        return
    else:
        exception
    '''    

def checkin(N):
    # User returning one or more batteries
    print('Drop battery in container')
    openSwitch()
    # Check the balance to see if the batteries are dropped
    while(not checkWeight()):
        if (cancelOperation()):
            print('Operation Cancelled')
            return
            # Return to main menu
        pass
    # Batteries are sensed
    updateBalance(N)
    
def unauthorized():
    # Routine for unauthorized user
    print('Unauthorized')

def employee():
    # Routine for employee badge
    print('Employe Authorized')
    openSwitch(18)

def admin():
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
            employee()
        elif validateID(ID) == 2:
            admin()

        sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
finally:
    GPIO.cleanup()
