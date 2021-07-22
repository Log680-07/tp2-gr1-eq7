
from signalrcore.hub_connection_builder import HubConnectionBuilder
from dotenv import load_dotenv
import logging
import sys
import requests
import json
import time
import os
import mysql.connector as mysql


class Main:
    def __init__(self, mytoken, nbTick, limitFroid, limitChaud, user, password, host, database):

    # test des valeurs recu en paramettre
        if nbTick <= 0:
            raise Exception (" Valeur invalide pour le nombre de TICKS!")
        elif limitChaud <= limitFroid :
            raise Exception (" Temperateur chaude en dessous de celle du froid !")
    # initialisation de variables recu en paramettre
        self._hub_connection = None
        self.NBTICK = nbTick
        self.LIMITCHAUD = limitChaud
        self.LIMITFROID = limitFroid
        self.TOKEN = mytoken
        self.USER = user
        self.PASSWORD = password
        self.HOST = host
        self.DATABASE = database
    # connection to the DB
        self.mydb = mysql.connect(
            user = user,
            password = password,
            host = host,
            database = database
        )
        if self.mydb.cursor:
            print("Connection etablie avec la DB")
        else :
            print("connection failed")
    #--------------    
    def __del__(self):
        if (self._hub_connection != None):
            self._hub_connection.stop()

    def setup(self):
        self.setSensorHub()        

    def start(self):
        self.setup()
        self._hub_connection.start() 

        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

        self._hub_connection.stop()
        sys.exit(0)


    def setSensorHub(self):
        self._hub_connection = HubConnectionBuilder()\
        .with_url(f"https://log680.vincentboivin.ca/SensorHub?token={self.TOKEN}")\
        .configure_logging(logging.INFO)\
        .with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
            "max_attempts": 999
        }).build()

        self._hub_connection.on("ReceiveSensorData", self.onSensorDataReceived)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(lambda data: print(f"||| An exception was thrown closed: {data.error}"))

    def onSensorDataReceived(self, data):
        try:        
            print(data[0]["date"]  + " --> " + data[0]["data"])
            date = data[0]["date"]
            dp = float(data[0]["data"])
            
            #- envois des données( on envoi la temperateur dp et la date de l evenement)
            self.sendDataToMysql(date,dp)

            # analyse de la temperature par le systeme.
            self.analyzeDatapoint(date, dp)
        except Exception as err:
            print(err)
    
    def analyzeDatapoint(self, date, data):
        if (data >= self.LIMITCHAUD):                
            self.sendActionToHvac(date, "TurnOnAc", self.NBTICK)
        elif (data <= self.LIMITFROID):                
            self.sendActionToHvac(date, "TurnOnHeater", self.NBTICK)

    def sendActionToHvac(self, date, action, nbTick):
        
        r = requests.get(f"https://log680.vincentboivin.ca/api/hvac/{self.TOKEN}/{action}/{nbTick}") 
        details = json.loads(r.text)
        print(details)

        # envoi des evenements vers la table log680_EVENS
        self.sendEventsToMysql(date, str(details))

            
    # send temperature data  to mysql
    def sendDataToMysql(self,date, temp):
       
        self._extracted_from_sendEventsToMysql_3(
            "INSERT INTO log680_tp3(heure,temperature) VALUES(%s,%s)",
            date,
            temp,
        )

    # send events data  to mysql
    def sendEventsToMysql(self,date, ev):
       
        self._extracted_from_sendEventsToMysql_3(
            "INSERT INTO log680_EVENS(heure,evenement) VALUES(%s,%s)", date, ev
        )

    def _extracted_from_sendEventsToMysql_3(self, arg0, date, arg2):
        query = arg0
        args = date, arg2
        try:
            self._extracted_from_sendEventsToMysql_8(query, args)
        except Error as error:
            print(error)

    def _extracted_from_sendEventsToMysql_8(self, query, args):
        cursor = self.mydb.cursor()
        cursor.execute(query, args)
        self.mydb.commit()

 #-----------------------------------------------   


if __name__ == '__main__':
    # print(load_dotenv())

    if load_dotenv() is True:
        # print("ici")
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        host = os.getenv("HOST")
        database = os.getenv("DATABASE")
        nbTick = int(os.getenv("NBTICK"))
        token = os.getenv("TOKEN")
        limitChaud = int(os.getenv("LIMITCHAUD"))
        limitFroid = int(os.getenv("LIMITFROID"))
    else: # valeur variables par defaut
        limitFroid = 20.0
        limitChaud = 80.0
        nbTick = 7

    # exécution de l'application
    main = Main(token, nbTick, limitFroid, limitChaud, user, password, host, database)
    main.start()