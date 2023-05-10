#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()


# Write your program here.
ev3.speaker.beep()

motorGauche = Motor(Port.A)
motorDroite = Motor(Port.C)

vroum = DriveBase(motorGauche, motorDroite, 55.5, 104)


# Librairie(s)
import socket

# Interface réseau et port TCP d'acoute
ADRESSE = ""
PORT = 1664

# Création d'une socket
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# On demande à l'OS d'attacher notre programme au port TCP demandé
serveur.bind((ADRESSE, PORT))
serveur.listen(10)

# Boucle de gestion des connexions des clients
fin = False
while fin == False:
    # Attente qu'un client se connecte
    client, adresse = serveur.accept()
    print(f"Connexion de {adresse}")

    # Réception de la requete du client sous forme de bytes et transformation en string
    requete = client.recv(1024)
    print(f"Réception de {requete.decode()}")
    if requete.decode() == "FIN":
        fin = True
    if requete.decode() == "VROUM":
        vroum.straight(100)

    # Préparation et envoi de la réponse
    reponse = "OK"
    client.send(reponse.encode())

    # Déconnexion avec le client
    print("Fermeture de la connexion avec le client.")
    client.close()

# Arrêt du serveur    
print("Arret du serveur.")
serveur.close()