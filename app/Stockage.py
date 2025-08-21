import PCthings
class Stockage:
    def __init__(self, type, chemin=None, ip_serveur=None, port_serveur=None):
        """
        si type == serveur, chemin est le nom du serveur
        """
        assert type in ["local", "serveur"], "type invalide"

        self.type = type
        self.chemin = chemin
        self.ip_serveur = ip_serveur
        self.port_serveur = port_serveur

        self.exists = False

        self.charger()

    def charger(self):
        if self.type == "local":
            if PCthings.is_dir_exists(self.chemin):
                self.exists = True