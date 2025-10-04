"""
Kingdom Game Version 3.0 - Main Entry Point
"""

import tkinter as tk
from src.main import KingdomGame
from src.ui.gui import KingdomGameGUI

def main():
    """Main entry point for Kingdom Game Version 3.0"""
    root = tk.Tk()
    game_controller = KingdomGame()
    gui = KingdomGameGUI(root, game_controller)
    game_controller.set_gui(gui)
    root.mainloop()

if __name__ == "__main__":
    main()