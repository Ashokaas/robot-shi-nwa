import math
import threading
import socket
import keyboard
import time
import pygame
import time
import xbox_controller

HOST = "10.229.253.70"
PORT = 2005

# Création de la socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion au serveur
client.connect((HOST, PORT))
client.send("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA".encode())
print(f"Connexion vers {HOST}:{PORT} reussie.")
"""

def on_key_down(event):
    if event.key == pygame.K_UP:
        client.send("K avancer".encode())
    elif event.key == pygame.K_LEFT:
        client.send("K gauche".encode())
    elif event.key == pygame.K_DOWN:
        client.send("K reculer".encode())
    elif event.key == pygame.K_RIGHT:
        client.send("K droite".encode())

def on_key_down(event):
    if event.key == pygame.K_UP:
        client.send("K avancer".encode())
    elif event.key == pygame.K_LEFT:
        client.send("K gauche".encode())
    elif event.key == pygame.K_DOWN:
        client.send("K reculer".encode())
    elif event.key == pygame.K_RIGHT:
        client.send("K droite".encode())
    elif event.key == pygame.K_SPACE:
        client.send("K espace".encode())



match input("Voulez vous controller le robot à la manette (y) ? "):
    case "y":
        print("Manette")
        
        # Création de la manette
        xbox = xbox_controller.XboxController()
        commandes = {"avancer": False, "gauche": False, "reculer": False, "droite": False}
        previous_inputs = xbox.read2()
        while True:
            current_inputs = xbox.read2()
            if current_inputs != previous_inputs:
                different_values = {key: current_inputs[key] for key in current_inputs if current_inputs[key] != previous_inputs.get(key)}
                print(different_values)
                for key, val in zip(different_values.keys(), different_values.values()):
                    # droite/gauche
                    if key == "x" and val == -1.0:
                        client.send("C gauche".encode())
                    if key == "x" and val in [-0.0, 0.0]:
                        client.send("C stop_tourner".encode())
                    if key == "x" and val == 1.0:
                        client.send("C droite".encode())

                    # Avancer
                    if key == "rightTrigger" and val == 4.0:
                        client.send("C avancer".encode())
                    if key == "rightTrigger" and val == 0.0:
                        client.send("C stop_avancer".encode())

                    # Reculer
                    if key == "leftTrigger" and val == 4.0:
                        client.send("C reculer".encode())
                    if key == "leftTrigger" and val == 0.0:
                        client.send("C stop_reculer".encode())

            previous_inputs = current_inputs

    case _:
        print("Clavier")

        pygame.init()

        # Création de la fenêtre Pygame
        window = pygame.display.set_mode((200, 200))

        # Boucle principale
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    on_key_down(event)
                elif event.type == pygame.KEYUP:
                    on_key_up(event)

        pygame.quit()



