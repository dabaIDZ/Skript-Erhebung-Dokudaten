# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_fenster_datengrundlage_einfach.ui'
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

class Ui_fenster_datengrundlage_einfach(object):
    def setupUi(self, fenster_datengrundlage_einfach):
        if not fenster_datengrundlage_einfach.objectName():
            fenster_datengrundlage_einfach.setObjectName(u"fenster_datengrundlage_einfach")
        fenster_datengrundlage_einfach.resize(447, 157)
        self.gridLayoutWidget = QWidget(fenster_datengrundlage_einfach)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 20, 431, 101))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.button_datengrundlage_einfach_durchsuchen = QPushButton(self.gridLayoutWidget)
        self.button_datengrundlage_einfach_durchsuchen.setObjectName(u"button_datengrundlage_einfach_durchsuchen")

        self.gridLayout.addWidget(self.button_datengrundlage_einfach_durchsuchen, 1, 1, 1, 1)

        self.textfeld_datengrundlage_einfach_speicherort = QLineEdit(self.gridLayoutWidget)
        self.textfeld_datengrundlage_einfach_speicherort.setObjectName(u"textfeld_datengrundlage_einfach_speicherort")

        self.gridLayout.addWidget(self.textfeld_datengrundlage_einfach_speicherort, 1, 0, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)
        self.label.setMinimumSize(0, 50)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.horizontalLayoutWidget_2 = QWidget(fenster_datengrundlage_einfach)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(90, 120, 231, 26))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.button_speichern = QPushButton(self.horizontalLayoutWidget_2)
        self.button_speichern.setObjectName(u"button_speichern")

        self.horizontalLayout_2.addWidget(self.button_speichern)

        self.button_abbrechen = QPushButton(self.horizontalLayoutWidget_2)
        self.button_abbrechen.setObjectName(u"button_abbrechen")

        self.horizontalLayout_2.addWidget(self.button_abbrechen)


        self.retranslateUi(fenster_datengrundlage_einfach)

        QMetaObject.connectSlotsByName(fenster_datengrundlage_einfach)
    # setupUi

    def retranslateUi(self, fenster_datengrundlage_einfach):
        fenster_datengrundlage_einfach.setWindowTitle(QCoreApplication.translate("fenster_datengrundlage_einfach", u"Datenauswahl", None))
        self.button_datengrundlage_einfach_durchsuchen.setText(QCoreApplication.translate("fenster_datengrundlage_einfach", u"Durchsuchen", None))
        self.label.setText(QCoreApplication.translate("fenster_datengrundlage_einfach", u"Bitte w\u00e4hlen Sie hier den Speicherort Ihrer Datengrundlage aus:", None))
        self.button_speichern.setText(QCoreApplication.translate("fenster_datengrundlage_einfach", u"Speichern", None))
        self.button_abbrechen.setText(QCoreApplication.translate("fenster_datengrundlage_einfach", u"Abbrechen", None))
    # retranslateUi

