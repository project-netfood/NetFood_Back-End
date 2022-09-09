#!/usr/bin/python3
import os, os.path

dicoCheckSyntax = {
    'html'  : '<!DOCTYPE html>',
    'sh'    : '#!/bin/bash',
    'py'    : '#!/usr/bin/python3'
    
} 

# echo '<!DOCTYPE html>' > testOK.html

def checkFile( fic ):
    #print(fic)
    ext = fic.split('.')[-1]
    f = open( fic, 'r')
    bloc = f.read()
    f.close()
    firstLine = bloc.split( '\n' )[0]
    if ext in dicoCheckSyntax.keys():
        if dicoCheckSyntax[ext] in firstLine:
            return True
    return False
