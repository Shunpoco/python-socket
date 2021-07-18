import socket

def send_msg(sock: socket.socket, msg: bytes):
    """ソケットに指定したバイト列を書き込む"""

    total_sent_len = 0
    total_msg_len = len(msg)

    while total_sent_len < total_msg_len:
        sent_len = sock.send(msg[total_sent_len:])
        
        if sent_len == 0:
            raise RuntimeError('socket connection broken')

        total_sent_len += sent_len


def recv_msg(sock: socket.socket, chunk_len=1024):
    """ソケットから接続が終わるまでバイト列を読み込むジェネレータ"""
    while True:
        received_chunk = sock.recv(chunk_len)

        if len(received_chunk) == 0:
            break

        yield received_chunk


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Address already in use を回避する
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    # クライアントからの接続を待ち受ける IP アドレスとポートを指定
    server_socket.bind(('127.0.0.1', 54321))

    # 接続の待受を開始
    server_socket.listen()

    # サーバが動作を開始したことを表示
    print('starting server...')

    # 接続の処理
    client_socket, (client_address, client_port) = server_socket.accept()

    # クライアント情報の表示
    print(f'accepted from {client_address}:{client_port}')

    # ソケットからバイト列を読み込む
    for received_msg in recv_msg(client_socket):
        # 読み込んだ内容をソケットに書き込み
        send_msg(client_socket, received_msg)

        # 送受信した内容を出力
        print(f'echo: {received_msg}')

    # 使い終わったソケットはクローズ
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
