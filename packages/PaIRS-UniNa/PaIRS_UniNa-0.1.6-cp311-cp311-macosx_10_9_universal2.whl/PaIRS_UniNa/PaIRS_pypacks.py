#PrintTA.flagPriority=PrintTAPriority.always
Flag_DEBUG=True #False
Flag_DEBUG_PARPOOL=False
pwddbg='Buss4Co1Pied1'
time_warnings_debug=-1 #10000 #milliseconds  #5000

basefold='./'
basefold='/Users/gerardo/Desktop/img/img1/'  #gerardo mac
#basefold='/Users/gerardo/Desktop/PIV_Img/swirler_png/'  #gerardo mac
#basefold='C:/desk/PIV_Img/swirler_png/'  #gerardo windows
basefold='C:/desk/PIV_Img/img1/'  #gerardo windows
#basefold='B:/dl/apairs/jetcross'
#basefold='../img/img1/'   #gerardo PIV_project
#basefold='L:/2022.02.23/Q5500_hd0/' #gerardo hd esterno
basefold_DEBUG=basefold

#fontName='Inter'
#fontName='Cambria'
fontName='Arial'
import platform
if (platform.system() == "Linux"):
  fontName='sans-serif'

Flag_SHOWSPLASH=False
Flag_GRAPHICS=True  #if True PaIRS plots while processing
Flag_NATIVEDIALOGS=True
Flag_DISABLE_onUpdate=False
Flag_RESIZEONRUN=False
Flag_GROUPSEPARATOR=True

imin_im_pair=1 #minimum index value for image pair

f_empty_width=250  #blank space in scrollable area within the main window
time_ScrollBar=250 #time of animation of scroll area
time_fun2_async=0  #time to test async callbacks
time_showSplashOnTop=250

icons_path="icons/"

from psutil import cpu_count
NUMTHREADS_PIV=cpu_count(logical=True)#-1
if NUMTHREADS_PIV<1: NUMTHREADS_PIV=1
NUMTHREADS_PIV_MAX=NUMTHREADS_PIV
ParFor_sleepTime=0.1
#multithreading
FlagStopWorkers=[0]#messo qui ma utilizzato solo da min e PIV
NUMTHREADS_gPaIRS=0
SleepTime_Workers=0.5 #for multithreading and other stuff
timeOutWorker=0  # used in parfor when the proces is stuck

from .__init__ import __version__,__year__,__mail__
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import*
from PySide6.QtGui import *
from PySide6.QtWidgets import*
from typing import cast
if Flag_DEBUG_PARPOOL: import debugpy

import numpy as np
import scipy.io, pickle
from PIL import Image
from PIL.ImageQt import ImageQt
import sys, os, glob, copy, re, traceback, datetime, uuid
from time import sleep as timesleep
from collections import namedtuple
from .plt_util import writePlt, readPlt
#from multiprocessing import cpu_count

from .tAVarie import *
deltaTimePlot=0.75
import concurrent.futures
import gc#garbage collection si può eliminare
import psutil

class ColorPrint:
    def __init__(self,flagTime=False,prio=PrintTAPriority.medium,faceStd=PrintTA.faceStd):
        self.flagTime=flagTime
        self.prio=prio
        self.faceStd=faceStd
        if flagTime:
            self.white = lambda flagReset=0, *args, **kwargs: PrintTA(PrintTA.white, faceStd,  prio).prTime(flagReset,*args,**kwargs)
            self.red = lambda flagReset=0, *args, **kwargs: PrintTA(PrintTA.red, faceStd,  prio).prTime(flagReset,*args,**kwargs)
            self.green = lambda flagReset=0, *args, **kwargs: PrintTA(PrintTA.green, faceStd,  prio).prTime(flagReset,*args,**kwargs)
            self.blue = lambda flagReset=0, *args, **kwargs: PrintTA(PrintTA.blue, faceStd,  prio).prTime(flagReset,*args,**kwargs)
            self.cyan = lambda flagReset=0, *args, **kwargs: PrintTA(PrintTA.cyan, faceStd,  prio).prTime(flagReset,*args,**kwargs)
            self.magenta = lambda flagReset=0, *args, **kwargs: PrintTA(PrintTA.magenta, faceStd,  prio).prTime(flagReset,*args,**kwargs)
            self.yellow = lambda flagReset=0, *args, **kwargs: PrintTA(PrintTA.yellow, faceStd,  prio).prTime(flagReset,*args,**kwargs)
        else:
            self.white = PrintTA(PrintTA.white, faceStd,  prio).pr 
            self.red = PrintTA(PrintTA.red, faceStd,  prio).pr
            self.green = PrintTA(PrintTA.green, faceStd,  prio).pr
            self.blue = PrintTA(PrintTA.blue, faceStd,  prio).pr
            self.cyan = PrintTA(PrintTA.cyan, faceStd,  prio).pr
            self.magenta = PrintTA(PrintTA.magenta, faceStd,  prio).pr
            self.yellow = PrintTA(PrintTA.yellow, faceStd,  prio).pr

class GPaIRSPrint:
    General=ColorPrint()
    Info=ColorPrint()
    Time=ColorPrint(flagTime=True,faceStd=PrintTA.faceUnderline)
    Error=ColorPrint(faceStd=PrintTA.faceBold)
    Process=ColorPrint()
    Callback=ColorPrint()


pri=GPaIRSPrint()
printTypes={
            'General': True,
            'Info': True,
            'Time': False,
            'Error':True,
            'Process': False,
            'Callback':False,
            }

def activateFlagDebug(Flag=True):
    ''' used to activate the debug mode;  when called with false disables'''
    Flag_DEBUG=Flag
    PrintTA.flagPriority=PrintTAPriority.veryLow   if  Flag_DEBUG else PrintTAPriority.always
    global basefold
    from .gPaIRS import Flag_fullDEBUG
    if not Flag_fullDEBUG:
        basefold='./'
    else:
        basefold=basefold_DEBUG

PaIRS_Header=f'PaIRS - version {__version__}\n'+\
    'Particle Image Reconstruction Software\n'+\
    f'(C) {__year__} Gerardo Paolillo & Tommaso Astarita.\nAll rights reserved.\n'+\
    f'email: {__mail__}\n'+\
    '****************************************\n'

from .parForMulti import *
#from pkg_resources import resource_filename
from .parForMulti import ParForMul

import faulthandler # per capire da dove vengono gli errori c
faulthandler.enable()

if __package__ or "." in __name__:
  import PaIRS_UniNa.PaIRS_PIV as PaIRS_lib
else:
  import sys
  if (platform.system() == "Darwin"):
    sys.path.append('../lib/mac')
  else:
    #sys.path.append('PaIRS_PIV')
    sys.path.append('../lib')
  import PaIRS_PIV as PaIRS_lib

if __package__ or "." in __name__:
    from pkg_resources import resource_filename
    foldPaIRS=resource_filename(__package__,'')+"\\"
    foldPaIRS=foldPaIRS.replace('\\','/')
else:
    foldPaIRS='./'

class outExt:
    cfg='.pairs_cfg'
    dum='.pairs_dum'
    min='.pairs_min'
    piv='.pairs_piv'
    pro='.pairs_pro'

lastcfgname='lastuicfg'+outExt.cfg

icons_path=foldPaIRS+"icons/"
lastcfgname=foldPaIRS+lastcfgname
pro_path=foldPaIRS+"pro/"
if not os.path.exists(pro_path):
    os.mkdir(pro_path)
custom_list_file="pro_list.txt"


exts = Image.registered_extensions()
supported_exts = sorted({ex for ex, f in exts.items() if f in Image.OPEN})
text_filter = "Common image files (*.bmp *.gif *.ico *.jpeg *.jpg *.png *.tif *.tiff *.webp"\
   + ");;"+" ;;".join(["{} ".format(fo[1:]) +"(*{})".format(fo) for fo in supported_exts])
#text_filter = "All files (*"\
#   + ");;"+" ;;".join(["{} ".format(fo[1:]) +"(*{})".format(fo) for fo in supported_exts])
#text_filter = "All files ("+ " ".join(["*{}".format(fo) for fo in supported_exts])\
#   + ");;"+" ;;".join(["{} ".format(fo[1:]) +"(*{})".format(fo) for fo in supported_exts])

if Flag_NATIVEDIALOGS: 
    optionNativeDialog=QFileDialog.Options()
else:
    optionNativeDialog=QFileDialog.Option.DontUseNativeDialog 
 
def warningDialog(self,Message,time_milliseconds=0,flagScreenCenter=''):
    if Message:
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Warning!")
        dlg.setText(str(Message))
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.setIcon(QMessageBox.Warning)
        if self:
            dlg.setFont(self.font())
            c=dlg.findChildren(QObject)
            for w in c:
                if hasattr(w,'setFont'):
                    font=w.font()
                    font.setFamily(fontName)
                    w.setFont(font)
        #dlg.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint) 
        if flagScreenCenter and hasattr(self,'MaxGeom'):
            geom=dlg.geometry()
            geom.moveCenter(self.MaxGeom.center())
            dlg.setGeometry(geom)
        if time_milliseconds:
            QTimer.singleShot(time_milliseconds, lambda : dlg.done(0))
        else:
            if Flag_DEBUG and time_warnings_debug>=0:
                QTimer.singleShot(time_warnings_debug, lambda : dlg.done(0))                
        dlg.exec()

def questionDialog(self,Message,icon=QMessageBox.Warning):
    dlg = QMessageBox(self)
    dlg.setWindowTitle("Warning!")
    dlg.setText(str(Message))

    dlg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
    dlg.setDefaultButton(QMessageBox.Yes)
    dlg.setIcon(icon)
    if self:
        dlg.setFont(self.font())
        c=dlg.findChildren(QObject)
        for w in c:
            if hasattr(w,'setFont'):
                font=w.font()
                font.setFamily(fontName)
                w.setFont(font)
    button = dlg.exec()
    return button==QMessageBox.Yes    

def inputDialog(self,title,label,icon=None,palette=None,completer_list=[],width=0,flagMouseCenter=False,flagScreenCenter=False):
    dlg = QtWidgets.QInputDialog(self)
    dlg.setWindowTitle(title)
    dlg.setLabelText(label)
    dlg.setTextValue("")
    if icon:
        dlg.setWindowIcon(icon)
    if palette:
        dlg.setPalette(palette)
    le = dlg.findChild(QtWidgets.QLineEdit)
    if self:
        dlg.setFont(self.font())
        c=dlg.findChildren(QObject)
        for w in c:
            if hasattr(w,'setFont'):
                font=w.font()
                font.setFamily(fontName)
                w.setFont(font)
    
    if len(completer_list):
        completer = QtWidgets.QCompleter(completer_list, le)
        completer.setCompletionMode(QCompleter.CompletionMode(1))
        le.setCompleter(completer)

    if not width: width=int(0.5*self.width())
    dlg.resize(width,dlg.height())
    dlg.updateGeometry()

    if flagMouseCenter:
        geom = dlg.geometry()
        geom.moveCenter(QtGui.QCursor.pos())
        dlg.setGeometry(geom)

    if flagScreenCenter and hasattr(self,'MaxGeom'):
        geom=dlg.geometry()
        geom.moveCenter(self.MaxGeom.center())
        dlg.setGeometry(geom)
    
    c=dlg.findChildren(QObject)
    for w in c:
        if hasattr(w,'setFont'):
            font=w.font()
            font.setFamily(fontName)
            w.setFont(font)

    ok, text = (
        dlg.exec() == QtWidgets.QDialog.Accepted,
        dlg.textValue(),
    )
    return ok, text
  
def errorDialog(self,Message,*args):
    if len(args): time_milliseconds = args[0]
    else:  time_milliseconds=0
    if Message:
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Warning!")
        dlg.setText(str(Message))
        copy_butt = dlg.addButton('Copy error to clipboard', QtWidgets.QMessageBox.YesRole)
        copy_butt.clicked.disconnect()
        def copy_fun():
           QApplication.clipboard().setText(Message)
           dlg.done(0)
        copy_butt.clicked.connect(copy_fun)
        ok_butt = dlg.addButton('Ok', QtWidgets.QMessageBox.YesRole)
        dlg.setIcon(QMessageBox.Critical)
        if self:
            dlg.setFont(self.font())
            c=dlg.findChildren(QObject)
            for w in c:
                if hasattr(w,'setFont'):
                    font=w.font()
                    font.setFamily(fontName)
                    w.setFont(font)
        #dlg.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint) 
        if time_milliseconds>=0:
            QTimer.singleShot(time_milliseconds, lambda : dlg.done(0))
        else:
            if Flag_DEBUG and time_warnings_debug>=0:
                QTimer.singleShot(time_warnings_debug, lambda : dlg.done(0))                
        dlg.exec()

def printException(stringa='',flagMessage=Flag_DEBUG,flagDispDialog=False,exception=None):  #timemilliseconds=-1 ***
    ''' used to print when an exception is raised TA has decided that the printing function is a simple
    print in this way we cannot have any problems when printing in non-compatible terminals
    use with something like

    try:
        a=1/0
    except :#non need to put a variable al the info are in traceback
        printException()
    * stringa is an additional string (to specify the point where the error comes from) 
    * flagMessage is a flag, if true the error message is generated; default value is Flag_DEBUG
    * flagDispDialog is a flag, if true a critical dialog appears after the exception
    * exception is the exception, normally you don't need it but for parForMul is required
    '''
    #print(f'***** ParForMul Exception *****  Deltat={time()-PrintTA.startTime}\n{traceback.format_exc()}',*args,**kwargs)
    #print(sys.exc_info()[2])
    Message=""
    if flagMessage or flagDispDialog:
        Message+=f'Please, mail to: {__mail__}\n\n'
        Message+=f'***** PaIRS Exception *****  time={time()-PrintTA.startTime}\n'+stringa
        Message+=f'***** traceback.print_exc() *****  \n'
        if exception is None:
          Message+=traceback.format_exc()
        else:
          Message+=''.join(traceback.format_exception(exception))
        Message+=f'***** traceback.extract_stack() *****  \n'
        # to print all the queue comment if not needed
        for st in traceback.format_list(   traceback.extract_stack()):
            if 'PAIRS_GUI' in st and 'printException'not in st:# limits to files that have  PAIRS_GUI in the path
                Message+=st
        Message+=f'***** PaIRS Exception -> End *****\n'
        if Flag_DEBUG: print(Message)
        #errorDialog(None,Message,timemilliseconds) ***
        if flagDispDialog:
            WarningMessage=f'PaIRS Exception!\n\n'+f'Do you want to copy the error message to the clipboard so that you can send it to: {__mail__}?'
            flagYes=questionDialog(None,WarningMessage,QMessageBox.Critical)
            if flagYes:
                QApplication.clipboard().setText(Message)
    return Message
   
def noPrint(*args,**kwargs):
    pass

#import unidecode
def myStandardPath(path):
    #path=unidecode.unidecode(path)
    currpath=path
    if currpath:
        while currpath[-1]==" ": currpath=currpath[:-1]
    currpath=re.sub(r'\\+',r'/',currpath)
    currpath=currpath+'/'
    currpath=re.sub('/+', '/',currpath)
    return currpath

def myStandardRoot(root):
    #root=unidecode.unidecode(root)
    currroot=root
    if currroot:
        while currroot[-1]==" ": currroot=currroot[:-1]
    currroot=re.sub(r'\\+',r'/',currroot)
    currroot=re.sub('/+', '/',currroot)
    return currroot

def findFiles_sorted(pattern):
    list_files=glob.glob(pattern)
    files=sorted([re.sub(r'\\+',r'/',f) for f in list_files],key=str.lower)
    return files

def transfIm(OUT,flagTransf:int=2,Images:list=[],flagRot=1):
    ''' the output is a copy (not deep) of  the input list)
    flagTransf==0 solo img
    flagTransf==1 solo piv
    flagTransf==2 solo entrambi (default)
    '''
    if  len(Images)==0: return

    if flagTransf==1:  #solo PIV
        ops=OUT.aimop
    else:
        if OUT.h>0 and OUT.w>0:
          for i,_ in enumerate(Images):
              Images[i]=Images[i][OUT.y:OUT.y+OUT.h,OUT.x:OUT.x+OUT.w]#limita l'img
        ops=OUT.bimop if flagTransf==0 else OUT.vecop
    
    
    if len(ops):
        for i,_ in enumerate(Images):# non funziona se si fa il normale ciclo for img in Images
            for op in ops:
                if op==1:  #rot 90 counter
                    Images[i]=np.rot90(Images[i],-1*flagRot)
                elif op==-1: #rot 90 clock
                    Images[i]=np.rot90(Images[i],1*flagRot)
                elif op==3: #flip
                    Images[i]=np.flipud(Images[i])
                elif op==2:
                    Images[i]=np.fliplr(Images[i])
            Images[i]=np.ascontiguousarray(Images[i])
    return Images # the input list is also changed accordingly but it may come in handy in some situation in order to avoid explicitly make a copy 



def transfVect(OUT,PIV):
    x,y,u,v=transfIm(OUT,flagTransf=1,Images=[PIV.x,PIV.y,PIV.u,PIV.v],flagRot=1)# l'output non sarebbe necessario ma così mi fa anche la copia (per ora virtuale)
    for op in OUT.aimop: 
        if op==-1:  #rot 90 counter
            # PIV.u,PIV.v=PIV.v,-PIV.u #questa da errore penso perchè non riesce a fare la copia
            u,v=v,-u
            x,y=y,OUT.w-x
        elif op==1: #rot 90 clock
            u,v=-v,u
            x,y=OUT.h-y,x
        elif op==2:#flip
            u=-u
            x=OUT.w-x
        elif op==3: #flip
            v=-v
            y=OUT.h-y
    return x,y,u,v


def readCustomListFile():
    custom_list=[]
    filename=pro_path+custom_list_file
    if os.path.exists(filename):
        with open(pro_path+custom_list_file,'r') as file:
            while True:
                line = file.readline()
                if not line:
                    break   
                else:
                    l=line.strip()
                    if l: custom_list.append(l)
            file.close()
    return custom_list

def setCustomList(task):
    custom_list=readCustomListFile()
    for k,name in enumerate(custom_list):
        filename=pro_path+name+outExt.pro
        try:
            with open(filename,'rb') as file:
                var=pickle.load(file)
                task(var,name)
        except Exception as inst:
            pri.Error.red(f'Error while loading custom process file {filename}\t[from list]:\n{traceback.print_exc}\n\n{inst}')
            custom_list.pop(k)
            if os.path.exists(filename):
                os.remove(filename)
    profiles=glob.glob(pro_path+f"*{outExt.pro}")
    for f in profiles:
        name=os.path.basename(f)[:-10]
        if not name in custom_list:
            filename=myStandardRoot(f)
            try:
                with open(filename,'rb') as file:
                    var=pickle.load(file)
                    task(var,name)
                    custom_list.append(name)
            except Exception as inst:
                pri.Error.red(f'Error while loading custom process file {filename}\t[from disk]:\n{traceback.print_exc}\n\n{inst}')
                if os.path.exists(filename):
                    os.remove(filename)
    rewriteCustomList(custom_list)
    return custom_list

def rewriteCustomList(custom_list):
    filename=pro_path+custom_list_file
    with open(filename,'w') as file:
        for c in custom_list:
            file.write(c+'\n')
        file.close()

PlainTextConverter=QtGui.QTextDocument()
def toPlainText(text):
    PlainTextConverter.setHtml(text) #for safety
    return PlainTextConverter.toPlainText()




