#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        DEFAULT_URL = "https://chat.openai.com/"
        # Erstelle das WebEngineView und setze es als zentrales Widget
        self.max = False
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # Lade eine Webseite
        self.browser.setUrl(QUrl(DEFAULT_URL))
        
        # bildschirmgröße berechnen
        screen = app.primaryScreen().availableGeometry()
        breite = int(screen.width()*0.43)
        hoehe = int(screen.height())
        xpos=int(screen.width()-breite)
        
        
        # Fenster eigenschaften setzen
        self.setWindowIcon(QIcon('/usr/share/pixmaps/webai.png'))
        self.setGeometry(xpos, 0, breite, hoehe)
        self.setFixedHeight(hoehe)
        self.setWindowFlag(Qt.FramelessWindowHint) # Fensterdekoration entfernen
        self.setWindowTitle("X-Live-WebAI")
        #self.show()

        # Tray Icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("/usr/share/pixmaps/webai.png"))
        self.tray_icon.setToolTip("X-Live Webai")

        # Tray Menu
        tray_menu = QMenu()
        open_action = QAction("öffnen/verstecken", self)
        exit_action = QAction("schließen", self)
        self.max_action = QAction("Maximieren", self)

        open_action.triggered.connect(self.toggle_window)
        exit_action.triggered.connect(QApplication.instance().quit)
        self.max_action.triggered.connect(self.max_window)

        tray_menu.addAction(open_action)
        tray_menu.addAction(self.max_action)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Minimize to Tray
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # Start minimized to tray
        self.hide()

    def toggle_window(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()  # Bringt das Fenster in den Vordergrund

    def max_window(self):
        screen = app.primaryScreen().availableGeometry()
        breite = int(screen.width()*0.33)
        max_breite = int(screen.width())
        hoehe = int(screen.height())
        xpos=int(screen.width()-breite)
        if self.max:
            self.setGeometry(xpos, 0, breite, hoehe)
            self.max = False
            self.max_action.setText("Maximieren")
        else:
            self.setGeometry(0, 0, max_breite, hoehe)
            self.max = True
            self.max_action.setText("Normale Größe")

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.toggle_window()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    # Remove main_window.show() to start minimized
    sys.exit(app.exec_())
