# Verwaltung Radsport Koch GmbH

Desktop-Verwaltungssoftware für einen Fahrradladen auf Basis von Python, PySide6, SQLAlchemy und SQLite.

## Oberfläche

### Dashboard

![Dashboard](docs/images/dashboard.png)

### Kundenverwaltung

![Kundenverwaltung](docs/images/customers.png)

## Was die Anwendung kann

- Dashboard mit Kennzahlen, Umsatz und Lagerwarnungen
- Kundenverwaltung mit Suchen, Bearbeiten, Löschen und Detailansicht
- Artikelverwaltung mit Kategorien, Preisen, Bestand und Mindestbestand
- Bestellverwaltung mit mehreren Positionen, Summenberechnung und Status
- CSV-Export für Kunden, Artikel und Bestellungen
- Seed-Daten, damit das Projekt direkt mit Beispieldaten startbar ist

## Projektstruktur einfach erklärt

### `app/database`

Hier ist alles für die Datenbankanbindung.

- `base.py`
  Hier liegt die gemeinsame SQLAlchemy-Basis, von der alle Datenmodelle erben.
- `session.py`
  Erstellt die Verbindung zur Datenbank und liefert Sessions fuer Datenbankzugriffe.
- `initializer.py`
  Startet die Datenbank, legt Tabellen an und führt beim ersten Start Seed-Daten ein.

### `app/models`

Hier stehen die eigentlichen Datenbanktabellen als Python-Klassen.

- `customer.py`
  Modell für Kunden
- `product.py`
  Modell für Artikel
- `order.py`
  Modell für Bestellungen
- `order_item.py`
  Modell für Bestellpositionen

Kurz gesagt:
`models` beschreiben, wie die Daten in der Datenbank gespeichert werden.

### `app/repositories`

Repositories kümmern sich nur um den Datenzugriff.

Beispiel:
- Kunden aus der Datenbank laden
- Artikel suchen
- Bestellungen filtern

Kurz gesagt:
`repositories` sind die Schicht zwischen Datenbank und Fachlogik.

### `app/schemas`

Hier liegt die Validierung mit Pydantic.

Beispiel:
- ist eine E-Mail gültig?
- sind Pflichtfelder gefüllt?
- ist eine Menge größer als 0?

Kurz gesagt:
`schemas` prüfen Eingaben, bevor damit gearbeitet oder gespeichert wird.

### `app/services`

Hier liegt die eigentliche Fachlogik.

Beispiel:
- Kunden anlegen oder aktualisieren
- Lagerbestand bei Bestellungen reduzieren
- Bestellsummen berechnen
- Dashboard-Daten zusammenstellen

Kurz gesagt:
`services` enthalten das Verhalten der Anwendung.

### `app/ui`

Hier ist die komplette grafische Oberfläche.

- `main_window.py`
  Hauptfenster mit Navigation
- `views/`
  Die großen Seiten wie Dashboard, Kunden, Artikel und Bestellungen
- `dialogs/`
  Fenster für Anlegen, Bearbeiten und Bestätigen
- `widgets/`
  Wiederverwendbare UI-Bausteine wie Karten, Tabellen und Filterleisten

### `app/utils`

Kleine Hilfsfunktionen, die an mehreren Stellen gebraucht werden.

Beispiel:
- Datumsformatierung
- Währungsformatierung
- CSV-Export
- Status-Hilfsfunktionen

## Wichtige Dateien kurz erklärt

### `main.py`

Das ist der eigentliche Einstiegspunkt der Anwendung.

Beim Start passiert hier:
- Logging wird vorbereitet
- die Datenbank wird initialisiert
- die Qt-Anwendung wird erzeugt
- das Hauptfenster wird gestartet

Wenn du die Anwendung normal startest, dann über `main.py`.

### `seed.py`

Diese Datei füllt die Datenbank mit Beispieldaten.

Sie ist praktisch, wenn du:
- die App testen willst
- direkt Beispielkunden und Beispielartikel brauchst
- eine leere Datenbank schnell befüllen willst

### `alembic.ini` und `migrations/`

Das gehört zu Alembic.

### Was ist Alembic?

Alembic ist das Migrationswerkzeug für SQLAlchemy.

Es sorgt dafür, dass man Datenbankstrukturen kontrolliert verändern kann.

Beispiel:
- neue Spalte hinzufügen
- neue Tabelle anlegen
- Schema sauber versionieren

Statt die Datenbank immer manuell umzubauen, macht Alembic das nachvollziehbar über Migrationen.

### `pyproject.toml`

Das ist eine moderne Projektdatei für Python.

Darin stehen zum Beispiel:
- Projektname
- Python-Version
- benötigte Abhängigkeiten
- Test-Konfiguration

### Was ist `.toml`?

`.toml` ist ein Konfigurationsformat.

Es wird oft in Python-Projekten verwendet, weil es übersichtlich und gut lesbar ist.

## Wie Datenfluss in der Anwendung funktioniert

Einfach erklaert:

1. Die GUI nimmt Eingaben vom Benutzer entgegen.
2. `schemas` prüfen die Daten.
3. `services` führen die Fachlogik aus.
4. `repositories` lesen oder speichern Daten.
5. `models` bilden die Tabellen in der Datenbank ab.

So bleibt das Projekt sauber getrennt und später gut erweiterbar.

## CSV-Export

Exportierte Dateien landen standardmäßig in:

`exports/`

also zum Beispiel unter:

`/Users/student/Documents/New project/RadSportKochGmbH/exports`

## Start in der Praxis

### 1. Virtuelle Umgebung aktivieren

```bash
cd "/Users/student/Documents/New project/RadSportKochGmbH"
source .venv/bin/activate
```

### 2. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 3. Umgebungsdatei anlegen

```bash
cp .env.example .env
```

### 4. Datenbank vorbereiten

```bash
alembic upgrade head
```

### 5. Seed-Daten einspielen

```bash
python seed.py
```

### 6. Anwendung starten

```bash
python main.py
```
