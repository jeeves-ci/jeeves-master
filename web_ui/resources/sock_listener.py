import os
import sys
import websocket

socket_path = sys.argv[1]
# print socket_path


def write_to_stdout(ws, data):
    os.system('echo \'{data}\''.format(data=data))


def on_error(ws, error):
    os.system('echo Connection to minion socket was terminated: \'{}\''
              .format(error))


def on_close(ws):
    os.system('echo Socket connection closed.')


if __name__ == '__main__':
    minion_socket = websocket.WebSocketApp(
        socket_path,
        on_message=write_to_stdout,
        on_error=on_error,
        on_close=on_close
    )
    minion_socket.run_forever()
