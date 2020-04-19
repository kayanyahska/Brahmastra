package com.example.myapplication;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void showLocationv(View view){
        Intent intent = new Intent(this, ShowLocationvActivity.class);
        startActivity(intent);
    }

    public void showLocation(View view){
        Intent intent = new Intent(this, ShowLocationActivity.class);
        startActivity(intent);
    }
}
