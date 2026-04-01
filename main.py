"""
Modul: main.py
Descriere: Se intra in aplicatie
Aici se  initializeaza fereastra principala Tkinter si porneste aplicatia.
"""

import tkinter as tk
from ui_app import ImageApp

if __name__ == "__main__":
    # Se initializeaza instanta principala  interfetei grafice
    root = tk.Tk()

    # Se porneste clasa aplicatiei  importata din ui_app.py
    app = ImageApp(root)

    # Se mentinem aplicatia deschisa pana la inchiderea ferestrei
    root.mainloop()