from .addwidgets_ps import icons_path
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'infoPaIRS.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QSizePolicy, QTabWidget,
    QWidget)

class Ui_InfoPaiRS(object):
    def setupUi(self, InfoPaiRS):
        if not InfoPaiRS.objectName():
            InfoPaiRS.setObjectName(u"InfoPaiRS")
        InfoPaiRS.resize(650, 500)
        InfoPaiRS.setMinimumSize(QSize(550, 500))
        font = QFont()
        font.setFamilies([u"Arial"])
        InfoPaiRS.setFont(font)
        icon = QIcon()
        icon.addFile(u""+ icons_path +"icon_PaIRS.png", QSize(), QIcon.Normal, QIcon.Off)
        InfoPaiRS.setWindowIcon(icon)
        self.centralwidget = QWidget(InfoPaiRS)
        self.centralwidget.setObjectName(u"centralwidget")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(10)
        self.centralwidget.setFont(font1)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabBarAutoHide(True)
        self.about = QWidget()
        self.about.setObjectName(u"about")
        self.about.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.gridLayout_2 = QGridLayout(self.about)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.logo = QLabel(self.about)
        self.logo.setObjectName(u"logo")
        self.logo.setMinimumSize(QSize(250, 250))
        self.logo.setMaximumSize(QSize(250, 250))
#if QT_CONFIG(accessibility)
        self.logo.setAccessibleDescription(u"")
#endif // QT_CONFIG(accessibility)
        self.logo.setPixmap(QPixmap(u""+ icons_path +"logo_PaIRS_completo.png"))
        self.logo.setScaledContents(True)

        self.gridLayout_2.addWidget(self.logo, 0, 0, 1, 1)

        self.info = QLabel(self.about)
        self.info.setObjectName(u"info")
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(14)
        self.info.setFont(font2)
        self.info.setTextFormat(Qt.RichText)
        self.info.setWordWrap(True)
        self.info.setOpenExternalLinks(True)
        self.info.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.gridLayout_2.addWidget(self.info, 0, 1, 1, 1)

        self.unina_dii = QLabel(self.about)
        self.unina_dii.setObjectName(u"unina_dii")
        self.unina_dii.setMaximumSize(QSize(16777215, 90))
        self.unina_dii.setPixmap(QPixmap(u""+ icons_path +"unina_dii.png"))
        self.unina_dii.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.unina_dii, 1, 0, 1, 1)

        self.info_uni = QLabel(self.about)
        self.info_uni.setObjectName(u"info_uni")
        self.info_uni.setTextFormat(Qt.RichText)
        self.info_uni.setWordWrap(True)

        self.gridLayout_2.addWidget(self.info_uni, 1, 1, 1, 1)

        self.tabWidget.addTab(self.about, "")
        self.authors = QWidget()
        self.authors.setObjectName(u"authors")
        self.authors.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.gridLayout = QGridLayout(self.authors)
        self.gridLayout.setObjectName(u"gridLayout")
        self.ger_cv = QLabel(self.authors)
        self.ger_cv.setObjectName(u"ger_cv")
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setPointSize(11)
        self.ger_cv.setFont(font3)
        self.ger_cv.setTextFormat(Qt.RichText)
        self.ger_cv.setScaledContents(True)
        self.ger_cv.setWordWrap(True)
        self.ger_cv.setMargin(5)
        self.ger_cv.setIndent(-5)

        self.gridLayout.addWidget(self.ger_cv, 0, 1, 1, 1)

        self.tom = QLabel(self.authors)
        self.tom.setObjectName(u"tom")
        self.tom.setMinimumSize(QSize(150, 150))
        self.tom.setMaximumSize(QSize(150, 150))
        self.tom.setPixmap(QPixmap(u""+ icons_path +"tom.png"))
        self.tom.setScaledContents(True)

        self.gridLayout.addWidget(self.tom, 1, 0, 1, 1)

        self.ger = QLabel(self.authors)
        self.ger.setObjectName(u"ger")
        self.ger.setMinimumSize(QSize(150, 150))
        self.ger.setMaximumSize(QSize(150, 150))
        self.ger.setPixmap(QPixmap(u""+ icons_path +"ger.png"))
        self.ger.setScaledContents(True)

        self.gridLayout.addWidget(self.ger, 0, 0, 1, 1)

        self.tom_cv = QLabel(self.authors)
        self.tom_cv.setObjectName(u"tom_cv")
        self.tom_cv.setFont(font3)
        self.tom_cv.setTextFormat(Qt.RichText)
        self.tom_cv.setWordWrap(True)
        self.tom_cv.setMargin(5)
        self.tom_cv.setIndent(-5)

        self.gridLayout.addWidget(self.tom_cv, 1, 1, 1, 1)

        self.tabWidget.addTab(self.authors, "")
        self.references = QWidget()
        self.references.setObjectName(u"references")
        self.references.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.horizontalLayout_2 = QHBoxLayout(self.references)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.list_ref = QLabel(self.references)
        self.list_ref.setObjectName(u"list_ref")
        self.list_ref.setTextFormat(Qt.RichText)
        self.list_ref.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.list_ref.setWordWrap(True)
        self.list_ref.setMargin(5)
        self.list_ref.setOpenExternalLinks(True)
        self.list_ref.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.horizontalLayout_2.addWidget(self.list_ref)

        self.tabWidget.addTab(self.references, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        InfoPaiRS.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(InfoPaiRS)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 650, 20))
        InfoPaiRS.setMenuBar(self.menubar)

        self.retranslateUi(InfoPaiRS)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(InfoPaiRS)
    # setupUi

    def retranslateUi(self, InfoPaiRS):
        InfoPaiRS.setWindowTitle(QCoreApplication.translate("InfoPaiRS", u"About PaIRS", None))
        self.logo.setText("")
        self.info.setText(QCoreApplication.translate("InfoPaiRS", u"<html><head/><body><p><span style=\" font-size:18pt; font-weight:700;\">PaIRS - version: #.#.#</span></p><p><span style=\" font-size:16pt; font-weight:700;\">Pa</span><span style=\" font-size:16pt;\">rticle </span><span style=\" font-size:16pt; font-weight:700;\">I</span><span style=\" font-size:16pt;\">mage </span><span style=\" font-size:16pt; font-weight:700;\">R</span><span style=\" font-size:16pt;\">econstruction </span><span style=\" font-size:16pt; font-weight:700;\">S</span><span style=\" font-size:16pt;\">oftware</span></p><p>\u00a9 yyyy Gerardo Paolillo &amp; Tommaso Astarita. All rights reserved.</p><p>email: mmmm</p></body></html>", None))
        self.unina_dii.setText("")
        self.info_uni.setText(QCoreApplication.translate("InfoPaiRS", u"<html><head/><body><p><span style=\" font-size:12pt;\">Experimental Thermo-Fluid Dynamics (ETFD) group, Department of Industrial Engineering (DII)</span></p><p><span style=\" font-size:12pt;\">University of Naples &quot;Federico II&quot;, Naples, Italy</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.about), QCoreApplication.translate("InfoPaiRS", u"About PaIRS", None))
        self.ger_cv.setText(QCoreApplication.translate("InfoPaiRS", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:11pt; font-weight:700;\">Gerardo Paolillo</span><span style=\" font-size:10pt;\"> received a Master's degree in Aerospace Engineering and a PhD degree in Industrial Engineering from Universit\u00e0 di Napoli &quot;Federico II&quot; in 2015 and 2018, respectively. </span></p><p align=\"justify\"><span style=\" font-size:10pt;\">He is currently a Research Associate in the Department of Industrial Engineering at Universit\u00e0 di Napoli &quot;Federico II&quot;.</span></p><p align=\"justify\"><span style=\" font-size:10pt;\">His research interests lie in the area of experimental fluid mechanics, with focus on applications of unsteady jets to flow control and electronics cooling, investigation into dynamics of turbulent Rayleigh-B\u00e8nard convection and development of 3D optical velocimetry techniques.</span></p></body></html>", None))
        self.tom.setText("")
        self.ger.setText("")
        self.tom_cv.setText(QCoreApplication.translate("InfoPaiRS", u"<html><head/><body><p align=\"justify\"><span style=\" font-weight:700;\">Tommaso Astarita</span><span style=\" font-size:10pt;\"> received a Master's degree in Aeronautical Engineering in 1993 and a PhD degree in Aerospace Engineering in 1997, both from Universit\u00e0 di Napoli &quot;Federico II&quot;. </span></p><p align=\"justify\"><span style=\" font-size:10pt;\">He was Post-doc at the von K\u00e0rm\u00e0n Institute for Fluid Dynamics and he is currently full Professor of Fluid Mechanics at Universit\u00e0 di Napoli &quot;Federico II&quot;. </span></p><p align=\"justify\"><span style=\" font-size:10pt;\">His main research interests are dedicated to the experimental study of problems in the fields of fluid mechanics and convective heat transfer, in particular, the application and development of IR thermography and stereoscopic and tomographic PIV techniques for fluid mechanics problems.</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.authors), QCoreApplication.translate("InfoPaiRS", u"Authors", None))
        self.list_ref.setText(QCoreApplication.translate("InfoPaiRS", u"<html><head/><body><p align=\"justify\"><span style=\" font-size:11pt;\">Please cite the following works if you are intended to use PaIRS-UniNa for your purposes: </span></p><p align=\"justify\"><span style=\" font-size:11pt; font-weight:700;\">[1] </span><span style=\" font-size:11pt;\">Astarita, T., &amp; Cardone, G. (2005). &quot;Analysis of interpolation schemes for image deformation methods in PIV&quot;. </span><span style=\" font-size:11pt; font-style:italic;\">Experiments in Fluids</span><span style=\" font-size:11pt;\">, 38(2), 233-243.doi: </span><a href=\"https://doi.org/10.1007/s00348-004-0902-3\"><span style=\" text-decoration: underline; color:#0000ff;\">10.1007/s00348-004-0902-3</span></a><span style=\" font-size:11pt;\">. </span></p><p align=\"justify\"><span style=\" font-size:11pt; font-weight:700;\">[2] </span><span style=\" font-size:11pt;\">Astarita, T. (2006). &quot;Analysis of interpolation schemes for image deformation methods in PIV: effect of noise on the accuracy and spatial resolutio"
                        "n&quot;. </span><span style=\" font-size:11pt; font-style:italic;\">Experiments in Fluids</span><span style=\" font-size:11pt;\">, vol. 40 (6): 977-987. doi: </span><a href=\"https://doi.org/10.1007/s00348-006-0139-4\"><span style=\" text-decoration: underline; color:#0000ff;\">10.1007/s00348-006-0139-4</span></a><span style=\" font-size:11pt;\">. </span></p><p align=\"justify\"><span style=\" font-size:11pt; font-weight:700;\">[3] </span><span style=\" font-size:11pt;\">Astarita, T. (2007). &quot;Analysis of weighting windows for image deformation methods in PIV.&quot; </span><span style=\" font-size:11pt; font-style:italic;\">Experiments in Fluids</span><span style=\" font-size:11pt;\">, 43(6), 859-872. doi: </span><a href=\"https://doi.org/10.1007/s00348-007-0314-2\"><span style=\" text-decoration: underline; color:#0000ff;\">10.1007/s00348-007-0314-2</span></a><span style=\" font-size:11pt;\">. </span></p><p align=\"justify\"><span style=\" font-size:11pt; font-weight:700;\">[4]</span><span style=\" font-s"
                        "ize:11pt;\"> Astarita, T. (2008). &quot;Analysis of velocity interpolation schemes for image deformation methods in PIV&quot;. </span><span style=\" font-size:11pt; font-style:italic;\">Experiments in Fluids</span><span style=\" font-size:11pt;\">, 45(2), 257-266. doi: </span><a href=\"https://doi.org/10.1007/s00348-008-0475-7\"><span style=\" text-decoration: underline; color:#0000ff;\">10.1007/s00348-008-0475-7</span></a><span style=\" font-size:11pt;\">. </span></p><p align=\"justify\"><span style=\" font-size:11pt; font-weight:700;\">[5] </span><span style=\" font-size:11pt;\">Astarita, T. (2009). &quot;Adaptive space resolution for PIV&quot;. </span><span style=\" font-size:11pt; font-style:italic;\">Experiments in Fluids</span><span style=\" font-size:11pt;\">, 46(6), 1115-1123. doi: </span><a href=\"https://doi.org/10.1007/s00348-009-0618-5\"><span style=\" text-decoration: underline; color:#0000ff;\">10.1007/s00348-009-0618-5</span></a><span style=\" font-size:11pt;\">. </span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.references), QCoreApplication.translate("InfoPaiRS", u"References", None))
    # retranslateUi

