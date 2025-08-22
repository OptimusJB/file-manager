import os
import socketserver

class Requete(socketserver.BaseRequestHandler):
    def list_to_str(self, liste):
        texte = ""
        for element in liste:
            assert not "&sllist&" in element, "&sllist& interdit"
            texte = texte + str(element) + "&sllist&"
        texte = texte[:len(texte) - len("&sllist&")]
        return texte

    def str_to_list(self, texte:str):
        liste = []
        for element in texte.split("&sllist&"):
            liste.append(element)
        return liste

    def envoyer(self, liste:list):
        assert type(liste) == list, "liste doit être une liste"
        texte_envoi = self.list_to_str(liste) + "&FINMESSAGE&"
        texte_envoi = bytes(texte_envoi, "utf-8")
        self.request.sendall(texte_envoi)

    def handle(self):
        # récupération du message
        texte_message = ""
        debit = 2**30

        while not "&FINMESSAGE&" in texte_message:
            reception = self.request.recv()
            texte_message = texte_message + str(reception, "utf-8")
        texte_message = texte_message[:len(texte_message) - len("&FINMESSAGE&")]

        data = self.str_to_list(texte_message)

        if data[1] != self.server.nom_serveur:
            # pas le bon serveur
            return None

        if data[0] == "check exist":
            self.envoyer(["trouvé"])

if __name__ == '__main__':
    if not "settings.txt" in os.listdir():
        fichier = open("settings.txt", "w")
        fichier.write("""nom serveur=stockage serveur
ip=0.0.0.0
port=25565""")
        fichier.close()

    fichier = open("settings.txt", "r")
    fichier_read = fichier.read()
    fichier.close()

    settings = fichier_read.split("\n")

    ip_serveur = settings[1].split("=")[1]
    port_serveur = int(settings[2].split("=")[1])
    serveur = socketserver.TCPServer((ip_serveur, port_serveur), Requete)
    serveur.nom_serveur = settings[0].split("=")[1]
    print("serveur lancé")
    print("nom serveur : " + serveur.nom_serveur)
    print("ip : " + ip_serveur + ":" + str(port_serveur))
    serveur.serve_forever()