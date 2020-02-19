from flask import Flask
import RPi.GPIO as GPIO
from time import sleep
import mysql.connector
import datetime

def getAttendanceData(mycursor, tableName):
    mycursor.execute("SELECT * FROM " + tableName)
    
    myresult = mycursor.fetchall()
    tableString = '''
                     <h1 style="text-align:center">Welcome to Attendance System With Flask</h1><br/>
                     <table style="width:100%; ", border = "1">
                          <tr>
                            <th>Student ID</th>
                            <th>Class ID</th> 
                            <th>Date and Time</th>
                          </tr>
                    '''
    for i in range(0, len(myresult)):
        tableString = tableString + '<tr style="text-align:right">'
        tableString = tableString + '<td>' + myresult[i][0] + '</td>'
        tableString = tableString + '<td>' + myresult[i][1] + '</td>'
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
    
