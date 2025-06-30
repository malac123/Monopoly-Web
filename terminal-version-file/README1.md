## *Monopoly Terminal Spiel*

Eine Terminal-basierte Implementierung des klassischen Monopoly Brettspiels

## *Beschreibung*

Dieses Projekt ist eine Python-basierte Terminal-Implementierung von Monopoly, die es Spielern ermöglicht, das klassische Brettspiel über einen Terminal zu erleben. Das Spiel bietet:

- Terminal basierte Benutzeroberfläche mit Farbunterstützung
- Klassische Monopoly-Spielmechaniken
- Interaktives Würfeln
- Immobilienverwaltung
- Spielerinteraktionen

## *Spielmerkmale*

- **Spieleranzahl**: 2-4 Spieler
- **Spielbrett**: Klassisches Monopoly-Brett mit 40 Feldern
- **Währung**: Spielgeld in $
- **Aktionen**:
  - Würfeln und sich bewegen
  - Immobilien kaufen und verkaufen
  - Häuser bauen auf eigenem Grundstück
  - Miete kassieren
  - Zwischen Bahnhöfe teleportieren
  - Ins Gefängnis gehen und es verlassen

## *Voraussetzungen*

- Python 3.6 oder höher
- pip (Python Paket-Manager)
- Ein Terminal 
- Mindestens 2 Spieler (sorry leider gibts keine bots)

## *Installation*

1. Repository klonen und zu dem Folder navigieren:
```bash
git clone https://github.com/SplatTB29/Monopoly-terminal.git
cd Monopoly-terminal
```

2. Zum dev Branch wechseln (wichtig!):
```bash
git checkout dev
```

3. Erforderliche Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

## *Projektstruktur*

```
Monopoly-terminal/
├── assets/                 # Spielressourcen und Assets
│   └── board_data.json     # Beinhaltet die "Properties", also die Spielfelder
├── game_logic/             # Kernspiellogik / Klassen
|   ├── __init__.py         # damit man die Klassen als Module importieren kann
|   ├── property.py         # Property Klasse für die Property Logik 
│   ├── game.py             # Hauptspiellogik
│   ├── player.py           # Spielerklasse
│   └── game_board.py       # Spielfeldlogik
├── tests/                  # Testdateien (jeder schreibt seine eigene tests ;-)
├── ui/                     # Benutzeroberflächenkomponenten
│   └── terminal_ui.py      # Terminal-UI-Implementierung und die Hauptspiellogik sind hier enthalten
├── main.py                 # run main.py um das Spiel zu starten
└── requirements.txt        # Abhängigkeiten
```

## *Spielstart*

1. Öffnen Sie ein Terminal oder eine Kommandozeile (Win + R & "cmd")

2. Navigieren Sie zum Projektverzeichnis:

```bash
cd *dein Folder eingeben*
```

3. Führen Sie den folgenden Befehl aus:

```bash
python main.py
```

## *Spielanleitung*

1. **Spielbeginn**:
   - Geben Sie die Anzahl der Spieler ein
   - Jeder Spieler erhält 1500€ Startkapital

2. **Spielablauf**:
   - Würfeln Sie mit den Würfeln
   - Bewegen Sie sich entsprechend der Zahl
   - Führen Sie die Aktion des Feldes aus
   - Der nächste Spieler ist an der Reihe

3. **Spielende**:
   - Das Spiel endet, wenn nur noch ein Spieler übrig ist bzw. nicht bankrott ist

## *Abhängigkeiten*

- **colorama (0.4.3)**: Für die Farbunterstützung im Terminal
- **pygame (2.0.1)**: gilt nur für die version im main branch

## *Fehlerbehebung*

Häufige Probleme und Lösungen:

1. **Farben werden nicht angezeigt**:
   - Stellen Sie sicher, dass Ihr Terminal Farben unterstützt
   - colorama installieren

2. **Falscher Speicherort**:
   - Überprüfen Sie die wo Sie die Repository gecloned haben
   - Stellen Sie sicher, dass sie zu, richtigen Folder und File navigieren

3. **Python-Fehler**:
   - Python-Version (am besten 3.6 oder höher)
   - alle Abhängigkeiten neu installieren (requirments.txt)


## *Mitwirken*

Wer will kann das Spiel gerne erweitern:
- Fehler melden via Issues auf github
- Code beitragen
- Dokumentation verbessern

## *Team*

- Ivano P.
- Liam H.
- Liam L.


## *MEMES*
![A Meme](https://github.com/SplatTB29/Monopoly-terminal/blob/main/memes/meme.png?raw=true)
![Another Meme](https://github.com/SplatTB29/Monopoly-terminal/blob/main/memes/meme2.png?raw=true)
![Another Meme](https://github.com/SplatTB29/Monopoly-terminal/blob/main/memes/meme3.png?raw=true)
