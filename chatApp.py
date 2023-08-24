from flask import Flask, render_template, request, redirect, url_for, session 
import csv
import os
import base64
server = Flask(__name__)
def chechUserExist(username,password):
  with open('users.csv', "r") as usersExist:
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
        if(chechUserExist(username, password)):
          return redirect('lobby')

       
    return render_template('login.html')


@server.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #print(username, password)
        #בדיקות תקינות לנתונים
        #הצפנת סיסמא
        encrypted_password = base64.b64encode(password.encode())
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
        rooms = os.listdir('rooms/')
        new_room = request.form['new_room']
        if (str(new_room) + '.txt') in rooms:
            print("exist in:" )
            return "exist"
        else:
            rooms.append(new_room)
            file = open('./rooms/'+ new_room +'.txt', 'w+')
            file.close()
            #return redirect('/chat/' + new_room, room=new_room)
            return redirect('chat/' + new_room ,)  

    return render_template("lobby.html")

@server.route("/chat/<room>")
def chat(room):
    return render_template('chat.html',room=room)

# @server.route("/chat/<room>",  methods = ['GET'])
# def update(room):
#     file_path='./rooms/'+ room +'.txt'
#     if os.path.getsize(file_path) == 0:
#         return "No messages yet"
#     with open(file_path, 'w+') as file:
#                 content = file.read()
#                 file.close()
#                 return content


@server.route('/api/chat/<room>', methods = ['POST'])
def sendMSG(room):
    if request.method == 'POST':
        user=session['username']
        file = open('./rooms/'+ room +'.txt', 'w+')
        user_mssage=new_room = request.form['msg']
        file.close()
        #return redirect('/chat/' + new_room, room=new_room)
        return redirect('chat/' + new_room ,)  
    

    
    # try:
    #     file=open("./rooms/" +room + ".txt", "W+")
    #     content = file.read()
    #     file.close()
    #     return content
    # except IOError:
    #     return "Room does not exist!!"
    # except:
    #     return "You have an error"


        #roomName = user = request.args.get('rname')

if __name__ == "__main__":
    server.run(host='0.0.0.0')