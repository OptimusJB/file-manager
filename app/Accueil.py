import sys
from Screen import resize_screen
from StorageListView import storage_list_view
import data
from Notification import notification
import pygame
pygame.init()
class Accueil:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.working_elements = [storage_list_view, notification]   # notification doit être en dernier
        data.focused = True

    def run(self):
        # boucle logiciel
        clock = pygame.time.Clock()
        while True:
            if not data.focused:
                # économie si pas de focus
                clock.tick(10)
                for event in pygame.event.get():
                    if event.type == pygame.WINDOWFOCUSGAINED:
                        data.focused = True
                continue

            clock.tick(30)

            resize_screen.fill("grey10")
            # blit des éléments
            for element in self.working_elements:
                element.blit()

            # listen_entry des éléments
            for event in pygame.event.get():
                if event.type == pygame.WINDOWFOCUSLOST:
                    data.focused = False

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for element in self.working_elements:
                    element.listen_entry(event)

            # refresh de l'écran
            resize_screen.flip()