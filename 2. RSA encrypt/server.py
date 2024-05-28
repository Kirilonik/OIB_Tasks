import socket
from threading import Thread
import rsa
import miller_rabin


def rsa_decrypt_text(encrypted_message, private_key):
    """ Расшифровка RSA сообщения """
    d, n = private_key
    k = (n.bit_length() + 7) // 8

    # Разбиение зашифрованного сообщения на блоки
    encrypted_blocks = [encrypted_message[i:i + k] for i in range(0, len(encrypted_message), k)]

    decrypted_blocks = []
    for encrypted_block in encrypted_blocks:
        # Преобразование блока в число
        encrypted_int = int.from_bytes(encrypted_block, byteorder='big')
        decrypted_int = rsa.rsa_decrypt_block(encrypted_int, d, n)

        # Преобразование обратно в байты и удаление случайного байта
        decrypted_block = decrypted_int.to_bytes(k, byteorder='big').lstrip(b'\x00')
        decrypted_blocks.append(decrypted_block)

    return b''.join(decrypted_blocks).decode('utf-8')


def generate_rsa_keys(bit_length):
    """Генерация ключей RSA заданной битности"""
    p = miller_rabin.generate_prime(bit_length)
    q = miller_rabin.generate_prime(bit_length)
    while p == q:
        q = miller_rabin.generate_prime(bit_length)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # Обычно выбирается такое значение
    d = pow(e, -1, phi)

    return (e, n), (d, n)


def handle_client(client_socket, private_key, public_key):
    """ Обработчик подключения нового клиента """
    e, n = public_key
    client_socket.send(f'{e},{n}'.encode('utf-8'))

    encrypted_message = client_socket.recv(1024)
    # encrypted_blocks = [int(block) for block in encrypted_message.decode('utf-8').split(',')]
    decrypted_message = rsa_decrypt_text(encrypted_message, private_key)

    print(f"Received message: {decrypted_message}")
    client_socket.close()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(('0.0.0.0', 9999))
    # server_socket.close()
    server_socket.listen(5)

    public_key, private_key = generate_rsa_keys(512)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_handler = Thread(target=handle_client, args=(client_socket, private_key, public_key))
        client_handler.start()


if __name__ == "__main__":
    server()
