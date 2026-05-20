# Desktop Pets

A fun desktop pet application that floats on your screen!

## How to Run

### On Windows 🪟
1. Simply double-click **`run.bat`**
2. It will automatically find Python, install required dependencies, and launch the pet!

### On macOS / Linux 🍎🐧
1. Open your terminal in this folder.
2. Run the script:
   ```bash
   bash run.sh
   ```

## Controls
- **Drag & Drop:** Click and drag the pet to move it around.
- **Right-Click:** Open the menu to start roaming, snap to corners, or quit.

## Customization

You can fully customize your Desktop Pet to use any custom image (such as your own photo, a custom pixel art, or other personal items):

1. **Via the Application Interface (Recommended):**
   - Right-click on the pet on your screen.
   - Select **🖼️ Change Pet Image...** from the menu.
   - Choose any transparent image (`.png`, `.jpg`, etc.) from your computer. The app will automatically configure it and save the preference locally.
   - To go back to the standard pet, simply right-click and select **🔄 Reset to Default Pet**.

2. **Via Local Files:**
   - Drop a file named `custom_pet.png` (or `amma.png` for legacy/private setups) directly in this directory.
   - The app will automatically prioritize detecting and loading these custom local images.

*Note: All custom images, files, and local configuration files (`config.json`) are automatically ignored by Git (`.gitignore`), meaning you can safely customize your pet locally without worrying about accidentally pushing your personal photos or settings to GitHub!*
