```markdown
# 📚 Jan-Buch-Finder

**Jan-Buch-Finder** ist eine Desktop-Anwendung, mit der du Bücher von **Jan Friske** durchsuchen und Informationen zu den verfügbaren Titeln anzeigen kannst.

Die Anwendung zeigt eine Liste von Büchern, deren **Cover**, **Kurz- und Langbeschreibungen**, sowie **ISBN** und einen **Shop-Link-Button**, um die Bücher zu erwerben.

---

## 🚀 Features

- Darstellung der Bücher mit Bild, Beschreibung, ISBN und Shop-Link
- Navigation über Tabs zwischen verschiedenen Titeln
- Lautstärkeregler und Musikfunktion (MP3)
- Hell-/Dunkelmodus umschaltbar
- Mit **Visual Studio** entwickelt (Projektdateien im Repository)
- Lokale JSON-Datei als Datenquelle (`buchdaten.json`)
- Eigenes Icon & MP3-Datei enthalten

---

## 🛠️ Installation & Ausführung

### Option 1: Ausführen per Python (empfohlen für Entwickler)

1. Stelle sicher, dass Python 3.x installiert ist.
2. Abhängigkeiten installieren (sofern nicht vorhanden):

   ```
   pip install PyQt5
   ```

3. Starte die Anwendung mit:

   ```
   python main.py
   ```

---

### Option 2: Windows-Executable nutzen

Navigiere in den Ordner `dist`. Dort findest du ausführbare Versionen des **Jan-Buch-Finder** in verschiedenen Ausbaustufen:

- `Version 1`
- `Version 1.1`
- `Version 1.2`
- `Version 1.3`

👉 Um eine Version herunterzuladen:

1. Klicke im Ordner `dist` auf die `.exe`-Datei der gewünschten Version.
2. In der nächsten Ansicht erscheint oben rechts ein **Dropdown-Menü** mit **Download-Option**.
3. Wähle dort „Download“, um die Anwendung herunterzuladen.

Die `.exe`-Dateien wurden mit Visual Studio erzeugt. Die zugehörigen `.spec`-Dateien und Builddaten sind im Repository enthalten.

---

## 🖥️ Benutzeroberfläche

Die App wurde mit **PyQt5** realisiert und bietet eine moderne, intuitive Benutzerführung – wahlweise im hellen oder dunklen Modus.

- 📸 Darstellung von Buchcovern, Autorenfoto und Icons
- 🎵 Musikuntermalung mit Lautstärkeregler
- 🌗 Licht-/Dunkelmodus-Umschaltung
- 🧩 Tabs zur Navigation zwischen den Büchern
- 🔗 Externe Buttons zu Shop & Social Media

---

### 🌑 Dunkelmodus (Dark Mode)

So sieht der **Dark Mode** der Anwendung aus:

![Screenshot: Jan-Buch-Finder im Dunkelmodus](assets/darkmode_screenshot.png)

> In dieser Ansicht ist das Buch *„Facebook Profil zensiert“* geöffnet. Die Tabs, Lautstärkeregler, Buttons und Texte passen sich automatisch dem gewählten Modus an.

---

## 📁 Projektstruktur

```
Jan-Buch-Finder/
├── covers/                     # Buchcover
├── dist/                       # Builds und ausführbare Dateien (.exe)
│   ├── Jan-Buch-Finder.exe     # Alle Versionen der Anwendung
│   └── ...                     # (Version 1, 1.1, 1.2, 1.3)
├── buchdaten.json              # Buchdaten (Titel, Beschreibung, ISBN etc.)
├── main.py                     # Hauptprogramm
├── main.spec                   # Build-Spezifikation
├── README.md                   # Diese Datei
├── LICENCE.txt                 # Lizenzinformationen
├── jan_icon.ico                # App-Icon
├── klassik.mp3                 # Hintergrundmusik
└── *.spec                      # Weitere Build-Dateien
```
# Jan-Buch-Finder

Jan-Buch-Finder ist eine Desktop-Anwendung, mit der du Bücher von Jan Friske durchsuchen und
Informationen zu den verfügbaren Titeln anzeigen kannst. Die Anwendung zeigt eine Liste von Büchern,
deren Cover, Kurz- und Langbeschreibungen sowie ISBN-Nummern. Darüber hinaus gibt es einen Button,
um direkt zum Online-Shop zu gelangen, um die Bücher zu kaufen. In der Version 1.2 kommen 3 weitere
Link-Buttons hinzu. Ein Button führt zum Facebook Profil von Jan Friske und die anderen beiden Buttons
verweisen auf die Github-Repositories von Figura KI/Figura AI und Jan-Buch-Finder. In der Version 1.3
kommen weitere Gestaltungselemente hinzu. Die GUI hat jetzt eine Hintergrundmusik, die man in der Lautstärke
regeln und auch stumm schalten kann. Die Buchverweise verweisen jetzt direkt auf die Bücher im Shop und
darüber hinaus gibt es einen Dunkel Modus und einen Licht Modus in der neuen Version 1.3.

## Funktionen

- **Buchübersicht:** Anzeige von Buchcovern und -beschreibungen.
- **Hyperlinks:** Direktes Öffnen von Links zu dem Online-Shop, bei dem die Bücher
von Jan Friske erhältlich sind.
- **Personalisierte Ansicht:** Integration eines persönlichen Bildes von Jan Friske.
- **Benutzerfreundlich:** Einfach zu navigierende Oberfläche mit Tabs für jedes Buch.

## Installation

### Voraussetzungen

- **Python 3.x++ (empfohlen: 3.7 oder höher)
- **Tkinter** und PyQt5 (standardmäßig in Python enthalten um Benutzeroberflächen zu gestalten)
- **Pillow** (für die Verarbeitung von Bildern)
  
### Windows .exe Datei

Für Benutzer, die nicht mit Python arbeiten möchten, gibt es 4 Versionen einer **Windows ausführbaren Datei (.exe)**
im `dist/`-Ordner des Repositories.

Du kannst diese `.exe` direkt ausführen, ohne Python installieren zu müssen.

1. Gehe zum Ordner `dist/`.
2. Doppelklicke auf `Jan-Buch-Finder Version 1.2.exe`und wähle dann auf der nächsten Seite,
   im Dropdown-Menü oben rechts Download.

### Anwendung starten

1. **Python-Version:** Falls du Python installiert hast, kannst du die Anwendung
durch Ausführen des folgenden Befehls im Terminal starten:

bash
python main.py


2. **.exe-Version:** Falls du die Windows-Executable verwendest, starte einfach
   die Datei `Jan-Buch-Finder.exe` aus dem `dist/`-Ordner.

## Lizenz

Dieses Projekt ist unter der [MIT-Lizenz](LICENSE) lizenziert.

---

**Jan-Buch-Finder** wurde von **Jan Friske** entwickelt. Wenn du Fragen oder
Anmerkungen hast, kannst du mich gerne kontaktieren.

---

## ℹ️ Lizenz

Dieses Projekt steht unter der **MIT-Lizenz**. Details findest du in der Datei `LICENCE.txt`.

---

## 👤 Autor

**Jan Friske**  
Website: [Link zum Shop oder Profil einfügen]  
GitHub: [https://github.com/JanFriske](https://github.com/JanFriske)

---

## ⭐ Feedback & Beiträge


---

Vielen Dank fürs Nutzen des Jan-Buch-Finder!
```
