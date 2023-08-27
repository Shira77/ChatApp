from flask import Flask , redirect,request,render_template,session
import csv
import os
import base64



#define env variable
os.environ["ROOM_PATH"] = "/rooms"



server = Flask(__name__)
server.secret_key="secret_key"
#check if user exit in the csv
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
        if chechUserExist(username, password):
            session['username'] = username
            return redirect('register')
        else:
            return "Invalid credentials. Please try again."
            #return "Hello"

       
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
    # if not session.get("username"):
    #     return redirect("/")
    if request.method == 'POST':
        rooms = os.listdir('rooms/')
        new_room = request.form['new_room']
        if (str(new_room) + '.txt') in rooms:
            #print("exist in:" )
            return "exist"
        else:
            rooms.append(new_room)
            file = open('./rooms/'+ new_room +'.txt', 'w+')
            file.close()
            #return redirect('/chat/' + new_room, room=new_room)
            return render_template('chat.html', room=new_room)  

    return render_template('lobby.html')

@server.route('/logout', methods = ['POST','GET'])
def logout():
    session.pop('username', None)
    return redirect('register')
# @server.route("/lobby", methods=['POST'])
# def lobby():
#     roomName = request.args.get('rname')
#     f = open(str('/rooms/') + str(roomName) + ".txt" ,"w+")
#     f.close()
#     for room in rooms:
#         if room == roomName:
#             return "Room Name already exist!!"
#     rooms.append(roomName)
#     return redirect(url_for('/chat/' + str(roomName), room_names = room))
#     return "you succeed!!"    

@server.route("/chat/<room>")
def chat(room):
    return render_template('chat.html',room=room)
# # Get the room from the parameter
#     room = request.args.get('room')

#     # Check if the room exists
#     if room not in rooms:
#         return render_template('error.html', message="The room does not exist.")

#     # Render the chat room page
#     return render_template('chat.html', room=room)


        #roomName = user = request.args.get('rname')

if __name__ == "__main__":
    server.run(host='0.0.0.0')