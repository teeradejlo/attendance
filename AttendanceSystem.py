import mysql.connector
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
from time import sleep
from gpiozero import Button
from datetime import datetime

def getStudentNickName(mycursor, id):
    mycursor.execute("SELECT * FROM students WHERE id = \"" + str(id) + "\"")
    
    myresult = mycursor.fetchall()
    return myresult[0][3]


def getClassName(mycursor, classid):
    mycursor.execute("SELECT * FROM classes WHERE id = \"" + str(classid) + "\"")
    
    myresult = mycursor.fetchall()
    return myresult[0][1]


def createTable(mycursor, tableName):
    if checkTableExistence(mycursor, tableName) == False:
        sql = "CREATE TABLE " + tableName + " (studentid VARCHAR(255) not null, classid VARCHAR(255) not null, datetime VARCHAR(255) not null)"
        mycursor.execute(sql)
        

def checkTableExistence(mycursor, tableName):
    mycursor.execute("SHOW TABLES")
    found = False
    
    for row in mycursor:
        if row[0] == tableName:
            print("\nThis table name already exist so we are going to use it instead.")
            found = True
        
    return found


def insertAttendance(mycursor, tableName, studentid, classid, datetime):
    sql = "INSERT INTO " + tableName + " (studentid, classid, datetime) VALUES (%s, %s, %s)"
    val = (studentid, classid, datetime)
    
    mycursor.execute(sql, val)
    mydb.commit()
    print("\n1 record inserted.\n-------------------------------")


def insertStudent(mycursor, tableName, id, fname, lname, nname):
    sql = "INSERT INTO " + tableName + " (id, firstname, lastname, nickname) VALUES (%s, %s, %s, %s)"
    val = (id, fname, lname, nname)
    
    mycursor.execute(sql, val)
    mydb.commit()

        

def findStudentExistence(mycursor, tableName, id):
    mycursor.execute("SELECT * FROM " + tableName + " WHERE id = \"" + id + "\"")
    
    myresult = mycursor.fetchall()
    if len(myresult) < 1:
        return False
    else:
        return True
    
    
def insertClasses (mycursor, tableName, className, teacherName):
    sql = "INSERT INTO " + tableName + " (name, teacher) VALUES (%s, %s)"
    val = (className, teacherName)
    
    mycursor.execute(sql, val)
    mydb.commit()

        

def findClassesExistence(mycursor, tableName, name):
    mycursor.execute("SELECT * FROM " + tableName + " WHERE name = \"" + name + "\"")
    
    myresult = mycursor.fetchall()
    if len(myresult) < 1:
        return False
    else:
        return True
    
    
def updateStudent(mycursor, tableName, id, topic, info):
    if topic == "firstname":
        segment = "firstname = " + "\"" + info + "\"" + "where id = " + "\"" + id + "\""
    elif topic == "lastname":
        segment = "lastname = " + "\"" + info + "\"" + "where id = " + "\"" + id + "\""
    elif topic == "nickname":
        segment = "nickname = " + "\"" + info + "\"" + "where id = " + "\"" + id + "\""
        
    mycursor.execute("update " + tableName + " set " + segment)
    
    mydb.commit()
    print("\nData Updated.\n-------------------------------")
    
    
def updateClasses(mycursor, tableName, name, topic, info):
    if topic == "classname":
        segment = "name = " + "\"" + info + "\"" + "where name = " + "\"" + name + "\""
    elif topic == "teacher":
        segment = "teacher = " + "\"" + info + "\"" + "where name = " + "\"" + name + "\""
        
    mycursor.execute("update " + tableName + " set " + segment)
    mydb.commit()
    print("\nData Updated.\n-------------------------------")
    
    
def deleteObject(mycursor, tableName, field, inputData):
    mycursor.execute("delete from " + tableName + " where " + field + " = " + "\"" + inputData + "\"")
    mydb.commit()
    print("\nData Deleted.\n-------------------------------")
    

def selectAll(mycursor, tableName):
    mycursor.execute("SELECT * FROM " + tableName)
    
    myresult = mycursor.fetchall()
    print("\nThe table \"" + tableName + "\" has the following information: \n")
    count = 1
    for x in myresult:
        #print(x[0], x[1]) print only field 0 and field 1 in one line
        #print(x)
        print("\t" + str(count) + ". " + x)
        count += 1
        

def showClasses(mycursor):
    mycursor.execute("SELECT * FROM classes")
    
    myresult = mycursor.fetchall()
    print("\nList of class:\n")
    count = 1
    for x in myresult:
        #print(x[0], x[1]) print only field 0 and field 1 in one line
        #print(x)
        print("\t" + str(count) + ". ID: " + str(x[0])
              + "\n\t   Class Name: " + str(x[1])
              + "\n\t   Teacher: " + str(x[2]) + "\n")
        count += 1

        
def showStudent(mycursor):
    mycursor.execute("SELECT * FROM students")
    
    myresult = mycursor.fetchall()
    print("\nList of student:\n")
    count = 1
    for x in myresult:
        #print(x[0], x[1]) print only field 0 and field 1 in one line
        #print(x)
        print("\t" + str(count) + ". ID: " + str(x[0])
              + "\n\t   First Name: " + str(x[1])
              + "\n\t   Last Name: " + str(x[2])
              + "\n\t   Nick Name: " + str(x[3]) + "\n")
        count += 1
        

def showAttendance(mycursor):
    mycursor.execute("SELECT * FROM attendance")
    
    myresult = mycursor.fetchall()
    print("\nList of attendance:\n")
    count = 1
    for x in myresult:
        #print(x[0], x[1]) print only field 0 and field 1 in one line
        #print(x)
        print("\t" + str(count) + ". Student ID: " + str(x[0])
              + "\n\t   Class ID: " + str(x[1])
              + "\n\t   Date and Time: " + str(x[2]) + "\n")
        count += 1
        
        
def showTables(mycursor):
    mycursor.execute("SHOW TABLES")
    print("\nTable lists: \n")
    for row in mycursor:
        print("\t" + row[0])


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database = "AttendanceSystem"
)

#students = "id, firstname, lastname, nickname"
#classes = "id, name, teacher"
#attendance = "studentid, classid, datetime"

mycursor = mydb.cursor()
reader = SimpleMFRC522()
button = Button(26)
lcd = CharLCD('PCF8574', 0x27)

smiley = (
     0b00000,
     0b01010,
     0b01010,
     0b00000,
     0b10001,
     0b10001,
     0b01110,
     0b00000,
)
lcd.create_char(0, smiley)

try:
    while True:
        yesOrNo =input("Want to continue? [Y/N]: ")
        if yesOrNo.lower() == "n":
            break
        attendanceOrAdmin = input("\nattendance or admin?: ")
        if attendanceOrAdmin.lower() == "admin":
            showTables(mycursor)
            tableName = input("\nWhich table do you want to work on?: ").lower()
            addOrUpdate = input("\nWant to add or update or delete or show information?: ").lower()
            if addOrUpdate == "add":
                if tableName == "students":
                    print("\nWhat is the student ID? Scan the tag...")
                    id, name = reader.read()
                    print(id)
                    if findStudentExistence(mycursor, tableName, str(id)) == False:
                        print("What is the student firstname?")
                        fname = input()
                        print("What is the student lastname?")
                        lname = input()
                        print("What is the student nickname?")
                        nname = input()
                        insertStudent(mycursor, tableName, str(id), fname, lname, nname)
                        print("\n1 record inserted.\n-------------------------------")
                    else:
                        print("\nThe id of this student already exist in the table. Please use update instead.\n-------------------------------")
                elif tableName == "classes":
                    print("What is the class name?")
                    className = input()
                    if findClassesExistence(mycursor, tableName, className) == False:
                        print("Who is the teacher?")
                        teacherName = input()
                        insertClasses(mycursor, tableName, className, teacherName)
                        print("\n1 record inserted.\n-------------------------------")
                    else:
                        print("\nThis class already exist in the table. Please use update instead.\n-------------------------------")
                else:
                    print("Can't add to attendance table")
            elif addOrUpdate == "update":
                if tableName == "students":
                    print("\nWhat is the student ID? Scan the tag...")
                    id, name = reader.read()
                    print(id)
                    print("What do you want to update [firstname, lastname, nickname]?")
                    topic = input().lower()
                    print("new " + topic + "?")
                    info = input()
                    updateStudent(mycursor, tableName, str(id), topic, info)
                elif tableName == "classes":
                    print("\nWhat is the class name?")
                    className = input().lower()
                    print("What do you want to update [classname, teacher]?")
                    topic = input().lower()
                    print("new " + topic + "?")
                    info = input()
                    updateClasses(mycursor, tableName, className, topic, info)
                else:
                    print("Can't update to attendance table")
            elif addOrUpdate == "delete":
                if tableName == "attendance":
                    print("Can't update to attendance table")
                else:
                    print("\nWhat field will you use for searching?")
                    field = input()
                    print("What is the information?")
                    infos = input()
                    deleteObject(mycursor, tableName, field, infos)
            elif addOrUpdate == "show":
                if tableName == "students":
                    showStudent(mycursor)
                elif tableName == "classes":
                    showClasses(mycursor)
                else:
                    showAttendance(mycursor)
            else:
                print("ERROR Incorrect input.\n-------------------------------")
        elif attendanceOrAdmin == "attendance":
            lcd.clear()
            lcd.write_string("Welcome to \r\nAttendance System!!")
            tableName = "attendance"
            showClasses(mycursor)
            classid = input("Class ID: ")
            lcd.write_string("\r\n\n" + str(classid))
            sleep(2)
            mycursor.execute("SELECT * FROM classes")
            print("")
            myresult = mycursor.fetchall()
            if int(classid) <= len(myresult):
                checking = True
                while checking:
                    lcd.clear()
                    lcd.write_string(getClassName(mycursor, classid) + "\r\n\nScan the tag..")
                    print("What is your student ID? Scan the tag... Press button to EXIT...\n-------------------------------")
                    while True:
                        if button.is_pressed:
                            checking = False
                            print("EXITTING.....\n-------------------------------")
                            lcd.clear()
                            lcd.write_string("Exitting....")
                            sleep(2)
                            lcd.clear()
                            break
                        elif reader.read_id_no_block():
                            id, name = reader.read()
                            print("ID: " + str(id))
                            now = datetime.now()
                            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                            print("Date and Time = " + dt_string)
                            insertAttendance(mycursor, tableName, str(id), classid, dt_string)
                            dt_string = now.strftime("%d/%m/%Y")
                            lcd.clear()
                            lcd.write_string("Welcome!\r\nID: " + str(id) + "\r\nName: " + getStudentNickName(mycursor, id) + "\r\nTime: " + dt_string)
                            sleep(2)
                            break
            else:
                lcd.clear()
                lcd.write_string("Class ID ERROR!!")
                sleep(2)
                lcd.clear()
                print("ERROR Incorrect input.\n-------------------------------")
        else:
            print("ERROR Incorrect input.\n-------------------------------")
                

finally:
    GPIO.cleanup()
    lcd.clear()
    lcd.write_string("Bye Bye ~~ \x00")
    sleep(2)
    lcd.clear()
    
    
    
    
    




