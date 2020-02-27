import csv
import os
import os.path

global_file_name = ' '
##function that builds the database
def buildDatabase():
    csv_file_name = input('Please enter the name of the csv file you would like to use: ')
    csv_name = csv_file_name.split('.')[0]
    ##checks if the file exists
    if os.path.isfile(csv_file_name):
        print('The file exists\n')
    else:
        print('That is not a valid csv file\n')
        return
    print('Building database...\n')
    ##opens csv file and reads information inside
    with open(csv_file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        data_file_name = csv_name + '.data.txt'
        g = open(data_file_name, 'w')
        column_names = ''
        ##loop that goes through every line within the CSV file
        for row in csv_reader:
            if line_count == 0:
                ##puts the name of the fields into one string
                for x in row:
                    if x != 'NAME':
                        column_names = column_names + x + ' '
                    else:
                        column_names = column_names[:0] + x + column_names[0:]
                        column_names = column_names[:4] + ' ' + column_names[4:]
                line_count += 1

            else:
                line_count += 1
         
                ##formats each string and writes to the .data file
                row0 = '{:40s}'.format(str(row[1]))
                row1 = '{:5s}'.format(str(row[0]))
                row2 = '{:20s}'.format(str(row[2]))
                row3 = '{:5s}'.format(str(row[3]))
                row4 = '{:10s}'.format(str(row[4]))
                row5 = '{:10s}'.format(str(row[5]))
                
                g.write(row0 + row1 + row2 + row3 + row4 + row5 + "\n")

        g.close()

        ##changes the number of lines to a string
        line_count = line_count - 1
        line_count_as_string = str(line_count)

        ##opens config file and adds number of records and name of the fields
        config_name = csv_name + '.config.txt'
        f = open(config_name, 'w')
        f.write('Number of records in the data file: ' + line_count_as_string +'\n')
        f.write('Names of the fields: ' + column_names + '\n')
        f.write('The size of field one is 40.\n')
        f.write('The size of field two is 5.\n')
        f.write('The size of field three is 20.\n')
        f.write('The size of field four is 5.\n')
        f.write('The size of field five is 10.\n')
        f.write('The size of field six is 10.\n')
        f.write('There are currently no records in the overflow file\n')
        f.close()

        ##creates the overflow file but doesn't add anything to it
        overflow_name = csv_name + '.overflow.txt'
        h = open(overflow_name , 'w')
        h.close()

##false variable that initializes no database has been opened yet
is_open = False

def openDatabase():
    ##global variables to check for opened database and so the files opened can be closed in another function
    ##a is the config file, b is the data file, and c is the overflow file
    global is_open
    global a
    global b
    global c
    global global_file_name

    if is_open == False:
        database_name = input('Please enter the name of the database you would like to open: ')
        data_name = database_name + '.data.txt'
        config_name = database_name + '.config.txt'
        overflow_name = database_name + '.overflow.txt'

        ##if all three of the files are found, the program continues. else the database doesn't exist
        if os.path.isfile(data_name) and os.path.isfile(config_name) and os.path.isfile(overflow_name):
            pass
        else:
            print('That database does not exist.\n')
            return

        global_file_name = database_name
        print('Opening the database\n')
        a = open(config_name , 'r+')
        b = open(data_name , 'r+')
        c = open(overflow_name , 'r+')
        is_open = True
    
    else:
        print('You must close the the database currently in use before opening a new one.\n')

def closeDatabase():
    ##global variables to check for opened database and so the files opened can be opened in another function
    global is_open
    global a
    global b
    global c

    ##if a database is open, the config, data, and overflow files are closed
    if is_open == True:
        print('Closing the database\n')
        a.close()
        b.close()
        c.close()
        is_open = False
        
    else:
        print('There is no database to be closed\n')

def displayRecord():
    global is_open
    global a
    global b
    global c

    if is_open == True:
        ##opens the config file and gets the num of records
        a.seek(0,0)
        first_line = a.readline()
        num_of_records = int(first_line.split()[7])
        print('A record can be displayed\n')
        record = input('Please enter the name of the company you would like to search for: ')
        record = record.upper()
        
        ##searches for the record
        record_found, record_line_number = binarySearch(b, record, num_of_records)
        line_city = record_found[45:64]
        line_city = line_city[slice(7)]

        ##if the city of the record found is "MISSING" this means this file was deleted and cannot be displayed
        if line_city == "MISSING":
            print('That file does not exist\n')
            return
        if record_found == 'Record not found\n':
            c.seek(0,0)
            record_name = '{:40s}'.format(record)
            for x in c:
                if x[0:40] == record_name:
                    print('The record was found in the overflow file!')
                    record_found = x
        print(record_found)
        record_line_number = str(record_line_number)

    else:
        print('No record can be found as there is no database open\n')

def getRecord(f, record_num, num_records):
    record = ' '
    record_size = 92

    if record_num>=1 and record_num<=num_records:
        f.seek(0, 0)
        f.seek(((record_num - 1)*record_size))
        record = f.readline()

    return record, record_num

def binarySearch(file_name, record_name, num_records):
    low = 0
    high = num_records - 1
    record = 'requested record not found'
    record_line_number = 0
    found = False

    while not found and high>=low:
        middle = (low + high) / 2
        middle = round(middle)
        record, record_line_number = getRecord(file_name, middle+1, num_records)
        middle_id = record[0:40]
        ##formats the name of the company the user is looking for to match the amound of characters within the data file
        record_name = '{:40s}'.format(record_name)

        if middle_id == record_name:
            found = True
        elif middle_id < record_name:
            low = middle+1
        else:
            high = middle-1

    if found == True:
        return record, record_line_number
    
    else:
        return 'Record not found\n', 0

def updateRecord(missing):
    global is_open
    global a
    global b
    global c
    global global_file_name
    
    if is_open == True:
        ##opens the config file to find the number of records
        a.seek(0,0)
        first_line = a.readline()
        num_of_records = int(first_line.split()[7])
        record_size = 92
        in_overflow = 0
        data_name = global_file_name + '.data.txt'
        overflow_name = global_file_name + '.overflow.txt'
        if (missing == 1):
                record_to_be_updated = input('Please enter the name of the record you would like to delete: ')
        else:
                record_to_be_updated = input('Please enter the name of the record you would like to update: ')
        
        record_to_be_updated = record_to_be_updated.upper()
        record_found, record_line_number = binarySearch(b, record_to_be_updated, num_of_records)
        if record_found == 'Record not found\n':
            c.seek(0,0)
            record_name = '{:40s}'.format(record_to_be_updated)
            overflow_line = 0
            for x in c:
                if x[0:40] == record_name:
                    print('The record was found in the overflow file!')
                    record_found = x
                    in_overflow = 1
                overflow_line+=1
        if record_found == 'Record not found\n':
            print('That file does not exist\n')
            return
        line_city = record_found[45:64]
        line_city = line_city[slice(7)]
        if line_city == "MISSING":
            print('That file does not exist\n')
            return
        print(record_found)
        
        company_name = '{:40s}'.format(record_found[0:39])
        company_rank = '{:5s}'.format(record_found[40:44])
        company_city = '{:20s}'.format(record_found[45:64])
        company_state = '{:5s}'.format(record_found[65:69])
        company_zip = '{:10s}'.format(record_found[70:79])
        company_employees = '{:10s}'.format(record_found[80:89])
        
        # if deleting report
        if (missing == 1):
            company_name = '{:40s}'.format(record_found[0:39])
            company_rank = '{:5s}'.format("0")
            company_city = '{:20s}'.format("MISSING")
            company_state = '{:5s}'.format("0")
            company_zip = '{:10s}'.format("0")
            company_employees = '{:10s}'.format("0")

            new_record = company_name + company_rank + company_city + company_state + company_zip + company_employees
            print('The record has been deleted!\n')

        #if updating report 
        else:
            ##asking if the company's rank is to be changed
            input_value = ' '
            while input_value not in ('1', '2'):
                input_value = input("Do you want to change the company's rank? Type 1 for yes or 2 for no: ")
            
            if input_value == '1':
                new_value = input('Please enter what you would like to change the rank to: ')
                print('\n')
                company_rank = new_value
            
            ##asking if the company's city is to be changed
            input_value = ' '
            while input_value not in ('1', '2'):
                input_value = input("Do you want to change the company's city? Type 1 for yes or 2 for no: ")
            
            if input_value == '1':
                new_value = input('Please enter what you would like to change the city to: ')
                print('\n')
                company_city = new_value

            ##asking if the company's state is to be changed
            input_value = ' '
            while input_value not in ('1', '2'):
                input_value = input("Do you want to change the company's state? Type 1 for yes or 2 for no: ")
            
            if input_value == '1':
                new_value = input('Please enter what you would like to change the state to: ')
                print('\n')
                company_state = new_value

            ##asking if the company's zipcode is to be changed
            input_value = ' '
            while input_value not in ('1', '2'):
                input_value = input("Do you want to change the company's zipcode? Type 1 for yes or 2 for no: ")
            
            if input_value == '1':
                new_value = input('Please enter what you would like to change the zipcode to: ')
                print('\n')
                company_zip = new_value

            ##asking if the company's number of employees is to be changed
            input_value = ' '
            while input_value not in ('1', '2'):
                input_value = input("Do you want to change the company's number of employees? Type 1 for yes or 2 for no: ")
            
            if input_value == '1':
                new_value = input('Please enter what you would like to change the number of employees to: ')
                print('\n')
                company_employees = new_value

            company_name = '{:40s}'.format(company_name)
            company_rank = '{:5s}'.format(company_rank)
            company_city = '{:20s}'.format(company_city)
            company_state = '{:5s}'.format(company_state)
            company_zip = '{:10s}'.format(company_zip)
            company_employees = '{:10s}'.format(company_employees)

            new_record = company_name + company_rank + company_city + company_state + company_zip + company_employees
            new_record = new_record.upper()
            print('The record has been changed!\n')

        if in_overflow == 0:
            b.seek(0,0)
            record_line_number = int(record_line_number)
            b.seek((record_line_number-1) * record_size)
            b.write(new_record)

            b.close()
            b = open(data_name, 'r+')

        elif in_overflow == 1:
            c.seek(0,0)
            overflow_list = []
            record_line_number = int(overflow_line)
            for x in c:
                overflow_list.append(x)
            c.close()
            c = open(overflow_name, 'w')
            c.seek(0,0)
            for x in overflow_list:
                if x[0:39] == new_record[0:39]:
                    c.write(new_record + '\n')
                else:
                    c.write(x)

            c.close()
            c = open(overflow_name, 'r+')
        
    else:
        print('Sorry, you cannot update a record without an open database\n')

def createReport():
    global b
    global is_open
    global global_file_name

    if is_open == True:
        report_name = global_file_name + '.report.txt'
        f = open(report_name, 'w+')
        b.seek(0,0)
        line_count = 0
        while line_count < 10:
            f.write(b.readline())
            line_count+=1
        print('The report was successfully created\n')
        f.close()

    else:
        print('There is no database open to create a report on\n')

num_overflow = 0
def addRecord():
    global a
    global b
    global c
    global is_open
    global global_file_name
    global num_overflow

    if is_open == True:
        overflow_name = global_file_name + '.overflow.txt'
        config_name = global_file_name + '.config.txt'
        ##get inputs for the new record that is being added. if the input is not valid, the user is instructed to enter a valid one
        ##ex) if user enters a word as the rank, zip, or employees it will not let them proceed without entering a number
        ##also, if a user enters a number as the city or state it will not let them proceed without entering a word
        name = input('Enter the company name for the new record: ')
        while(name == '') or name.isspace():
            name = input('That is not a valid input. Please enter a valid name: ')

        rank = input('Enter the rank of the company for the new record: ')
        while(rank == '') or rank.isspace() or not rank.isdigit():
            rank = input('That is not a valid input. Please enter a valid rank: ')

        city = input('Enter the city the new company is located in: ')
        while(city == '') or city.isspace() or city.isdigit():
            city = input('That is not a valid input. Please enter a valid city: ')

        state = input('Enter the state the new company is located in: ')
        while(state == '') or state.isspace() or state.isdigit():
            state = input('That is not a valid input. Please enter a valid state: ')

        zipcode = input('Enter the zip code for the new company: ')
        while(zipcode == '') or zipcode.isspace() or not zipcode.isdigit():
            zipcode = input('That is not a valid input. Please enter a valid zip code: ')

        employees = input('Enter the amount of employees the new company has: ')
        while(employees == '') or employees.isspace() or not employees.isdigit():
            employees = input('That is not a valid input. Please enter a valid amount of employees: ')

        ##format each field and add all fields to a string named new_record
        name = '{:40s}'.format(name)
        rank = '{:5s}'.format(rank)
        city = '{:20s}'.format(city)
        state = '{:5s}'.format(state)
        zipcode = '{:10s}'.format(zipcode)
        employees = '{:10s}'.format(employees)
        new_record = name + rank + city + state + zipcode + employees
        new_record = new_record.upper()

        ##for loop that gets the total number of lines within the overflow file
        line_count = 0
        for line in c:
            line_count += 1
        
        ##if there are less than 4 lines in the overflow, a new record is added to the overflow file
        if line_count < 4:
            print('\nAdding new record to the overflow file\n')
            c.write(new_record + '\n')
            c.close()
            c = open(overflow_name, 'r+')
            num_overflow+=1
            a.seek(0,0)
            config_lines = []
            for x in a:
                config_lines.append(x)
            a.close()
            a = open(config_name, 'w')
            count = 1
            for x in config_lines:
                if count < 9:
                    a.write(x)
                    count +=1
                else:
                    a.write('There are currently ' + str(num_overflow) + ' records in the overflow')
            a.close()
            a = open(config_name, 'r+')
            


        ##else if there are 4 records in the overflow, those 4 are taken out, sorted, and stored in a list.
        ##the old overflow records are removed from the overflow file
        ##the new record that was trying to be added is now a lone record within the overflow file
        else:
            print('\nPutting records from overflow into the data file\n')
            c.seek(0, 0)
            line_count = 1
            overflow_record_list = []
            for line in c:
                ##if its the 1st line in the overflow file, the record on that line is added to a list
                if line_count == 1:
                    overflow_record_list.append(line)
                    line_count+=1

                ##if its the 2nd line in the overflow file, the key for that record is compared to the key of the only record in the list
                elif line_count == 2:
                    line_name = line[0:39]
                    if line_name < overflow_record_list[0][0:39]:
                        overflow_record_list.insert(0, line)
                    else:
                        overflow_record_list.append(line)
                    line_count+=1

                ##if its the 3rd line in the overflow file, the key for the record is compared to the other 2 in the list
                ## placed accordingly.
                elif line_count == 3:
                    line_name = line[0:39]
                    if line_name < overflow_record_list[0][0:39]:
                        overflow_record_list.insert(0, line)
                    elif line_name > overflow_record_list[0][0:39] and line_name < overflow_record_list[1][0:39]:
                        overflow_record_list.insert(1, line)
                    else:
                        overflow_record_list.append(line)
                    line_count+=1

                ##if its the 4th line in the overflow file, the key for the record is compared to the other 3 in the list and placed accordingly.
                elif line_count == 4:
                    line_name = line[0:39]
                    if line_name < overflow_record_list[0][0:39]:
                        overflow_record_list.insert(0, line)
                    elif line_name > overflow_record_list[0][0:39] and line_name < overflow_record_list[1][0:39]:
                        overflow_record_list.insert(1, line)
                    elif line_name > overflow_record_list[1][0:39] and line_name < overflow_record_list[2][0:39]:
                        overflow_record_list.insert(2, line)
                    else:
                        overflow_record_list.append(line)
                    line_count+=1
            ##now, overflow_record_list contains a list of our overflow records in sorted order

            ##close overflow file and re-open in write to remove old overflow records and add new one
            c.close()
            c = open(overflow_name, 'w')
            c.write(new_record + '\n')
            config_lines1 = []
            for x in a:
                config_lines1.append(x)
            a.close()
            a = open(config_name, 'w')
            count = 1
            num_overflow = 1
            for x in config_lines1:
                if count < 9:
                    a.write(x)
                    count +=1
                else:
                    a.write('There are currently ' + str(num_overflow) + ' records in the overflow')
            a.close()
            a = open(config_name, 'r+')
            sortFile(overflow_record_list)

        c.close()
        c = open(overflow_name, 'r+')

    else:
        print('You must open a database to add a record to\n')

def sortFile(overflow_list):
    global global_file_name
    global a
    global b
    ##creates temporary file for sorting data
    temp_file = open('sortfile.txt', 'w+')
    temp_file.close()
    config_name = global_file_name + '.config.txt'
    a.close()
    a = open(config_name, 'r+')
    a.seek(0,0)
    line_count = 1
    b.seek(0,0)
    
    data_name = global_file_name + '.data.txt'
    temp_file = open('sortfile.txt', 'r+')
    for line in b:
        key_of_line = line[0:39]
        line_city = line[45:64]
        line_city = line_city[slice(7)]

        if line_city == "MISSING":
            pass

        else:
            ##checks if the overflow list is empty
            if not overflow_list:
                temp_file.write(line)
                line_count+=1
            
            ##if not empty, loops through overflow list and checks if records are less than current record
            else:
                for x in overflow_list:
                    if x[0:39] < key_of_line:
                        temp_file.write(x)
                        overflow_list.remove(x)
                        line_count+=1
                temp_file.write(line)
                line_count+=1

    ##checks if there is an overflow record being added that is greater than all data records and continues adding if there is more than one
    if (len(overflow_list) > 0) and b.readline() == '':
        while len(overflow_list) > 0:
            temp_file.write(overflow_list[0])
            del overflow_list[0]
            line_count+=1

    ##writes new number of records to config file
    a.write('Number of records in the data file: ' + str(line_count-1))
    a.close()
    a = open(config_name, 'r+')
    b.close()
    temp_file.close()
    
    ##renames current .data.txt and then deletes it
    os.rename(data_name, 'testfile.txt')
    
    if os.path.exists('testfile.txt'):
        os.remove('testfile.txt')

    ##renames sortfile.txt to DATABASE + .data.txt
    os.rename('sortfile.txt', data_name)

    if os.path.exists('sortfile.txt'):
        os.remove('sortfile.txt')
    b = open(data_name, 'r+')

val = ''
while(val != '9') or is_open == True:
    ##menu for user input
    print("Welcome to our database control center.")
    print("1) Create new database")
    print("2) Open database")
    print("3) Close database")
    print("4) Display record")
    print("5) Update record")
    print("6) Create report")
    print("7) Add record")
    print("8) Delete record")
    print("9) Quit")

    val = input("Please enter your selection: ")
    print("Your choice is " + str(val) + "\n")
    if(val == "1"):
        buildDatabase()

    elif(val == "2"):
        openDatabase()

    elif(val == "3"):
        closeDatabase()
    
    elif(val == "4"):
        displayRecord()

    elif(val == "5"):
        updateRecord(2)

    elif(val == "6"):
        createReport()

    elif(val == "7"):
        addRecord()
        
    elif(val =="8"):
        updateRecord(1)
    
    elif(val == "9") and (is_open == True):
        print('You must first close the open database before exiting the program\n')

print('Quitting\n')



