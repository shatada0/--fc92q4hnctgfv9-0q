package com.example.notes;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Arrays;

/** ЛР7: заметки — добавление кнопкой, удаление долгим нажатием, хранение в SharedPreferences. */
public class MainActivity extends Activity {
    private static final String KEY = "notes";

    private final ArrayList<String> notes = new ArrayList<>();
    private ArrayAdapter<String> adapter;
    private SharedPreferences prefs;
    private TextView counter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        prefs = getSharedPreferences(KEY, MODE_PRIVATE);
        String saved = prefs.getString(KEY, "");
        if (!saved.isEmpty()) {
            notes.addAll(Arrays.asList(saved.split("\n")));
        }

        EditText input = findViewById(R.id.noteInput);
        ListView list = findViewById(R.id.notesList);
        counter = findViewById(R.id.counter);
        adapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, notes);
        list.setAdapter(adapter);

        findViewById(R.id.addButton).setOnClickListener(v -> {
            String text = input.getText().toString().trim();
            if (text.isEmpty()) {
                input.setError("Введите текст заметки");
                return;
            }
            notes.add(text);
            input.setText("");
            onNotesChanged();
        });

        list.setOnItemLongClickListener((parent, view, position, id) -> {
            notes.remove(position);
            onNotesChanged();
            Toast.makeText(this, "Заметка удалена", Toast.LENGTH_SHORT).show();
            return true;
        });

        updateCounter();
    }

    private void onNotesChanged() {
        adapter.notifyDataSetChanged();
        prefs.edit().putString(KEY, String.join("\n", notes)).apply();
        updateCounter();
    }

    private void updateCounter() {
        counter.setText("Заметок: " + notes.size());
    }
}
