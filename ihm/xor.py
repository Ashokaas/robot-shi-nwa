import random

"""
Fichier permettant de chiffrer et déchiffrer un caractere grace a un masque jetable
"""


def key_generator(length):
    """ Génère une clé aléatoire de la longueur spécifiée.

    Args:
        length (int): Longueur de la clé.

    Returns:
        str: Clé générée.
        
    """
    alphabet: list = []
    for i in range(26):
        alphabet.append(chr(i+65))

    key: str = ""
    for i in range(length):
        key += random.choice(alphabet)

    return key


def chiffrement(message: str, cle=None):
    """ Chiffre le message en utilisant une clé de chiffrement.

    Args:
        message (str): Message à chiffrer.
        cle (str): Clé de chiffrement (facultatif).

    Returns:
        tuple: Tuple contenant le message chiffré et la clé utilisée.

    """
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
