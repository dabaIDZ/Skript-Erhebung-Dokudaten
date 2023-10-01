# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_zeitraum_festlegen.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QRadioButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_fenster_zeitraum_festlegen(object):
    def setupUi(self, fenster_zeitraum_festlegen):
        if not fenster_zeitraum_festlegen.objectName():
            fenster_zeitraum_festlegen.setObjectName(u"fenster_zeitraum_festlegen")
        fenster_zeitraum_festlegen.resize(480, 538)
        self.verticalLayoutWidget = QWidget(fenster_zeitraum_festlegen)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 10, 451, 515))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)
        # self.label needs more space to display the text
        self.label.setMinimumSize(0, 70)

        self.verticalLayout.addWidget(self.label)
        self.listWidget_zeitraum_spalten = QListWidget(self.verticalLayoutWidget)
        self.listWidget_zeitraum_spalten.setObjectName(u"listWidget_zeitraum_spalten")
        self.listWidget_zeitraum_spalten.setSelectionMode(QAbstractItemView.SingleSelection)

        self.verticalLayout.addWidget(self.listWidget_zeitraum_spalten)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)
        self.label_2.setMinimumSize(0, 50)

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setWordWrap(True)
        self.label_3.setMinimumSize(0, 30)


        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radio_zeitraum_beginn = QRadioButton(self.verticalLayoutWidget)
        self.radio_zeitraum_beginn.setObjectName(u"radio_zeitraum_beginn")

        self.horizontalLayout.addWidget(self.radio_zeitraum_beginn)

        self.text_zeitraum_beginn = QLineEdit(self.verticalLayoutWidget)
        self.text_zeitraum_beginn.setObjectName(u"text_zeitraum_beginn")


        self.horizontalLayout.addWidget(self.text_zeitraum_beginn)



        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radio_zeitraum_ende = QRadioButton(self.verticalLayoutWidget)
        self.radio_zeitraum_ende.setObjectName(u"radio_zeitraum_ende")

        self.horizontalLayout_2.addWidget(self.radio_zeitraum_ende)

        self.text_zeitraum_ende = QLineEdit(self.verticalLayoutWidget)
        self.text_zeitraum_ende.setObjectName(u"text_zeitraum_ende")

        self.horizontalLayout_2.addWidget(self.text_zeitraum_ende)



        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radio_zeitraum_inhalt = QRadioButton(self.verticalLayoutWidget)
        self.radio_zeitraum_inhalt.setObjectName(u"radio_zeitraum_inhalt")

        self.horizontalLayout_3.addWidget(self.radio_zeitraum_inhalt)

        self.text_zeitraum_inhalt = QLineEdit(self.verticalLayoutWidget)
        self.text_zeitraum_inhalt.setObjectName(u"text_zeitraum_inhalt")

        self.horizontalLayout_3.addWidget(self.text_zeitraum_inhalt)



        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.radio_zeitraum_genau = QRadioButton(self.verticalLayoutWidget)
        self.radio_zeitraum_genau.setObjectName(u"radio_zeitraum_genau")

        self.horizontalLayout_4.addWidget(self.radio_zeitraum_genau)

        self.text_zeitraum_genau = QLineEdit(self.verticalLayoutWidget)
        self.text_zeitraum_genau.setObjectName(u"text_zeitraum_genau")

        self.horizontalLayout_4.addWidget(self.text_zeitraum_genau)

        # all horizontal layouts are added to the vertical layout
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        # all horizontal layouts should have the same size
        self.text_zeitraum_inhalt.setFixedWidth(220)
        self.text_zeitraum_beginn.setFixedWidth(220)
        self.text_zeitraum_ende.setFixedWidth(220)
        self.text_zeitraum_genau.setFixedWidth(220)



        self.radio_zeitraum_irgendwas = QRadioButton(self.verticalLayoutWidget)
        self.radio_zeitraum_irgendwas.setObjectName(u"radio_zeitraum_irgendwas")

        self.verticalLayout.addWidget(self.radio_zeitraum_irgendwas)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_5.addWidget(self.pushButton)

        self.button_zeitraum_speichern = QPushButton(self.verticalLayoutWidget)
        self.button_zeitraum_speichern.setObjectName(u"button_zeitraum_speichern")

        self.horizontalLayout_5.addWidget(self.button_zeitraum_speichern)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(fenster_zeitraum_festlegen)

        QMetaObject.connectSlotsByName(fenster_zeitraum_festlegen)
    # setupUi

    def retranslateUi(self, fenster_zeitraum_festlegen):
        myFont = QFont()
        myFont.setBold(True)
        fenster_zeitraum_festlegen.setWindowTitle(QCoreApplication.translate("fenster_zeitraum_festlegen", u"Auswahl des Erhebungsjahres", None))
        self.label.setText(QCoreApplication.translate("fenster_zeitraum_festlegen", u"Bitte w\u00e4hlen Sie die Spalte in Ihrer Dokumentation aus, in der das Erhebungsjahr gespeichert wird.", None))
        self.label_2.setText(QCoreApplication.translate("fenster_zeitraum_festlegen", u"Wie kann das Jahr des ersten Beratungskontaktes in den den Daten identifiziert werden?", None))
        self.label.setFont(myFont)
        self.label_3.setText(QCoreApplication.translate("fenster_zeitraum_festlegen", u"Dies kommen noch einige Mustereintr\u00e4ge aus der ausgew\u00e4hlten Spalte.", None))
        self.radio_zeitraum_beginn.setText(QCoreApplication.translate("fenster_zeitraum_festlegen", u"Inhalt der Spalte beginnt mit:", None))
        self.radio_zeitraum_ende.setText(QCoreApplication.translate("fenster_zeitraum_festlegen", u"Inhalt der Spalte endet mit:", None))
        self.radio_zeitraum_inhalt.setText(QCoreApplication.translate("fenster_zeitraum_festlegen", u"Inhalt der Spalte beinhaltet:", None))
        self.radio_zeitraum_genau.setText(QCoreApplication.translate("fenster_zeitraum_festlegen", u"Inhalt der Spalte ist genau:", None))
        self.radio_zeitraum_irgendwas.setText(QCoreApplication.translate("fenster_zeitraum_festlegen", u"DIe Spalte beinhaltet irgendeinen Wert.", None))
        self.pushButton.setText(QCoreApplication.translate("fenster_zeitraum_festlegen", u"Abbrechen", None))
        self.button_zeitraum_speichern.setText(QCoreApplication.translate("fenster_zeitraum_festlegen", u"Speichern", None))
    # retranslateUi

