## Installation

1. Klone das Repository:
    ```sh
    git clone <https://github.com/Trawollta/videoflix-backend>
    git clone <https://github.com/Trawollta/videoflix-frontend>
    cd videoflix
    ```

2. Erstelle und aktiviere eine virtuelle Umgebung:
    ```sh
    python -m venv env
    source env/bin/activate 
    ```
    

3. Installiere die Abhängigkeiten:
    ```sh
    pip install -r requirements.txt
    ```

4. Erstelle eine `.env`-Datei im Verzeichnis `videoflix_app` und füge die notwendigen Umgebungsvariablen hinzu:
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

## Tests

Um die Tests auszuführen, verwende den folgenden Befehl:
```sh
python manage.py test