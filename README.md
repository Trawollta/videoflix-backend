## Installation
Kurze Beschreibung mit Hinweis auf Git Frontend


1. Klone das Repository:
    ```sh
    git clone <https://github.com/Trawollta/videoflix-backend>
    cd videoflix_app
    ```

2. Erstelle und aktiviere eine virtuelle Umgebung:
    ```sh
    #Erstellen des virtuellen environments für MacOS/ Linux
    python3 -m venv env

    #Aktivierung des virtuellen environments für Windows
     source env/scripts/activate

    #Aktivierung des virtuellen environments für MacOS/ Linux
    source env/bin/activate
    ```

3. Installiere die Abhängigkeiten:
    ```sh
    pip install -r requirements.txt
    ```

4. Benenne die Datei `.env model` im Verzeichnis `videoflix_app in `.env` um.
    Ändere die `.env` und füge deine Daten hinzu:
    ```env
    EMAIL_HOST=<dein-email-host>
    EMAIL_PORT=<dein-email-port>
    EMAIL_USE_TLS=<true/false>
    EMAIL_USE_SSL=<true/false>
    EMAIL_HOST_USER=<dein-email-benutzer>
    EMAIL_HOST_PASSWORD=<dein-email-passwort>
    DEFAULT_FROM_EMAIL=<deine-standard-email>
    DOMAIN=<deine-domain>
    DOMAIN_FRONTEND=<deine-frontend-domain>
    ```

5. Führe die Migrationen aus:
    ```sh
    python manage.py migrate
    ```

6. Starte den Entwicklungsserver:
    ```sh
    python manage.py runserver
    ```


7. Starte den RQ Worker

``Für Unix-basierte Systeme (Linux/MacOS)
rqworker

``Für Windows (mit gevent)
rqworker --with-gevent


## Tests

Um die Tests auszuführen, verwende den folgenden Befehl:
```sh
python manage.py test