# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(497, 681)
        self.actionLaden = QAction(MainWindow)
        self.actionLaden.setObjectName(u"actionLaden")
        self.actionLaden.setEnabled(True)
        self.actionSpeichern = QAction(MainWindow)
        self.actionSpeichern.setObjectName(u"actionSpeichern")
        self.actionLebensbereich = QAction(MainWindow)
        self.actionLebensbereich.setObjectName(u"actionLebensbereich")
        self.actionLebensbereich.setEnabled(False)
        self.actionDiskriminierungsmerkmal = QAction(MainWindow)
        self.actionDiskriminierungsmerkmal.setObjectName(u"actionDiskriminierungsmerkmal")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 120, 461, 391))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.gridLayoutWidget)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 11, 2, 1, 1)

        self.fortschritt_datenauswahl = QProgressBar(self.gridLayoutWidget)
        self.fortschritt_datenauswahl.setObjectName(u"fortschritt_datenauswahl")
        self.fortschritt_datenauswahl.setValue(0)
        self.fortschritt_datenauswahl.setTextVisible(False)
        self.fortschritt_datenauswahl.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.fortschritt_datenauswahl, 1, 1, 1, 1)

        self.button_dismerkmal_bearbeiten = QPushButton(self.gridLayoutWidget)
        self.button_dismerkmal_bearbeiten.setObjectName(u"button_dismerkmal_bearbeiten")
        self.button_dismerkmal_bearbeiten.setEnabled(True)

        self.gridLayout.addWidget(self.button_dismerkmal_bearbeiten, 8, 3, 1, 1)

        self.fortschritt_disform = QProgressBar(self.gridLayoutWidget)
        self.fortschritt_disform.setObjectName(u"fortschritt_disform")
        self.fortschritt_disform.setValue(0)
        self.fortschritt_disform.setTextVisible(False)
        self.fortschritt_disform.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.fortschritt_disform, 9, 1, 1, 1)

        self.fortschritt_dismerkmal = QProgressBar(self.gridLayoutWidget)
        self.fortschritt_dismerkmal.setObjectName(u"fortschritt_dismerkmal")
        self.fortschritt_dismerkmal.setEnabled(True)
        self.fortschritt_dismerkmal.setValue(0)
        self.fortschritt_dismerkmal.setTextVisible(False)
        self.fortschritt_dismerkmal.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.fortschritt_dismerkmal, 8, 1, 1, 1)

        self.fortschritt_zeitraum = QProgressBar(self.gridLayoutWidget)
        self.fortschritt_zeitraum.setObjectName(u"fortschritt_zeitraum")
        self.fortschritt_zeitraum.setValue(0)
        self.fortschritt_zeitraum.setTextVisible(False)
        self.fortschritt_zeitraum.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.fortschritt_zeitraum, 5, 1, 1, 1)

        self.fortschritt_intervform = QProgressBar(self.gridLayoutWidget)
        self.fortschritt_intervform.setObjectName(u"fortschritt_intervform")
        self.fortschritt_intervform.setValue(0)
        self.fortschritt_intervform.setTextVisible(False)
        self.fortschritt_intervform.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.fortschritt_intervform, 10, 1, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        # label_§ needs to be able to display 2 lines of text
        self.label_3.setWordWrap(True)

        self.gridLayout.addWidget(self.label_3, 3, 2, 1, 1)

        self.button_lebensbereich_bearbeiten = QPushButton(self.gridLayoutWidget)
        self.button_lebensbereich_bearbeiten.setObjectName(u"button_lebensbereich_bearbeiten")

        self.gridLayout.addWidget(self.button_lebensbereich_bearbeiten, 7, 3, 1, 1)

        self.button_zeitraum_bearbeiten = QPushButton(self.gridLayoutWidget)
        self.button_zeitraum_bearbeiten.setObjectName(u"button_zeitraum_bearbeiten")

        self.gridLayout.addWidget(self.button_zeitraum_bearbeiten, 5, 3, 1, 1)

        self.fortschritt_lebensbereich = QProgressBar(self.gridLayoutWidget)
        self.fortschritt_lebensbereich.setObjectName(u"fortschritt_lebensbereich")
        self.fortschritt_lebensbereich.setValue(0)
        self.fortschritt_lebensbereich.setTextVisible(False)
        self.fortschritt_lebensbereich.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.fortschritt_lebensbereich, 7, 1, 1, 1)

        self.button_disform_bearbeiten = QPushButton(self.gridLayoutWidget)
        self.button_disform_bearbeiten.setObjectName(u"button_disform_bearbeiten")
        self.button_disform_bearbeiten.setEnabled(True)

        self.gridLayout.addWidget(self.button_disform_bearbeiten, 9, 3, 1, 1)

        self.fortschritt_aggrelevanz = QProgressBar(self.gridLayoutWidget)
        self.fortschritt_aggrelevanz.setObjectName(u"fortschritt_aggrelevanz")
        self.fortschritt_aggrelevanz.setValue(0)
        self.fortschritt_aggrelevanz.setTextVisible(False)
        self.fortschritt_aggrelevanz.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.fortschritt_aggrelevanz, 11, 1, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignBottom | Qt.AlignLeading | Qt.AlignLeft)

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.label_10 = QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 5, 2, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMidLineWidth(0)
        self.label_5.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.gridLayout.addWidget(self.label_5, 6, 1, 1, 1)

        self.button_intervform_bearbeiten = QPushButton(self.gridLayoutWidget)
        self.button_intervform_bearbeiten.setObjectName(u"button_intervform_bearbeiten")
        self.button_intervform_bearbeiten.setEnabled(True)

        self.gridLayout.addWidget(self.button_intervform_bearbeiten, 10, 3, 1, 1)

        self.label_9 = QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.gridLayout.addWidget(self.label_9, 4, 1, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 7, 2, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)

        self.button_aggrelevanz_bearbeiten = QPushButton(self.gridLayoutWidget)
        self.button_aggrelevanz_bearbeiten.setObjectName(u"button_aggrelevanz_bearbeiten")
        self.button_aggrelevanz_bearbeiten.setEnabled(True)

        self.gridLayout.addWidget(self.button_aggrelevanz_bearbeiten, 11, 3, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 8, 2, 1, 1)

        self.label_11 = QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 10, 2, 1, 1)

        self.button_datengrundlage_bearbeiten = QPushButton(self.gridLayoutWidget)
        self.button_datengrundlage_bearbeiten.setObjectName(u"button_datengrundlage_bearbeiten")

        self.gridLayout.addWidget(self.button_datengrundlage_bearbeiten, 1, 3, 1, 1)

        self.button_template_bearbeiten = QPushButton(self.gridLayoutWidget)
        self.button_template_bearbeiten.setObjectName(u"button_template_bearbeiten")
        self.button_template_bearbeiten.setEnabled(True)
        self.button_template_bearbeiten.setFlat(False)

        self.gridLayout.addWidget(self.button_template_bearbeiten, 3, 3, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 9, 2, 1, 1)

        self.fortschritt_template = QProgressBar(self.gridLayoutWidget)
        self.fortschritt_template.setObjectName(u"fortschritt_template")
        self.fortschritt_template.setValue(0)
        self.fortschritt_template.setTextVisible(False)
        self.fortschritt_template.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.fortschritt_template, 3, 1, 1, 1)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 520, 481, 80))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.button_auswertungen = QPushButton(self.horizontalLayoutWidget)
        self.button_auswertungen.setObjectName(u"button_auswertungen")
        self.button_auswertungen.setMinimumSize(QSize(0, 50))

        self.horizontalLayout.addWidget(self.button_auswertungen)

        self.button_template_speichern = QPushButton(self.horizontalLayoutWidget)
        self.button_template_speichern.setObjectName(u"button_template_speichern")
        self.button_template_speichern.setEnabled(True)
        self.button_template_speichern.setMinimumSize(QSize(0, 50))

        self.horizontalLayout.addWidget(self.button_template_speichern)

        self.button_skript_schliessen = QPushButton(self.horizontalLayoutWidget)
        self.button_skript_schliessen.setObjectName(u"button_skript_schliessen")
        self.button_skript_schliessen.setEnabled(True)
        self.button_skript_schliessen.setMinimumSize(QSize(0, 50))

        self.horizontalLayout.addWidget(self.button_skript_schliessen)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(True)
        self.pushButton.setGeometry(QRect(370, 600, 111, 20))
        self.version = QLabel(self.centralwidget)
        self.version.setObjectName(u"version")
        self.version.setGeometry(QRect(10, 640, 80, 16))
        self.version.setWordWrap(True)
        self.version.setText("Version: ")
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(10, 10, 471, 81))
        self.label_13.setWordWrap(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 497, 22))
        MainWindow.setMenuBar(self.menubar)
        QWidget.setTabOrder(self.button_template_bearbeiten, self.button_datengrundlage_bearbeiten)
        QWidget.setTabOrder(self.button_datengrundlage_bearbeiten, self.button_lebensbereich_bearbeiten)
        QWidget.setTabOrder(self.button_lebensbereich_bearbeiten, self.button_dismerkmal_bearbeiten)
        QWidget.setTabOrder(self.button_dismerkmal_bearbeiten, self.button_auswertungen)
        QWidget.setTabOrder(self.button_auswertungen, self.button_template_speichern)
        QWidget.setTabOrder(self.button_template_speichern, self.button_skript_schliessen)

        self.retranslateUi(MainWindow)

        self.button_template_bearbeiten.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Startfenster", None))
        self.actionLaden.setText(QCoreApplication.translate("MainWindow", u"Laden", None))
        self.actionSpeichern.setText(QCoreApplication.translate("MainWindow", u"Speichern", None))
        self.actionLebensbereich.setText(QCoreApplication.translate("MainWindow", u"Lebensbereich", None))
        self.actionDiskriminierungsmerkmal.setText(QCoreApplication.translate("MainWindow", u"Diskriminierungsmerkmal", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"AGG-Relevanz", None))
        self.button_dismerkmal_bearbeiten.setText(QCoreApplication.translate("MainWindow", u"Bearbeiten", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Einlesen der Vorlage (.pkl)", None))
        self.button_lebensbereich_bearbeiten.setText(QCoreApplication.translate("MainWindow", u"Bearbeiten", None))
        self.button_zeitraum_bearbeiten.setText(QCoreApplication.translate("MainWindow", u"Bearbeiten", None))
        self.button_disform_bearbeiten.setText(QCoreApplication.translate("MainWindow", u"Bearbeiten", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Kategorienvorlage einlesen", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Auswahl des Zeitraums", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Kategorien zuordnen", None))
        self.button_intervform_bearbeiten.setText(QCoreApplication.translate("MainWindow", u"Bearbeiten", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Zeitraum", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Lebensbereich(e)", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Auswahl der Datengrundlage", None))
        self.button_aggrelevanz_bearbeiten.setText(QCoreApplication.translate("MainWindow", u"Bearbeiten", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Diskriminierungsmerkmal(e)", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Interventionsform(en)", None))
        self.button_datengrundlage_bearbeiten.setText(QCoreApplication.translate("MainWindow", u"Auswählen", None))
#if QT_CONFIG(tooltip)
        self.button_template_bearbeiten.setToolTip(QCoreApplication.translate("MainWindow", u"Kategorienvorlage einlesen", None))
#endif // QT_CONFIG(tooltip)
        self.button_template_bearbeiten.setText(QCoreApplication.translate("MainWindow", u"Auswählen", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Datenauswahl", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Diskriminierungsform(en)", None))
        self.button_auswertungen.setText(QCoreApplication.translate("MainWindow", u"Auswertungen", None))
        self.button_template_speichern.setText(QCoreApplication.translate("MainWindow", u"Vorlage speichern", None))
        self.button_skript_schliessen.setText(QCoreApplication.translate("MainWindow", u"Skript schlie\u00dfen", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"spezialfunktionen", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Dieses Tool dient zur \u00dcbersetzung von bestehenden Dokumentationssystemen f\u00fcr Antidiskriminierungsberatungen in die Kategorien der von der Antidiskriminierungsstelle des Bundes herausgegebenen Mindeststandards.\nBitte arbeiten Sie die Schritte von oben nach unten durch.", None))
        myFont = QFont()
        myFont.setBold(True)
        self.label_13.setFont(myFont)

    # retranslateUi

