import netfood_bdd

class Observer():
    def __init__( self, nom_plat,nom_client,numero_commande, IN, OK, KO, comment ):
        self.nom_plat = nom_plat
        self.nom_client = nom_client
        self.numero_commande = numero_commande
        self.IN = IN 
        self.OK = OK 
        self.KO = KO 
        self.comment = comment 
        self.status = 'S'

    def start():
        self.status = 'R'

    def stop():
        self.status = 'S'
    
    def isActiv():
        return (self.status == 'R')

    def create():
        return "INSERT INTO observer ( nom, IN, OK, KO, comment, status ) VALUES (nom_plat='"+self.nom_plat+"', '"+self.nom+"', '"+self.IN+"', '"+self.OK+"', '"+self.KO+"', '"+self.comment+"', '"+self.status+"');" 

    def read():

    def update():
        return "UPDATE observer SET ( nom_plat='"+self.nom_plat+"', IN='"+self.IN+"', OK='"+self.OK+"', KO='"+self.KO+"', comment='"+self.comment+"', status='"+self.status+"' WHERE id="+self.idObs+" );" 

