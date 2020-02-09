"""
This module describes behaviour of the GUI application.
"""

# import necessary modules
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
import csv
import datetime

from employee import *
from attendance import *


TITLE = 'Employee Attendance Management System'
ICON = 'xclock.ico'


def window_position(window, size_hor, size_vert):
    """
    The function defines windows position depending on its size.
    """
    w = window.winfo_screenwidth()
    h = window.winfo_screenheight()
    w = w // 2
    h = h // 2
    w = w - size_hor // 2
    h = h - size_vert // 2 - 50
    window.geometry('{}x{}+{}+{}'.format(size_hor, size_vert, w, h))
    # User can't change app size
    window.resizable(False, False)


def show_employees_screen(file, window, title='The list of employees'):
    """
    The function creates view to show employees on the GUI screen.
    """
    global frame
    # Construct frame
    frame = Frame(window)
    frame.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

    # Create header
    main_label = Label(frame, text=title)
    main_label.grid(row=0, column=0, columnspan=2)

    # Create tree view
    header = ['id', 'first name', 'last name', 'status', 'phone', 'age']

    tree = ttk.Treeview(frame, columns=header, show="headings")
    tree.grid(row=1, column=0)

    for col in header:
        tree.heading(col, text=col.title(), anchor="w")

    tree.column('id', width=10)
    tree.column('first name', width=80)
    tree.column('last name', width=100)
    tree.column('status', width=70)
    tree.column('phone', width=100)
    tree.column('age', width=60)

    # For each row in file we add new line to the tree view of employees.
    with open(file) as f:
        reader = csv.DictReader(f, delimiter=';')
        point = 0
        for row in reader:
            employee_id = row['id']
            first_name = row['first name']
            last_name = row['last name']
            status = row['status']
            phone = row['phone']
            age = row['age']
            tree.insert('', point, values=(employee_id, first_name, last_name, status, phone, age))
            point += 1

    tree.config(height=8)

    # Add a scrollbar to the list of employees.
    scroll_bar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
    tree.config(yscroll=scroll_bar.set)
    scroll_bar.grid(row=1, column=1, sticky='ns')

    # Create close button.
    close_button = Button(window, text='Close', width=10, command=window.destroy)
    close_button.grid(row=1, column=1, padx=20, pady=10, stick=E)


def show_attendance_screen(file, window, title):
    """
    The function creates view to show data from attendance file to the screen.
    """
    # Construct frame
    frame = Frame(window)
    frame.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

    # Create header
    main_label = Label(frame, text=title)
    main_label.grid(row=0, column=0, columnspan=2)

    # Create tree view
    header = ['first name', 'last name', 'arr. date', 'arr. time', 'dep. date', 'dep. time']

    tree = ttk.Treeview(frame, columns=header, show="headings")
    tree.grid(row=1, column=0)

    for col in header:
        tree.heading(col, text=col.title(), anchor="w")

    tree.column('first name', width=80)
    tree.column('last name', width=100)
    tree.column('arr. date', width=70)
    tree.column('arr. time', width=70)
    tree.column('dep. date', width=70)
    tree.column('dep. time', width=70)

    # For each row in file we add new line to the tree view.
    with open(file) as f:
        reader = csv.DictReader(f, delimiter=';')
        point = 0
        for row in reader:
            first_name = row['first name']
            last_name = row['last name']
            arrival_date = row['arrival date']
            arrival_time = row['arrival time']
            dep_date = row['departure date']
            dep_time = row['departure time']
            tree.insert('', point, values=(first_name, last_name, arrival_date, arrival_time, dep_date, dep_time))
            point += 1

    tree.config(height=8)

    # Add a scroll bar.
    scroll_bar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
    tree.config(yscroll=scroll_bar.set)
    scroll_bar.grid(row=1, column=1, sticky='ns')

    # Create close button.
    close_button = Button(window, text='Close', command=window.destroy)
    close_button.grid(row=1, column=1, padx=20, pady=10, stick=E)


def list_of_statuses():
    """
    The function creates a list of all employees statuses. We will use it choose status for new employee
    or to select employees for different reports.
    """
    statuses = set()
    with open('employees.csv', newline='') as file:
        data = csv.DictReader(file, delimiter=';')
        for row in data:
            status = row['status']
            statuses.add(status)

    statuses = list(statuses)
    statuses.sort()

    return statuses


def add_manually_button():
    """
    The procedure executes when 'Add new employee' button has pressed. It takes data from user input, calls method
    'add employee' from employee class and shows new data on the GUI screen.
    """
    # Read data from user input
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    status = status_from_label.get()
    phone = phone_entry.get()
    phone = clean_phone(phone)
    age = age_entry.get()

    # Check if all entered data is correct. If not, we leave the function with showing error to user.
    while True:
        try:
            check_data(first_name, last_name, status, phone, age)
        except TypeError as err:
            response = messagebox.showerror('Error', err)
            if response == 'ok':
                top.deiconify()
                return
        except ValueError as err:
            response = messagebox.showerror('Error', err)
            if response == 'ok':
                top.deiconify()
                return
        except Exception as err:
            response = messagebox.showerror('Error', err)
            if response == 'ok':
                top.deiconify()
                return
        else:
            # If all data is correct, we avoid duplication of employees with status 'boss' in the system,
            # because its impossible in real life.
            statuses = list_of_statuses()
            if status == 'boss' and 'boss' in statuses:
                response = messagebox.showerror('Error', 'There cann\'t be two bosses in one company. '
                                                         'Choose another status, please.')
                if response == 'ok':
                    top.deiconify()
                    return
            else:
                # If everything is OK, we add an employee to the system
                first_name = first_name.title()
                last_name = last_name.title()
                age = int(age)
                add_manually(first_name, last_name, status, phone, age)
                # We clean the entry boxes
                first_name_entry.delete(0, END)
                last_name_entry.delete(0, END)
                phone_entry.delete(0, END)
                age_entry.delete(0, END)
                break

    # Show new data on the screen.
    show_employees_screen('employees.csv', root)

    # Ask user if he wants to add one more employee.
    response = messagebox.askyesno('Question', 'The employee\'s added successfully. '
                                               'Do you want to add one more employee?')
    if response == 1:
        top.deiconify()
    else:
        top.destroy()


def choose_status():
    """
    The function let user to choose employee's status from the list of existing statuses.
    """
    global choose_status_screen
    global status_listbox

    # Create new screen and define its parameters.
    choose_status_screen = Toplevel()
    choose_status_screen.title("Choose status")
    choose_status_screen.iconbitmap(ICON)

    size_hor = 220
    size_vert = 210
    window_position(choose_status_screen, size_hor, size_vert)

    # Create header of the screen.
    title_label = Label(choose_status_screen, text='Choose status:')
    title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

    # Create frame with listbox and scroll bar near it.
    frame = LabelFrame(choose_status_screen, padx=10, pady=10)
    frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 10))

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    status_listbox = Listbox(frame, height=5, selectmode=SINGLE)

    statuses = list_of_statuses()
    for row in statuses:
        status_listbox.insert(END, row)

    status_listbox.pack(side=LEFT, fill=BOTH)

    status_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=status_listbox.yview)

    # Create ok button
    ok_button = Button(choose_status_screen, text='OK', width=10, command=set_status)
    ok_button.grid(row=2, column=0, padx=(20, 10), pady=10)

    # Create close button.
    close_button = Button(choose_status_screen, text='Close', width=10, command=choose_status_screen.destroy)
    close_button.grid(row=2, column=1, padx=(10, 20), pady=10)


def set_status():
    """
    The function set chosen status to the label on the 'Add new employee' screen.
    """
    status_from_label.set(status_listbox.get(ACTIVE))
    choose_status_screen.destroy()
    top.deiconify()
    phone_entry.focus()


def add_status():
    """
    The function creates screen to add new status to new employee.
    """
    global add_status_screen
    global status_entry
    # Screen properties
    add_status_screen = Toplevel()
    add_status_screen.title("Add new status")
    add_status_screen.iconbitmap(ICON)

    size_hor = 250
    size_vert = 90
    window_position(add_status_screen, size_hor, size_vert)

    # Screen header.
    label = Label(add_status_screen, text='New status')
    label.grid(row=0, column=0, padx=(20, 0), pady=10)

    # Entry for user's input.
    status_entry = Entry(add_status_screen)
    status_entry.grid(row=0, column=1, padx=(20, 0), pady=10)

    # OK and Close buttons.
    ok_button = Button(add_status_screen, text='OK', command=set_new_status)
    ok_button.grid(row=1, column=0, padx=(20, 0), pady=10, ipadx=20, sticky='W')

    close_button = Button(add_status_screen, text='Close', command=add_status_screen.destroy)
    close_button.grid(row=1, column=1, padx=(20, 0), pady=10, ipadx=20, sticky='E')


def set_new_status():
    """
    The function set new status to the label on the 'Add new employee' screen.
    """
    new_status = status_entry.get()
    if not new_status.isalpha():  # Check the input
        response = messagebox.showerror('Error', 'Something is wrong with your input. Try again.')
        if response == 'ok':
            add_status_screen.deiconify()
            status_entry.focus()
            return
    else:
        status_from_label.set(status_entry.get())
        add_status_screen.destroy()
        top.deiconify()
        phone_entry.focus()


def add_manually_menu():
    """
    The function creates top screen to add new employee.
    """
    global top
    # Screen parameters.
    top = Toplevel()
    top.title("Add employee")
    top.iconbitmap(ICON)

    size_hor = 330
    size_vert = 210
    window_position(top, size_hor, size_vert)

    global first_name_entry
    global last_name_entry
    global status_from_label
    global status
    global phone_entry
    global age_entry

    # Create text boxes
    first_name_entry = Entry(top, width=30)
    first_name_entry.grid(row=0, column=1, columnspan=2, padx=20, pady=(10, 0))
    first_name_entry.focus()

    last_name_entry = Entry(top, width=30)
    last_name_entry.grid(row=1, column=1, columnspan=2, padx=20)

    choose_status_button = Button(top, text='Choose', command=choose_status)
    choose_status_button.grid(row=2, column=1, padx=20, pady=5, sticky='W')

    add_status_button = Button(top, text='Add new', command=add_status)
    add_status_button.grid(row=2, column=2, padx=(0, 20), pady=5, sticky='E')

    status_from_label = StringVar()
    status = Label(top, textvariable=status_from_label)
    status.grid(row=3, column=1, columnspan=2, padx=20, sticky='W')

    phone_entry = Entry(top, width=30)
    phone_entry.grid(row=4, column=1, columnspan=2, padx=20)

    age_entry = Entry(top, width=30)
    age_entry.grid(row=5, column=1, columnspan=2, padx=20)

    # Create labels
    f_name_label = Label(top, text="First name")
    f_name_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky='W')

    l_name_label = Label(top, text="Last name")
    l_name_label.grid(row=1, column=0, padx=20, sticky='W')

    status_label = Label(top, text="Status")
    status_label.grid(row=2, column=0, padx=20, sticky='W')

    phone_label = Label(top, text="Phone")
    phone_label.grid(row=4, column=0, padx=20, sticky='W')

    age_label = Label(top, text="Age")
    age_label.grid(row=5, column=0, padx=20, sticky='W')

    # Create add button
    add_button = Button(top, text='Add employee', command=add_manually_button)
    add_button.grid(row=6, column=0, columnspan=2, padx=(20, 0), pady=20, ipadx=20, sticky='W')

    # Create close button
    close_button = Button(top, text='Close', command=top.destroy)
    close_button.grid(row=6, column=2, padx=(0, 20), pady=20, ipadx=30, sticky='E')


def add_from_file_menu():
    """
    The function add new employees from given csv file.
    """
    file_name = filedialog.askopenfilename(initialdir='C:\Programming\Python\SheCodes\Employee Attendance Management System',
                                               title='Select a file',
                                               filetypes=(('csv files', '*.csv'), ('all files', '*.*')))

    # Check file for any kind of problems.
    try:
        check_file(file_name)
    except TypeError as err:
        response = messagebox.showerror('Error', err)
        if response == 'ok':
            return
    except FileNotFoundError as err:
        response = messagebox.showerror('Error', err)
        if response == 'ok':
            return
    except ValueError as err:
        response = messagebox.showerror('Error', err)
        if response == 'ok':
            return
    else:
        is_err = add_from_file(file_name)
        # Check data in the file
        if is_err == 1:
            response = messagebox.showerror('Error', 'Something is wrong with data in file. Check it and try again.')
            if response == 'ok':
                return

    # If everything goes right, we show new list of employees on the screen.
    show_employees_screen('employees.csv', root)

    messagebox.showinfo('Success', 'Employees are added successfully.')


def delete_manually_button():
    """
    The function deletes employee from the system.
    """
    # Check that user's input is digit.
    try:
        index = int(id_entry.get())
    except ValueError:
        response = messagebox.showerror('Error', 'Your input is not a number. Try again.')
        if response == 'ok':
            delete_screen.deiconify()
            id_entry.focus()
            return
    else:
        # Read employees' ids.
        data = read_from_file('employees.csv')
        id_list = []
        for row in data:
            id_list.append(int(row['id']))
        # If there is no given employee's id in the system, we show an error.
        if index not in id_list:
            response = messagebox.showerror('Error', 'There is no employee with number {} in the system.'.format(index))
            if response == 'ok':
                delete_screen.deiconify()
                id_entry.focus()
                return
        else:
            # If we've found employee's id, we have to ask user,
            # if he really wants to delete this employee from the system.
            for row in data:
                if int(row['id']) == index:
                    person = (row['first name'], row['last name'])
                    response = messagebox.askyesno('Warning', 'Are you sure you want to delete {} {} from the system?'.
                                                   format(person[0], person[1]))
                    if not response:
                        return
                    else:  # And if the answer is yes, we delete him.
                        delete_manually(index)

    # Clear entry.
    id_entry.delete(0, END)

    # Show updated list of employees.
    show_employees_screen('employees.csv', root)

    # Ask if use wants to delete someone else.
    response = messagebox.askyesno('Question', 'The employee\'s deleted successfully. '
                                               'Do you want to delete one more employee?')
    if response == 1:
        delete_screen.deiconify()
    else:
        delete_screen.destroy()


def delete_manually_menu():
    """
    The function creates screen 'Delete employee;
    """
    global delete_screen
    # Screen parameters.
    delete_screen = Toplevel()
    delete_screen.title("Delete employee")
    delete_screen.iconbitmap(ICON)

    size_hor = 260
    size_vert = 100
    window_position(delete_screen, size_hor, size_vert)

    global id_entry
    # Create text boxes
    id_entry = Entry(delete_screen, width=10)
    id_entry.grid(row=0, column=1, padx=10, pady=(20, 0))
    id_entry.focus()

    id_label = Label(delete_screen, text="Employee's id", anchor=E)
    id_label.grid(row=0, column=0, padx=10, pady=(20, 0))

    # Create delete button
    delete_button = Button(delete_screen, text='Delete employee', command=delete_manually_button)
    delete_button.grid(row=1, column=0, pady=10, padx=10, ipadx=20)

    # Create close button
    close_button = Button(delete_screen, text='Close', command=delete_screen.destroy)
    close_button.grid(row=1, column=1, padx=10, pady=10, ipadx=20)


def delete_from_file_menu():
    """
    The function deletes employees, which ids contains in the file, from the system
    """
    # User choose a file.
    file_name = filedialog.askopenfilename(
        initialdir='C:/Programming/Python/SheCodes/Employee Attendance Management System',
        title='Select a file',
        filetypes=(('csv files', '*.csv'), ('all files', '*.*')))

    # Check file: does it exist, does it have csv extension, does it empty or not.
    try:  # And check it for any kind of problems.
        check_file(file_name)
    except TypeError as err:
        response = messagebox.showerror('Error', err)
        if response == 'ok':
            return
    except FileNotFoundError as err:
        response = messagebox.showerror('Error', err)
        if response == 'ok':
            return
    except ValueError as err:
        response = messagebox.showerror('Error', err)
        if response == 'ok':
            return
    else:
        # Check data in the file: does it contains employees ids or something wrong.
        is_err = delete_from_file(file_name)
        if is_err == 1:
            response = messagebox.showerror('Error', 'Something is wrong with data in file. Check it and try again.')
            if response == 'ok':
                return
        elif is_err == 2:
            response = messagebox.showerror('Error', 'File doesn\'t contain employee\'s ids.  Check it and try again.')
            if response == 'ok':
                return
        elif is_err == 3:
            response = messagebox.showerror('Error', 'There are no employees with ids from this file in the system. '
                                                     'Check your file and try again.')
            if response == 'ok':
                return
        else:
            # If everything is ok, employees deletes and the message box shows to user succeed result.
            show_employees_screen('employees.csv', root)
            response = messagebox.showinfo('Success', 'Employees deleted successfully.')
            if response == 'ok':
                return


def check_arrival():
    """
    The function takes employee's id, name and surname, current date and time and add all this data to the system.
    """
    # Getting data.
    data = employees_listbox.get(ACTIVE)
    employee_id, first_name, last_name = data.split()
    employee_id = employee_id[:-1]

    now = datetime.datetime.today()
    current_date = now.strftime('%d/%m/%Y')

    # Check if employee has come and didn't leave job yet.
    attendance_data = read_from_file('attendance.csv')
    for row in attendance_data:
        if row['employee id'] == employee_id and row['arrival date'] == current_date:
            this_row = row
            if this_row['departure date'] == 'None':
                response = messagebox.showerror('Error', 'This employee\'s arrived already. '
                                                         'Choose another one or close the window.')
                if response == 'ok':
                    top.deiconify()
                    return

    # Add attendance data to the system.
    date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    time = date.strftime('%H:%M')
    date = date.strftime('%d/%m/%Y')
    add_arrival_to_system(employee_id, first_name, last_name, date, time)

    # Show succeed message.
    response = messagebox.askyesno(top, 'Arrival checked successfully. Do you want to check someone else?')
    if response == 1:
        top.deiconify()
    else:
        top.destroy()


def check_arrival_menu():
    """
    Create top level screen to check arrival.
    """
    global employees_listbox
    global top

    # Screen properties.
    top = Toplevel()
    top.title("Check arrival")
    top.iconbitmap(ICON)
    size_hor = 280
    size_vert = 210
    window_position(top, size_hor, size_vert)

    # Frame with lis of employees and scroll bar near it.
    frame = LabelFrame(top, padx=10, pady=10)
    frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    employees_listbox = Listbox(frame)

    data = read_from_file('employees.csv')
    for row in data:
        employees_listbox.insert(END, row['id'] + '. ' + row['first name'] + ' ' + row['last name'])

    employees_listbox.pack(side=LEFT, fill=BOTH)

    employees_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=employees_listbox.yview)

    # Create buttons
    check_button = Button(top, text='Check Arrival', command=check_arrival)
    check_button.grid(row=0, column=1)

    close_button = Button(top, text='Close', command=top.destroy)
    close_button.grid(row=1, column=1)


def check_departure():
    """
    The function takes employee's id, current date and time and add departure's data to the system.
    """
    data = employees_listbox.get(ACTIVE)
    employee_id, first_name, last_name = data.split()
    employee_id = employee_id[:-1]

    # Check if we have all this data in the system. If the employee has gone yet, e.g. his departure date and time
    # not equal 'None', the system returns an error.
    attendance_data = read_from_file('attendance.csv')

    flag = False
    for row in attendance_data:
        if row['employee id'] == employee_id and row['departure date'] == 'None':
            flag = True

    if not flag:
        response = messagebox.showerror('Error', 'This employee has gone already. '
                                                 'Choose another one or close the window.')
        if response == 'ok':
            top.deiconify()
            return

    # Update data in the system according to the id of the employee who is going away now.
    for row in attendance_data:
        if row['employee id'] == employee_id and row['departure date'] == 'None':
            this_row = row
            attendance_id = this_row['attendance id']
            now = datetime.datetime.today()
            date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
            time = date.strftime('%H:%M')
            date = date.strftime('%d/%m/%Y')
            add_departure_to_system(attendance_id, date, time)

    # Show succeed message and ask use if he wants to check some employee's arrival else.
    response = messagebox.askyesno(top, 'Departure checked successfully. Do you want to check someone else?')
    if response == 1:
        top.deiconify()
    else:
        top.destroy()


def check_departure_menu():
    """
    Create top level screen to check departure.
    """
    global employees_listbox
    global top
    # Screen properties.
    top = Toplevel()
    top.title("Check departure")
    top.iconbitmap(ICON)
    size_hor = 300
    size_vert = 210
    window_position(top, size_hor, size_vert)

    # Create frame with employees' names listbox and scroll bar near it.
    frame = LabelFrame(top, height=100, width=30, padx=10, pady=10)
    frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    employees_listbox = Listbox(frame)

    data = read_from_file('employees.csv')
    for row in data:
        employees_listbox.insert(END, row['id'] + '. ' + row['first name'] + ' ' + row['last name'])

    employees_listbox.pack(side=LEFT, fill=BOTH)

    employees_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=employees_listbox.yview)

    # Create buttons.
    check_button = Button(top, text='Check Departure', command=check_departure)
    check_button.grid(row=0, column=1)

    close_button = Button(top, text='Close', command=top.destroy)
    close_button.grid(row=1, column=1)


def show_employees_button():
    """
    The function creates a screen with list of employees with given status.
    """
    status_list = []
    # Read the list of all employee's statuses.
    statuses = list_of_statuses()

    # Get indexes of chosen statuses from list box.
    indexes = status_listbox.curselection()
    for i in indexes:
        status_list.append(statuses[i])

    # If user doesn't choose any status, show warning message.
    if not status_list:
        messagebox.showwarning('Warning', 'You didn\'t choose anything. Please, choose something.')
        select_status_screen.deiconify()
        return
    else:
        # Create a title for the list of employees with chosen status.
        title = 'All employees with status'
        for item in status_list:
            title = title + ' ' + item
            if item != status_list[-1]:
                title += ','

    # Show report in a new screen.
    top_show = Toplevel()
    top_show.title("Show employees")
    top_show.iconbitmap(ICON)
    top_show.resizable(False, False)

    # Select employees with necessary statuses from the system.
    data = read_from_file('employees.csv')
    data = [row for row in data if row['status'] in status_list]

    # Write chosen employees to the temp file.
    with open('employees_temp.csv', 'a', newline='') as file:  # Open file to write data
        fieldnames = ['id', 'first name', 'last name', 'status', 'phone', 'age']  # define the header
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';', dialect='excel')  # and configure parameters
        writer.writeheader()
        for row in data:
            writer.writerow(row)  # and write it into the file

    # Show them in a new screnn.
    show_employees_screen('employees_temp.csv', top_show, title)

    # Remove temp file.
    os.remove('employees_temp.csv')


def show_employees():
    """
    The function creates screen to show employees with chosen statuses.
    """
    global select_status_screen
    global status_listbox

    # Screen parameters.
    select_status_screen = Toplevel()
    select_status_screen.title("Select")
    select_status_screen.iconbitmap(ICON)
    size_hor = 195
    size_vert = 200
    window_position(select_status_screen, size_hor, size_vert)

    # Screen header.
    title_label = Label(select_status_screen, text='Select statuses to show')
    title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10,0))

    # Frame with employees in a tree view and scroll bar near it.
    frame = LabelFrame(select_status_screen, padx=10, pady=10)
    frame.grid(row=1, column=0, columnspan=2, padx=15, pady=10)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    status_listbox = Listbox(frame, height=5, selectmode=MULTIPLE)

    statuses = list_of_statuses()
    for status in statuses:
        status_listbox.insert(END, status)

    status_listbox.pack(side=LEFT, fill=BOTH)

    status_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=status_listbox.yview)

    # Create buttons
    show_report_button = Button(select_status_screen, text='Show Report', command=show_employees_button)
    show_report_button.grid(row=2, column=0, rowspan=2)

    show_report_button = Button(select_status_screen, text='Close', command=select_status_screen.destroy)
    show_report_button.grid(row=2, column=1, rowspan=2)


def show_attendance_button():
    """
    The function creates a screen with list of attendance for employees with given status.
    And if it's necessary - with employees who are late.
    """
    status_list = []
    statuses = list_of_statuses()

    # Get indexes of chosen statuses from list box.
    indexes = status_listbox.curselection()
    for i in indexes:
        status_list.append(statuses[i])

    # If user doesn't choose any status, show warning message.
    if not status_list:
        messagebox.showwarning('Warning', 'You didn\'t choose anything. Please, choose something.')
        select_status_screen.deiconify()
        return
    else:
        # Create a header
        title = 'Attendance of employees with status'
        for item in status_list:
            title = title + ' ' + item
            if item != status_list[-1]:
                title += ','

    # Select employees with necessary statuses from the system.
    data = read_from_file('employees.csv')
    data = [row for row in data if row['status'] in status_list]

    # Select necessary employees' ids
    id_list = []
    for row in data:
        id_list.append(row['id'])

    # Create new screen to show data of attendance.
    top_show = Toplevel()
    top_show.title("Show employees")
    top_show.iconbitmap(ICON)
    top_show.resizable(False, False)

    # Choose employees to show
    att_data = read_from_file('attendance.csv')
    att_data = [row for row in att_data if row['employee id'] in id_list]

    # If user want to show only employees who are late, e.g. comes to work after 9:30 in the morning.
    right_time = datetime.datetime.strptime('9:30', '%H:%M')
    new_data = []
    flag = False
    if var.get() == 1:
        title += ' who comes late'
        for row in att_data:
            arrival_time = row['arrival time']
            arrival_time = datetime.datetime.strptime(arrival_time, '%H:%M')
            if arrival_time > right_time:
                flag = True
                new_data.append(row)
        # If there are no employees to show, raise info message.
        if not flag:
            top_show.destroy()
            response = messagebox.showinfo('Info', 'These employees never come late.')
            if response == 'ok':
                select_status_screen.deiconify()
                return
        else:
            att_data = new_data

    # Create temp attendance file with data to show.
    with open('attendance_temp.csv', 'a', newline='') as file:
        fieldnames = ['first name', 'last name', 'arrival date', 'arrival time', 'departure date', 'departure time']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';', dialect='excel')
        writer.writeheader()
        for row in att_data:
            del row['attendance id']
            del row['employee id']
            writer.writerow(row)

    # Show attendance data on the screen.
    show_attendance_screen('attendance_temp.csv', top_show, title)

    # Remove temp file.
    os.remove('attendance_temp.csv')


def show_attendance():
    """
    The function creates screen to show attendance of employees with chosen statuses: all of then
    or only those who are late.
    """
    global select_status_screen
    global status_listbox
    global var

    # screen properties.
    select_status_screen = Toplevel()
    select_status_screen.title("Select")
    select_status_screen.iconbitmap(ICON)
    size_hor = 195
    size_vert = 230
    window_position(select_status_screen, size_hor, size_vert)

    # Screen header.
    title_label = Label(select_status_screen, text='Select statuses to show')
    title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0))

    # Create frame with list of statuses and scroll bar near it.
    frame = LabelFrame(select_status_screen, padx=10, pady=10)
    frame.grid(row=1, column=0, columnspan=2, padx=15, pady=(10, 0))

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    status_listbox = Listbox(frame, height=5, selectmode=MULTIPLE)

    statuses = list_of_statuses()
    for row in statuses:
        status_listbox.insert(END, row)

    status_listbox.pack(side=LEFT, fill=BOTH)

    status_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=status_listbox.yview)

    # Create a check button to mark if user want to select only employees who are late.
    var = BooleanVar()
    c = Checkbutton(select_status_screen, text='late', variable=var, onvalue=1, offvalue=0)
    c.deselect()
    c.grid(row=2, column=0, stick=W, padx=20, pady=5)

    # Create buttons.
    show_report_button = Button(select_status_screen, text='Show Report', command=show_attendance_button)
    show_report_button.grid(row=3, column=0)

    show_report_button = Button(select_status_screen, text='Close', command=select_status_screen.destroy)
    show_report_button.grid(row=3, column=1)


def show_help():
    """
    The function shows information to the user.
    """
    help_screen = Toplevel()
    help_screen.title("Help")
    help_screen.iconbitmap(ICON)
    size_hor = 420
    size_vert = 380
    window_position(help_screen, size_hor, size_vert)

    text1 = 'Employee Attendance Management System'
    text2 = 'Built on February, 2020'
    text3 = 'Copyright: ' + '\N{COPYRIGHT SIGN} ' + 'Olga Shebeko'
    text4 = """This program maintain employees attendance for a company.\n
Program has following functionality:
- Add employee manually.
- Add employee from file (file has to contain all employees data: first     and last name, status, phone, age).
- Delete employee manually.
- Delete employee from file (file has to contain employees ids on diffe-  rent lines).
- Mark attendance getting date and time from computer clock.
- Create report for employees with given status.
- Create report for employees attendance and only for those who were late.

This is a training version of a program!
    """

    # Create a label with the text.
    help_label1 = Label(help_screen, text=text1, font=12)
    help_label1.pack(padx=10, pady=10, anchor='w')

    help_label2 = Label(help_screen, text=text2)
    help_label2.pack(padx=10, anchor='w')

    help_label3 = Label(help_screen, text=text3)
    help_label3.pack(padx=10, pady=(0, 10), anchor='w')

    help_label4 = Text(help_screen, width=55, heigh=15, bg='grey93', font='Helvetika 9', bd=0)
    help_label4.pack(padx=15, pady=(0, 10), anchor='w')
    help_label4.insert(1.0, text4)
    help_label4.config(state=DISABLED)

    # Create a close button
    close_button = Button(help_screen, text='Close', width=10, command=help_screen.destroy)
    close_button.pack(ipadx=10)


def main_screen():
    """
    Create main window.
    """
    global root
    # Screen properties.
    root = Tk()
    root.title(TITLE)
    root.iconbitmap(ICON)
    size_hor = 480
    size_vert = 300
    window_position(root, size_hor, size_vert)

    # Create menu.
    mainmenu = Menu(root)
    root.config(menu=mainmenu)

    employee_menu = Menu(mainmenu, tearoff=0)

    add_employee = Menu(employee_menu, tearoff=0)
    add_employee.add_command(label="Manually", command=add_manually_menu)
    add_employee.add_command(label="From File", command=add_from_file_menu)
    employee_menu.add_cascade(label="Add Employee", menu=add_employee)

    delete_employee = Menu(employee_menu, tearoff=0)
    delete_employee.add_command(label="Manually", command=delete_manually_menu)
    delete_employee.add_command(label="From File", command=delete_from_file_menu)
    employee_menu.add_cascade(label="Delete Employee", menu=delete_employee)

    mainmenu.add_cascade(label='Employees', menu=employee_menu)

    attendance_menu = Menu(mainmenu, tearoff=0)
    attendance_menu.add_command(label="Check Arrival", command=check_arrival_menu)
    attendance_menu.add_command(label="Check Departure", command=check_departure_menu)
    mainmenu.add_cascade(label="Attendance", menu=attendance_menu)

    report_menu = Menu(mainmenu, tearoff=0)
    report_menu.add_command(label="Employees", command=show_employees)
    report_menu.add_command(label="Attendance", command=show_attendance)
    mainmenu.add_cascade(label="Reports", menu=report_menu)

    mainmenu.add_command(label='Help', command=show_help)

    # Printing employees on the screen.
    show_employees_screen('employees.csv', root)

    root.mainloop()


if __name__ == "__main__":
    main_screen()
