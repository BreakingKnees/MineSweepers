# 💣 Minesweeper — Python GUI Edition  

A modern, animated take on the classic **Minesweeper** game built with **Python** and **PyQt6 / Tkinter**.  
Enjoy smooth visuals, multiple difficulty levels, and a stylish interface that goes beyond the boring grid.

---

## 🕹️ Features

✨ **Beautiful GUI:** Modern dark theme with animations  
🎮 **Difficulty Levels:** Easy • Medium • Hard  
⚙️ **Recursive Reveal:** Automatically clears empty regions  
💾 **Save / Load System:** Game progress saved to `minesweeper_save.txt`  
🏆 **Win Detection:** Clear all safe cells to win  
💥 **Explosion Animation:** Visual feedback on hitting a mine  

---

## 🧩 Project Structure
Minesweeper/

├── main.py # Entry point — main menu + GUI + difficulty selector

├── board.py # Handles board drawing, cell objects & click events

├── game_logic.py # Core logic — mine generation, recursion, win/loss

├── file_manager.py # Save / load system for game state

├── assets/ # Icons, sprites, sounds (optional)

└── README.md # You are here 💡

---

## ⚙️ Setup & Installation

> Works on **Windows**, **macOS**, and **Linux** (tested on Pop!_OS)

### 1️⃣ Make sure Python 3 is installed

Run:
```bash
python3 --version
```
If not installed, get it from python.org/downloads
## 2️⃣ Create and activate a virtual environment (optional but recommended)
```bash
python3 -m venv venv
source venv/bin/activate   # On Linux / macOS
venv\Scripts\activate      # On Windows
```
## 3️⃣ Install dependencies'
Install everything required to run the GUI version:
```bash
sudo apt install python3-tk    # Linux
```
## 🚀 Running the Game
```bash
cd ~/ms
python3 main.py
```
