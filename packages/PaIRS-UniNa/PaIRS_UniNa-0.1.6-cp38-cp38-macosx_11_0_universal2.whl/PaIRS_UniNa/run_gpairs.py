'''run_gpairs.py '''
from .gPaIRS import *
if __name__ == "__main__":
    app,gui=launchPaIRS(True)
    gui.show()
    sys.exit(app.exec())
