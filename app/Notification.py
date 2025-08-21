from Screen import resize_screen
import pygame
pygame.init()

class Notification:
    def __init__(self):
        self.notifs = []    # liste de tuples (texte, temps_debut)
        self.duree_notif = 3000 # en ms
        self.police = pygame.font.Font("assets/police.otf", 40)

    def add_notif(self, texte):
        self.notifs.append((texte, pygame.time.get_ticks()))

    def create_button(self, texte:str, color="grey15"):
        texte_bouton = self.police.render(texte, True, "white")
        texte_bouton_rect = texte_bouton.get_rect()
        texte_bouton_rect.width += 20
        texte_bouton_rect.height += 20

        image_bouton = pygame.surface.Surface(texte_bouton_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(image_bouton, color, texte_bouton_rect, border_radius=20)
        image_bouton.blit(texte_bouton, (texte_bouton_rect.x + 10, texte_bouton_rect.y + 10))

        return (image_bouton, texte_bouton_rect)

    def blit(self):
        y = 1000

        a_supprimer = []
        for notif in self.notifs:
            if pygame.time.get_ticks() - notif[1] > self.duree_notif:
                # suppression
                a_supprimer.append(notif)

            bouton = self.create_button(notif[0], "blue")
            bouton[1].center = (1920//2, y)
            resize_screen.blit(bouton[0], bouton[1].topleft)

            y = y - 100

        for element in a_supprimer:
            self.notifs.remove(element)

    def listen_entry(self, event):
        pass
notification = Notification()