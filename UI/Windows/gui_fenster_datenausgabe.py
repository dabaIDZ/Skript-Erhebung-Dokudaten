# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_fenster_datenausgabe.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_fenster_datenausgabe(object):
    def setupUi(self, fenster_datenausgabe):
        if not fenster_datenausgabe.objectName():
            fenster_datenausgabe.setObjectName(u"fenster_datenausgabe")
        fenster_datenausgabe.resize(447, 157)
        self.gridLayoutWidget = QWidget(fenster_datenausgabe)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 431, 131))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.textfeld_datenausgabe = QLineEdit(self.gridLayoutWidget)
        self.textfeld_datenausgabe.setObjectName(u"textfeld_datenausgabe")

        self.gridLayout.addWidget(self.textfeld_datenausgabe, 1, 0, 1, 1)

        self.button_datenausgabe_durchsuchen = QPushButton(self.gridLayoutWidget)
        self.button_datenausgabe_durchsuchen.setObjectName(u"button_datenausgabe_durchsuchen")

        self.gridLayout.addWidget(self.button_datenausgabe_durchsuchen, 1, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button_speichern = QPushButton(self.gridLayoutWidget)
        self.button_speichern.setObjectName(u"button_speichern")

        self.horizontalLayout_2.addWidget(self.button_speichern)

        self.button_abbrechen = QPushButton(self.gridLayoutWidget)
        self.button_abbrechen.setObjectName(u"button_abbrechen")

        self.horizontalLayout_2.addWidget(self.button_abbrechen)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)


        self.retranslateUi(fenster_datenausgabe)

        QMetaObject.connectSlotsByName(fenster_datenausgabe)
    # setupUi

    def retranslateUi(self, fenster_datenausgabe):
        fenster_datenausgabe.setWindowTitle(QCoreApplication.translate("fenster_datenausgabe", u"Datenauswahl", None))
        self.label.setText(QCoreApplication.translate("fenster_datenausgabe", u"Wo sollen die Ergebnisse gespeichert werden?", None))
        self.button_datenausgabe_durchsuchen.setText(QCoreApplication.translate("fenster_datenausgabe", u"Durchsuchen", None))
        self.button_speichern.setText(QCoreApplication.translate("fenster_datenausgabe", u"Speichern", None))
        self.button_abbrechen.setText(QCoreApplication.translate("fenster_datenausgabe", u"Abbrechen", None))
    # retranslateUi

