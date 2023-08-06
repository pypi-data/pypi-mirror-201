import sqlite3
from contextlib import contextmanager
from sqlite3 import Error
import time
from import Files_Cdvst import *

class Database:
    """
    Eine Singleton-Klasse zum Verwalten von SQLite-Datenbanken.

    Beispiel:

    db = Database("example.db")
    db.create_table()
    db.add_entry(name="Module Name", description="Description", version="0.1", dirpath=r"F:\users\cdvst\OneDrive\Desktop\Pypi Module\ModuleName")
    entry = db.get_entry(ID=1)
    editor = db.edit_entry(ID=1).name("New Name")
    editor.update()
    db.delete_entry(1)
    db.close()
    """

    _instance = None

    def __new__(cls, db_path):
        """
        Erstellt eine neue Instanz der Klasse oder gibt eine vorhandene Instanz zurück.

        Args:
            db_path (str): Der Pfad zur Datenbankdatei.

        Returns:
            Eine Instanz der Klasse Database.

        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_path = db_path
            cls._instance.conn = None
            cls._instance.cursor = None
        return cls._instance

    def create_table(self):

        """
        Erstellt eine Tabelle in der Datenbank, wenn sie nicht bereits existiert.

        """
        with self.connect() as cursor:
            try:
                cursor.execute('CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, name TEXT, description TEXT, version TEXT, dirpath TEXT, timestamp INTEGER)')
                self.conn.commit()
            except Error as e:
                print(f"Fehler beim Erstellen der Tabelle: {e}")

    @contextmanager
    def connect(self):

        """
        Stellt eine Verbindung zur Datenbank her und gibt den Cursor zurück.

        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            yield self.cursor
        except Error as e:
            print(f"Fehler bei der Verbindung zur Datenbank: {e}")
            raise
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def validate_entry(self, name, description, version, dirpath):
        """
        Überprüft, ob die Daten für einen neuen Eintrag gültig sind.

        Args:
            name (str): Der Name des Moduls.
            description (str): Die Beschreibung des Moduls.
            version (str): Die Versionsnummer des Moduls.
            dirpath (str): Der Dateipfad zum Modul.

        Returns:
            True, wenn die Daten gültig sind, False sonst.

        """
        if not name or not description or not version or not dirpath:
            print("Ungültige Eingabe: Alle Felder müssen ausgefüllt sein.")
            return False

        # Weitere Validierungen können hier hinzugefügt werden.

        return True

    def add_entry(self, name, description, version, dirpath):
        """
        Fügt einen neuen Eintrag zur Datenbank hinzu.

        Args:
            name (str): Der Name des Moduls.
            description (str): Die Beschreibung des Moduls.
            version (str): Die Versionsnummer des Moduls.
            dirpath (str): Der Dateipfad zum Modul.

        """
        if not self.validate_entry(name, description, version, dirpath):
            return

        with self.connect() as cursor:
            try:
                cursor.execute('INSERT INTO entries (name, description, version, dirpath, timestamp) VALUES (?, ?, ?, ?, ?)', (name, description, version, dirpath, int(time.time())))
                self.conn.commit()
            except Error as e:
                print(f"Fehler beim Erstellen des Eintrags: {e}")

    def get_entry(self, *args, **kwargs):
        """
        Ruft einen Eintrag aus der Datenbank ab.

        Args:
            kwargs: Die Bedingungen für die Abfrage als Schlüsselwertpaare.

        Returns:
            Eine Liste mit den abgerufenen Einträgen.

        """
        with self.connect() as cursor:
            try:
                # create a# Liste von Bedingungen für die Abfrage
                conditions = []
                for key, value in kwargs.items():
                    conditions.append(f"{key}='{value}'")

                # Erstelle die Abfrage-Zeichenfolge
                query_string = 'SELECT * FROM entries'
                if conditions:
                    query_string += f' WHERE {" AND ".join(conditions)}'

                # Führe die Abfrage aus
                cursor.execute(query_string)
                return cursor.fetchall()
            except Error as e:
                print(f"Fehler beim Abrufen der Einträge: {e}")
                return []

    class EntryEditor:
        """
        Eine Unterklasse zum Bearbeiten von Einträgen in der Datenbank.

        Beispiel:

        editor = db.edit_entry(ID=1).name("New Name")
        editor.update()

        """

        def __init__(self, db, entry_id):
            self.db = db
            self.entry_id = entry_id
            self.updates = {}

        def __getattr__(self, attr):
            def wrapper(value):
                self.updates[attr] = value
                return self
            return wrapper

        def update(self):
            """
            Aktualisiert den Eintrag in der Datenbank mit den neuen Werten.

            """
            if not self.updates:
                return
            with self.db.connect() as cursor:
                try:
                    # create a list of update statements for the query
                    updates = []
                    for key, value in self.updates.items():
                        updates.append(f"{key}='{value}'")

                    # create the query string
                    query_string = f"UPDATE entries SET {', '.join(updates)} WHERE id={self.entry_id}"
                    # execute the query
                    cursor.execute(query_string)
                    self.db.conn.commit()
                except Error as e:
                    print(f"Fehler beim Aktualisieren des Eintrags: {e}")

    def edit_entry(self, *args, **kwargs):
        """
        Öffnet den Eintrag in der Datenbank zum Bearbeiten.

        Args:
            kwargs: Die Bedingungen zum Öffnen des Eintrags als Schlüsselwertpaare.

        Returns:
            Eine Instanz der Klasse EntryEditor zum Bearbeiten des Eintrags.

        """
        if 'ID' not in kwargs:
            print("Ungültige Eingabe: Es muss eine ID angegeben werden.")
            return

        entry_id = kwargs.pop('ID')

        if not kwargs:
            return


        editor = Database.EntryEditor(self, entry_id)
        for key, value in kwargs.items():
            setattr(editor, key, value)
        return editor

    def delete_entry(self, entry_id):
        """
        Löscht einen Eintrag aus der Datenbank.
        Args:
            entry_id (int): Die ID des zu löschenden Eintrags.

        """
        with self.connect() as cursor:
            try:
                cursor.execute('DELETE FROM entries WHERE id=?', (entry_id,))
                self.conn.commit()
            except Error as e:
                print(f"Fehler beim Löschen des Eintrags: {e}")
        print("Hello")
    def close(self):
        """
        Schließt die Verbindung zur Datenbank.

        """
        if self.conn:
            self.conn.close()



class ConfigManager:
    import json
    import os
    CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "config.json")
    DEFAULT_API_KEY = "INSERT_YOUR_API_KEY_HERE"

    @classmethod
    def load_config(cls):
        if not os.path.isfile(cls.CONFIG_FILE_PATH):
            cls.save_config(cls.DEFAULT_API_KEY)
        with open(cls.CONFIG_FILE_PATH, "r") as f:
            config = json.load(f)
        return config

    @classmethod
    def save_config(cls, api_key):
        config = {"api_key": api_key}
        with open(cls.CONFIG_FILE_PATH, "w") as f:
            json.dump(config, f)

class FavoritesManager:
    import json
    import os
    FAVORITES_FILE_PATH = os.path.join(os.path.dirname(__file__), "favorites.json")
    DEFAULT_CATEGORIES = {
        "Category 1": [
            "Prompt 1",
            "Prompt 2"
        ],
        "Category 2": [
            "Prompt 3",
            "Prompt 4"
        ]
    }

    @classmethod
    def load_favorites(cls):
        if not os.path.isfile(cls.FAVORITES_FILE_PATH):
            cls.save_favorites(cls.DEFAULT_CATEGORIES)
        with open(cls.FAVORITES_FILE_PATH, "r") as f:
            favorites = json.load(f)
        return favorites

    @classmethod
    def save_favorites(cls, favorites):
        with open(cls.FAVORITES_FILE_PATH, "w") as f:
            json.dump(favorites, f)

if __name__ == "__main__":
    # Beispiel:
    db_path = "example.db"
    db = Database(db_path)
    db.create_table()
    db.add_entry(name="Module Name", description="Description", version="0.1", dirpath=r"F:\users\cdvst\OneDrive\Desktop\Pypi Module\ModuleName")
    entry = db.get_entry(ID=1)
    print(entry)
    editor = db.edit_entry(ID=1).name("New Name")
    editor.update()
    db.delete_entry(1)
    db.close()
