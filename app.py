import requests
from flask_login import LoginManager, current_user,login_user
from flask import Flask, request
from flask_socketio import SocketIO, send,join_room, leave_room
from User import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins='*', async_mode="eventlet")
login_manager = LoginManager()
login_manager.init_app(app)

@socketio.on('connect')
def chat_connect():
    print('connected')


@socketio.on('authorization')
def authorization(data):
    print(data)
    response = requests.get('http://127.0.0.1:5001/authorization', data)
    join_room(response.json()["userkey"])
    socketio.emit("authorization", response.json(), broadcast=True, room=response.json()["userkey"])
    print(response.json())

@socketio.on('home')
def room_list(data):
    print(data)
    rooms = requests.get('http://127.0.0.1:5001/home',data)
    print(rooms.json())
    socketio.emit('home', rooms.json(), broadcast=True, room=data["userkey"])


@socketio.on('handle_msg')
def handle_message(message):
    print(message)
    requests.post('http://127.0.0.1:5001/msgsocket', message)

    socketio.emit('handle_msg', message, broadcast=True, room=message["room_id"])


@socketio.on('join')
def on_join(data):
    room = data['room']
    print("join")
    join_room(room)
    messages = requests.get('http://127.0.0.1:5001/msgsocket', {"room_id": data['room']})
    print(messages.json())
    socketio.emit('join', messages.json(), broadcast=True, room=data["userkey"])

@socketio.on('leave')
def on_leave(data):
    print(data)
    room = data['room_id']
    leave_room(room)
    socketio.emit('leave', broadcast=True, room=room)
    print("leave")


if __name__ == '__main__':
    socketio.run(app, port=5000,host='192.168.31.89', debug=True)