import json


def getConf(file):
    try:
        with open(file) as cy:
            data = json.load(cy)
            return data
    except:
        print( "fichier de conf absent")
