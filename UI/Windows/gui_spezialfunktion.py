# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_spezialfunktion.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_fenster_spezialfunktion(object):
    def setupUi(self, fenster_spezialfunktion):
        if not fenster_spezialfunktion.objectName():
            fenster_spezialfunktion.setObjectName(u"fenster_spezialfunktion")
        fenster_spezialfunktion.resize(480, 155)
        self.label = QLabel(fenster_spezialfunktion)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 20, 441, 41))
        self.label.setLineWidth(1)
        self.label.setWordWrap(True)
        self.line_spezialfunktion = QLineEdit(fenster_spezialfunktion)
        self.line_spezialfunktion.setObjectName(u"line_spezialfunktion")
        self.line_spezialfunktion.setGeometry(QRect(20, 70, 441, 21))
        self.pushButton_OK = QPushButton(fenster_spezialfunktion)
        self.pushButton_OK.setObjectName(u"pushButton_OK")
        self.pushButton_OK.setGeometry(QRect(380, 110, 75, 24))

        self.retranslateUi(fenster_spezialfunktion)

        QMetaObject.connectSlotsByName(fenster_spezialfunktion)
    # setupUi

    def retranslateUi(self, fenster_spezialfunktion):
        fenster_spezialfunktion.setWindowTitle(QCoreApplication.translate("fenster_spezialfunktion", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("fenster_spezialfunktion", u"Bitte geben Sie hier den Code f\u00fcr die Spezialfunktion ein. Beachten Sie bitte Gro\u00df- und Kleinschreibung.", None))
        self.pushButton_OK.setText(QCoreApplication.translate("fenster_spezialfunktion", u"OK", None))
    # retranslateUi

