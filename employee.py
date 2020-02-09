""" This module describes a class called employee and some functions that deal with it.
This class is used to define behavior of an employee that works for a company.

An employee can start to work so we need to add him to our system. We can do this manually or upload data from file.
We use csv file format for data storage.

An employee may either leave the company so we have to delete him from the system. We can do this manually or we can
delete several number of employees together using csv file with id-numbers of employees to delete.
"""

# So we start by importing some necessary modules.
import os
import csv


# And we create a class which contains description, attributes and methods useful for our purpose.
class Employee:

    def __init__(self):
        """
        This function creates an instance of our class and initialize a list which contains employees' id numbers.
        It doesn't take any argument because we want to create new employees two different ways: manually
        and from file.
        """
        self.ids = []  # a list of ids
        self.employee_id = 0
        self.first_name = ''
        self.last_name = ''
        self.status = ''
        self.phone = ''
        self.age = ''

    def add(self, first_name, last_name, status, phone, age):
        """
        Add method helps us add a new employee. It takes some inputs to add data to the employee: name, status,
        phone number and age. Id number adds automatically depending on the last existing employee's number
        in the system.
        """
        if len(self.ids) == 0:  # If there are no employees yet in the system, we start to count from 1.
            self.ids.append(1)
        else:  # Otherwise
            index = self.ids[-1]  # we takes the last id number from the list which contains all id numbers (ids),
            new_index = index + 1  # add 1 to it,
            self.ids.append(new_index)  # append to the id list,
        self.employee_id = self.ids[-1]  # and associate to a new employee's id number.

        # Also we associate another data from input to the attributes of an employee.
        self.first_name = first_name
        self.last_name = last_name
        self.status = status
        self.phone = phone
        self.age = age

    def delete(self, id_number):
        """
        Delete method helps us delete an employee from the system. It takes one argument: employee's id and deletes it
        from the list of ids and returns an index of the deleted number. Later we'll be able to find an employee in our
        employee's csv file by this index and delete all the information about him.
        """
        point = self.ids.index(id_number)  # This instruction returns an index of the employee to delete.
        del self.ids[point]  # Now we delete employee's id from the list of all ids
        return point  # and returns an index of the id number to calling function to delete related data from the file.

    def get_index(self, id_number):
        """
        This method just returns the position of a required employee from the list of ids.
        """
        return self.ids.index(id_number)

    def get_employee(self):
        """
        This method returns all employee's data.
        """
        result = [self.employee_id, self.first_name, self.last_name, self.status, self.phone, self.age]
        return result


# So we create an instance of our class Employee.
person = Employee()


def read_from_file(file_name):
    """
    The function helps us read data from a given file.
    :param file_name: file with data we want to read
    :return: data from the file
    """
    with open(file_name, 'r', newline='') as file:  # Open a csv file
        reader = csv.DictReader(file, delimiter=';', dialect='excel')  # like a csv-dictionary
        data = [row for row in reader]  # and convert it to the list of dictionaries,
    return data  # each row contains pairs {name of the column: a piece of data}


def write_to_file(file_name, data, header=0, massive=0):
    """
    The function helps us write data to the file.
    :param file_name: File to write data into it
    :param data: a list of lists with data
    :param header: defines whether we need to write to the file also a header or not. 1 - we need to, 0 - do not.
    :param massive: defines whether we send one simple list of data (0) or list of lists (1)
    :return: the function doesn't return anything, it just write data to the file.
    """
    with open(file_name, 'a', newline='') as file:  # Open file to write data
        fieldnames = ['id', 'first name', 'last name', 'status', 'phone', 'age']  # define the header
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';', dialect='excel')  # and configure parameters
        if header == 1:  # If we write new data to the file,
            writer.writeheader()  # first we need to write the header.
        if massive == 0:  # If we pass only one line of data,
            writer.writerow(dict(zip(fieldnames, data)))  # we construct only one dictionary {header: data}.
        else:  # Else if we send several number of lines with data (about some employees),
            for row in data:  # for each line
                input_string = dict(zip(fieldnames, row))  # we construct its one dictionary
                writer.writerow(input_string)  # and write it into the file


def check_data(first_name, last_name, status, phone, age):
    """
    Here we check an input data about an employee.
    :param first_name: first name should to be a string of letters
    :param last_name: also last name
    :param status: and status
    :param phone: phone should to consist of digits
    :param age: and age too
    :return: an exception if it occurs
    """
    if not first_name.isalpha() or not last_name.isalpha() or not status.isalpha() \
            or not phone.isdigit() or not age.isdigit():  # Here we check our input if its correct or not
        raise TypeError('Something is wrong with your input.')  # If not - raise TypeError
    if int(age) < 14 or int(age) > 120:  # And the age of our employee
        raise ValueError("Age can not be less then 14 and more then 120.")  # and if it's wrong, it raises ValueError
    if 10 < len(phone) < 12:  # and the phone number: if it too short or too long
        raise Exception("The phone number can't be less then 10 and more then 12 digits")  # Exception


def check_file(file_name):
    """
    This function checks the file user want to use. It takes the name of the file as a parameter and returns an error,
    if it occurs.
    :param file_name: The name of the file
    :return: The string which describes an error
    """
    if not file_name.endswith('.csv'):  # If this is not a csv-file,
        raise TypeError("Wrong file type. You have to upload csv-file.")  # it raises TypeError
    if not os.path.exists(file_name):  # If the file doesn't exist,
        raise FileNotFoundError("File doesn't exist.")  # it raise FileNotFoundError
    if os.path.getsize(file_name) == 0:  # If the file is empty,
        raise ValueError("The file is empty.")  # it raises ValueError


def clean_phone(phone_number):
    """
    This function helps us to clean the phone number from all unnecessary characters.
    :param phone_number: user-defined phone number
    :return: cleaned phone number
    """
    new_phone_number = ''
    for i in phone_number:
        if i.isdigit():
            new_phone_number += i
    return new_phone_number


def add_manually(first_name, last_name, status, phone, age):
    """
    The function takes input from user and add it to the file with all employees' data
    """
    person.add(first_name, last_name, status, phone, age)

    #  Then we receive the data back with the employee's id number
    data = person.get_employee()
    # and call the function to write received data to the file with all employees.
    write_to_file('employees.csv', data)


def add_from_file(file_name):
    """
    This function adds new employees from file. The file consist of several field of data according to the number
    of people we want to add to our system. The columns are the same: first name, last name, status, phone number and
    age - everything without id number, because it will be constructed by the system.
    """
    # If everything is OK with the file, we put all the data from file into the list persons' data
    data_to_add = read_from_file(file_name)
    # Next we need to check every row in our data set for proper values.
    for row in data_to_add:
        first_name, last_name, status, phone, age = row.values()
        phone = clean_phone(phone)
        try:
            check_data(first_name, last_name, status, phone, age)
        except TypeError:
            return 1
        except ValueError:
            return 1
        except Exception:
            return 1

    # If again everything is OK, we can add all the data from file to the employees' system.
    for row in data_to_add:
        first_name, last_name, status, phone, age = row.values()
        phone = clean_phone(phone)
        person.add(first_name, last_name, status, phone, age)
        data = person.get_employee()
        write_to_file('employees.csv', data)
    return 0


def delete_manually(index):
    """
    The function deletes an employee from the system. It asks user to enter id number of an employee he wants to delete
    and does it.
    """
    # First we need to read all the data from an employees' file to manipulate with them.
    data = read_from_file('employees.csv')

    # Now we need to check, if an employee with this number exists in the system.
    try:
        person.delete(index)
    except ValueError:  # if not, we say to user, that an employee with this id isn't found.
        return 1
    else:  # if he exists in the system,
        rest_of_data = [row for row in data if row['id'] != str(index)]  # we make a list of all employees except him.
        new_data = [[value for value in item.values()] for item in rest_of_data]  # We need to leave only the values
        write_to_file('employees-temp.csv', new_data, header=1, massive=1)  # and write it to the temp file

        os.remove('employees.csv', )  # We remove previous file
        os.rename('employees-temp.csv', 'employees.csv')  # and rename temp file as it used to be.

        return 0


def delete_from_file(file_name):
    """
    The function deletes employees from the system using additional file which consists id-number of employees
    user wants to delete.
    """
    # First we need to read all the data from an employees' file to manipulate with them.
    data = read_from_file('employees.csv')

    # Then we ask user to enter the name of the file with employees ids to delete and check the input for errors.
    try:
        check_file(file_name)
    except TypeError:
        return 1
    except FileNotFoundError:
        return 1
    except ValueError:
        return 1

    # If everything is OK, we read the file with ids and put all the ids into one list of numbers.
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        try:
            to_delete = []
            for i in reader:
                to_delete.append(int(i[0]))
        except Exception:
            return 2

    # Now we can dismiss people.
    for index in to_delete:
        try:  # If an employee exists in the system, it's OK
            person.delete(index)
        except ValueError:  # If not, we raise an error.
            return 3
        else:  # Things go on with new data
            data = [row for row in data if row['id'] != str(index)]
            new_data = [[value for value in item.values()] for item in data]

            # We write all the rest of the data to the temp file
            write_to_file('employees-temp.csv', new_data, header=1, massive=1)

            os.remove('employees.csv', )  # We remove previous file
            os.rename('employees-temp.csv', 'employees.csv')  # and rename temp file as it used to be.


if __name__ == '__main__':
    print(help(Employee))
