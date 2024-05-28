import socket
import rsa


def rsa_encrypt_message(message, e, n, block_size):
    """ Шифрование RSA сообщения """
    k = (n.bit_length() + 7) // 8
    m = k - 1

    # Преобразование сообщения в байты
    message_bytes = message.encode('utf-8')
    blocks = [message_bytes[i:i + m] for i in range(0, len(message_bytes), m)]

    encrypted_blocks = []
    for block in blocks:
        # Преобразование блока в число
        block_int = int.from_bytes(block, byteorder='big')
        encrypted_int = rsa.rsa_encrypt_block(block_int, e, n)

        # Преобразование обратно в байты
        encrypted_block = encrypted_int.to_bytes(k, byteorder='big')
        encrypted_blocks.append(encrypted_block)

    return b''.join(encrypted_blocks)


def client():
    msg = "1 2 3 4 5 6 7 8 9 0 - = ! @ @ # $ % ^ & * ( ) _ + q w e r t y u i o p [ ] a s d f g h j k l ; ' z x c v b n m , . / Q W E R T Y U I O P { } | A S D F G H J K L : Z X C V B B N M < > ?"
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))

    public_key = client_socket.recv(1024).decode('utf-8')
    e, n = map(int, public_key.split(','))

    k_block_size = 256
    encrypted_message = rsa_encrypt_message(msg, e, n, k_block_size)

    client_socket.send(encrypted_message)
    client_socket.close()


if __name__ == "__main__":
    client()
