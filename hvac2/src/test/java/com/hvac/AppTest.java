package com.hvac;
import com.microsoft.signalr.HubConnectionState;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

/**
 * Unit test for simple App.
 */
public class AppTest 
{
    @Test
    public void getMaxTemperature() {
        HVACController hvac = new HVACController(100.0f,0.0f,"testhost","testurl","testAPI","testtoken");
        assertEquals(100.0f, hvac.getMaxTemperature(),0.01f );
    }
}
