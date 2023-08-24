from flask import Flask, render_template, request, redirect,session
import csv
import base64
import os

server = Flask(__name__) 

def chechUserExist(username,password):
  with open('users.csv', 'r', newline='') as usersExist:
    users=csv.reader(usersExist)
    for user in users:
        if(user[0] == username and user[1] == password):
           return True 
  return False  

@server.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        b=chechUserExist(username, password)
        if(b):
          session['username'] = username
          return redirect('lobby')
    return render_template('login.html')
#אתחול החדרים הקיימים 
rooms = []
for filename in os.listdir("rooms"):
    if filename.endswith(".txt"):
       room_name = filename[:-4]
       rooms.append(room_name)   
    
if __name__ == "__main__":
    server.run(host='0.0.0.0', port="5000")