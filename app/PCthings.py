# regroupe tous les trucs liés au pc (du style la sélection de dossier)
import tkinter.filedialog
import os
import pygame
pygame.init()

import data
def ask_dir():
    """
    renvoie un chemin de dossier choisi par l'utilisateur
    retourne False si rien
    """
    dossier = tkinter.filedialog.askdirectory()
    if len(dossier) == 0:
        dossier = False
    #data.focused = True # le logiciel perd le focus à cause de la nouvelle fenêtre
    pygame.event.get()
    return dossier

def is_dir_exists(chemin_dossier):
    """
    retourne True si le dossier passé en paramètre existe
    """
    return os.path.isdir(chemin_dossier)

def calcul_taille(dossier):
    """
    retourne la taille en octets du dossier passé en paramètre
    """
    if dossier[len(dossier) - 1] == "/":
        dossier = dossier[:len(dossier) - 1]

    dossiers = [dossier]
    fichiers = []
    compteur = 0

    avancement = 0
    while avancement < len(dossiers):
        chemin = dossiers[avancement]
        for element in os.listdir(dossiers[avancement]):
            if os.path.isdir(chemin + "/" + element):
                dossiers.append(chemin + "/" + element)
            elif os.path.isfile(chemin + "/" + element):
                fichiers.append(chemin + "/" + element)
        avancement = avancement + 1

    for fichier in fichiers:
        compteur = compteur + os.path.getsize(fichier)

    return compteur

def octets_to_gibioctet(nb_octets:int):
    return nb_octets / (2**30)