#Time Complexity Data Visualization Project (Documented on GitHub)
#Libraries
import sqlite3 #connect to database & run SQL code
import random #to randomly generate values
import string #ascii values
import csv #built in functions for handling csv files
import time #used to track processor execution time for the sorts

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
        return GenerateDatabase()
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
            Item TEXT NOT NULL PRIMARY KEY
        )
        ''') #commits transaction
    elif overwrite_or_add.lower() == "a":     #add
        #Creates a new table Database.db if it doesn't already exists: single column "Item" - primary key
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Database (
            Item TEXT NOT NULL PRIMARY KEY
        )
        ''')
    connect.commit() #commits transaction

    amount_of_items = int(input("Enter number of items to be generated: ")) #stores amount of items to be generated
    item_length = 6

    #Loops until received valid input
    item_type = input("Enter the type of items you want to generate:   Letters Only (L) / Digits Only (D) / Mix Of Both (M)\n")
    while item_type.lower() != "l" and item_type.lower() != "d" and item_type.lower() != "m":
        item_type = input("Incorrect Input! Enter L, D or M!\nEnter the type of items you want to generate:   Letters Only (L) / Digits Only (D) / Mix Of Both (M)\n")
    
    #Adds item one by one until amount of items to be generated is fulfilled
    for i in range(amount_of_items):
        item_generated = GenerateItem(item_type,item_length)
        cursor.execute("INSERT INTO Database (Item) VALUES (?)", (item_generated,)) #Inserts current item_generated into the Item column
        connect.commit() #commits transaction

#Item Generation Function - generated a random sequence of characters, digits, or mix of both based on user input and returns Item    
def GenerateItem(item_type,item_length):
    if item_type.lower() == "l":
        return (''.join(random.choices(string.ascii_letters, k=item_length)))
    elif item_type.lower() == "d":
        return (''.join(random.choices(string.digits, k=item_length)))
    elif item_type.lower() == "m":
        return (''.join(random.choices(string.ascii_letters + string.digits, k=item_length))) 

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
def BubbleSort():
    # CODE GOES HERE
    return "BS"

#Insertion Sort Function 
def InsetionSort():
    # CODE GOES HERE
    return "IS"

#Merge Sort Function
def MergeSort():
    # CODE GOES HERE
    return "MS"

#Processor Execution Timing Function Based on Sort Performed
def ExecutionTimer(SortFunction): #Takes type of sort as the parameter
    start_timer = time.perf_counter()
    SortFunction() #Performs sort
    stop_timer = time.perf_counter()

    time_taken = stop_timer - start_timer #calculates final time
    return time_taken

#GenerateDatabase() #calls the function
Menu()