#!/usr/bin/python3
# coding: utf-8

from cmath import log
import socket
import platform

from datetime import datetime
from threading import Timer

import argparse
import slip_logging
import mysql.connector  # pip install mysql-connector-python

import flask
from flask import render_template, render_template_string, request
from flask_cors import CORS, cross_origin
import json
from os.path import exists

from slip_config import getConf
from slip_bdd import fetchBDD, executeBDD, jsonSerializeDateTime, checkBDD, getBDDState
from slip_checkDirectory import checkDirectory, ThreadCheckDirectory
from slip_checkFile import checkFile
from slip_logging import log_debug, log_error, log_getAll, log_info, log_fatal, log_warning, log_setConfig


dem = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--config-file',
                    default='config.json',
                    dest='config',
                    help='Load specified config file',
                    type=str)

parser.add_argument('-H', '--host',
                    default='0.0.0.0',
                    dest='host',
                    help='Bind API to specified host',
                    type=str)

parser.add_argument('-P', '--port',
                    default=8888,
                    dest='port',
                    help='Bind API to specified port',
                    type=int)

parser.add_argument('-l', '--log-level',
                    dest='logLevel',
                    help='Select log level',
                    type=int)

parser.add_argument('-L', '--log-file',
                    dest='logFile',
                    help='Specify log file',
                    type=str)

args = parser.parse_args()

# Loading conf datas
confData = getConf(args.config)

# Put data from arguments into conf
if args.port != 8888:
    confData['port'] = args.port

if args.logLevel is not None:
    confData['logLevel'] = args.logLevel

if args.logFile is not None:
    confData['logFile'] = args.logFile

log_setConfig(confData)
checkBDD(confData)

#if getBDDState():


threadCheck = ThreadCheckDirectory()
threadCheck.start()

log_info("S.L.I.P. Starting")

# Create flask instance
app = flask.Flask(__name__)
cors = CORS(app)
app.config['DEBUG'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/getLog', methods=['GET'])
@cross_origin()
def getLog():
    slip_logging.log_debug("API Call /getLog")
    ret = {}
    try:
        ret['log'] = log_getAll()
    except Exception as e:
        log_fatal(str(e))
    return flask.Response(json.dumps(ret, default=jsonSerializeDateTime), mimetype='application/json')


@app.route('/getFilesErr', methods=['GET'])
@cross_origin()
def getFilesErr():

    resp = fetchBDD("select * from files where files.status = 'KO' AND not del  ORDER BY date DESC;", confData)
    return flask.Response(json.dumps(resp, default=jsonSerializeDateTime), mimetype='application/json')


@app.route('/getFilesProd', methods=['GET'])
@cross_origin()
def getFilesProd():
    request_prod = {}
    request_prod = fetchBDD( "SELECT * from files where status = 'ok' and not del  ORDER BY date DESC;", confData)
    return flask.Response(json.dumps(request_prod, default=jsonSerializeDateTime), mimetype='application/json')


@app.route('/getFilesDel', methods=['GET'])
@cross_origin()
def getFilesDel():
    request_prod = {}
    request_prod = fetchBDD(
        "SELECT * from files where del  ORDER BY date DESC;", confData)
    return flask.Response(json.dumps(request_prod, default=jsonSerializeDateTime), mimetype='application/json')


@app.route('/getFilesIn', methods=['GET'])
@cross_origin()
def getFilesIn():
    tab = fetchBDD(
        "select * from files where not del  ORDER BY date DESC;", confData)
    return flask.Response(json.dumps(tab, default=jsonSerializeDateTime), mimetype='application/json')


@app.route('/getFilesDone', methods=['GET'])
@cross_origin()
def getFilesDone():
    request_prod = fetchBDD( "SELECT * from files where files.status = 'ok' OR files.status = 'KO' and not del  ORDER BY date DESC;", confData)
    return flask.Response(json.dumps(request_prod, default=jsonSerializeDateTime), mimetype='application/json')

@app.route('/filesStat', methods=['GET'])
@cross_origin()
def getFilesStat():
    dic = []
    request_stat = fetchBDD("SELECT status, COUNT(status) AS nb_status  FROM files WHERE date_format(modifDate,'%Y-%m-%d') = curdate()GROUP BY status;", confData)
    request_del = fetchBDD( "SELECT del, COUNT(del) AS nb_deleted FROM files WHERE date_format(modifDate,'%Y-%m-%d') = curdate() group by del;", confData)
    request_all = fetchBDD("SELECT COUNT(name) AS nb_today  FROM files WHERE date_format(modifDate,'%Y-%m-%d') = curdate();", confData)
    """ dic = request_stat + request_del + request_all """
    dic = request_all + request_stat + request_del 
    return flask.Response(json.dumps(dic, default=jsonSerializeDateTime), mimetype='application/json')




"""
        DEBUT Fonctionnalité qui supprime une occurence dans tableau
"""


@app.route('/DelFilesIn/<id>')
@ cross_origin()
def DelFilesIn(id):
    #print('>>>>', id)
    executeBDD( "UPDATE SLIP.files SET del = 1, `deleteDate` = now() WHERE (`id` = " + id + ");", confData)
    return json.dumps(id)


"""
        DEBUT Fonctionnalité qui restaure une occurence dans tableau
"""

@app.route('/RestoreFilesIn/<id>')
@ cross_origin()
def RestoreFilesIn(id):
    #print('>>>>', id)
    executeBDD( "UPDATE SLIP.files SET del = 0, `deleteDate` = NULL WHERE (`id` = " + id + ");", confData)
    return json.dumps(id)



@ app.route('/getInfo', methods=['GET'])
def home():
    now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    dico = {}
    dico['date'] = str(now)
    return json.dumps(dico)


@ app.route('/machine', methods=['GET'])
def host():
    info = {}
    info['hostname'] = socket.gethostname()
    return json.dumps(info)


""" FIN fonction GetInfo qui retourne les infos de la machine
(exemple ; l'heure de la machine, nom de machine...)"""

# Test si la BDD est connecté ou non


@app.route('/checkBDD', methods=['GET'])
def checkBase():
    if checkBDD(confData):
        return json.dumps('OK')
    return json.dumps('KO')

@app.route('/', methods=['GET'])
def index():
        page = """
        <h2>list of API service {{name}}</h2>
        <table>
        <tr><td>/getLog</td><td>GET</td></tr>
        <tr><td>/getFilesErr</td><td>GET</td></tr>
        <tr><td>/getFilesProd</td><td>GET</td></tr>
        <tr><td>/getFilesDel</td><td>GET</td></tr>
        <tr><td>/getFilesIn</td><td>GET</td></tr>
        <tr><td>/getFilesDone</td><td>GET</td></tr>
        <tr><td>/DelFilesIn/&ltid&gt</td><td>GET</td></tr>
        <tr><td>/getInfo</td><td>GET</td></tr>
        <tr><td>/machine</td><td>GET</td></tr>
        <tr><td>/checkBDD</td><td>GET</td></tr>
        </table>
        <br>
            <h3>Path IN : {{IN}}</h3>
            <h3>Path PROD : {{PROD}}</h3>
            <h3>Path ERROR : {{ERR}}</h3>
        """
        return render_template_string( 
                page, 
                IN=confData[ 'filesIN'],
                PROD=confData[ 'filesPROD'],
                ERR=confData[ 'filesERR']
                )



try:
    app.run(host=args.host, port=confData['port'])
except ZeroDivisionError as e:  
    print( 'division moisie' )
except Exception as e:  
    print( 'erreur inkonue' )



app.run(host=args.host, port=confData['port'])
