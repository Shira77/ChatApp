import csv
from flask import Flask, render_template, request, redirect
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
if __name__ == "__main__":
    server.run(host='0.0.0.0', port="5000", debug=True)
    
    
    
@server.route("/lobby", methods=['GET','POST'])
def lobbyPage():
        return render_template('login.html')    
    
    
