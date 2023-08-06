from .addwidgets_ps import*

app = QApplication(sys.argv)

margin=15
spacing=15
bsize=30
nbutt=5

w=bsize*nbutt+spacing*(nbutt-1)+2*margin
h=bsize+2*margin
print(w,h)
dlg=QDialog()
dlg.setGeometry(100,100,w,h)
dlg.setFixedSize(w,h)
dlg.setWindowFlags(Qt.Window|Qt.FramelessWindowHint)
dlg.setAttribute(Qt.WA_TranslucentBackground)
dlg.setAttribute(Qt.WA_NoSystemBackground)

lay_dlg=QHBoxLayout()
lay_dlg.setContentsMargins(0, 0, 0, 0)

dlg.setLayout(lay_dlg)
widget=QFrame()
lay_dlg.addWidget(widget)

lay=QHBoxLayout()
lay.setContentsMargins(margin, 0, margin, 0)
lay.setSpacing(spacing)
widget.setLayout(lay)

for i in range(nbutt):
    button=QToolButton(widget)
    icon=QIcon()
    icon.addFile(icons_path+f"w{i+1}.png", QSize(), QIcon.Normal, QIcon.Off)
    button.setIcon(icon)
    button.setArrowType(Qt.NoArrow)
    button.setMinimumSize(30,30)
    button.setMaximumSize(30,30)
    button.clicked.connect(dlg.close)
    
    lay.addWidget(button)


color = widget.palette().color(QtGui.QPalette.Window)
col=f"rgba({color.red()}, {color.green()}, {color.blue()}, 255)"
widget.setObjectName('ResizePopup')
ss=f"QWidget#{widget.objectName()}"+"{border: 1px solid gray;border-radius: 15px; background:"+col+"}"
widget.setStyleSheet(ss)
dlg.exec()

