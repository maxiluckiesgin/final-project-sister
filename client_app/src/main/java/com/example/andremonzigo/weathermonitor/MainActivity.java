package com.example.andremonzigo.weathermonitor;

import android.app.ActionBar;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    private static Button buttonMonitor;
    private static Button buttonAbout;
    private static Button buttonCredit;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        onClickButtonListenerMonitor();
        onClickButtonListenerAbout();
        onClickButtonListenerCredit();
    }

    public void onClickButtonListenerMonitor() {
        buttonMonitor = (Button)findViewById(R.id.btnMonitor);
        buttonMonitor.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View v) {
                        Intent intentMonitor = new Intent("com.example.andremonzigo.weathermonitor.Monitor");
                        startActivity(intentMonitor);
                    }
                }
        );
    }

    public void onClickButtonListenerAbout() {
        buttonAbout = (Button)findViewById(R.id.btnAbout);
        buttonAbout.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View v) {
                        Intent intentAbout = new Intent("com.example.andremonzigo.weathermonitor.About");
                        startActivity(intentAbout);
                    }
                }
        );
    }

    public void onClickButtonListenerCredit() {
        buttonCredit = (Button)findViewById(R.id.btnCredit);
        buttonCredit.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View v) {
                        Intent intentCredit = new Intent("com.example.andremonzigo.weathermonitor.Credit");
                        startActivity(intentCredit);
                    }
                }
        );
    }
}
