# AWS Gomoku Game

A simple Gomoku (Five in a Row) game implemented with Pygame, using official AWS EC2 and S3 icons as game pieces.

## Game Description

Gomoku is a traditional Japanese board game where players take turns placing stones on a grid. The goal is to get five stones in a row horizontally, vertically, or diagonally. In this AWS-themed version:

- Player 1 uses EC2 icons (orange)
- Player 2 uses S3 icons (blue)
- The game is played on a 15x15 grid

## How to Play

1. Run the game: `python gomoku.py`
2. Click on the board to place your icon
3. Take turns with another player
4. Get 5 icons in a row to win
5. Press 'R' to reset the game

## Requirements

- Python 3.x
- Pygame
- NumPy

## Installation

```bash
# Create a virtual environment (optional)
python -m venv pygame_venv
source pygame_venv/bin/activate  # On Linux/Mac
# or
pygame_venv\Scripts\activate  # On Windows

# Install dependencies
pip install pygame numpy
```

## Project Structure

```
pygame_project/
├── assets/
│   ├── images/
│   │   ├── Res_Amazon-EC2_Instances_48.png
│   │   └── Res_Amazon-Simple-Storage-Service_S3-Standard_48.png
├── gomoku.py
└── README.md
```

## Credits

The AWS service icons are the property of Amazon Web Services and are used in accordance with the AWS trademark guidelines.
