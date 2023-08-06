from .PaIRS_pypacks import *
#from ui_Tree_Tab import Ui_TreeTab

QLocale.setDefault(QLocale.Language.English)
curr_locale = QLocale()

InitCheck=True   #False=Collap closed, True=opened
#fonts
font_italic=True
font_weight=QFont.DemiBold
backgroundcolor_changing=" background-color: rgb(255,230,230);"
color_changing="color: rgb(33,33,255); "+backgroundcolor_changing
color_changing_black="color: rgb(0,0,0); "+backgroundcolor_changing

#********************************************* Operating Widgets
def setSS(b,style):
    ss=f"{b.metaObject().className()}{'{'+style+'}'}\\nQToolTip{'{'+b.initialStyle+'}'}"
    return ss

class MyTabLabel(QtWidgets.QLabel):
    def __init__(self,parent):
        super().__init__(parent)
        #self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.addfuncclick={}

    def mousePressEvent(self, event):
        for f in self.addfuncclick:
             self.addfuncclick[f]()
        return super().mousePressEvent(event)

#MyQLineEdit=QtWidgets.QLineEdit
class MyQLineEdit(QtWidgets.QLineEdit):
    def __init__(self,parent):
        super().__init__(parent)
        self.addlab=QtWidgets.QLabel()
        self.addwid=[]
        self.initFlag=False
        self.styleFlag=False
        self.addfuncin={}
        self.addfuncout={}
        self.addfuncreturn={}
        self.FlagCompleter=False
        self.FunSetCompleterList=lambda: None

    def setup(self):
        if not self.initFlag:
            self.initFlag=True
            self.font_changing = QtGui.QFont(self.font())
            self.font_changing.setItalic(font_italic)
            self.font_changing.setWeight(font_weight)
            children=self.parent().children()[:]
            self.bros=children+self.addwid
            for b in self.bros:
                hasStyleFlag=hasattr(b,'styleFlag')
                if hasattr(b,'setStyleSheet'):
                    if hasStyleFlag:
                        if b.styleFlag: continue
                    b.flagS=True
                    b.initialStyle=b.styleSheet()
                    b.setEnabled(False)
                    b.disabledStyle=b.styleSheet()
                    b.setEnabled(True)
                    b.setStyleSheet(setSS(b,b.initialStyle))
                else:
                    b.flagS=False
                if hasattr(b,'setFont'):
                    b.flagF=True
                    b.initialFont=b.font()
                else:
                    b.flagF=False
                if hasStyleFlag: b.styleFlag=True

    def setup2(self):
        for b in self.bros:
            if hasattr(b,'bros'):
                self.bros=self.bros+b.bros
        self.bros=[*set(self.bros)]

    def setCompleterList(self):
        if not self.FlagCompleter:
            self.FunSetCompleterList()
            self.FlagCompleter=True
        self.showCompleter()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event) #to preserve classical behaviour before adding the below
        self.setCompleterList()

    def focusInEvent(self, event):
        super().focusInEvent(event)
        for f in self.addfuncin:
            self.addfuncin[f]()
        self.focusInFun()
    
    def setFocus(self):
        super().setFocus()
        self.focusInFun()

    def focusInFun(self):
        self.setCompleterList()
        if not self.font()==self.font_changing:
            self.setStyleSheet(setSS(self,self.initialStyle+" "+color_changing))
            self.setFont(self.font_changing)
            for b in self.bros:
                if (not b==self) and b.flagS:
                        b.setStyleSheet(setSS(b,b.initialStyle+" "+color_changing_black))
                 
    def focusOutEvent(self, event):
        super().focusOutEvent(event) #to preserve classical behaviour before adding the below
        for f in self.addfuncout:
            self.addfuncout[f]()
        self.focusOutFun()

    def clearFocus(self):
        super().clearFocus()
        self.focusOutFun()

    def focusOutFun(self):
        if self.font()==self.font_changing:
           for b in self.bros:
                if b.flagS:
                    b.setStyleSheet(setSS(b,b.initialStyle))
                if b.flagF:
                    b.setFont(b.initialFont)
        #self.addlab.clear()
            
    def showCompleter(self):
        if self.completer():
            self.completer().complete()

class MyQLineEditNumber(MyQLineEdit):
    def __init__(self,parent):
        super().__init__(parent)       

    def keyPressEvent(self, event):
        #infoPrint.white(event.key())
        if event.key() in (32, #space
            44, #comma 
            16777219,16777223, #del, canc
            16777234,16777236, #left, right
            16777220 #return
            ) \
            or (event.key()>=48 and event.key()<=57):
            super().keyPressEvent(event)
        if event.key()==16777220:
            for f in self.addfuncreturn:
                self.addfuncreturn[f]()
        
class MyQCombo(QtWidgets.QComboBox):
    def wheelEvent(self, event):
        event.ignore()

#MyQSpin=QtWidgets.QSpinBox
class MyQSpin(QtWidgets.QSpinBox):
    def __init__(self,parent):
        super().__init__(parent)
        self.addwid=[]
        self.initFlag=False
        self.styleFlag=False
        self.addfuncin={} 
        self.addfuncout={} 
        self.addfuncreturn={}
        
        self.setAccelerated(True)
        self.setGroupSeparatorShown(True)

    def setup(self): 
        if not self.initFlag:
            self.initFlag=True
            self.font_changing = QtGui.QFont(self.font())
            self.font_changing.setItalic(font_italic)
            self.font_changing.setWeight(font_weight)
            self.bros=[self]+self.addwid
            for b in self.bros:
                if b.styleFlag: continue
                b.initialStyle=b.styleSheet()
                b.initialFont=b.font()
                b.styleFlag=True

    def setFocus(self):
        super().setFocus()
        self.focusInFun()

    def focusInEvent(self, event):
        super().focusInEvent(event) #to preserve classical behaviour before adding the below
        for f in self.addfuncin:
            self.addfuncin[f]()
        self.focusInFun()

    def focusInFun(self):
        if not self.font()==self.font_changing:
           for b in self.bros:
                b.setStyleSheet(b.initialStyle+" "+color_changing)
                b.setFont(self.font_changing)

    def focusOutEvent(self, event):
        super().focusOutEvent(event) #to preserve classical behaviour before adding the below
        for f in self.addfuncout:
            self.addfuncout[f]()
        if self.font()==self.font_changing:
            for b in self.bros:
                b.setStyleSheet(b.initialStyle)
                b.setFont(b.initialFont)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() in (16777220,16777221) and self.hasFocus():
            for f in self.addfuncreturn:
                self.addfuncreturn[f]()
    
    def wheelEvent(self, event):
        event.ignore()

    def textFromValue(self, value):
        if Flag_GROUPSEPARATOR:
            text=self.locale().toString(float(value), 'd')
        else:
            text=f"{value:f}"
        return (text).rstrip('0').rstrip(curr_locale.decimalPoint()) 
        #return ('%f' % value).rstrip('0').rstrip('.') 
class MyQSpinXW(MyQSpin):
    def __init__(self,parent):
        super().__init__(parent)
        self.Win=-1

    def focusInEvent(self, event):
        super().focusInEvent(event) #to preserve classical behaviour before adding the below
        if len(self.addwid)>0:
            self.Win=self.addwid[0].value()

class MyToolButton(QtWidgets.QToolButton):
    def __init__(self,parent):
        super().__init__(parent)

class MyQDoubleSpin(QtWidgets.QDoubleSpinBox):
    def __init__(self,parent):
        super().__init__(parent)
        self.addwid=[]
        self.initFlag=False
        self.styleFlag=False
        self.addfuncin={}
        self.addfuncout={}
        self.addfuncreturn={}

        self.setAccelerated(True)
        self.setGroupSeparatorShown(True)

    def setup(self): 
        if not self.initFlag:
            self.initFlag=True
            self.font_changing = QtGui.QFont(self.font())
            self.font_changing.setItalic(font_italic)
            self.font_changing.setWeight(font_weight)
            self.bros=[self]+self.addwid
            for b in self.bros:
                if self.styleFlag: continue
                b.initialStyle=b.styleSheet()
                b.initialFont=b.font()
                b.styleFlag=True

    def focusInEvent(self, event):
        super().focusInEvent(event) #to preserve classical behaviour before adding the below
        for f in self.addfuncin:
            self.addfuncin[f]()
        if not self.font()==self.font_changing:
           for b in self.bros:
                b.setStyleSheet(b.initialStyle+" "+color_changing)
                b.setFont(self.font_changing)

    def focusOutEvent(self, event):
        super().focusOutEvent(event) #to preserve classical behaviour before adding the below
        for f in self.addfuncout:
            self.addfuncout[f]()
        if self.font()==self.font_changing:
            for b in self.bros:
                b.setStyleSheet(b.initialStyle)
                b.setFont(b.initialFont)
                
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() in (16777220,16777221) and self.hasFocus():
            for f in self.addfuncreturn:
                self.addfuncreturn[f]()
    
    def wheelEvent(self, event):
        event.ignore()
    
    def textFromValue(self, value):
        if Flag_GROUPSEPARATOR:
            text=self.locale().toString(float(value), 'f', self.decimals())
        else:
            text=f"{value:f}"
        return (text).rstrip('0').rstrip(curr_locale.decimalPoint()) 
        #return ('%f' % value).rstrip('0').rstrip('.') 

class CollapsibleBox(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initFlag=False
        self.FlagPush=False
        self.dpix=5

    def setup(self,*args):
        if not self.initFlag:
            if len(args):
                self.ind=args[0]
                self.stretch=args[1]
            else:
                self.ind=-1
                self.stretch=0
            self.initFlag=True
            self.toggle_button=self.findChild(QtWidgets.QToolButton)
            self.content_area=self.findChild(QtWidgets.QGroupBox)
            self.push_button=self.findChild(MyToolButton)

            self.content_area.setStyleSheet("QGroupBox{border: 1px solid gray; border-radius: 6px;}")
            self.OpenStyle=\
            "QToolButton { border: none; }\n"+\
            "QToolButton::hover{color: rgba(0,0,255,200);}"+\
            "QToolButton::focus{color: rgba(0,0,255,200);}"
            #"QToolButton::hover{border: none; border-radius: 6px; background-color: rgba(0, 0,128,32); }"
            self.ClosedStyle=\
            "QToolButton { border: 1px solid lightgray; border-radius: 6px }\n"+\
            "QToolButton::hover{ border: 1px solid rgba(0,0,255,200); border-radius: 6px; color: rgba(0,0,255,200);}"+\
            "QToolButton::focus{ border: 1px solid rgba(0,0,255,200); border-radius: 6px; color: rgba(0,0,255,200);}" #background-color: rgba(0, 0,128,32); }" 
            self.toggle_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

            self.heightToogle=self.toggle_button.minimumHeight()
            self.heightOpened=self.minimumHeight()
            self.heightArea=self.heightOpened-20
            self.toggle_button.clicked.connect(self.on_click)    
            self.toggle_button.setChecked(InitCheck)
            self.on_click()
            

    #@QtCore.pyqtSlot()
    def on_click(self):
        checked = self.toggle_button.isChecked()
        if checked:
            self.content_area.show()
            if self.FlagPush: 
                self.push_button.show()
            else:
                self.push_button.hide()
            self.toggle_button.setArrowType(QtCore.Qt.ArrowType.DownArrow)
           
            self.toggle_button.setMinimumHeight(self.heightToogle)
            self.toggle_button.setMaximumHeight(self.heightToogle)
            self.setMinimumHeight(self.heightOpened)
            self.setMaximumHeight(int(self.heightOpened*1.5))
            self.content_area.setMinimumHeight(self.heightArea)
            self.content_area.setMaximumHeight(int(self.heightArea*1.5))

            self.toggle_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
            self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum)
            self.content_area.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

            self.toggle_button.setStyleSheet(self.OpenStyle)
            if self.ind>0:
                self.parent().layout().setStretch(self.ind,self.stretch)
        else:
            self.content_area.hide()
            self.push_button.hide()
            self.toggle_button.setArrowType(QtCore.Qt.ArrowType.RightArrow)
            
            self.toggle_button.setMinimumHeight(self.heightToogle+self.dpix)
            self.toggle_button.setMaximumHeight(self.heightToogle+self.dpix)
            self.setMinimumHeight(self.heightToogle+self.dpix*2)
            self.setMaximumHeight(self.heightToogle+self.dpix*2)
            self.content_area.setMinimumHeight(0)
            self.content_area.setMaximumHeight(0)

            self.toggle_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
            self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
            self.content_area.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
            
            self.toggle_button.setStyleSheet(self.ClosedStyle)
            
            if self.ind>0:
                self.parent().layout().setStretch(self.ind,0)

    def openBox(self):
        self.toggle_button.setChecked(True)
        self.on_click()

    def closeBox(self):
        self.toggle_button.setChecked(False)
        self.on_click()

class myToolButtonIcon(QToolButton):
    def __init__(self,parent):
        super().__init__(parent)
        self.addfuncin={}
        self.addfuncout={}
        self.addfuncreturn={}
        self.addfuncshift_pressed={}
        self.addfuncshift_released={}
        self.addfuncdel_pressed={}
        self.addfuncarrows_pressed={}
        self.addfunckey_pressed={}

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Shift:
            super().keyPressEvent(event) #to preserve classical behaviour before adding the b
            for f in self.addfuncshift_pressed:
                self.addfuncshift_pressed[f]()
        elif  event.key() == QtCore.Qt.Key_Delete or event.key() == QtCore.Qt.Key_Backspace:
            super().keyPressEvent(event) #to preserve classical behaviour before adding the b
            for f in self.addfuncdel_pressed:
                self.addfuncdel_pressed[f]()
        elif event.key() == QtCore.Qt.Key_Up or event.key() == QtCore.Qt.Key_Down:
            Flag=True
            for f in self.addfuncarrows_pressed:
                Flag=Flag and self.addfuncarrows_pressed[f](event.key())
            if Flag: super().keyPressEvent(event) #to preserve classical behaviour before adding the b
        else:
            super().keyPressEvent(event) #to preserve classical behaviour before adding the b
            for f in self.addfunckey_pressed:
                self.addfunckey_pressed[f](event.key())

class myQTreeWidget(QTreeWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.FlagArrowKeysNormal=False
        self.addfuncin={}
        self.addfuncout={}
        self.addfuncreturn={}
        self.addfuncshift_pressed={}
        self.addfuncshift_released={}
        self.addfuncdel_pressed={}
        self.addfuncarrows_pressed={}
        self.addfuncarrows_released={}
        self.addfunckey_pressed={}
        #self.ui:Ui_TreeTab=None
        self.ui=None

    def focusInEvent(self, event):
        super().focusInEvent(event) #to preserve classical behaviour before adding the below
        for f in self.addfuncin:
            self.addfuncin[f]()

    def focusOutEvent(self, event):
        super().focusOutEvent(event) #to preserve classical behaviour before adding the below
        for f in self.addfuncout:
            self.addfuncout[f]()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Shift:
            super().keyPressEvent(event) #to preserve classical behaviour before adding the b
            for f in self.addfuncshift_pressed:
                self.addfuncshift_pressed[f]()
        elif  event.key() == QtCore.Qt.Key_Delete or event.key() == QtCore.Qt.Key_Backspace:
            super().keyPressEvent(event) #to preserve classical behaviour before adding the b
            for f in self.addfuncdel_pressed:
                self.addfuncdel_pressed[f]()
        elif event.key() == QtCore.Qt.Key_Up or event.key() == QtCore.Qt.Key_Down:
            if self.FlagArrowKeysNormal:
                return super().keyPressEvent(event) #to preserve classical behaviour before adding the b
            else:
                Flag=True
                for f in self.addfuncarrows_pressed:
                    Flag=Flag and self.addfuncarrows_pressed[f](event.key())
                #if Flag: super().keyPressEvent(event) #to preserve classical behaviour before adding the b
        else:
            super().keyPressEvent(event) #to preserve classical behaviour before adding the b
            for f in self.addfunckey_pressed:
                self.addfunckey_pressed[f](event.key())

    def keyReleaseEvent(self, event):
        super().keyReleaseEvent(event) #to preserve classical behaviour before adding the b
        if event.key() == QtCore.Qt.Key_Shift:
            for f in self.addfuncshift_released:
                self.addfuncshift_released[f]()
        elif event.key() == QtCore.Qt.Key_Up or event.key() == QtCore.Qt.Key_Down:
            if self.FlagArrowKeysNormal:
                return super().keyReleaseEvent(event) #to preserve classical behaviour before adding the b
            else:
                Flag=True
                for f in self.addfuncarrows_released:
                    Flag=Flag and self.addfuncarrows_released[f](event.key())
                #if Flag: super().keyPressEvent(event) #to preserve classical behaviour before adding the b
                
class ToggleSplitterHandle(QtWidgets.QSplitterHandle):
    def mousePressEvent(self, event):
        super().mousePressEvent(event) 
        for f in self.parent().addfuncin:
            self.parent().addfuncin[f]()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event) 
        for f in self.parent().addfuncout:
            self.parent().addfuncout[f]()

class myQSplitter(QSplitter):
    def __init__(self,parent):
        super().__init__(parent)
        self.OpWidth=0
        self.OpMaxWidth=0
        self.addfuncin={}
        self.addfuncout={}
        self.addfuncreturn={}
    
    def createHandle(self):
        return ToggleSplitterHandle(self.orientation(), self)

class RichTextPushButton(QPushButton):
    margin=0
    spacing=5

    def __init__(self, parent=None, text=None):
        if parent is not None:
            super().__init__(parent)
        else:
            super().__init__()
        
        self.__lyt = QHBoxLayout()
        self.__lyt.setContentsMargins(self.margin, 0, self.margin, 0)
        self.__lyt.setSpacing(self.spacing)
        self.setLayout(self.__lyt)

        self.__icon= QLabel(self)
        self.__icon.setAttribute(Qt.WA_TranslucentBackground)
        self.__icon.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.__icon.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding,
        )
        self.__icon.setTextFormat(Qt.RichText)
        self.__icon.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        

        self.__lbl = QLabel(self)
        if text is not None:
            self.__lbl.setText(text)
        self.__lbl.setAttribute(Qt.WA_TranslucentBackground)
        self.__lbl.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.__lbl.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding,
        )
        self.__lbl.setTextFormat(Qt.RichText)
        self.__lbl.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.__lyt.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.__lyt.addWidget(self.__icon)     
        self.__lyt.addWidget(self.__lbl)  
        self.__lyt.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))      
        return

    def setText(self, text):
        self.__lbl.setText(text)
        self.updateGeometry()
        return
    
    def setIcon(self, icon):
        h=int(self.size().height()/2)
        pixmap = icon.pixmap(QSize(h,h))
        self.__icon.setPixmap(pixmap) 
        self.updateGeometry()
        return

    def sizeHint(self):
        s = QPushButton.sizeHint(self)
        w_lbl = self.__lbl.sizeHint()
        w_icon = self.__icon.sizeHint()
        s.setWidth(w_lbl.width()+w_icon.width()
                   +self.margin*2+self.spacing)
        s.setHeight(w_lbl.height())
        return s
    
#********************************************* Matplotlib
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as pyplt
import matplotlib.image as mplimage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure as mplFigure
from mpl_toolkits.axes_grid1 import make_axes_locatable
 
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=8, height=8, dpi=100):
        self.fig = mplFigure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.gca() #self.fig.add_subplot(111)
        self.addfuncrelease={}
        mpl.rcParams["font.family"]=fontName
        super(MplCanvas, self).__init__(self.fig)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        for f in self.addfuncrelease:
            self.addfuncrelease[f]()

