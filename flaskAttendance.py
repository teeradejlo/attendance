from flask import Flask
import RPi.GPIO as GPIO
from time import sleep
import mysql.connector
import datetime

def getClassName(mycursor, classid):
    mycursor.execute("SELECT * FROM classes WHERE id = \"" + str(classid) + "\"")
    
    myresult = mycursor.fetchall()
    return myresult[0][1]


def getStudentName(mycursor, id):
    mycursor.execute("SELECT * FROM students WHERE id = \"" + str(id) + "\"")
    
    myresult = mycursor.fetchall()
    return myresult[0][1] + " " + myresult[0][2]


def getAttendanceData(mycursor, tableName):
    mycursor.execute("SELECT * FROM " + tableName)
    
    myresult = mycursor.fetchall()
    tableString = '''
                     <style>
                     
                         body {
                             background-color:#151515;
                         }
                         
                         h1 {
                             color: white;
                             text-align: center;
                             font-family: Arial, Heveltica, san-serif;
                         }
                         
                         table {
                             width: 80%;
                             color: white;
                             text-align:center;
                             border: 2px solid white;
                             border-right: transparent;
                             border-bottom: transparent;
                         }
                         
                         th, td {
                             border-right: 2px solid white;
                             border-bottom: 2px solid white;
                             height: 50px;
                         }
                         
                     </style>
                        
                     <h1>Welcome to Attendance System With Flask</h1><br/>
                     <table align = "center">
                          <tr>
                            <th width = "20%";>Student ID</th>
                            <th>Student Name</th>
                            <th>Class Name</th> 
                            <th>Date and Time</th>
                          </tr>
                    '''
    for i in range(0, len(myresult)):
        tableString = tableString + '<tr>'
        tableString = tableString + '<td>' + myresult[i][0] + '</td>'
        tableString = tableString + '<td>' + getStudentName(mycursor, myresult[i][0]) + '</td>'
        tableString = tableString + '<td>' + getClassName(mycursor, myresult[i][1]) + '</td>'
        tableString = tableString + '<td>' + myresult[i][2] + '</td>' 
        tableString = tableString + '</tr>'
        
    tableString = tableString + "</table>"
        
    return tableString



app = Flask(__name__, static_url_path = "/stuff", static_folder = "static")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database = "AttendanceSystem"
)
tableName = "attendance"
mycursor = mydb.cursor()
      
@app.route("/")
def home():
    myhtml = getAttendanceData(mycursor, tableName)
    return myhtml



#localhost:5000
if __name__ == "__main__":
    app.run()
    
