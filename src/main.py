import tkinter as tk
from src.ui import NQueenUI

def main():
    root = tk.Tk()
    app = NQueenUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
