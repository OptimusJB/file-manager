from Screen import resize_screen
import pygame
import PCthings
import data
pygame.init()

class StorageListView:
    def __init__(self):
        self.dimensions_rect = pygame.rect.Rect(10, 10, 500, 950)
        self.police = pygame.font.Font("assets/police.otf", 40)
        self.rects_stockages = []

        # éléments scroll
        self.y = 0
        self.y_offset = 0

        # boutons
        self.new_stockage = self.create_button("nouveau stockage", "grey20")
        self.new_stockage[1].midtop = (self.dimensions_rect.centerx, 950 + 10 + 20)


    def create_button(self, texte, color="grey15"):
        texte_bouton = self.police.render(texte, True, "white")
        texte_bouton_rect = texte_bouton.get_rect()
        texte_bouton_rect.width += 20
        texte_bouton_rect.height += 20

        image_bouton = pygame.surface.Surface(texte_bouton_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(image_bouton, color, texte_bouton_rect, border_radius=20)
        image_bouton.blit(texte_bouton, (texte_bouton_rect.x + 10, texte_bouton_rect.y + 10))

        return (image_bouton, texte_bouton_rect)

    def blit(self):
        # blit du fond
        resize_screen.draw_rect("grey20", self.dimensions_rect, 50)

        # blit du fond du titre
        surface = pygame.Surface((self.dimensions_rect.size[0] + 10, 100), pygame.SRCALPHA)
        pygame.draw.rect(surface, "grey15", self.dimensions_rect, border_radius=50)
        resize_screen.blit(surface, (0, 0))

        # blit du titre
        titre = self.police.render("stockages actifs", True, "white")
        titre_rect = titre.get_rect()
        titre_rect.center = (self.dimensions_rect.centerx, 60)
        resize_screen.blit(titre, titre_rect.topleft)

        # blit des stockages
        self.rects_stockages = []
        self.y = 130
        for stockage in data.stockages:
            texte_stockage = stockage
            if len(texte_stockage) > 18:
                texte_stockage = texte_stockage[:18] + "..."

            bouton_stockage = self.create_button(texte_stockage)
            bouton_stockage[1].midtop = (self.dimensions_rect.centerx, self.y + self.y_offset)
            resize_screen.blit(bouton_stockage[0], bouton_stockage[1].topleft)
            self.rects_stockages.append(bouton_stockage[1])
            self.y = self.y + 100


        # blit du cache en bas
        resize_screen.draw_rect("grey10", pygame.rect.Rect(10, 950 + 10, 500, 1080- (950 + 10)))

        # blit du bouton nouveau stockage
        resize_screen.blit(self.new_stockage[0], self.new_stockage[1].topleft)

    def listen_entry(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.new_stockage[1].collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                    chemin_dossier = PCthings.ask_dir()
                    if chemin_dossier:
                        if not chemin_dossier in data.stockages:
                            # ajout du nouveau stockage
                            data.stockages.append(chemin_dossier)

            elif event.button == 3:
                for rect_stockage in self.rects_stockages:
                    if rect_stockage.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                        index_rect = self.rects_stockages.index(rect_stockage)
                        data.stockages.pop(index_rect)

storage_list_view = StorageListView()