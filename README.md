🧨 Minesweeper (Python)

A fully functional Minesweeper game built in Python, featuring a clean separation between game logic and user interface.

This project started as a console-based implementation and was later extended into a GUI and mobile-ready architecture, making it a great example of scalable Python design.

🚀 Features
Classic Minesweeper gameplay
Configurable board size and mine count
Flood-fill reveal for empty cells
Flagging system
Win/loss detection
Chording (auto-reveal adjacent cells when flags match number)
Multiple UI implementations:
Console version
Tkinter GUI version
Kivy (mobile-ready) version
🧠 Architecture

The project is built with a clear separation of concerns:

minesweeper.py → Core game engine
GUI layer (Tkinter / Kivy) → Handles rendering and user input

This allows the same game logic to be reused across different interfaces.

🖥 Console Version

Run the original console-based game:

python minesweeper.py
Controls:
r ROW COL   -> reveal cell
f ROW COL   -> flag/unflag cell
q           -> quit game
🪟 GUI Version (Tkinter)

Run the desktop GUI:

python minesweeper_gui.py
Controls:
Left-click → Reveal cell
Right-click → Flag cell
📱 Mobile Version (Kivy)

Run the mobile-friendly version:

python minesweeper_mobile.py

Note: Designed for touch interfaces and can be extended for iOS/Android using Kivy tooling.

⚙️ Installation
Clone the repository:
git clone https://github.com/YOUR_USERNAME/minesweeper-python.git
cd minesweeper-python
Install dependencies:
pip install kivy

(Tkinter is included with most Python installations)

🛠 Future Improvements
Timer and mine counter
Difficulty selection (Beginner / Intermediate / Expert)
Improved UI/UX and animations
Sound effects and haptics
High score tracking
App Store / mobile deployment
📚 What I Learned
Structuring Python projects with separation of logic and UI
Implementing grid-based game mechanics
Flood-fill algorithms using queues
Event-driven programming (GUI and touch input)
Preparing Python apps for cross-platform deployment
🤝 Contributing

Contributions, suggestions, and improvements are welcome.

📄 License

This project is open-source and available under the MIT License.

👨‍💻 Author

Peter Thomson

⭐ Acknowledgements

Inspired by the classic Minesweeper game.
