import secrets


def is_prime(n, k=40):
    """Тест Миллера-Рабина для проверки числа на простоту"""
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n == 1:
        return False

    # Представим n-1 в виде 2^r * s
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    # Проведем k раундов теста Миллера-Рабина
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  # a in [2, n-2]
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime_candidate(length):
    """Генерация простого числа заданной битности."""
    while True:
        candidate = secrets.randbits(length)
        # Убедимся, что число нечётное и имеет нужную битность
        candidate |= (1 << length - 1) | 1
        if is_prime(candidate):
            return candidate


def generate_prime(length, k=128):
    """Генерация простого числа по длинне бит."""
    candidate = generate_prime_candidate(length)
    while not is_prime(candidate, k):
        candidate = generate_prime_candidate(length)
    return candidate
