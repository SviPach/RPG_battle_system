# 🎮 RPG Battle System

A simple Python-based text RPG battle system with turn-based combat.

## ✨ Features
- Turn-based combat system
- Leveling-up and attribute upgrade mechanics
- Multiple characters and simple party management
- Colored text output in the terminal
- Random events and enemy AI behavior
- Mana/health potions
- Equipment

## 📦 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rpg-battle-system.git
   cd rpg-battle-system
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
## ▶️ Usage
Run the main game file:
  ```bash
    python main.py
  ```

## 📂 Project Structure
  ```bash
  .
  ├── classes/             # Game logic and modules
      ├── __init__.py      # __init__ for the project
      ├── bcolors          # Console colors
      ├── equipment.py     # Equipment class
      ├── get_choice.py    # Function for choosing actions
      ├── line_eraser.py   # Line eraser function (escape-sequence)
      ├── magic.py         # Magic class
      ├── person.py        # Person class
      └── potion.py        # Potion class
  ├── .flake8              # flake8 config
  ├── LICENCE              # Licence
  ├── README.md
  ├── main.py              # Entry point
  └── requirements.txt     # Dependencies
  ```
## 🛠 Technologies
- Python 3.11+
- colorama for terminal colors
- Standard library modules (random, math, etc.)
