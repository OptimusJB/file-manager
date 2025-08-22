import socket
debit = 2**22

class Client:
    def __init__(self, ip_serveur, port_serveur):
        self.ip_serveur = ip_serveur
        self.port_serveur = int(port_serveur)

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
        """
        note : tous les éléments de la liste sont convertis en str
        """
        assert type(liste) == list, "liste doit être une liste"
        try:
            texte_envoi = self.list_to_str(liste) + "&FINMESSAGE&"
            texte_envoi = bytes(texte_envoi, "utf-8")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip_serveur, self.port_serveur))
            self.socket.sendall(texte_envoi)

            # attente de réponse
            texte_reponse = ""

            while not "&FINMESSAGE&" in texte_reponse:
                reception = self.socket.recv(debit)
                texte_reponse = texte_reponse + str(reception, "utf-8")

            texte_reponse = texte_reponse[:len(texte_reponse) - len("&FINMESSAGE&")]
            liste_reponse = self.str_to_list(texte_reponse)
            return liste_reponse
        except:
            return "crash"