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

def validateID(id):
    if id in admins:
        return 2
    elif id in employees:
        return 1
    else:
        return 0

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
            unautorized()
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
