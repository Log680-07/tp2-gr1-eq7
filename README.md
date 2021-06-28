
# HvacController-Python

## How to use PipEnv to create a virtual environment
### Install required packages from requirements.txt
At root level in terminal, enter command : ```pipenv install```

Select the python interpreter of this virtual environment
### To install new package
```pipenv install <package>```

### To generate requirements.txt
```pipenv lock -r > requirements.txt```


## To run project
In terminal: ```python main.py```
The system will ask you if you want a dynamique or autoset test.
    - Choose 0, for autoset
    - Choose 1, to enter your own values for heat and cold.

## Pass arguments to container 

Up to 4 arguments can be specified: _token, nbTick, coldLimit, hotLimit_ (Note: please respect upper case characters)

 ```docker run -e nbTick=1 -e token=1234 -e coldLimit=10 -e hotLimit=30 image_name```

## Unit Test

### To run unit test
At the root folder: run ```python -m unittest discover -v```

## SignalR & API
The client use SignalR to receive data and get request to activate the hvac unit
Server: https://log680.vincentboivin.ca

### SignalR
To receive continuous data from the server, we use SignalR. SignalR allow us to mimic real-time data sent to the client. https://github.com/mandrewcito/signalrcore

To receive data from the server, start a connection with SignalR and connect to this hub: *{serverurl}/SensorHub?token={token}*.

### Endpoints
To control the Hvac, we use GET HTTP requests. The nbTicks represent for how long the AC or Heater will be activated.

- To turn off the unit : *GET {serverUrl}/api/Hvac/{token}/TurnOffHvac*
- To start the AC of the unit : *GET {serverUrl}/api/Hvac/{token}/TurnOnAc/{nbTicks}*
- To start the Heater of the unit : *GET {serverUrl}/api/Hvac/{token}/TurnOnHeater/{nbTicks}*

The server also has a Healthcheck endpoint to test if the server is running properly:
- Healtcheck : *GET {serverUrl}/api/health*

