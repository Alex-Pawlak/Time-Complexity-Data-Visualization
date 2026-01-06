#Time Complexity Data Visualization Project (Documented on GitHub)
#Libraries
import sqlite3 #connect to database & run SQL code
import random #to randomly generate values
import string #ascii values
import csv #built in functions for handling csv files
import time #used to track processor execution time for the sorts
import sys #to perform system operations such as force quit application
import os #operating system library

#Establish Connection with Database
connect = sqlite3.connect("Database.db") 
cursor = connect.cursor() #acts as a pointer

#Simple Text Based Menu Function 
def Menu():
    choice=int(input("""
============================== MENU ==============================
= 1 - Generate New Database (Overwrite) or Add Items to Database =
= 2 - Convert .db file to .csv file                              =
= 3 - Perform Bubble Sort on .csv file                           =
= 4 - Perform Insertion Sort on .csv file                        =
= 5 - Perform Merge Sort on .csv file                            =
==================================================================
"""))
    if choice == 1:
        print(GenerateDatabase())
    elif choice == 2:
        print(DBtoCSV())
    elif choice == 3:
        print(ExecutionTimer(BubbleSort))
    elif choice == 4:
        print(ExecutionTimer(InsetionSort))
    elif choice == 5:
        print(ExecutionTimer(MergeSort))
    else:
        print("Invalid Choice")
    
    #checks if a sort has been executed
    if choice == 3 or choice == 4 or choice == 5: 
        create = input("Create sortedlist.csv of this data? (Y/N)")
        if create.lower() == "y":
            match choice: #choice is the type of sort performed by the user
                case 3:
                    sort_type = SortedListCSV(BubbleSort) #creates sorted list file
                case 4:
                    sort_type = SortedListCSV(InsetionSort) #creates sorted list file
                case 5:
                    sort_type = SortedListCSV(MergeSort) #creates sorted list file
            print(sort_type)
        elif create.lower() =="n": #user does not want sorted list file
            print("sortedlist.csv not updated/created")
        else: #any other input
            print("Invalid Choice")
    
#Databse Generation Function (Users able to upload their own .db files if they wish however)
def GenerateDatabase():
    #User determines whether to overwrite current database, or add to the existing one
    overwrite_or_add = input("Would you like to overwrite the Database file if it exists (O), or add items to the current Database (A)\n")
    
    #Loops until received valid input
    while overwrite_or_add.lower() != "o" and overwrite_or_add.lower() != "a":
        overwrite_or_add = input("Incorrect Input!\nWould you like to overwrite the Database file if it exists (O), or add items to the current Database (A)\n")

    #Selection statements determine whether to overwrite Database or add to existing Database
    if overwrite_or_add.lower() == "o":     #overwrite
        #Executes SQL Code - deletes any previous Database.db file if it exists
        cursor.execute('''DROP TABLE IF EXISTS Database''')
        #Creates a new table Database.db: single column "Item" - primary key
        cursor.execute('''
        CREATE TABLE Database (
            Item TEXT NOT NULL
        )
        ''') #commits transaction
        print("Database has been overwrited")
    elif overwrite_or_add.lower() == "a":     #add
        #Creates a new table Database.db if it doesn't already exists: single column "Item" - primary key
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Database (
            Item TEXT NOT NULL
        )
        ''')
    connect.commit() #commits transaction

    amount_of_items = int(input("Enter number of items to be generated: ")) #stores amount of items to be generated
    item_length = 6

    #Loops until received valid input
    item_type = input("Enter the type of items you want to generate:   Letters Only (L) / Digits Only (D)\n")
    while item_type.lower() != "l" and item_type.lower() != "d":
        item_type = input("Incorrect Input! Enter L or D!\nEnter the type of items you want to generate:   Letters Only (L) / Digits Only (D)\n")
    
    #Adds item one by one until amount of items to be generated is fulfilled
    for i in range(amount_of_items):
        item_generated = GenerateItem(item_type,item_length)
        if item_generated is True:
            print("Type Error: Attempted to add digits to letters, or letters to digits in database")
            sys.exit() #to prevent the return statement from printing, force stops program
        cursor.execute("INSERT INTO Database (Item) VALUES (?)", (item_generated,)) #Inserts current item_generated into the Item column
        connect.commit() #commits transaction
    
    return "Items successfully added to the database"

#Item Generation Function - generated a random sequence of characters, digits, or mix of both based on user input and returns Item    
def GenerateItem(item_type,item_length):
    cursor.execute("SELECT Item FROM Database")
    rows = cursor.fetchall()
    existing_items = [str(row[0]) for row in rows]
    type_error = False

    if item_type.lower() == "l": #letters only
        if all(x.isalpha() for x in existing_items):
            return (''.join(random.choices(string.ascii_letters, k=item_length)))
        else:
            type_error = True
            return type_error
        
    elif item_type.lower() == "d": #digits only
        if all(x.isdigit() for x in existing_items):
            return (''.join(random.choices(string.digits, k=item_length))) #sometimes generates 5 length digit - if 0 is the first num for example, it gets ignored in python
        else:
            type_error = True
            return type_error
    
    #can't sort letters and digits
    #elif item_type.lower() == "m":
    #    return (''.join(random.choices(string.ascii_letters + string.digits, k=item_length))) 

#Function which converts .db files to .csv files
def DBtoCSV():
    cursor.execute("SELECT * FROM Database") #selects all values from the database file
    rows = cursor.fetchall() #stores returned values from Item row in a single variable

    #Opens/Overwrites current or makes a new csv file if it doesn't already exists and writes data from .db file to .csv file
    with open("list.csv","w",newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return ".db file successfully converted to .csv file"

#Bubble Sort Function
def BubbleSort(list):
    for i in range(len(list)-1): #passes
        for x in range(len(list)-1-i): #swaps
            if list[x] > list[x+1]: #value to left greater than value to the right
                temp = list[x+1] #temporary variable to prevent it from being overwritten
                list[x+1] = list[x] #next 2 lines swap them around
                list[x] = temp
    return list

#Insertion Sort Function 
def InsetionSort(list):
    for i in range(1,len(list)): #loop through list starting from second element
        current_item = list[i]
        index = i-1 #sotres position of item before current_item
        while index >= 0 and list[index] > current_item: #moves left until items no longer greater than current item
            list[index+1] = list[index] #shift larger item to the right
            index -= 1 #return to previous position
        list[index+1] = current_item #reset current item
    return list

#Merge Sort Function
def MergeSort(list):
    if len(list) <= 1: #if there are 0 or 1 elements, list is sorted
        return list
    
    middle_position = len(list) // 2 #index of middle value in list
    
    sorted_left_half = MergeSort(list[:middle_position]) #uses recursive function to keep sorting left half items
    sorted_right_half = MergeSort(list[middle_position:]) #uses recursive function to keep sorting left half items

    return Merge(sorted_left_half,sorted_right_half) #merges and returns both halfs

#Merge Function
def Merge(sorted_left,sorted_right):
    sorted_list = [] #stores sorted list in this array
    i=0
    x=0
    
    while i < len(sorted_left) and x < len(sorted_right): #loops until no items remaining
        if sorted_left[i] < sorted_right[x]: #compares items
            sorted_list.append(sorted_left[i]) #appends smaller item from left
            i+=1 #moves to next item to the left
        else:
            sorted_list.append(sorted_right[x]) #otherwise append smaller item to the right
            x+=1 #moves to next item to the right

    sorted_list += sorted_left[i:] #any remaining items appended from left
    sorted_list += sorted_right[x:] #any remaining items appended from right

    return sorted_list 

#Processor Execution Timing Function Based on Sort Performed
def ExecutionTimer(SortFunction): #Takes type of sort as the parameter
    items = LoadCSV("list.csv")
    start_timer = time.perf_counter()
    print(SortFunction(items)) #Performs sort
    stop_timer = time.perf_counter()

    time_taken = stop_timer - start_timer #calculates final time
    return time_taken

#Function which loads the CSV file so that it can be passed to the sort functions
def LoadCSV(name_of_file):
    #Checks if csv file exists
    if not os.path.exists(name_of_file):
        return "File Path Not Found"
    #CSV file exists - opens file, reads lines, stores in the variable items
    with open (name_of_file, newline="") as file:
        reader = csv.reader(file)
        items = [row[0] for row in reader] #scans row by row and stores data as a string
        if all(x.isdigit() for x in items): #checks list is of digits only
            items = [int(x) for x in items] #converts to integer type
        elif all(x.isalpha() for x in items): #checks list is of letters only
            pass #already formatted as string
        else:
            return "Mixed or Invalid CSV File - Must be letters or digits only" #only seen if user uploads faulty csv file
        return items

#Function which creates a sorted list csv file after a sort is performed
def SortedListCSV(SortFunction):
    items = LoadCSV("list.csv") #loads csv and stores the unsorted list of items in the variable: items
    #Opens/Overwrites current or makes a new csv file if it doesn't already exists and writes sorted item list into sortedlist.csv file
    with open("sortedlist.csv","w",newline="") as file:
        writer = csv.writer(file)
        for i in SortFunction(items): #for each item in the sorted list
            writer.writerow([i]) #write individual item

    return "sortedlist.csv file has been created" #verification for user that the list has been created

Menu()