import math
import threading
import socket
import keyboard
import time
import pygame
import time
import xbox_controller

"""
HOST = "127.0.0.1"
PORT = 1234

# Création de la socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion au serveur
client.connect((HOST, PORT))
client.send("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA".encode())
print(f"Connexion vers {HOST}:{PORT} reussie.")
"""

def on_key_down(event):
    if event.key == pygame.K_UP:
        client.send("avancer".encode())
    elif event.key == pygame.K_LEFT:
        client.send("gauche".encode())
    elif event.key == pygame.K_DOWN:
        client.send("reculer".encode())
    elif event.key == pygame.K_RIGHT:
        client.send("droite".encode())


def on_key_up(event):
    if event.key == pygame.K_UP:
        client.send("stop_avancer".encode())
    elif event.key == pygame.K_LEFT:
        client.send("stop_gauche".encode())
    elif event.key == pygame.K_DOWN:
        client.send("stop_reculer".encode())
    elif event.key == pygame.K_RIGHT:
        client.send("stop_droite".encode())
        

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
                    if key == "x" and val ==:

                
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



