#!/usr/bin/env pybricks-micropython
import time
import xor

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
        self.barre = Motor(Port.B, Direction.CLOCKWISE)

        self.vroumBase = DriveBase(motorGauche, motorDroite, 55.5, 104)
        self.vroumBase.reset()

        self.ultrasonic = UltrasonicSensor(Port.S2)
        self.color = ColorSensor(Port.S3)

        # Touches appuyées
        self.up = False
        self.left = False
        self.right = False
        self.down = False
        self.space = False

        # Manettes appuyés
        self.rightTrigger = False
        self.leftTrigger = False
        self.xLeft = False
        self.xRight = False

        self.levage = False

    def drive(self, speed, angle):
        self.vroumBase.drive(speed, angle)

    def get_datas(self):
        return self.ultrasonic.distance(), self.color.ambient() / 10, self.vroumBase.distance()

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
        boost = 200 * self.robot.space
        vitesse = (300 + boost) * self.robot.up - (300 + boost) * self.robot.down
        angle = 60 * self.robot.right - 60 * self.robot.left
        vitesse += 1 if angle != 0 and vitesse == 0 else 0

        print("u")

        self.robot.drive(vitesse, angle)

    def controller_handling(self):
        vitesse = 300 * self.robot.rightTrigger - 300 * self.robot.leftTrigger
        angle = 60 * self.robot.xRight - 60 * self.robot.xLeft
        vitesse += 1 if angle != 0 and vitesse == 0 else 0

        self.robot.drive(vitesse, angle)

    def barre_handling(self):
        # self.robot.barre.run_until_stalled(-500 + 1000 * self.robot.levage)
        pass

    def send_datas(self, client):
        while True:
            time.sleep(0.5)
            datas = robot.get_datas()
            datas = str(datas)
            datas, cle = xor.chiffrement(datas)
            datas += cle
            client.send(datas.encode())

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
            requetestr = str(requete.decode())
            length = len(requetestr)
            message, cle = requetestr[:length//2], requetestr[length//2:]
            requetestr, cle = xor.chiffrement(message, cle)
            print("Réception de " + requetestr)

            if requetestr[0] == "K":
                cmd = requetestr[2:]

                self.robot.up = True if cmd == "avancer" else False if cmd == "stop_avancer" else self.robot.up
                self.robot.left = True if cmd == "gauche" else False if cmd == "stop_gauche" else self.robot.left
                self.robot.right = True if cmd == "droite" else False if cmd == "stop_droite" else self.robot.right
                self.robot.down = True if cmd == "reculer" else False if cmd == "stop_reculer" else self.robot.down
                self.robot.space = True if cmd == "espace" else False if cmd == "stop_espace" else self.robot.space

                if cmd == "barre":
                    self.robot.levage = not self.robot.levage
                    self.barre_handling()

                self.keyboard_handling()

            elif requetestr[0] == "C":
                print("douleur")
                cmd = requetestr[2:]

                self.robot.rightTrigger = True if cmd == "avancer" else False if cmd == "stop_avancer" else self.robot.rightTrigger
                self.robot.xLeft = True if cmd == "gauche" else False if cmd == "stop_tourner" else self.robot.xLeft
                self.robot.xRight = True if cmd == "droite" else False if cmd == "stop_tourner" else self.robot.xRight
                self.robot.leftTrigger = True if cmd == "reculer" else False if cmd == "stop_reculer" else self.robot.leftTrigger

                if cmd == "barre":
                    self.robot.levage = not self.robot.levage
                    self.barre_handling()

                self.controller_handling()

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
