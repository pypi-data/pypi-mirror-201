# Postleid Excel

Skript zum Korrigieren von Postleitzahlen in Excel

## Voraussetzungen

[Python 3](https://www.python.org/about/)

Installation der benötigten Module
(`openpyxl`, `pandas`, `xlrd` und `PyYAML`) in einem aktiven
_[Python Virtual Environment](https://docs.python.org/library/venv.html):_

```
pip install -r requirements.txt
```

## Aufruf

_ebenfalls im aktiven Virtual Environment_

```
python pl_wrapper.py EXCELDATEI
```

 – wobei `EXCELDATEI` für den Pfad zu einer Exceldatei steht –

Ausgabe von `python pl_wrapper.py -h` als Orientierung:

```
Rufe den Befehl 'python -m postleid -h' auf …
Aufruf: postleid [-h] [--version] [-v | -q] [-g] [-l] [-o AUSGABEDATEI]
                 EXCELDATEI

Postleitzahlen in Excel-Dateien korrigieren

Positionsparameter:
  EXCELDATEI            die Original-Exceldatei

Optionen:
  -h, --help            diese Meldung anzeigen und beenden
  --version             Version ausgeben und beenden
  -g, --guess-1000s     Postleitzahlen unter 1000 mit 1000 multiplizieren
                        (Achtung, für PLZs aus Bahrain liefert diese Option
                        falsche Ergebnisse!)
  -l, --list-supported-countries
                        Unterstützte Länder anzeigen (der Dateiname muss in
                        diesem Fall zwar auch angegeben werden, wird jedoch
                        ignoriert)
  -o AUSGABEDATEI, --output-file AUSGABEDATEI
                        die Ausgabedatei (Standardwert: Name der Original-
                        Exceldatei mit vorangestelltem 'fixed-')

Logging-Optionen:
  steuern die Meldungsausgaben (Standard-Loglevel: INFO)

  -v, --verbose         alle Meldungen ausgeben (Loglevel DEBUG)
  -q, --quiet           nur Warnungen und Fehler ausgeben (Loglevel WARNING)

```
