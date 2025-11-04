💣 Minesweeper Deluxe
A sleek, animated, and modern version of the classic Minesweeper built with PyQt6.


🧠 About the Game
Minesweeper Deluxe is a reimagined version of the classic puzzle game — built with a modern dark aesthetic, soft neon highlights, and smooth animations.
You can choose difficulty levels, flag mines, and test your logic — all wrapped in a beautiful, responsive PyQt6 GUI.


🎮 Features
✅ Modern neon-dark UI with hover effects
✅ Multiple difficulty levels (Easy / Medium / Hard)
✅ Smooth transitions and animations
✅ Recursive reveal logic for empty tiles
✅ Game state management and win/loss pop-ups
✅ Cross-platform — works on Windows, macOS, and Linux


⚙️ Prerequisites
Before running the game, make sure you have the following installed:

Requirement	Description
🐍 Python 3.10+	Check if installed via python3 --version
📦 pip (Python package manager)	Should come with Python; verify via pip --version


📦 Installation
Run these commands step-by-step in your terminal or command prompt:

# 1️⃣ Clone or download the project
git clone https://github.com/yourusername/minesweeper-deluxe.git
cd minesweeper-deluxe

# 2️⃣ Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate      # (Linux/macOS)
venv\Scripts\activate         # (Windows)

# 3️⃣ Install required dependencies
pip install PyQt6

(Optional but recommended)
If you’re on Linux and get Qt plugin errors (like “Could not load the xcb plugin”), run:

sudo apt install python3-pyqt6.qtbase libxcb-cursor0


🚀 Running the Game
Once everything’s installed, start the game with:

python3 main.py


🎯 Controls
Action	Description
Left Click	Reveal a tile
Right Click / Long Press	Flag or unflag a tile
Win Condition	Reveal all non-mine tiles
Lose Condition	Click on a mine 💥


🧱 File Structure
minesweeper-deluxe/
│
├── main.py             # Main PyQt6 GUI game
├── board.py            # (optional modular split)
├── game_logic.py       # Core tile & reveal logic
├── file_manager.py     # Save/load game state
├── README.md           # You’re here!
└── minesweeper_save.txt # Saved game data


🧩 Tech Stack
Component	Library / Framework
GUI	PyQt6
Language	Python 3
Animation	QPropertyAnimation / Stylesheet hover effects
Save System	JSON / Text serialization


⚠️ License
This project is open-source.
You can modify, distribute, and use it for personal or educational purposes.


💬 Need Help?
If you face any issues (like missing Qt plugins), try:

sudo apt install libxcb-cursor0
pip install --upgrade PyQt6



Or open an issue on GitHub — help will arrive faster than a mine explosion 💥