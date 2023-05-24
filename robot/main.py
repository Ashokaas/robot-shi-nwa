#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Librairie(s)
import socket


class Robot:
    def __init__(self):
        # Create your objects here.
        ev3 = EV3Brick()

        # Write your program here.
        ev3.speaker.beep()

        motorGauche = Motor(Port.A, Direction.CLOCKWISE)
        motorDroite = Motor(Port.C, Direction.CLOCKWISE)
        motorCentre = Motor(Port.B, Direction.CLOCKWISE)

        # self.vroum = DriveBase(motorGauche, motorDroite, 55.5, 104)

        self.vroum = (motorGauche, motorDroite, motorCentre)

        self.ultrasonic = UltrasonicSensor(Port.S2)
        self.color = ColorSensor(Port.S3)

    def drive(self, speed, angle):
        self.vroum[0].run(speed)
        self.vroum[1].run(speed)

    def stop(self):
        self.vroumBase.stop()


class Server:
    def __init__(self, adresse, port, robot: Robot):
        self.serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # On demande à l'OS d'attacher notre programme au port TCP demandé
        self.serveur.bind((adresse, port))
        self.serveur.listen(10)

        self.robot = robot

    def listen(self):
        fin = False
        client, adresse = self.serveur.accept()
        print("Connexion de " + str(adresse))
        while fin == False:
            # Attente qu'un client se connecte
            print("oui")
            # Réception de la requete du client sous forme de bytes et transformation en string
            requete = client.recv(1024)
            print("Réception de " + requete.decode())
            print("oui")
            reponse = "OK"
            if requete.decode() == "FIN":
                fin = True
            if requete.decode() == "start_drive":
                self.robot.drive(100, 0)
            if requete.decode() == "stop_drive":
                self.robot.stop()

            # Préparation et envoi de la réponse
            reponse = "OK"
            client.send(reponse.encode())

        # Déconnexion avec le client
        print("Fermeture de la connexion avec le client.")
        client.close()

    def close(self):
        try:
            self.serveur.close()
            print("Arret du serveur")
        except:
            print("Une erreur est survenue")


robot = Robot()
serveur = Server("", 2005, robot)

serveur.listen()
serveur.close()
