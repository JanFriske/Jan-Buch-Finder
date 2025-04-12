```markdown
# Jan-Buch-Finder

**Jan-Buch-Finder** ist eine Desktop-Anwendung, mit der du Bücher von Jan Friske durchsuchen und Informationen zu den verfügbaren Titeln anzeigen kannst.
Die Anwendung zeigt eine Liste von Büchern, deren Cover, Kurz- und Langbeschreibungen sowie ISBN-Nummern.
Darüber hinaus gibt es einen Button, um direkt zum Online-Shop zu gelangen, um die Bücher zu kaufen.

## Funktionen

- **Buchübersicht:** Anzeige von Buchcovern und -beschreibungen.
- **Hyperlinks:** Direktes Öffnen von Links zu den Online-Shops der Bücher.
- **Personalisierte Ansicht:** Integration eines persönlichen Bildes von Jan Friske.
- **Benutzerfreundlich:** Einfach zu navigierende Oberfläche mit Tabs für jedes Buch.

## Installation

### Voraussetzungen

- **Python 3.x** (empfohlen: 3.7 oder höher)
- **Tkinter** (standardmäßig in Python enthalten)
- **Pillow** (für die Verarbeitung von Bildern)
  
Die benötigten Python-Pakete kannst du mit folgendem Befehl installieren:

```bash
pip install -r requirements.txt
```

Die `requirements.txt`-Datei ist im Repository enthalten und listet alle erforderlichen Abhängigkeiten auf.

### Windows .exe Datei

Für Benutzer, die nicht mit Python arbeiten möchten, gibt es eine **Windows ausführbare Datei (.exe)** im `dist/`-Ordner des Repositories.
Du kannst diese `.exe` direkt ausführen, ohne Python installieren zu müssen.

1. Gehe zum Ordner `dist/`.
2. Doppelklicke auf `Jan-Buch-Finder.exe`, um die Anwendung zu starten.

### Anwendung starten

1. **Python-Version:** Falls du Python installiert hast, kannst du die Anwendung durch Ausführen des folgenden Befehls im Terminal starten:

```bash
python main.py
```

2. **.exe-Version:** Falls du die Windows-Executable verwendest, starte einfach die Datei `Jan-Buch-Finder.exe` aus dem `dist/`-Ordner.

## Lizenz

Dieses Projekt ist unter der [MIT-Lizenz](LICENSE) lizenziert.

---

**Jan-Buch-Finder** wurde von **Jan Friske** entwickelt. Wenn du Fragen oder Anmerkungen hast, kannst du mich gerne kontaktieren.
```

### Erklärungen:
1. **Projektbeschreibung:** Eine kurze Übersicht, was das Projekt macht.
2. **Installation:** Beschreibt die notwendigen Schritte, um das Projekt zu installieren und auszuführen, sowohl mit Python als auch mit der `.exe`-Datei.
3. **Windows .exe Datei:** Weist auf die im Ordner `dist/` vorhandene `.exe`-Datei hin, die von Windows-Nutzern ausgeführt werden kann, ohne dass Python benötigt wird.
4. **Lizenz:** Es wird auf die Lizenz des Projekts hingewiesen (in diesem Fall wird die MIT-Lizenz angenommen, die du in der `LICENSE`-Datei definieren kannst).
