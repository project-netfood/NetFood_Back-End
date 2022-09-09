import netfood_bdd

#Class Error
class BddNotConfiguredError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class BddError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message



class Observer:
    def __init__(self, name, folderIn=None, folderProd=None, folderErr=None, comment=None, confBdd=None) -> None:
        self.name = name
        self._id = None # id BDD
        self.folderIn = folderIn
        self.folderProd = folderProd
        self.folderErr = folderErr
        self.comment = comment
        self.status = "created"
        self.confBdd = confBdd
    


    def start(self):
        self.status = "started"

    def stop(self):
        self.status = "stopped"

    def run(self):
        #fonction executer quand Observer est démarrer
        if self.status == "started" : 
            #code à excuter ( lancement de checkDirectory ) en attent de la modification de fonction
            pass

    def setfolder(self, folderIn=None, folderProd=None, folderErr=None):
        self.folderIn = folderIn if folderIn != None else self.folderIn
        self.folderProd = folderProd if folderProd != None else self.folderProd
        self.folderErr = folderErr if folderErr != None else self.folderErr

        # little verif
        return self

    def setConfBdd(self, confBdd):
        self.confBdd = confBdd
        return self


    

    def flushBdd(self):
        if self.confBdd == None:
            # lancer une exception
            raise BddNotConfiguredError("configuration BDD non configuré, utiliser la fonction setConfBdd pour le configurer")
        #save instance in BDD
        try:
            if self._id == None:
                slip_bdd.executeBDD(f""""INSERT INTO observer (name, FilesIN, FilesPROD, FilesERR, commentaire, status) 
                                    VALUES (`{self.name}`, `{self.folderIn}`, `{self.folderProd}`, `{self.folderErr}`, `{self.comment}`, `{self.status}`) ;""", self.confBdd) 
                # requete pour recuperer ID 
                objetFetch = slip_bdd.fetchBDD(f"""SELECT MAX(id) AS id FROM observer WHERE name = `{self.name}` ; 
                """, self.confBdd)

                self._id = objetFetch['id']
            else: 
                slip_bdd.executeBDD(f"""UPDATE observer SET name = `{self.name}`,
                                                            IN = `{self.folderIn}`,
                                                            PROD = `{self.folderProd}`,
                                                            ERR = `{self.folderErr}`,
                                                            comment = `{self.comment}`,
                                                            status = `{self.status}`
                                        WHERE id = '{self._id}';
                """, self.confBdd)
            return self
        except Exception as e:
            print("Une erreur c'est produit")
            raise BddError(f"une erreur est arriver : {str(e)}")
