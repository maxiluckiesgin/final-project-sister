package com.example.andremonzigo.weathermonitor;

import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.StringTokenizer;

public class Monitor extends AppCompatActivity {

    private String TAG = MainActivity.class.getSimpleName();
    private ListView lv;

    ArrayList<HashMap<String, String>> temperatureHumidity;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_monitor);

        temperatureHumidity = new ArrayList<>();
        lv = (ListView) findViewById(R.id.list);

        new GetNode().execute();
    }

    private class GetNode extends AsyncTask<Void, Void, Void> {
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            Toast.makeText(Monitor.this, "Loading...", Toast.LENGTH_LONG).show();

        }


        protected Void doInBackground(Void... arg0) {
            HttpHandler sh = new HttpHandler();
            // Making a request to url and getting response
            String url = "http://192.168.43.53:5566/node";
            String jsonStr = sh.makeServiceCall(url);

            Log.e(TAG, "Response from url: " + jsonStr);
            if (jsonStr != null) {
                try {
                    JSONObject jsonObj = new JSONObject(jsonStr);

                    // Getting JSON Array node
                    JSONArray node = jsonObj.getJSONArray("node");
                    //JSONArray node = new JSONArray(jsonStr);

                    // looping through All Node
                    for (int i = 0; i < node.length(); i++) {
                        JSONObject c = node.getJSONObject(i);
                        String kelembaban_max = c.getString("kelembaban_max");
                        String wilayah = c.getString("wilayah");
                        String kelembaban_avg = c.getString("kelembaban_avg");
                        String suhu_avg = c.getString("suhu_avg");
                        String suhu_max = c.getString("suhu_max");

                        // tmp hash map for single contact
                        HashMap<String, String> thisnode = new HashMap<>();

                        // adding each child node to HashMap key => value
                        thisnode.put("kelembaban_max", kelembaban_max);
                        thisnode.put("wilayah", wilayah);
                        thisnode.put("kelembaban_avg", kelembaban_avg);
                        thisnode.put("suhu_avg", suhu_avg);
                        thisnode.put("suhu_max", suhu_max);

                        // adding contact to contact list
                        temperatureHumidity.add(thisnode);
                    }
                } catch (final JSONException e) {
                    Log.e(TAG, "Json parsing error: " + e.getMessage());
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(getApplicationContext(),
                                    "Json parsing error: " + e.getMessage(),
                                    Toast.LENGTH_LONG).show();
                        }
                    });

                }

            } else {
                Log.e(TAG, "Couldn't get json from server.");
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(getApplicationContext(),
                                "Couldn't get json from server. Check LogCat for possible errors!",
                                Toast.LENGTH_LONG).show();
                    }
                });
            }

            return null;
        }
        @Override
        protected void onPostExecute(Void result) {
            super.onPostExecute(result);

            ListAdapter adapter = new SimpleAdapter(
                    Monitor.this, temperatureHumidity,
                    R.layout.list_item, new String[]{ "wilayah","kelembaban_avg","kelembaban_max","suhu_avg","suhu_max"},
                    new int[]{R.id.wilayah, R.id.kelembaban_avg, R.id.kelembaban_max, R.id.suhu_avg, R.id.suhu_max});
            lv.setAdapter(adapter);
        }
    }
}
