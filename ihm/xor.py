"""
Fonction permettant de chiffrer et déchiffrer un caractere grace a un masque jetable
"""
import random


def key_generator(length):
    alphabet: list = []
    for i in range(26):
        alphabet.append(chr(i+65))

    key: str = ""
    for i in range(length):
        key += random.choice(alphabet)

    return key


def chiffrement(message: str, cle=None):
    if cle is None:
        cle = key_generator(len(message))
    liste_char: list = [*message]
    for i in range(len(liste_char)):
        liste_char[i] = ord(liste_char[i]) ^ ord(cle[i])

    message: str = ""
    for i in range(len(liste_char)):
        message += chr(liste_char[i])

    return message, cle


if __name__ == "__main__":
    msg = "Les amis nous pouvons désormais chiffrer nos messages pour sécuriser nos communications avec le grand et puissant robot shi-nwa"
    key = key_generator(len(msg))
    msg = chiffrement(msg, key)
    print(msg)
    print(key)
    print(chiffrement(msg, key))
