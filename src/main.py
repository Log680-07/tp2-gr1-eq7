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


        if nbTick <=0:
            raise Exception (" Temperature en dessous de Zero")
        elif limitChaud <= limitFroid :
            raise Exception (" Temperateur au desus de la chaleur max")

        self._hub_connection = None
        self.NBTICK = nbTick
        self.LIMITCHAUD = limitChaud
        self.LIMITFROID = limitFroid
        self.TOKEN = mytoken
    
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
        .with_url(f"https://log680.vincentboivin.ca/sensor/SensorHub?token={self.TOKEN}")\
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

            self.analyzeDatapoint(date, dp)
        except Exception as err:
            print(err)
    
    def analyzeDatapoint(self, date, data):
        if (data <= self.LIMITFROID):                
            self.sendActionToHvac(date, "TurnOnHeater", self.NBTICK)
        elif (data >= self.LIMITCHAUD):                
            self.sendActionToHvac(date, "TurnOnAc", self.NBTICK)
        

    def sendActionToHvac(self, date, action, nbTick):
        
        r = requests.get(f"https://log680.vincentboivin.ca/sensor/api/hvac/{self.TOKEN}/{action}/{nbTick}") 
        details = json.loads(r.text)
        print(details)

if __name__ == '__main__':

    limitFroid = 20.0
    limitChaud = 80.0
    nbTick = 7
    mytoken = "f0c51c904ed6dd637b2f"

    
    if "NBTICK" in os.environ:
        nbTick = int(os.environ["NBTICK"])
    if "LIMITCHAUD" in os.environ:
        limitChaud = float(os.environ["LIMITCHAUD"])
    if "LIMITFROID" in os.environ:
        limitFroid = float(os.environ["LIMITFROID"])
    if "TOKEN" in os.environ:
        token = os.environ["TOKEN"]

    main = Main(mytoken, nbTick, limitFroid, limitChaud)
    main.start()



