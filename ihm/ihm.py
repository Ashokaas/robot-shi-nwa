import math
import threading
import socket
import keyboard
import time

HOST = "10.229.253.70"
PORT = 2005

# Création de la socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion au serveur
client.connect((HOST, PORT))
client.send("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA".encode())
print(f"Connexion vers {HOST}:{PORT} reussie.")
import pygame

pygame.init()


def on_key_down(event):
    if event.key == pygame.K_UP:
        client.send("K avancer".encode())
    elif event.key == pygame.K_LEFT:
        client.send("K gauche".encode())
    elif event.key == pygame.K_DOWN:
        client.send("K reculer".encode())
    elif event.key == pygame.K_RIGHT:
        client.send("K droite".encode())


def on_key_up(event):
    if event.key == pygame.K_UP:
        client.send("K stop_avancer".encode())
    elif event.key == pygame.K_LEFT:
        client.send("K stop_gauche".encode())
    elif event.key == pygame.K_DOWN:
        client.send("K stop_reculer".encode())
    elif event.key == pygame.K_RIGHT:
        client.send("K stop_droite".encode())


# Création de la fenêtre Pygame (n'est pas utilisée dans cet exemple)
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
