# regroupe tous les trucs liés au pc (du style la sélection de dossier)
import tkinter.filedialog
import pygame

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