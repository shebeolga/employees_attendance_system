import os
import csv


# First we create a class which contains description, attributes and methods for attendance checking.
class Attendance:

    def __init__(self):
        """
        Create an instance of the class and initialise ids list.
        """
        self.ids = []
        self.attendance_id = 0
        self.employee_id = 0
        self.first_name = ''
        self.last_name = ''
        self.arrival_date = 'None'
        self.arrival_time = 'None'
        self.departure_date = 'None'
        self.departure_time = 'None'

    def get_attendance(self):
        """
        Method returns all attendance attributes.
        """
        result = [self.attendance_id, self.employee_id, self.first_name, self.last_name,
                  self.arrival_date, self.arrival_time,
                  self.departure_date, self.departure_time]
        return result

    def add_arrival(self, employee_id, first_name, last_name, arrival_date, arrival_time):
        """
        This method add line of data with arrival id, employee's id, his first and last name, arrival's date and time.
        Departure date and time are stayed 'None'. They'll be changed late.
        """
        # If the system is new, we initiate ids list.
        if len(self.ids) == 0:
            self.ids.append(1)
        else:  # Otherwise we continue to count from the last number in id's list.
            index = self.ids[-1]
            new_index = index + 1
            self.ids.append(new_index)
        self.attendance_id = self.ids[-1]

        # And add all necessary data to the instance.
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.arrival_date = arrival_date
        self.arrival_time = arrival_time

    def add_departure(self, departure_date, departure_time):
        """
        Method sets departure date and time to the instance.
        """
        self.departure_date = departure_date
        self.departure_time = departure_time


# Create an instance.
attendance = Attendance()


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
    :param massive:
    :return: the function doesn't return anything, it just write data to the file.
    """
    with open(file_name, 'a', newline='') as file:  # Open file to write data
        # Define a header.
        fields = ['attendance id', 'employee id', 'first name', 'last name', 'arrival date', 'arrival time',
                  'departure date', 'departure time']
        writer = csv.DictWriter(file, fieldnames=fields, delimiter=';', dialect='excel')  # and configure parameters
        if header == 1:  # If we write new data to the file,
            writer.writeheader()  # first we need to write the header.
        if massive == 0:  # If we pass only one line of data,
            writer.writerow(dict(zip(fields, data)))  # we construct only one dictionary {header: data}.
        else:  # Else if we send several number of lines with data (about some employees),
            for row in data:  # for each line
                input_string = dict(zip(fields, row))  # we construct its own dictionary
                writer.writerow(input_string)  # and write it into the file


def add_arrival_to_system(employee_id, first_name, last_name, arrival_date, arrival_time):
    """
    The method add arrival to the system and write it to attendance file.
    """
    # First we construct new attendance instance and add data to it.
    # The method add arrival id to the instance automatically.
    attendance.add_arrival(employee_id, first_name, last_name, arrival_date, arrival_time)

    #  Then we receive data back with the attendance instance we've just create.
    data = attendance.get_attendance()
    # and call the function to write received data to the attendance.csv file.
    if os.path.isfile('attendance.csv'):
        write_to_file('attendance.csv', data)
    else:
        write_to_file('attendance.csv', data, header=1)


def add_departure_to_system(attendance_id, departure_date, departure_time):
    """
    This method adds departure information to the given attendance.
    """
    # First we find the line we need to add departure in attendance.csv file
    data = read_from_file('attendance.csv')
    row_to_change = [row for row in data if row['attendance id'] == str(attendance_id)]
    # Add necessary information
    row_to_change[0]['departure date'] = departure_date
    row_to_change[0]['departure time'] = departure_time
    new_data = [[value for value in item.values()] for item in data]
    # And write it to the temp file
    write_to_file('attendance-temp.csv', new_data, header=1, massive=1)

    # Then remove previous file and rename temp file as attendance.csv
    os.remove('attendance.csv', )  # We remove previous file
    os.rename('attendance-temp.csv', 'attendance.csv')  # and rename temp file as it used to be.


if __name__ == '__main__':
    print(help(Attendance))