import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout,
    QTabWidget, QScrollArea, QSlider
)
from PyQt5.QtGui import QPixmap, QFont, QDesktopServices
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def lade_buchdaten():
    pfad = get_resource_path("buchdaten.json")
    try:
        with open(pfad, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


class BuchTab(QWidget):
    def __init__(self, buch):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 20)

        titel = QLabel(buch.get("titel", "Unbekannter Titel"))
        titel.setFont(QFont("Arial", 20, QFont.Bold))
        titel.setAlignment(Qt.AlignCenter)
        layout.addWidget(titel)

        inhalt_layout = QHBoxLayout()
        inhalt_layout.setSpacing(30)
        inhalt_layout.setContentsMargins(30, 0, 30, 0)

        kurz_label = QLabel(buch.get("kurzbeschreibung", ""))
        kurz_label.setWordWrap(True)
        kurz_label.setFont(QFont("Arial", 13))
        kurz_label.setFixedWidth(260)
        kurz_label.setStyleSheet("padding: 10px;")
        inhalt_layout.addWidget(kurz_label)

        cover_path = get_resource_path(buch.get("cover", ""))
        pixmap = QPixmap(cover_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(300, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            cover_label = QLabel()
            cover_label.setPixmap(pixmap)
            cover_label.setAlignment(Qt.AlignCenter)
            inhalt_layout.addWidget(cover_label)
        else:
            inhalt_layout.addWidget(QLabel("Kein Cover verfügbar"))

        beschreibung = QTextEdit()
        beschreibung.setText(buch.get("beschreibung", ""))
        beschreibung.setFont(QFont("Arial", 13))
        beschreibung.setReadOnly(True)
        # Erhöhe die Breite der Beschreibung um ca. 30%
        beschreibung.setFixedWidth(880)
        beschreibung.setStyleSheet("padding: 10px;")
        inhalt_layout.addWidget(beschreibung)

        layout.addLayout(inhalt_layout)

        isbn = QLabel(f"ISBN: {buch.get('isbn', 'Keine ISBN')}")
        isbn.setFont(QFont("Arial", 11, italic=True))
        isbn.setStyleSheet("color: gray;")
        isbn.setAlignment(Qt.AlignCenter)
        layout.addWidget(isbn)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        shop_button = QPushButton("Zum Shop")
        shop_button.setStyleSheet("padding: 8px 16px;")
        shop_button.setFont(QFont("Arial", 11))
        shop_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(buch.get("link", "#"))))
        button_layout.addWidget(shop_button)

        for btn in buch.get("buttons", []):
            button = QPushButton(btn.get("text", "Mehr Infos"))
            button.setStyleSheet("padding: 8px 16px;")
            button.setFont(QFont("Arial", 11))
            button.clicked.connect(lambda _, url=btn.get("url", "#"): QDesktopServices.openUrl(QUrl(url)))
            button_layout.addWidget(button)

        layout.addLayout(button_layout)
        self.setLayout(layout)


class JanBuchFinder(QWidget):
    def __init__(self):
        super().__init__()
        # Titelleiste bleibt unverändert
        self.setWindowTitle("Jan-Buch-Finder 1.3 – von Jan Friske")
        self.setMinimumSize(1100, 700)
        self.darkmode = False

        self.player = QMediaPlayer()
        music_path = get_resource_path("klassik.mp3")
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(music_path)))
        self.player.setVolume(50)
        self.player.play()
        self.player.mediaStatusChanged.connect(self.loop_music)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Oberer Bereich: Dreispaltiges Layout (links: Bild+Repo, Mitte: Titel, rechts: Steuerung)
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Linke Spalte: Bild und Repository-Button
        left_top_layout = QVBoxLayout()
        left_top_layout.setAlignment(Qt.AlignCenter)
        bild_label = QLabel()
        jan_bild = QPixmap(get_resource_path("jan_2.jpg"))
        if not jan_bild.isNull():
            jan_bild = jan_bild.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            bild_label.setPixmap(jan_bild)
        else:
            bild_label.setText("Kein Bild")
        left_top_layout.addWidget(bild_label)
        repo_button = QPushButton("Zum Jan-Buch-Finder Repository")
        repo_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/JanFriske/Jan-Buch-Finder")))
        left_top_layout.addWidget(repo_button)
        top_layout.addLayout(left_top_layout, 1)
        
        # Mittlere Spalte: Titel (zentriert)
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        title_label = QLabel("Jan-Buch-Finder 1.3")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(title_label)
        top_layout.addLayout(center_layout, 3)
        
        # Rechte Spalte: Steuerung (Mute, Lautstärke, Dunkel-/Lichtmodus)
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignCenter)
        self.mute_button = QPushButton("🔇 Musik stummschalten")
        self.mute_button.clicked.connect(self.toggle_mute)
        right_layout.addWidget(self.mute_button)
        volume_label = QLabel("Lautstärke")
        right_layout.addWidget(volume_label)
        volume_slider = QSlider(Qt.Horizontal)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(50)
        volume_slider.valueChanged.connect(self.player.setVolume)
        right_layout.addWidget(volume_slider)
        self.darkmode_button = QPushButton("🌙 Dunkelmodus")
        self.darkmode_button.clicked.connect(self.toggle_darkmode)
        right_layout.addWidget(self.darkmode_button)
        top_layout.addLayout(right_layout, 1)
        
        main_layout.addLayout(top_layout)
        
        buchdaten = lade_buchdaten()
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)  # Reiter horizontal oben
        tabs.setStyleSheet("""
            QTabWidget::pane { margin: 0px; padding: 0px; }
            QTabBar::tab { background-color: #f0f0f0; color: black; padding: 10px; border: 1px solid #ccc; }
            QTabBar::tab:selected { background-color: #ddd; color: black; }
        """)
        for buch in lade_buchdaten():
            tab = BuchTab(buch)
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setWidget(tab)
            tabs.addTab(scroll, buch.get("titel", "Buch"))
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

    def toggle_mute(self):
        muted = not self.player.isMuted()
        self.player.setMuted(muted)
        self.mute_button.setText("🔈 Musik aktivieren" if muted else "🔇 Musik stummschalten")

    def toggle_darkmode(self):
        self.darkmode = not self.darkmode
        if self.darkmode:
            self.setStyleSheet("""
                QWidget { background-color: #121212; color: #ffffff; }
                QTextEdit, QLabel { background-color: #1e1e1e; color: #ffffff; }
                QPushButton { background-color: #2c2c2c; color: #ffffff; }
                QTabWidget::pane { margin: 0px; padding: 0px; }
                QTabBar::tab { background-color: #333333; color: #ffffff; padding: 10px; border: 1px solid #555555; }\n
                QTabBar::tab:selected { background-color: #555555; color: black; }\n
            """)
            self.darkmode_button.setText("☀️ Lichtmodus")
        else:
            self.setStyleSheet("")
            self.darkmode_button.setText("🌙 Dunkelmodus")

    def loop_music(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.setPosition(0)
            self.player.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JanBuchFinder()
    window.show()
    sys.exit(app.exec_())
