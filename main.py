import sys
import os
import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMenu, QInputDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QCursor, QAction
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITESHEET_PATH = os.path.join(SCRIPT_DIR, "amma.png")
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
        self.is_spritesheet = False  # Use single-image mode (amma.png)
        image_path = sys.argv[1] if len(sys.argv) > 1 else SPRITESHEET_PATH
        
        if not os.path.exists(image_path):
            QMessageBox.critical(None, "Missing Image", f"Could not find pet image at:\n{image_path}\n\nPlease place an 'amma.png' file in the folder or run with an image path argument.")
            sys.exit(1)
            
        self.spritesheet = QPixmap(image_path)
        
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
        
        self.is_roaming = False
        self.update_frame()
        self.show()

    def update_frame(self):
        if self.is_spritesheet:
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
        else:
            scaled_pixmap = self.spritesheet.scaled(
                200, 
                200, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.label.setPixmap(scaled_pixmap)
            self.label.resize(scaled_pixmap.width(), scaled_pixmap.height())
            self.resize(scaled_pixmap.width(), scaled_pixmap.height())

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
            pass  # Don't auto-resume roaming after drag

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def showContextMenu(self, pos):
        context_menu = QMenu(self)

        talk_action = QAction("💬  Give Task (Antigravity)", self)
        talk_action.triggered.connect(self.talk_to_antigravity)
        context_menu.addAction(talk_action)

        context_menu.addSeparator()

        # Snap to Position submenu
        snap_menu = QMenu("📌  Snap to Position", self)
        positions = {
            "⬆️ ⬅️  Top Left":     "top-left",
            "⬆️ ➡️  Top Right":    "top-right",
            "⬇️ ⬅️  Bottom Left":  "bottom-left",
            "⬇️ ➡️  Bottom Right": "bottom-right",
            "⚫  Center":           "center",
        }
        for label, anchor in positions.items():
            action = QAction(label, self)
            action.triggered.connect(lambda checked, a=anchor: self.snap_to(a))
            snap_menu.addAction(action)
        context_menu.addMenu(snap_menu)

        context_menu.addSeparator()

        # Toggle roaming
        roam_label = "🛑  Stop Roaming" if self.is_roaming else "🏃  Start Roaming"
        roam_action = QAction(roam_label, self)
        roam_action.triggered.connect(self.toggle_roaming)
        context_menu.addAction(roam_action)

        context_menu.addSeparator()

        quit_action = QAction("❌  Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        context_menu.addAction(quit_action)

        context_menu.exec(pos)

    def snap_to(self, anchor):
        self.is_roaming = False
        screen = QApplication.primaryScreen().geometry()
        margin = 10
        w, h = self.width(), self.height()
        taskbar = 48  # approximate taskbar height
        positions = {
            "top-left":     (margin, margin),
            "top-right":    (screen.width() - w - margin, margin),
            "bottom-left":  (margin, screen.height() - h - taskbar),
            "bottom-right": (screen.width() - w - margin, screen.height() - h - taskbar),
            "center":       ((screen.width() - w) // 2, (screen.height() - h) // 2),
        }
        x, y = positions[anchor]
        self.move(x, y)

    def toggle_roaming(self):
        self.is_roaming = not self.is_roaming

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
        pass  # Roaming no longer auto-resumes; user controls it via menu

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec())
