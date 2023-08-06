import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("已连接到服务器")


@sio.event
def disconnect():
    print("已断开与服务器的连接")


@sio.event
def message(data):
    print("收到消息:", data)


def main():
    sio.connect('http://localhost:8080')

    while True:
        try:
            message = input("输入消息: ")
            sio.emit('websocket_chat', message)
        except KeyboardInterrupt:
            break

    sio.disconnect()


if __name__ == '__main__':
    main()
