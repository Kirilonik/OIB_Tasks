def rsa_encrypt_block(block, e, n):
    """Шифрование блока с использованием RSA"""
    return pow(block, e, n)


def rsa_decrypt_block(block, d, n):
    """Расшифровка блока с использованием RSA"""
    return pow(block, d, n)
