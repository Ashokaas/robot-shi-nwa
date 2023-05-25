#!/usr/bin/env pybricks-micropython
import time

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import multiprocessing as mp
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

        self.vroumBase = DriveBase(motorGauche, motorDroite, 55.5, 104)

        self.vroum = (motorGauche, motorDroite, motorCentre)

        self.ultrasonic = UltrasonicSensor(Port.S2)
        self.color = ColorSensor(Port.S3)

        # Touches appuyées
        self.up = False
        self.left = False
        self.right = False
        self.down = False

    def drive(self, speed, angle):
        self.vroumBase.drive(speed, angle)

    def get_datas(self):
        return self.ultrasonic.distance(silent=True), self.color.ambient() / 10, self.vroumBase.distance()

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

    def keyboard_handling(self):
        vitesse = 500 * self.robot.up - 500 * self.robot.down
        angle = 30 * self.robot.right - 30 * self.robot.left
        vitesse += 1 if angle > 0 and vitesse == 0 else 0

        self.robot.drive(vitesse, angle)

    def controller_handling(self):
        vitesse = 300 * self.robot.rightTrigger - 300 * self.robot.leftTrigger
        angle = 60 * self.robot.xRight - 60 * self.robot.xLeft
        vitesse += 1 if angle != 0 and vitesse == 0 else 0

        self.robot.drive(vitesse, angle)

    def send_datas(self, client):
        while True:
            time.sleep(0.5)
            datas = robot.get_datas()
            client.send(str(datas).encode())

    def listen(self):
        fin = False
        client, adresse = self.serveur.accept()
        print("Connexion de " + str(adresse))
        process = mp.Process(target=self.send_datas, args=[client])
        process.start()
        while not fin:
            # Attente qu'un client se connecte
            # Réception de la requete du client sous forme de bytes et transformation en string
            requete = client.recv(1024)
            requetestr = requete.decode()
            print("Réception de " + requetestr)

            if requetestr.startswith("K "):
                cmd = requetestr.removeprefix("K ")

                self.robot.up = True if cmd == "avancer" else False if cmd == "stop_avancer" else self.robot.up
                self.robot.left = True if cmd == "gauche" else False if cmd == "stop_gauche" else self.robot.left
                self.robot.right = True if cmd == "droite" else False if cmd == "stop_droite" else self.robot.right
                self.robot.down = True if cmd == "reculer" else False if cmd == "stop_reculer" else self.robot.down

                self.keyboard_handling()

            # Préparation et envoi de la réponse
            reponse = "OK"
            client.send(reponse.encode())

        # Déconnexion avec le client
        print("Fermeture de la connexion avec le client.")
        process.terminate()
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
