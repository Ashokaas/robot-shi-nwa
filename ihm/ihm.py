import socket
import pygame
import xbox_controller
import multiprocessing
from web.bdd import bdd as db
import xor

HOST = "10.229.253.70"
PORT = 2005

# Création de la socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion au serveur
client.connect((HOST, PORT))
# client.send("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA".encode())
print(f"Connexion vers {HOST}:{PORT} reussie.")


def receive_datas(client, exploration, pilote):
    database = db.BDD(file_name="/home/labbec/PycharmProjects/robot-shi-nwa/bdd/identifier.sqlite")
    while True:
        datas = client.recv(1024)
        datas.decode()
        length = len(datas)
        message, cle = datas[:length//2], datas[length//2:]
        datas, cle = xor.chiffrement(message, cle)
        datas = tuple(datas)
        print(datas[0])
        database.request(0, [exploration, datas[2], datas[1], pilote])


def on_key_up(event):
    if event.key == pygame.K_UP:
        message = "".join(xor.chiffrement("K stop_avancer"))
    elif event.key == pygame.K_LEFT:
        message = "".join(xor.chiffrement("K stop_gauche"))
    elif event.key == pygame.K_DOWN:
        message = "".join(xor.chiffrement("K stop_reculer"))
    elif event.key == pygame.K_RIGHT:
        message = "".join(xor.chiffrement("K stop_droite"))
    elif event.key == pygame.K_SPACE:
        message = "".join(xor.chiffrement("K stop_espace"))
    client.send(message.encode())


def on_key_down(event):
    message = None
    if event.key == pygame.K_UP:
        message = "".join(xor.chiffrement("K avancer"))
    elif event.key == pygame.K_LEFT:
        message = "".join(xor.chiffrement("K gauche"))
    elif event.key == pygame.K_DOWN:
        message = "".join(xor.chiffrement("K reculer"))
    elif event.key == pygame.K_RIGHT:
        message = "".join(xor.chiffrement("K droite"))
    elif event.key == pygame.K_SPACE:
        message = "".join(xor.chiffrement("K espace"))
    elif event.key == pygame.K_CAPSLOCK:
        message = "".join(xor.chiffrement("K barre"))
    if message is not None:
        client.send(message.encode())    


exploration = input("Nom de l'exploration : ")
pilote = input("Nom du pilote : ")

process = multiprocessing.Process(target=receive_datas, args=[client, exploration, pilote])

match input("Voulez vous controller le robot à la manette (y) ? "):
    case "y":
        print("Manette")
        # Création de la manette
        xbox = xbox_controller.XboxController()
        commandes = {"avancer": False, "gauche": False, "reculer": False, "droite": False}
        previous_inputs = xbox.read2()
        process.start()
        while True:
            current_inputs = xbox.read2()
            if current_inputs != previous_inputs:
                different_values = {key: current_inputs[key] for key in current_inputs if
                                    current_inputs[key] != previous_inputs.get(key)}
                print(different_values)
                for key, val in zip(different_values.keys(), different_values.values()):
                    message = None
                    # droite/gauche
                    if key == "x" and val == -1.0:
                        message = "".join(xor.chiffrement("C gauche"))
                    elif key == "x" and val in [-0.0, 0.0]:
                        message = "".join(xor.chiffrement("C stop_tourner"))
                    elif key == "x" and val == 1.0:
                        message = "".join(xor.chiffrement("C droite"))
                    if message is not None:
                        client.send(message.encode())

                    message = None
                    # Avancer
                    if key == "rightTrigger" and val == 4.0:
                        message = "".join(xor.chiffrement("C avancer"))
                    elif key == "rightTrigger" and val == 0.0:
                        message = "".join(xor.chiffrement("C stop_avancer"))
                    if message is not None:
                        client.send(message.encode())

                    message = None
                    # Reculer
                    if key == "leftTrigger" and val == 4.0:
                        message = "".join(xor.chiffrement("C reculer"))
                    elif key == "leftTrigger" and val == 0.0:
                        message = "".join(xor.chiffrement("C stop_reculer"))
                    if message is not None:
                        client.send(message.encode())

                    message = None
                    # Barre
                    if key == "A" and val == 1.0:
                        message = "".join(xor.chiffrement("C barre"))
                    if message is not None:
                        client.send(message.encode())

            previous_inputs = current_inputs

    case _:
        print("Clavier")

        pygame.init()
        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        my_font = pygame.font.SysFont('Comic Sans MS', 30)

        # Création de la fenêtre Pygame
        window = pygame.display.set_mode((500, 500))
        text_surface = my_font.render('Some Text', False, (0, 0, 0))

        # Boucle principale
        running = True
        process.start()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    on_key_down(event)
                elif event.type == pygame.KEYUP:
                    on_key_up(event)
            pygame.display.update()

        pygame.quit()
process.terminate()
