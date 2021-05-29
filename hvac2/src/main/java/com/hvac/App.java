package com.hvac;
import java.lang.*;

public class App 
{
    public static void main(String[] args) {
        //Sensor Token
        String token = System.getenv("HVAC_TOKEN");

        //Temperature Thresholds to trigger HVAC control
        float maxTemperature = 70.0f;
        float minTemperature = 40.0f;

        //URLS
        String host = System.getenv("HVAC_HOST");
        String HubURL = "/SensorHub?token=";
        String ApiURL = "/api/Hvac/";

        //Create and start HVAC
        System.out.println("Starting HVAC");
        HVACController hvac = new HVACController(maxTemperature,minTemperature,host,HubURL,ApiURL,token);
        hvac.SetupController();
        hvac.StartController();
    }
}

