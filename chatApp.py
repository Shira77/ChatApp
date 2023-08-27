from flask import Flask, render_template, request, redirect, url_for, session 
import csv
import os
import base64
from datetime import datetime
server = Flask(__name__)
#define env variable
os.environ["ROOM_PATH"] = "/rooms"

def chechUserExist(username,password):
   with open('users.csv', "r", newline="") as usersExist:
        users=csv.reader(usersExist)
        for user in users:
            if(user[0] == username and user[1] == decode_password(password)):
                return True 
        return False 


#encode password
def encode_password(user_pass):
    pass_bytes = user_pass.encode('ascii')
    base64_bytes = base64.b64encode(pass_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

#decode password
def decode_password(user_pass):
    base64_bytes = user_pass.encode('ascii')
    pass_bytes = base64.b64decode(base64_bytes)
    user_pass = pass_bytes.decode('ascii')
    return user_pass

@server.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if(chechUserExist(username, password)):
            session['username'] = username
            return redirect('lobby')

       
    return render_template('login.html')


@server.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #בדיקות תקינות לנתונים
        #הצפנת סיסמא
        encrypted_password = encode_password(password)
        #בדיקה אם השם משתמש והסיסמא קיימים
        with open("users.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                # Check if the name and phone number are in the row
                if row[0] == username and row[1] == encrypted_password:
                  return redirect('login')
            
        with open("users.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, encrypted_password])
        return redirect('login')
    return render_template('register.html')

@server.route('/lobby', methods = ['POST','GET'])
def lobby():
    if request.method == 'POST':
        new_room = request.form['new_room']
        if (str(new_room) + '.txt') in rooms:
            #print("exist in:" )
            return "exist"
        else:
            file = open('./rooms/'+ new_room +'.txt', 'w+')
            file.close()
            return redirect('chat/' + new_room)
            #return redirect('/chat/' + new_room, room=new_room)
    all_rooms=[x[:-4] for x in rooms]
    return render_template("lobby.html", all_rooms = all_rooms) 

   

@server.route('/logout', methods = ['POST','GET'])
def logout():
    session.pop('username', None)
    return redirect('register')  

@server.route("/chat/<room>")
def chat(room):
    return render_template('chat.html', room=room)

@server.route('/api/chat/<room>', methods = ['GET','POST'])
def manage_chat(room):
    file_path='./rooms/'+ room +'.txt'
    user= session.get('username')
    if user==None:
        user="guest"
    if request.method == 'POST':
        user_mssage= request.form['msg']
        #message in format:  [2023-08-21 11:00:11] yuval: hello
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        full_message= "[" + dt_string + "] " + user + ": " + user_mssage + '\n'
        with open(file_path, 'a+') as file:
            file.write(full_message)
            file.close()
    if os.path.getsize(file_path) == 0:
        content = str(user) + ", No messages yet"
    else:
        with open(file_path, 'r+') as f:
            content = f.read() 
            f.close()
    return content
    
if __name__ == "__main__":
    server.run(host='0.0.0.0')