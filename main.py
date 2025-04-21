# CODE (angepasst) – nur relevanter Teil wurde geändert

import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QTabWidget, QScrollArea,
    QFrame, QSplitter, QSizePolicy, QSlider
)
from PyQt5.QtGui import QPixmap, QFont, QDesktopServices, QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWebEngineWidgets import QWebEngineView

def get_resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def lade_buchdaten():
    pfad = get_resource_path("buchdaten.json")
    try:
        with open(pfad, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def lade_verlage():
    pfad = get_resource_path("verlage.json")
    try:
        with open(pfad, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

class BuchTab(QWidget):
    def __init__(self, buch):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 20)

        titel = QLabel(buch.get("titel", "Unbekannter Titel"))
        titel.setFont(QFont("Arial", 20, QFont.Bold))
        titel.setAlignment(Qt.AlignCenter)
        layout.addWidget(titel)

        inhalt = QHBoxLayout()
        inhalt.setSpacing(30)
        inhalt.setContentsMargins(0, 0, 0, 0)

        kurz = QLabel(buch.get("kurzbeschreibung", ""))
        kurz.setWordWrap(True)
        kurz.setFont(QFont("Arial", 13))
        kurz.setFixedWidth(260)
        kurz.setStyleSheet("padding:10px;")
        inhalt.addWidget(kurz)

        cover_path = get_resource_path(buch.get("cover", ""))
        pix = QPixmap(cover_path)
        if not pix.isNull():
            pix = pix.scaled(300, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            cover = QLabel()
            cover.setPixmap(pix)
            cover.setAlignment(Qt.AlignCenter)
            inhalt.addWidget(cover)
        else:
            inhalt.addWidget(QLabel("Kein Cover verfügbar"))

        beschr = QTextEdit()
        beschr.setText(buch.get("beschreibung", ""))
        beschr.setFont(QFont("Arial", 13))
        beschr.setReadOnly(True)
        beschr.setStyleSheet("padding:10px;")
        beschr.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        beschr.setMinimumWidth(300)
        inhalt.addWidget(beschr, stretch=2)

        layout.addLayout(inhalt)

        isbn = QLabel(f"ISBN: {buch.get('isbn', 'Keine ISBN')}")
        isbn.setFont(QFont("Arial", 11, italic=True))
        isbn.setStyleSheet("color:gray;")
        isbn.setAlignment(Qt.AlignCenter)
        layout.addWidget(isbn)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)

        shop = QPushButton("Zum Shop")
        shop.setFont(QFont("Arial", 11))
        shop.setStyleSheet("padding:8px 16px;")
        shop.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(buch.get("link", "#"))))
        btn_layout.addWidget(shop)

        for b in buch.get("buttons", []):
            btn = QPushButton(b.get("text", "Mehr Infos"))
            btn.setFont(QFont("Arial", 11))
            btn.setStyleSheet("padding:8px 16px;")
            btn.clicked.connect(lambda _, u=b.get("url", "#"): QDesktopServices.openUrl(QUrl(u)))
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

class JanBuchFinder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jan-Buch-Finder 1.4 – von Jan Friske")
        self.setMinimumSize(1100, 700)
        self.darkmode = False

        self.player = QMediaPlayer()
        music = get_resource_path("klassik.mp3")
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(music)))
        self.player.setVolume(50)
        self.player.play()
        self.player.mediaStatusChanged.connect(self.loop_music)

        main = QVBoxLayout(self)
        main.setSpacing(10)
        main.setContentsMargins(10, 10, 10, 10)

        header = QHBoxLayout()
        left = QVBoxLayout()
        left.setAlignment(Qt.AlignCenter)
        foto = QLabel()
        pix = QPixmap(get_resource_path("jan_2.jpg"))
        if not pix.isNull():
            pix = pix.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            foto.setPixmap(pix)
        else:
            foto.setText("Kein Bild")
        left.addWidget(foto)
        repo = QPushButton("Zum Jan-Buch-Finder Repository")
        repo.clicked.connect(lambda: QDesktopServices.openUrl(
            QUrl("https://github.com/JanFriske/Jan-Buch-Finder")))
        left.addWidget(repo)
        header.addLayout(left, 1)

        center = QVBoxLayout()
        center.setAlignment(Qt.AlignCenter)
        lbl = QLabel("Jan-Buch-Finder 1.4")
        lbl.setFont(QFont("Arial", 18, QFont.Bold))
        lbl.setAlignment(Qt.AlignCenter)
        center.addWidget(lbl)
        header.addLayout(center, 3)

        right = QVBoxLayout()
        right.setAlignment(Qt.AlignCenter)
        self.mute_btn = QPushButton("🔇 Musik stummschalten")
        self.mute_btn.clicked.connect(self.toggle_mute)
        right.addWidget(self.mute_btn)
        vol_lbl = QLabel("Lautstärke")
        right.addWidget(vol_lbl)
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(50)
        slider.valueChanged.connect(self.player.setVolume)
        right.addWidget(slider)
        self.dark_btn = QPushButton("🌙 Dunkelmodus")
        self.dark_btn.clicked.connect(self.toggle_darkmode)
        right.addWidget(self.dark_btn)
        header.addLayout(right, 1)

        main.addLayout(header)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setStyleSheet("""
            QTabWidget::pane { margin:0; padding:0; }
            QTabBar::tab { background:#f0f0f0; padding:8px; color:black; }
            QTabBar::tab:selected { background:#ddd; color:black; }
        """)
        main.addWidget(self.tabs)

        for buch in lade_buchdaten():
            page = BuchTab(buch)
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setWidget(page)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.tabs.addTab(scroll, buch.get("titel", "Buch"))

        self.tabs.addTab(self.build_verlage_widget(), "Verlage")

    def build_verlage_widget(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Vertical)
        layout.addWidget(splitter)

        top_f = QFrame()
        top_l = QVBoxLayout(top_f)
        top_l.setContentsMargins(0, 0, 0, 0)
        top_l.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        for v in lade_verlage():
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(0)

            btn = QPushButton(v.get("name", "Unbekannter Verlag"))
            btn.setFont(QFont("Arial", 12))
            btn.setFixedHeight(40)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            url = v.get("url", "#")
            if not url.startswith("http"):
                url = "https://" + url
            btn.clicked.connect(lambda _, u=url: QDesktopServices.openUrl(QUrl(u)))
            row.addWidget(btn)

            map_btn = QPushButton("📍")
            map_btn.setFixedSize(40, 40)
            map_btn.clicked.connect(lambda _, o=v.get("adresse", v.get("name")): self.showOnMap(o))
            row.addWidget(map_btn)

            cl.addLayout(row)

        content.setLayout(cl)
        scroll.setWidget(content)
        top_l.addWidget(scroll)
        top_f.setLayout(top_l)

        bot_f = QFrame()
        bot_l = QHBoxLayout(bot_f)
        bot_l.setContentsMargins(0, 0, 0, 0)
        bot_l.setSpacing(10)

        self.map_toggle = QPushButton("🗺️ Verlage auf Karte online anzeigen")
        self.map_toggle.setFixedHeight(40)
        self.map_toggle.clicked.connect(self.toggleMap)
        bot_l.addWidget(self.map_toggle, 1)

        self.map_view = QWebEngineView()
        self.map_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.map_enabled = False
        self._setMapInactiveMessage()
        bot_l.addWidget(self.map_view, 3)

        splitter.addWidget(top_f)
        splitter.addWidget(bot_f)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        return w

    def toggle_mute(self):
        muted = not self.player.isMuted()
        self.player.setMuted(muted)
        self.mute_btn.setText("🔈 Musik aktivieren" if muted else "🔇 Musik stummschalten")

    def toggle_darkmode(self):
        self.darkmode = not self.darkmode
        if self.darkmode:
            self.setStyleSheet("""
                QWidget { background:#121212; color:#ffffff; }
                QTextEdit, QLabel { background:#1e1e1e; color:#ffffff; }
                QPushButton { background:#2c2c2c; color:#ffffff; }
                QTabBar::tab { background:#333333; color:#ffffff; }
                QTabBar::tab:selected { background:#555555; color:#ffffff; }
            """)
            self.dark_btn.setText("☀️ Lichtmodus")
        else:
            self.setStyleSheet("")
            self.dark_btn.setText("🌙 Dunkelmodus")

    def loop_music(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.setPosition(0)
            self.player.play()

    def toggleMap(self):
        self.map_enabled = not self.map_enabled
        if self.map_enabled:
            self.map_view.setHtml(
                "<h3 style='color:gray;text-align:center;margin-top:50px;'>Wählen Sie einen Verlag 📍</h3>"
            )
            self.map_toggle.setText("🚫 Kartenfunktion deaktivieren")
        else:
            self._setMapInactiveMessage()
            self.map_toggle.setText("🗘️ Verlage auf Karte online anzeigen")

    def _setMapInactiveMessage(self):
        self.map_view.setHtml(
            "<h3 style='color:darkred;text-align:center;margin-top:50px;'>Kartenfunktion nicht aktiviert</h3>"
        )

    def showOnMap(self, ort):
        if not self.map_enabled:
            return
        q = ort.replace(" ", "+")
        html = f"""
            <html><body style="margin:0;padding:0;">
            <iframe width="100%" height="100%" frameborder="0"
              src="https://www.google.com/maps?q={q}&output=embed"
              allowfullscreen></iframe>
            </body></html>
        """
        self.map_view.setHtml(html)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_resource_path("jan_icon.ico")))
    window = JanBuchFinder()
    window.show()
    sys.exit(app.exec_())







