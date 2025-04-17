import tkinter as tk
from game import WordGame

if __name__ == "__main__":
    root = tk.Tk()
    game = WordGame(root)
    root.mainloop()