package com.hvac;
import com.microsoft.signalr.Action1;
import com.microsoft.signalr.HubConnection;
import com.microsoft.signalr.HubConnectionBuilder;
import com.microsoft.signalr.OnClosedCallback;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.URI ;
import java.net.http.HttpResponse;
import java.util.concurrent.TimeUnit;

public class HVACController {

    //Temperature Thresholds to trigger HVAC control
    private float maxTemperature;
    private float minTemperature;

    //URLS
    private String host;
    private String HubURL;
    private String ApiURL;

    //Sensor Token
    private String token;

    //Hub Connection
    private HubConnection hubConnection;

    public HVACController(float maxTemperature, float minTemperature, String host, String hubURL, String apiURL, String token) {
        this.maxTemperature = maxTemperature;
        this.minTemperature = minTemperature;
        this.host = host;
        this.HubURL = hubURL;
        this.ApiURL = apiURL;
        this.token = token;
    }

    public void SetupController() {
        //Build Connection to Hub
        this.hubConnection = HubConnectionBuilder
                .create(getHost() + getHubURL() + getToken())
                .build();

        //Temperature Handler
        this.hubConnection.on("ReceiveSensorData", SensorDataCallback(), SensorData.class);

        this.hubConnection.onClosed((Exception exception) -> {
            try {
                TimeUnit.SECONDS.sleep(2);
                this.hubConnection.start();
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        });
    }

    public void StartController(){
        //Connect to Sensors
        this.hubConnection.start();
    }

    private Action1<SensorData> SensorDataCallback() {
        return (SensorData message) -> {
            if (message.data > getMaxTemperature())
            {
                System.out.println("Requesting AC");
                ControlHVAC("/TurnOnAc/2");
            }
            else if (message.data < getMinTemperature())
            {
                System.out.println("Requesting Heater");
                ControlHVAC("/TurnOnHeater/2");
            }
        };
    }

    private void ControlHVAC(String path) {
        //Build HTTP GET request
        String url = getHost() + getApiURL() + getToken() + path;
        HttpRequest request = HttpRequest.newBuilder(
                URI.create(url))
                .setHeader("User-Agent", "HVAC Controller")
                .build();
        try {
            //Execute HTTP request
            HttpClient client = HttpClient.newHttpClient();
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            System.out.println(response.body());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public float getMaxTemperature() {
        return maxTemperature;
    }

    public float getMinTemperature() {
        return minTemperature;
    }

    public String getHost() {
        return host;
    }

    public String getHubURL() {
        return HubURL;
    }

    public String getApiURL() {
        return ApiURL;
    }

    public String getToken() {
        return token;
    }

    public HubConnection getConnection() {return this.hubConnection; }

    public void setMaxTemperature(float maxTemperature) {
        this.maxTemperature = maxTemperature;
    }

    public void setMinTemperature(float minTemperature) {
        this.minTemperature = minTemperature;
    }

    public void setHost(String host) {
        this.host = host;
    }

    public void setHubURL(String hubURL) {
        HubURL = hubURL;
    }

    public void setApiURL(String apiURL) {
        ApiURL = apiURL;
    }

    public void setToken(String token) {
        this.token = token;
    }
}
