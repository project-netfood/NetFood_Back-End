#!/usr/bin/python3

from distutils.command.bdist_dumb import bdist_dumb
from math import prod
import os, os.path, time
from datetime import datetime
from threading import Timer, Thread

from netfood_bdd import fetchBDD, executeBDD
from netfood_config import getConf
from netfood_checkFile import checkFile
from netfood_files import move_file
from netfood_logging import log_info


class ThreadCheckDirectory(Thread):
    # overide of the function parent
    def run(self):
        log_info("starting ThreadCheckDirectory")
        while True:
            checkDirectory()
            time.sleep(1)



confData = getConf('config.json')

if not (os.path.exists(confData['filesIN']) and os.path.exists(confData['filesERR']) and os.path.exists(confData['filesPROD'])):
    print('dossier "filesIN","filesERR" ou "filesPROD manquand. Arrêt de l\'API')
    exit()

#fonction pour recup date et heure de la modif
def get_creation_date(file):
    stat = os.stat(file)
    try:
        return stat.st_birthtime
    except AttributeError:
        return stat.st_mtime


######################################
# lecture répertoire

def checkDirectory( ):
    listFiles = os.listdir( confData[ 'filesIN']  )
    #print( listFiles )
    for fic in listFiles:
        ext = fic.split('.')[-1]
        fic = confData[ 'filesIN'] + "/" + fic

        #print( fic )
        if os.path.isfile( fic ):
            res = fetchBDD ("db.orders.find().count( {  $name: '{fic}' +';'  } ))", confData )
            #print( res )
            if ( res[0]['cnt'] == 0 ):
                if checkFile( fic ):
                    executeBDD ( "db.files.insertOne ({'name' : '{fic}','status':'ok'})" , confData )                    
                    move_file(fic,confData[ 'filesPROD'])
                else:
                    executeBDD ( "db.files.insertOne ({'name' : '{fic}','status':'ok', 'type' : {ext}})" , confData )
                    move_file(fic,confData[ 'filesERR'])


if __name__ == "__main__" : 

    confData = getConf('config.json')
    print( "je lance le fichier" )

    #lance la fonction cheackFile en THREAD
