import os

from Accueil import Accueil
from Screen import resize_screen
from Save import save
import pygame
pygame.init()

class State:
    def __init__(self):
        self.states = {"accueil": Accueil}
        self.state_actuel = "accueil"

    def run(self):
        pygame.display.set_caption("File manager")
        pygame.display.set_icon(pygame.transform.smoothscale(pygame.image.load("assets/logo.png"), (32, 32)))
        dimensions = pygame.display.get_desktop_sizes()[0]
        resize_screen.set_mode((dimensions[0] * 0.6, dimensions[1] * 0.6), pygame.RESIZABLE)

        # chargement des stockages
        if "&stockages&" in os.listdir("data"):
            save.charger_stockages()

        # boucle logiciel
        while True:
            self.states[self.state_actuel](self).run()

if __name__ == '__main__':
    State().run()