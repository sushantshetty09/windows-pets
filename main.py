import sys
import os
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMenu, QInputDialog
from PyQt6.QtGui import QPixmap, QCursor, QAction
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect

SPRITESHEET_PATH = r"C:\Users\sadiq\.codex\pets\sparky\spritesheet.webp"
FRAME_WIDTH = 192
FRAME_HEIGHT = 208

ANIMATIONS = {
    "idle": {"row": 0, "frames": 6},
    "running-right": {"row": 1, "frames": 8},
    "running-left": {"row": 2, "frames": 8},
    "waving": {"row": 3, "frames": 4},
    "jumping": {"row": 4, "frames": 5},
    "failed": {"row": 5, "frames": 8},
    "waiting": {"row": 6, "frames": 6},
    "running": {"row": 7, "frames": 6},
    "review": {"row": 8, "frames": 6},
}

class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()
        self.spritesheet = QPixmap(SPRITESHEET_PATH)
        self.current_anim = "idle"
        self.frame_index = 0
        
        self.initUI()
        self.offset = QPoint()
        
    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.label = QLabel(self)
        self.label.resize(FRAME_WIDTH // 2, FRAME_HEIGHT // 2)
        
        self.resize(FRAME_WIDTH // 2, FRAME_HEIGHT // 2)
        
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() // 2, screen.height() // 2)
        
        # Animation timer
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update_frame)
        self.anim_timer.start(100) # 100ms per frame

        # Physics timer
        self.physics_timer = QTimer(self)
        self.physics_timer.timeout.connect(self.update_physics)
        self.physics_timer.start(16) # ~60 FPS
        
        self.dx = random.choice([-3, 3])
        self.dy = 0
        self.gravity = 1
        
        self.is_roaming = True
        self.update_frame()
        self.show()

    def update_frame(self):
        anim_data = ANIMATIONS[self.current_anim]
        row = anim_data["row"]
        frames = anim_data["frames"]
        
        self.frame_index = (self.frame_index + 1) % frames
        
        # Extract the specific frame
        rect = QRect(self.frame_index * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT)
        frame_pixmap = self.spritesheet.copy(rect)
        
        # Scale the size in half
        scaled_pixmap = frame_pixmap.scaled(
            FRAME_WIDTH // 2, 
            FRAME_HEIGHT // 2, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.FastTransformation
        )
        self.label.setPixmap(scaled_pixmap)
        self.label.resize(FRAME_WIDTH // 2, FRAME_HEIGHT // 2)
        self.resize(FRAME_WIDTH // 2, FRAME_HEIGHT // 2)

    def update_physics(self):
        if self.is_roaming:
            screen = QApplication.primaryScreen().geometry()
            
            # Apply gravity
            self.dy += self.gravity
            
            new_x = self.x() + self.dx
            new_y = self.y() + self.dy
            
            # Floor collision (approx taskbar height is 40)
            floor_y = screen.height() - 40 - self.height()
            if new_y >= floor_y:
                new_y = floor_y
                self.dy = 0
                
                # 1% chance to jump when on the ground
                if random.random() < 0.01:
                    self.dy = -15
            
            # Wall collisions
            if new_x <= 0 or new_x + self.width() >= screen.width():
                self.dx = -self.dx
                new_x = self.x() + self.dx
            
            # Set animation state based on movement
            if self.dy != 0:
                self.current_anim = "jumping"
            else:
                self.current_anim = "running-right" if self.dx > 0 else "running-left"
            
            self.move(new_x, new_y)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.offset = event.pos()
            self.is_roaming = False
            self.current_anim = "waving"
        elif event.button() == Qt.MouseButton.RightButton:
            self.showContextMenu(event.globalPosition().toPoint())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_roaming = True

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def showContextMenu(self, pos):
        context_menu = QMenu(self)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        context_menu.addAction(quit_action)
        
        talk_action = QAction("Give Task (Antigravity)", self)
        talk_action.triggered.connect(self.talk_to_antigravity)
        context_menu.addAction(talk_action)
        
        context_menu.exec(pos)

    def talk_to_antigravity(self):
        self.is_roaming = False
        self.current_anim = "waiting"
        
        task, ok = QInputDialog.getText(self, "Antigravity Chatbox", "What task should I perform?")
        
        if ok and task:
            # Simulate thinking
            self.current_anim = "running"
            print(f"Task received: {task}")
            # For now, append to a file to simulate IPC
            with open("pet_tasks.txt", "a") as f:
                f.write(f"Task: {task}\n")
                
            # Start workflow transitions
            QTimer.singleShot(3000, self.finish_task)
        else:
            self.is_roaming = True

    def finish_task(self):
        self.current_anim = "review"
        QTimer.singleShot(2000, self.resume_roaming)

    def resume_roaming(self):
        self.is_roaming = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec())
