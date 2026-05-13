import sys
import os
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMenu
from PyQt6.QtGui import QPixmap, QCursor, QAction
from PyQt6.QtCore import Qt, QTimer, QPoint

class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.offset = QPoint()
        
    def initUI(self):
        # Make the window frameless and transparent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Load a default pet image or a color block
        self.label = QLabel(self)
        self.label.resize(100, 100)
        self.label.setStyleSheet("background-color: transparent; border: 5px solid cyan; border-radius: 50px;")
        # If we had a sprite, we would use QPixmap
        # pixmap = QPixmap("ig_idle.png")
        # self.label.setPixmap(pixmap)
        
        self.resize(100, 100)
        
        # Start position
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() // 2, screen.height() // 2)
        
        # Roaming timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.roam)
        self.timer.start(50) # 50ms updates
        
        self.dx = random.choice([-2, 2])
        self.dy = 0
        
        self.show()

    def roam(self):
        # Basic roaming logic
        screen = QApplication.primaryScreen().geometry()
        new_x = self.x() + self.dx
        new_y = self.y() + self.dy
        
        if new_x <= 0 or new_x + self.width() >= screen.width():
            self.dx = -self.dx
        
        self.move(self.x() + self.dx, self.y() + self.dy)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.offset = event.pos()
        elif event.button() == Qt.MouseButton.RightButton:
            self.showContextMenu(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def showContextMenu(self, pos):
        context_menu = QMenu(self)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        context_menu.addAction(quit_action)
        
        talk_action = QAction("Talk to Antigravity", self)
        talk_action.triggered.connect(self.talk_to_antigravity)
        context_menu.addAction(talk_action)
        
        context_menu.exec(pos)

    def talk_to_antigravity(self):
        print("Pet is attempting to access Antigravity chatbox abilities...")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec())
