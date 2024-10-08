#!/usr/bin/python3

import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt

# Definiere den Pfad zur Datei, die die URL speichert
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.config', 'x-live', 'webai')
os.makedirs(CONFIG_DIR, exist_ok=True)  # Stelle sicher, dass das Verzeichnis existiert
URL_FILE_PATH = os.path.join(CONFIG_DIR, 'current_url.txt')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Standard-URL
        DEFAULT_URL = "https://chat.openai.com/"
        # Lade die URL aus der Datei, falls vorhanden, ansonsten verwende die Standard-URL
        URL = self.load_url_from_file() or DEFAULT_URL
        
        # Erstelle das WebEngineView und setze es als zentrales Widget
        self.max = False
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.prozent = 0.43

        # Lade eine Webseite
        self.browser.setUrl(QUrl(URL))
        
        # Auf das Signal screenGeometryChanged reagieren
        self.screen = QApplication.primaryScreen()
        self.screen.geometryChanged.connect(self.adjust_to_screen)

        # Zusätzlich screenChanged-Signal abonnieren, falls sich der Bildschirm wechselt oder die Auflösung ändert
        app.screenAdded.connect(self.screen_changed)
        app.screenRemoved.connect(self.screen_changed)
        
        # Bildschirmgröße berechnen
        screen_geometry = self.screen.availableGeometry()
        breite = int(screen_geometry.width()*self.prozent)
        hoehe = int(screen_geometry.height())
        xpos = int(screen_geometry.width() - breite)
        print(hoehe)
        
        # Fenster-Eigenschaften setzen
        self.setWindowIcon(QIcon('/usr/share/pixmaps/webai.png'))
        self.setGeometry(xpos, 0, breite, hoehe)
        self.setFixedHeight(hoehe)
        self.setWindowFlag(Qt.FramelessWindowHint) # Fensterdekoration entfernen
        self.setWindowTitle("X-Live-WebAI")
        
        # Tray Icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("/usr/share/pixmaps/webai.png"))
        self.tray_icon.setToolTip("X-Live Webai")

        # Tray Menu
        tray_menu = QMenu()
        open_action = QAction("öffnen/verstecken", self)
        exit_action = QAction("schließen", self)
        self.max_action = QAction("Maximieren", self)
        self.autostart_action = QAction("Autostart □", self)
        if os.path.exists(os.path.expanduser("~/.config/autostart/webai.desktop")):
            self.autostart_action.setText("Autostart ✓")

        # Menü KI-Auswahl
        self.change_menu = QMenu("ki-auswählen", self)
        copilot_action = QAction("MicorSoft Copilot", self)
        gemini_action = QAction("Google Gemini", self)
        chatgpt_action = QAction("OpenAI Chat-GPT", self)
        fragai_action = QAction("Frag die Ki", self)

        self.change_menu.addAction(copilot_action)
        self.change_menu.addAction(gemini_action)
        self.change_menu.addAction(chatgpt_action)
        self.change_menu.addAction(fragai_action)

        copilot_action.triggered.connect(lambda: self.change_url('https://copilot.microsoft.com/'))
        gemini_action.triggered.connect(lambda: self.change_url('https://gemini.google.com/'))
        chatgpt_action.triggered.connect(lambda: self.change_url('https://chat.openai.com/'))
        fragai_action.triggered.connect(lambda: self.change_url('https://www.aichatting.net/de/ask-ai/'))
        

        open_action.triggered.connect(self.toggle_window)
        exit_action.triggered.connect(QApplication.instance().quit)
        self.max_action.triggered.connect(self.max_window)
        self.autostart_action.triggered.connect(self.toogle_autostart)

        tray_menu.addMenu(self.change_menu)
        tray_menu.addAction(self.max_action)
        tray_menu.addAction(self.autostart_action)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Minimize to Tray
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # Start minimized to tray
        self.hide()
        

    def adjust_to_screen(self):
        """Passt die Fenstergröße an die aktuelle Bildschirmgeometrie an."""
        screen_geometry = self.screen.availableGeometry()
        #self.setGeometry(screen_geometry)
        print("Bildschirmgröße angepasst:", screen_geometry)
        print(screen_geometry.height())
        breite = int(screen_geometry.width()*self.prozent)
        max_breite = int(screen_geometry.width())
        hoehe = int(screen_geometry.height())
        xpos = int(screen_geometry.width() - breite)
        #print(hoehe)
        
        if self.max == True:
            self.setGeometry(0, 0, max_breite, hoehe)
            #print("show max")
            #print(breite)
        else:
            self.setGeometry(xpos, 0, breite, hoehe)
            #print("show no max")
            #print(breite)
                
    def screen_changed(self):
        """Ruft die aktuelle Bildschirmgeometrie nach einer Änderung ab."""
        self.screen = QApplication.primaryScreen()
        print("Bildschirm geändert. Neue Geometrie:", self.screen.availableGeometry())
        self.adjust_to_screen()


    def change_url(self, url):
        self.browser.setUrl(QUrl(url))
        self.save_url_to_file(url)

    def save_url_to_file(self, url):
        with open(URL_FILE_PATH, 'w') as file:
            file.write(url)

    def load_url_from_file(self):
        if os.path.exists(URL_FILE_PATH):
            with open(URL_FILE_PATH, 'r') as file:
                return file.read().strip()
        return None

    def toogle_autostart(self):
        PATH = os.path.expanduser("~/.config/autostart/webai.desktop")
        if os.path.exists(PATH):
            os.system("rm "+PATH)
        else:
            os.system("cp /usr/share/x-live/webai/webai.desktop "+PATH)

        if os.path.exists(PATH):
            self.autostart_action.setText("Autostart ✓")
        else:
            self.autostart_action.setText("Autostart □")

    def toggle_window(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            screen_geometry = self.screen.availableGeometry()
            breite = int(screen_geometry.width()*self.prozent)
            max_breite = int(screen_geometry.width())
            hoehe = int(screen_geometry.height())
            xpos = int(screen_geometry.width() - breite)
            #print(hoehe)
        
            if self.max == True:
                self.setGeometry(0, 0, max_breite, hoehe)
                #print("show max")
                #print(breite)
            else:
                self.setGeometry(xpos, 0, breite, hoehe)
                #print("show no max")
                #print(breite)
                
            self.raise_()  # Bringt das Fenster in den Vordergrund

    def max_window(self):
        #screen = app.primaryScreen().availableGeometry()
        screen = self.screen.availableGeometry()
        breite = int(screen.width()*self.prozent)
        max_breite = int(screen.width())
        hoehe = int(screen.height())
        xpos = int(screen.width() - breite)
        print("max")
        if self.max:
            self.setGeometry(xpos, 0, breite, hoehe)
            self.max = False
            self.max_action.setText("Maximieren")
            print("no_max")
        else:
            self.setGeometry(0, 0, max_breite, hoehe)
            self.max = True
            self.max_action.setText("Normale Größe")
            print("max")

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.toggle_window()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
