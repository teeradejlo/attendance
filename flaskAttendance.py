from flask import Flask
import RPi.GPIO as GPIO
from time import sleep
import mysql.connector
import datetime

app = Flask(__name__, static_url_path = "/stuff", static_folder = "static")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database = "AttendanceSystem"
)
tableName = "attendance"
      
@app.route("/")
def home():
    
    myhtml = '''
                <h1>Welcome to Flask</h1><br/>
                <table style="width:100%; ", border = "1">
                  <tr>
                    <th>Firstname</th>
                    <th>Lastname</th> 
                    <th>Age</th>
                  </tr>
                  <tr style="text-align:right">
                    <td>Jill</td>
                    <td>Smith</td> 
                    <td>50</td>
                  </tr>
                  <tr style="text-align:right">
                    <td>Eve</td>
                    <td>Jackson</td> 
                    <td>94</td>
                  </tr>
                </table>'''
    return myhtml



#localhost:5000
if __name__ == "__main__":
    app.run()
    
