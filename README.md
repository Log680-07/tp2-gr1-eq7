
# HvacController-Java

## How to use Maven to package the application
At the folder level where the pom file is located enter command : ```mvn package -f pom.xml``` 
The executable jar will be in the folder called "target" under the name ```hvac2-1.0-SNAPSHOT-jar-with-dependencies```

## To run project
In terminal: ```java -jar .\hvac2-1.0-SNAPSHOT-jar-with-dependencies.jar```


## Unit Test

### To run unit test
At the root folder: run ```mvn test -f pom.xml```

## SignalR & API
The client use SignalR to receive data and get request to activate the hvac unit
Server: https://log680.vincentboivin.ca

### SignalR
To receive continuous data from the server, we use SignalR. SignalR allow us to mimic real-time data sent to the client. https://docs.microsoft.com/en-us/aspnet/core/signalr/java-client?view=aspnetcore-5.0

To receive data from the server, start a connection with SignalR and connect to this hub: *{serverurl}/SensorHub?token={token}*.

### Endpoints
To control the Hvac, we use get Http request. The nbTicks represent for how long the AC or Heater will be activated.

- To turn off the unit : *GET {serverUrl}/api/Hvac/{token}/TurnOffHvac*
- To start the AC of the unit : *GET {serverUrl}/api/Hvac/{token}/TurnOnAc/{nbTicks}*
- To start the Heater of the unit : *GET {serverUrl}/api/Hvac/{token}/TurnOnHeater/{nbTicks}*

The server also has a Healthcheck endpoint to test if the server is running properly:
- Healtcheck : *GET {serverUrl}/api/health*

