from signalrcore.hub_connection_builder import HubConnectionBuilder
import logging
import sys
import requests
import json
import time
import os
import mysql.connector as mysql

class Main:
    def __init__(self, mytoken, nbTick, limitFroid, limitChaud):

    # test des valeurs recu en paramettre
        if nbTick <=0:
            raise Exception (" Valeur invalide pour le nombre de TICKS!")
        elif limitChaud <= limitFroid :
            raise Exception (" Temperateur chaude en dessous de celle du froid !")
    # initialisation de variables recu en paramettre
        self._hub_connection = None
        self.NBTICK = nbTick
        self.LIMITCHAUD = limitChaud
        self.LIMITFROID = limitFroid
        self.TOKEN = mytoken
    # connection a la DB
        self.mydb = mysql.connect(
            user ='tp3',
            password='Tp@3!55.',
            host ='ec2-3-237-178-114.compute-1.amazonaws.com',
            database ='tp3'
        )
        if self.mydb.cursor:
            print("Connection etablie avec la DB")
        else :
            print("connection failed")
    
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
            #- envois des données
            self.sendDataToMysql(date,dp)
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
        # envois d evenements a la DB
        self.sendEventsToMysql(date, str(details))

         
    # send temperature data  to mysql
    def sendDataToMysql(self,date, temp):
       
        query = "INSERT INTO log680_tp3(heure,temperature) " \
            "VALUES(%s,%s)"
        args = (date, temp)

        try:
            cursor = self.mydb.cursor()
            cursor.execute(query, args)
            self.mydb.commit()
        except Error as error:
            print(error)

    # send events data  to mysql
    def sendEventsToMysql(self,date, ev):
       
        query = "INSERT INTO log680_EVENS(heure,evenement) " \
            "VALUES(%s,%s)"
        args = (date, ev)

        try:
            cursor = self.mydb.cursor()
            cursor.execute(query, args)
            self.mydb.commit()
        except Error as error:
            print(error)

 #-----------------------------------------------   

if __name__ == '__main__':
    
    # valeur variables par defaut
    limitFroid = 20.0
    limitChaud = 80.0
    nbTick = 6
    token ="f0c51c904ed6dd637b2f"
    # si variable d'environnement existe, on le prend, sinon, valeur par defaut

    if "NBTICK" in os.environ:
        nbTick = int(os.environ["NBTICK"])
    
    if "TOKEN" in os.environ:
        token = os.environ["TOKEN"]
    testtype = 2
    while testtype not in [0, 1]:
         testtype = int(input ("Pour un test preconfiguré, entrer le '0', si non le '1' pour choisir limite froid et chaud : "))
    
    # test automatique avec les valeurs 20 et 80, pour les temperatures
    if(testtype==0):
        if "LIMITCHAUD" in os.environ:
            limitChaud = float(os.environ["LIMITCHAUD"])
        if "LIMITFROID" in os.environ:
            limitFroid = float(os.environ["LIMITFROID"])
    # test dynamique. Les valeurs de température dependent de ce que l'utilisateur va entrer
    elif(testtype==1):
        limitChaud= int(input("Entrer limite chaleur max de control : "))
        limitFroid= int(input("Entrer limite froid min de control : "))
    # test main sans image
    
    # exécution de l'application
    main = Main(token, nbTick, limitFroid, limitChaud)
    main.start()



