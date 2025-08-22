class Arbre:
    def __init__(self, valeur, gauche=None, droite=None):
        self.valeur = valeur
        self.gauche = gauche
        self.droite = droite
class Save:
    def __init__(self):
        pass

    def get_minimum(self, dico:dict):
        found = False
        minimum = float("inf")
        for element in dico.keys():
            if dico[element] < minimum:
                found = element
                minimum = dico[element]
        if found:
            return found
        return False

    def get_code(self, arbre, dico=None, code_actuel=""):
        if dico == None:
            dico = {}
        if type(arbre.gauche) != Arbre:
            dico[arbre.gauche] = code_actuel + "0"
        else:
            #print("a")
            self.get_code(arbre.gauche, dico, code_actuel + "0")

        if type(arbre.droite) != Arbre:
            dico[arbre.droite] = code_actuel + "1"
        else:
            #print("a")
            self.get_code(arbre.droite, dico, code_actuel + "1")

        return dico

    def creer_arbre(self, dico_occurences):
        if len(dico_occurences.keys()) == 1:
            lettre = list(dico_occurences.keys())[0]
            return (Arbre(dico_occurences[lettre], lettre), [lettre, dico_occurences[lettre]])
        # création de l'arbre
        liste_taille = []  # lettres + nombre triées selon leur nombre d'occurences (croissant)
        while len(dico_occurences) >= 2:
            new_arbre = Arbre(0)
            minimum = self.get_minimum(dico_occurences)
            new_arbre.valeur += dico_occurences[minimum]
            new_arbre.gauche = minimum

            if not type(minimum) == Arbre:
                liste_taille.append(minimum)
                liste_taille.append(dico_occurences[minimum])

            dico_occurences.pop(minimum)

            minimum = self.get_minimum(dico_occurences)
            new_arbre.valeur += dico_occurences[minimum]
            new_arbre.droite = minimum

            if not type(minimum) == Arbre:
                liste_taille.append(minimum)
                liste_taille.append(dico_occurences[minimum])

            dico_occurences.pop(minimum)

            dico_occurences[new_arbre] = new_arbre.valeur

        arbre_code = list(dico_occurences.keys())[0]  # dico_occurences.keys() = 1 seul élément

        return (arbre_code, liste_taille)

    def chiffrer(self, texte:str):
        #assert "&slchaine&" in texte or "&slcaract&" in texte, "texte interdit"
        if texte == "":
            return ""

        dico_occurences = {}
        for element in texte:
            if not element in dico_occurences.keys():
                dico_occurences[element] = texte.count(element)

        creation_arbre = self.creer_arbre(dico_occurences)
        arbre_code = creation_arbre[0]
        liste_taille = creation_arbre[1]

        # création du dico lettre/code
        codes = self.get_code(arbre_code)

        # création du texte final
        texte_final = ""
        for element in liste_taille:
            texte_final = texte_final + str(element) + "&slcaract&"
        texte_final = texte_final[:len(texte_final) - len("&slcaract&")]

        texte_final = texte_final + "&slchaine&"

        for element in texte:
            texte_final = texte_final + codes[element]

        return texte_final

    def dechiffrer(self, texte:str):
        if texte == "":
            return ""

        parties = texte.split("&slchaine&")
        occurences = parties[0].split("&slcaract&")
        texte_code = parties[1]

        # création du dico d'occurences
        dico_occurences = {}
        for avancement in range(len(occurences)):
            if avancement % 2 == 0:
                dico_occurences[occurences[avancement]] = int(occurences[avancement + 1])

        creation_arbre = self.creer_arbre(dico_occurences)
        arbre_code = creation_arbre[0]

        # déchiffrement
        texte_final = ""
        curseur = arbre_code
        while len(texte_code) > 0:
            if texte_code[0] == "0":
                if type(curseur.gauche) == Arbre:
                    curseur = curseur.gauche
                else:
                    texte_final = texte_final + curseur.gauche
                    curseur = arbre_code

            elif texte_code[0] == "1":
                if type(curseur.droite) == Arbre:
                    curseur = curseur.droite
                else:
                    texte_final = texte_final + curseur.droite
                    curseur = arbre_code
            else:
                assert False, "problème, pas égal à '0' ou '1'"
            texte_code = texte_code[1:]
        return texte_final

    def sauvegarder_stockages(self):
        import data

        texte = ""
        for stockage in data.stockages:
            # test s'il y a des mots interdits
            for element in [stockage.chemin, stockage.ip_serveur, stockage.port_serveur]:
                assert not "&slattr&" in str(element), "&slattr& est interdit"
                assert not "&slstockage&" in str(element), "&slstockage& est interdit"

            texte = texte + str(stockage.type) + "&slattr&" + str(stockage.chemin) + "&slattr&" + str(stockage.ip_serveur) + "&slattr&" + str(stockage.port_serveur) + "&slstockage&"
        texte = texte[:len(texte) - len("&slstockage&")]
        texte = self.chiffrer(texte)
        fichier = open("data/&stockages&", "w") # &stockages& doit être un nom de fichier interdit
        fichier.write(texte)
        fichier.close()

    def charger_stockages(self):
        import data
        from Stockage import Stockage
        data.stockages = []

        fichier = open("data/&stockages&", "r")
        fichier_read = fichier.read()
        fichier.close()
        fichier_read = self.dechiffrer(fichier_read)

        if fichier_read == "":
            return None

        for stockage in fichier_read.split("&slstockage&"):
            stockages_specs = stockage.split("&slattr&")

            for avancement in range(len(stockages_specs)):
                if stockages_specs[avancement] == "None":
                    stockages_specs[avancement] = None

            new_stockage = Stockage(stockages_specs[0], stockages_specs[1], stockages_specs[2], stockages_specs[3])
            data.stockages.append(new_stockage)

save = Save()