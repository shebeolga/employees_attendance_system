# Import user-defined modules for employee and attendance
from employee import *
from attendance import *
from gui import main_screen
import csv

# We open a file with employee's data to identify their numbers and send them to the list of ids in employee class.
# It's necessary if we want to add new employee: he has to have the next number after
# the last employee's number in the system.
# If file does not exist, we skip an error. We'll create it with the first employee.
try:
    with open('employees.csv', 'r', newline='') as file:
        data = csv.DictReader(file, delimiter=';', dialect='excel')
        indexes = []
        for row in data:
            indexes.append(int(row['id']))
        person.ids = indexes
except FileNotFoundError:
    pass

# Also we need to open attendance file to read data from it and send attendance ids to the system for the same purpose.
try:
    with open('attendance.csv', 'r', newline='') as file:
        data = csv.DictReader(file, delimiter=';', dialect='excel')
        indexes = []
        for row in data:
            indexes.append(int(row['attendance id']))
        attendance.ids = indexes
except FileNotFoundError:
    pass

# So we start the program.
main_screen()
