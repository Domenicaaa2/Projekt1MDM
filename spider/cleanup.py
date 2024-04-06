# python cleanup.py

import jsonlines
import os

def remove_duplicates_based_on_title(file_path):
    unique_titles = set()
    unique_entries = []

    with jsonlines.open(file_path) as reader:
        for entry in reader:
            title = entry.get('title', '')
            if title not in unique_titles:
                unique_titles.add(title)
                unique_entries.append(entry)

    with jsonlines.open(file_path, mode='w') as writer:
        for entry in unique_entries:
            writer.write(entry)

# Pfad zum aktuellen Arbeitsverzeichnis, in dem das Skript ausgeführt wird
current_directory = os.path.dirname(__file__)

# Pfad zur Datei, die gereinigt werden soll
file_path = os.path.join(current_directory, 'file.jl')

# Aufruf der Funktion, um Duplikate basierend auf dem Titel zu entfernen
remove_duplicates_based_on_title(file_path)
