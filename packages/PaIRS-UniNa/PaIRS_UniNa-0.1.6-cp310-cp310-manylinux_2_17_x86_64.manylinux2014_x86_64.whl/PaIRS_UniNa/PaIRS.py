from .gPaIRS import *

def run():
    gui:gPaIRS
    app,gui=launchPaIRS()
    quitPaIRS(app)

def cleanRun():
    if os.path.exists(lastcfgname):
        os.remove(lastcfgname)
    run()
   
def debugRun():
    gui:gPaIRS
    app,gui=launchPaIRS(flagInputDebug=True)
    quitPaIRS(app)


