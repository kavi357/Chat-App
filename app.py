from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

# python dictionary , store conneced user. Key is socketid and value is username and avatarurl
users = {}


@app.route('/')
def index():
    return render_template('index.html')

#connect someone
@socketio.on("connect")
def handle_connect(auth=None):  # Add 'auth' parameter
    username = f"User_{random.randint(1000, 9999)}"
    
    gender = random.choice(["girl", "boy"])
    avatar_url = f"https://avatar.iran.liara.run/public/{gender}?username={username}"
 
    users[request.sid] = {"username": username, "avatar": avatar_url}

    emit("user_joined", {"username": username, "avatar": avatar_url}, broadcast=True)
    emit("set_username", {"username": username})




#disconnect someone
@socketio.on("disconnect")
def handle_disconnect():
    user = users.pop(request.sid, None)
    if user:
        emit("user_left", {"username":user["username"]},broadcast=True)



#send message
@socketio.on("send_message")
def handle_message(data):
    user = users.get(request.sid)
    if user:
        emit("new_message", {
            "username":user["username"],
            "avatar": user["avatar"],
            "message":data["message"]
        },broadcast=True)


# Update username
@socketio.on("update_username")
def update_username(data):
    user = users.get(request.sid)
    if user:
        old_username = user["username"]
        new_username = data["username"]
        # Update only the username, keep the existing avatar and gender
        user["username"] = new_username

        emit("username_updated", {
            "old_username": old_username,
            "new_username": new_username
        }, broadcast=True)




if __name__ == "__main__":
    socketio.run(app)