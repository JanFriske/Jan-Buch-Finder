import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os
import sys
import webbrowser
import functools

def get_resource_path(relative_path):
    """
    Ermittelt den absoluten Pfad für eine Ressource.
    Bei einer gepackten .exe (mit PyInstaller) wird sys._MEIPASS genutzt.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def lade_buchdaten():
    """
    Lädt die Buchdaten aus der JSON-Datei. Falls die Datei nicht 
    existiert oder fehlerhaft ist, werden Fallback-Daten genutzt.
    Nach dem Laden wird geprüft, ob für bestimmte Buchtitel der Schlüssel
    "buttons" fehlt – falls ja, wird er ergänzt.
    """
    fallback_buchdaten = [
        {
            "isbn": "978-3-819071-79-9",
            "titel": "Figura KI/Figura AI",
            "beschreibung": "Tauchen Sie ein in die Welt fortschrittlicher künstlicher Intelligenz mit Figura-KI/Figura-AI.",
            "kurzbeschreibung": "Figura-KI/Figura-AI: Multimodular KI.",
            "cover": "covers/figura_ai.jpg",
            "link": "https://www.epubli.com/shop/figura-ki-figura-ai-9783819071799",
            "buttons": [
                {
                    "text": "GitHub-Repository von Figura KI",
                    "url": "https://github.com/JanFriske/Figura-KI---Figura-AI"
                }
            ]
        },
        {
            "isbn": "978-3-819075-02-5",
            "titel": "Facebook Profil zensiert",
            "beschreibung": "Dieses Buch erzählt die Geschichte eines Facebook-Nutzers, der sich gegen Zensur wehrte.",
            "kurzbeschreibung": "Facebook: Zensur und Widerstand.",
            "cover": "covers/facebook_zensur.jpg",
            "link": "https://www.epubli.com/shop/ein-stark-zensiertes-facebook-profil-9783819075025",
            "buttons": [
                {
                    "text": "Zu meinem Facebook-Profil",
                    "url": "https://www.facebook.com/share/165fX45xHq/"
                }
            ]
        },
        {
            "isbn": "978-3-752964-67-7",
            "titel": "Cannabis-Anbau – Drinnen",
            "beschreibung": "Ein einfacher Leitfaden zum Cannabisanbau in Innenräumen.",
            "kurzbeschreibung": "Grundlagen des Cannabis-Anbaus.",
            "cover": "covers/cannabis_drinnen.jpg",
            "link": "https://www.epubli.com/shop/cannabis-anbau-drinnen-9783752964677"
        },
        {
            "isbn": "978-3-752961-28-7",
            "titel": "Cannabis-Anbau – Die Grundlagen",
            "beschreibung": "Ein umfassender Leitfaden zu den Grundlagen des Cannabisanbaus.",
            "kurzbeschreibung": "Cannabis-Anbau für Anfänger.",
            "cover": "covers/cannabis_grundlagen.jpg",
            "link": "https://www.epubli.com/shop/cannabis-anbau-die-grundlagen-9783752961287"
        }
    ]
    
    pfad = get_resource_path("buchdaten.json")
    try:
        with open(pfad, "r", encoding="utf-8") as f:
            daten = json.load(f)
            print(f"[DEBUG] Buchdaten aus Datei geladen: {len(daten)} Bücher gefunden.")
            buchdaten = daten
    except Exception as e:
        print(f"[DEBUG] Fehler beim Laden von 'buchdaten.json': {e}\nVerwende Fallback-Daten.")
        buchdaten = fallback_buchdaten

    # Ergänze fehlende "buttons" für bestimmte Buchtitel, falls nicht vorhanden
    for buch in buchdaten:
        titel = buch.get("titel", "")
        if titel == "Figura KI/Figura AI" and "buttons" not in buch:
            buch["buttons"] = [{
                "text": "GitHub-Repository von Figura KI",
                "url": "https://github.com/JanFriske/Figura-KI---Figura-AI"
            }]
        if titel == "Facebook Profil zensiert" and "buttons" not in buch:
            buch["buttons"] = [{
                "text": "Zu meinem Facebook-Profil",
                "url": "https://www.facebook.com/share/165fX45xHq/"
            }]
        # Debug-Ausgabe der Keys für jedes Buch
        print(f"[DEBUG] Buch '{titel}' enthält keys: {list(buch.keys())}")
        if "buttons" in buch:
            print(f"        Zusatz-Buttons: {buch['buttons']}")
        else:
            print("        Zusatz-Buttons: Nicht vorhanden.")

    return buchdaten

class JanBuchFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jan-Buch-Finder Version 1.2 von Jan Friske")
        self.buchdaten = lade_buchdaten()

        self.setup_oben_frame()
        self.setup_notebook()

    def setup_oben_frame(self):
        """Erstellt oben links das persönliche Bild plus einen Button zum Jan-Buch-Finder Repository."""
        oben_frame = tk.Frame(self.root)
        oben_frame.pack(fill="x", padx=10, pady=10, anchor="nw")

        # Persönliches Bild
        bild_pfad = get_resource_path("jan_2.jpg")
        try:
            image = Image.open(bild_pfad).resize((150, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            bild_label = tk.Label(oben_frame, image=photo)
            bild_label.image = photo
            bild_label.pack(side="left", padx=(0, 20))
        except Exception as e:
            print(f"[DEBUG] Fehler beim Laden des persönlichen Bildes: {e}")
            tk.Label(oben_frame, text="(Kein Bild verfügbar)").pack(side="left", padx=(0, 20))

        # Repo-Button
        repo_button = tk.Button(
            oben_frame,
            text="Zum Jan-Buch-Finder Repository",
            font=("Helvetica", 9),
            fg="white",
            bg="#24292e",
            cursor="hand2",
            command=lambda: self.oeffne_link("https://github.com/JanFriske/Jan-Buch-Finder")
        )
        repo_button.pack(side="left")

    def setup_notebook(self):
        """Erstellt das Notebook und den Titel."""
        title_label = tk.Label(self.root, text="Jan-Buch-Finder Version 1.2 von Jan Friske", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=5)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        self.erstelle_tabs()

    def erstelle_tabs(self):
        """Erstellt für jedes Buch einen Tab im Notebook."""
        for buch in self.buchdaten:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=buch.get("titel", "Kein Titel"))
            self.erzeuge_inhalt(tab, buch)

    def erzeuge_inhalt(self, tab, buch):
        """Erzeugt den Inhalt eines Tabs (Cover, Kurzbeschreibung, Buttons, ISBN, lange Beschreibung)."""
        self.zeige_cover(tab, buch)
        self.zeige_kurzbeschreibung(tab, buch)
        self.zeige_buttons(tab, buch)
        self.zeige_isbn(tab, buch)
        self.zeige_lange_beschreibung(tab, buch)

    def zeige_cover(self, tab, buch):
        cover_pfad = get_resource_path(buch.get("cover", ""))
        try:
            image = Image.open(cover_pfad).resize((150, 200))
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(tab, image=photo)
            label.image = photo
            label.pack(pady=10)
        except Exception as e:
            print(f"[DEBUG] Fehler beim Laden des Covers für '{buch.get('titel')}': {e}")
            tk.Label(tab, text="Kein Cover verfügbar").pack(pady=10)

    def zeige_kurzbeschreibung(self, tab, buch):
        tk.Label(tab, text=buch.get("kurzbeschreibung", ""), wraplength=500, font=("Helvetica", 11)).pack(pady=5)

    def zeige_buttons(self, tab, buch):
        """Erstellt alle Buttons in einem einzigen Frame (Shop-Link plus Zusatz-Buttons)."""
        frame = tk.Frame(tab)
        frame.pack(fill="x", padx=10, pady=5)

        # Shop-Link-Button (immer vorhanden)
        shop_link = buch.get("link", "https://www.epubli.com/?s=Jan+Friske")
        self.erzeuge_button(frame, "Zum Shop", shop_link, fg="blue", underline=True)

        # Zusatz-Buttons (falls vorhanden)
        zusatz_buttons = buch.get("buttons", [])
        if zusatz_buttons:
            for btn in zusatz_buttons:
                text = btn.get("text", "Mehr Infos")
                url = btn.get("url", "")
                self.erzeuge_button(frame, text, url, fg="black", underline=False)
        else:
            print(f"[DEBUG] Buch '{buch.get('titel')}' enthält keine zusätzlichen Buttons.")

    def zeige_isbn(self, tab, buch):
        tk.Label(tab, text=f"ISBN: {buch.get('isbn', 'Keine ISBN')}", font=("Helvetica", 9, "italic"), fg="gray").pack(pady=10)

    def zeige_lange_beschreibung(self, tab, buch):
        text_widget = tk.Text(tab, wrap="word", height=10, font=("Helvetica", 10))
        text_widget.insert("1.0", buch.get("beschreibung", ""))
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)

    def erzeuge_button(self, parent, text, url, fg="black", underline=False):
        if not url:
            return
        font = ("Helvetica", 10, "underline") if underline else ("Helvetica", 10)
        btn = tk.Button(parent, text=text, font=font, fg=fg, cursor="hand2",
                        command=lambda: self.oeffne_link(url))
        btn.pack(side="left", padx=5)

    def oeffne_link(self, url):
        try:
            webbrowser.open_new_tab(url)
        except Exception as e:
            messagebox.showerror("Fehler", f"Der Link konnte nicht geöffnet werden: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JanBuchFinderApp(root)
    root.mainloop()
