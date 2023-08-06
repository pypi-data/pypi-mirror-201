'''run_gpairs.py '''
from .gPaIRS import *
if __name__ == "__main__":
    app,gui=launchPaIRS(True)
    gui.show()
    app.exec()
    app.quit()
    app=None
