import socket

def send_msg(sock: socket.socket, msg: bytes):
    """ソケットに指定したビアと列を書き込む関数"""
    # これまでに送信したバイト数を格納
    total_sent_len = 0

    # 送信するバイト数を格納
    total_msg_len = len(msg)

    # まだ送信したいデータが残っているか判定
    while total_sent_len < total_msg_len:
        # ソケットにバイト列を書き込んで、そのバイト数を得る
        sent_len = sock.send(msg[total_sent_len:])

        # 書き込めなかったらソケットの接続が終了している
        if sent_len == 0:
            raise RuntimeError('socket connection broken')
        
        # 書き込めた分を加算
        total_sent_len += sent_len


def recv_msg(sock: socket.socket, chunk_len=1024):
    """ソケットから接続が終わるまでバイト列を読み込むジェネレータ関数"""
    while True:
        # ソケットから指定したバイト数を読み込む
        received_chunk = sock.recv(chunk_len)

        # 読めない場合は接続が終了
        if len(received_chunk) == 0:
            break

        # 受信したバイト列を返す
        yield received_chunk


def main():
    # IPv4 / TCP で通信するソケットの用意
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ループバックアドレスのTCP/80 ポートに接続
    client_socket.connect(('127.0.0.1', 80))

    # HTTPサーバからドキュメントを取得するためのGETリクエスト
    request_text = 'GET / HTTP/1.0\r\n\r\n'

    # 文字列をバイト列にエンコード
    request_bytes = request_text.encode('ASCII')

    # ソケットにリクエストバイト列を書き込む
    send_msg(client_socket, request_bytes)

    # ソケットからレスポンスのバイト列を読み込む
    received_bytes = b''.join(recv_msg(client_socket))

    # 読み込んだバイト列をデコード
    received_text = received_bytes.decode('ASCII')

    print(received_text)

    # クローズ
    client_socket.close()


if __name__ == '__main__':
    main()

