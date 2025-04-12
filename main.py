import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import sys
import webbrowser
import functools  # Für partial-Funktion

def get_resource_path(relative_path):
    """
    Ermittelt den absoluten Pfad für eine Ressource.
    Bei der .exe wird sys._MEIPASS verwendet.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def lade_buchdaten():
    """
    Lädt die Buchdaten aus der JSON-Datei.
    """
    pfad = get_resource_path("buchdaten.json")
    try:
        with open(pfad, "r", encoding="utf-8") as f:
            daten = json.load(f)
            print(f"Buchdaten geladen: {len(daten)} Bücher gefunden.")
            if daten and "link" in daten[0]:
                print(f"Erster Link: {daten[0]['link']}")
            return daten
    except FileNotFoundError:
        sys.exit(f"Die Datei '{pfad}' wurde nicht gefunden!")
    except json.JSONDecodeError as e:
        sys.exit(f"Die JSON-Datei konnte nicht gelesen werden: {e}")

class JanBuchFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jan-Buch-Finder Version 1.1 von Jan Friske")
        
        # Setze das Programm-Icon
        icon_path = get_resource_path("jan_icon.ico")
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Fehler beim Setzen des Icons: {e}")

        # Persönliches Bild
        self.zeige_persönliches_bild()

        # Titel
        title_label = tk.Label(root, text="Jan-Buch-Finder Version 1.1 von Jan Friske", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Tabs
        self.buchdaten = lade_buchdaten()
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.erstelle_tabs()

    def zeige_persönliches_bild(self):
        personal_image_path = get_resource_path("jan_2.jpg")
        try:
            personal_image = Image.open(personal_image_path).resize((150, 150))
            personal_photo = ImageTk.PhotoImage(personal_image)
            personal_label = tk.Label(self.root, image=personal_photo)
            personal_label.image = personal_photo
            personal_label.pack(pady=10)
        except FileNotFoundError as e:
            print(f"Fehler beim Laden des persönlichen Bildes: {e}")
            tk.Label(self.root, text="(Kein Bild verfügbar)").pack(pady=10)

    def erstelle_tabs(self):
        for buch in self.buchdaten:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=buch["titel"])

            self.zeige_cover(tab, buch)
            self.zeige_kurzbeschreibung(tab, buch)
            self.zeige_hyperlink_button(tab, buch)
            self.zeige_isbn(tab, buch)
            self.zeige_lange_beschreibung(tab, buch)

    def zeige_cover(self, tab, buch):
        cover_path = get_resource_path(buch["cover"])
        try:
            cover_image = Image.open(cover_path).resize((150, 200))
            cover_photo = ImageTk.PhotoImage(cover_image)
            cover_label = tk.Label(tab, image=cover_photo)
            cover_label.image = cover_photo
            cover_label.pack(pady=10)
        except FileNotFoundError:
            tk.Label(tab, text="(Kein Cover verfügbar)").pack(pady=10)

    def zeige_kurzbeschreibung(self, tab, buch):
        kurzbeschreibung_label = tk.Label(
            tab,
            text=buch["kurzbeschreibung"],
            wraplength=500,
            justify="left",
            font=("Helvetica", 11)
        )
        kurzbeschreibung_label.pack(padx=10, pady=5)

    def zeige_hyperlink_button(self, tab, buch):
        """
        Fügt einen Hyperlink-Button hinzu.
        Prüft und bereinigt die URL.
        """
        default_link = "https://www.epubli.com/?s=Jan+Friske"
        link = buch.get("link", "").strip()

        if not link:
            print(f"Warnung: Kein Link für Buch '{buch['titel']}' gefunden!")
            link = default_link
        else:
            print(f"Buch: {buch['titel']}, Roh-Link: '{link}'")
            if not link.startswith("http://") and not link.startswith("https://"):
                link = "https://" + link

        print(f"Verwendeter Link: {link}")  # Debug-Ausgabe

        link_button = tk.Button(
            tab,
            text="Zum Shop",
            font=("Helvetica", 10, "underline"),
            fg="blue",
            cursor="hand2",
            command=functools.partial(self.öffne_hyperlink, link)
        )
        link_button.pack(pady=5)

    def zeige_isbn(self, tab, buch):
        isbn_label = tk.Label(
            tab,
            text=f"ISBN: {buch['isbn']}",
            font=("Helvetica", 9, "italic"),
            fg="gray"
        )
        isbn_label.pack(pady=(0, 10))

    def zeige_lange_beschreibung(self, tab, buch):
        beschreibung = tk.Text(tab, wrap="word", height=10, font=("Helvetica", 10))
        beschreibung.insert("1.0", buch["beschreibung"])
        beschreibung.config(state="disabled")
        beschreibung.pack(padx=10, pady=10, fill="both", expand=True)

    def öffne_hyperlink(self, url):
        try:
            print(f"[DEBUG] Öffne URL: {url}")
            webbrowser.open_new_tab(url)
        except Exception as e:
            messagebox.showerror("Fehler", f"Der Link konnte nicht geöffnet werden: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JanBuchFinderApp(root)
    root.mainloop()
