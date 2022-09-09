

from venv import create


class Manager():
    def __init__( self, environement ):
        self.environement = environement 
        self.listObservers = []

    def loadListObserver():
       
        liste = fetchBDD ( "db.observer.insertOne.find()({'observerData':'id','observerData':'nom', 'observerData':'IN'', 'observerData':'OK', 'observerData':'KO', 'observerData':'comment')}", , self.environement)
       
            self.listObservers.append( obs )


    def addObserver( obs ):
        executeBDD( db.observer.create(), self.environement)
        self.listObservers.append( obs )


man = Manager( confData )
man.loadListObserver()


