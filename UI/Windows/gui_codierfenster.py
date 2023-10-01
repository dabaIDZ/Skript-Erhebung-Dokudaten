# -*- coding: utf-8 -*-
################################################################################
## Form generated from reading UI file 'gui_codierfenster.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QDialog,
    QGridLayout, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QListWidget, QListWidgetItem, QProgressBar,
    QPushButton, QRadioButton, QSizePolicy, QTabWidget,
    QVBoxLayout, QWidget, QScrollArea)

class Ui_fenster_codieren(object):
    def setupUi(self, fenster_codieren):
        if not fenster_codieren.objectName():
            fenster_codieren.setObjectName(u"fenster_codieren")
        fenster_codieren.resize(494, 717)
        self.tabwidg_inhalt = QTabWidget(fenster_codieren)
        self.tabwidg_inhalt.setObjectName(u"tabwidg_inhalt")
        self.tabwidg_inhalt.setEnabled(True)
        self.tabwidg_inhalt.setGeometry(QRect(10, 170, 481, 541))
        self.tabwidg_inhalt.setTabShape(QTabWidget.Triangular)
        self.tabwidg_inhalt.setDocumentMode(False)
        self.tabwidg_inhalt.setTabsClosable(False)
        self.tabwidg_inhalt.setMovable(False)
        self.tabwidg_inhalt.setTabBarAutoHide(False)
        self.tab_spalten = QWidget()
        self.tab_spalten.setObjectName(u"tab_spalten")
        self.label = QLabel(self.tab_spalten)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 441, 100))
        self.label.setWordWrap(True)
        self.horizontalLayoutWidget = QWidget(self.tab_spalten)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 120, 451, 220))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.listWidget_Spalten = QListWidget(self.horizontalLayoutWidget)
        self.listWidget_Spalten.setObjectName(u"listWidget_Spalten")
        self.listWidget_Spalten.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.horizontalLayout.addWidget(self.listWidget_Spalten)

        self.text_spaltenauswahl = QLabel(self.horizontalLayoutWidget)
        self.text_spaltenauswahl.setObjectName(u"text_spaltenauswahl")
        self.text_spaltenauswahl.setWordWrap(True)

        self.horizontalLayout.addWidget(self.text_spaltenauswahl)

        self.verticalLayoutWidget = QWidget(self.tab_spalten)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 330, 451, 124))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.check_Spalte_genannt = QCheckBox(self.verticalLayoutWidget)
        self.check_Spalte_genannt.setObjectName(u"check_Spalte_genannt")


        self.horizontalLayout_6.addWidget(self.check_Spalte_genannt)

        self.verticalLayout.addSpacing(20)
        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button_spaltenauswahl_speichern = QPushButton(self.verticalLayoutWidget)
        self.button_spaltenauswahl_speichern.setObjectName(u"button_spaltenauswahl_speichern")

        self.horizontalLayout_2.addWidget(self.button_spaltenauswahl_speichern)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tabwidg_inhalt.addTab(self.tab_spalten, "")
        self.tab_details = QWidget()
        self.tab_details.setObjectName(u"tab_details")
        self.tabwidg_inhalt.addTab(self.tab_details, "")
        self.tab_genannt_markierungen = QWidget()
        self.tab_genannt_markierungen.setObjectName(u"tab_genannt_markierungen")
        self.tab_genannt_markierungen.setEnabled(False)
        self.verticalLayoutWidget_6 = QWidget(self.tab_genannt_markierungen)
        self.verticalLayoutWidget_6.setObjectName(u"verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(20, 17, 418, 491))
        self.verticalLayout_5 = QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.verticalLayoutWidget_6)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setWordWrap(True)

        self.verticalLayout_5.addWidget(self.label_11)

        self.label_genannt_beispiele = QLabel(self.verticalLayoutWidget_6)
        self.label_genannt_beispiele.setObjectName(u"label_genannt_beispiele")

        self.verticalLayout_5.addWidget(self.label_genannt_beispiele)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.radio_genannt_nichtleer = QRadioButton(self.verticalLayoutWidget_6)
        self.radio_genannt_nichtleer.setObjectName(u"radio_genannt_nichtleer")

        self.horizontalLayout_7.addWidget(self.radio_genannt_nichtleer)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.radio_genannt_zeichen = QRadioButton(self.verticalLayoutWidget_6)
        self.radio_genannt_zeichen.setObjectName(u"radio_genannt_zeichen")

        self.horizontalLayout_8.addWidget(self.radio_genannt_zeichen)

        self.line_genannt_zeichen = QLineEdit(self.verticalLayoutWidget_6)
        self.line_genannt_zeichen.setObjectName(u"line_genannt_zeichen")

        self.horizontalLayout_8.addWidget(self.line_genannt_zeichen)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.radio_genannt_nichtzeichen = QRadioButton(self.verticalLayoutWidget_6)
        self.radio_genannt_nichtzeichen.setObjectName(u"radio_genannt_nichtzeichen")

        self.horizontalLayout_9.addWidget(self.radio_genannt_nichtzeichen)

        self.line_genannt_nichtzeichen = QLineEdit(self.verticalLayoutWidget_6)
        self.line_genannt_nichtzeichen.setObjectName(u"line_genannt_nichtzeichen")

        self.horizontalLayout_9.addWidget(self.line_genannt_nichtzeichen)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.button_genannt_markierung_speichern = QPushButton(self.verticalLayoutWidget_6)
        self.button_genannt_markierung_speichern.setObjectName(u"button_genannt_markierung_speichern")

        self.horizontalLayout_10.addWidget(self.button_genannt_markierung_speichern)


        self.verticalLayout_5.addLayout(self.horizontalLayout_10)

        self.tabwidg_inhalt.addTab(self.tab_genannt_markierungen, "")
        self.tab_trennzeichen = QWidget()
        self.tab_trennzeichen.setObjectName(u"tab_trennzeichen")
        self.tab_trennzeichen.setEnabled(False)
        self.verticalLayoutWidget_2 = QWidget(self.tab_trennzeichen)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 20, 441, 481))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_2)

        spacer3 = QWidget(self)
        spacer3.setFixedSize(1, 15)

        self.verticalLayout_2.addWidget(spacer3)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lineEdit_trennzeichen3 = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_trennzeichen3.setObjectName(u"lineEdit_trennzeichen3")

        self.gridLayout_2.addWidget(self.lineEdit_trennzeichen3, 3, 1, 1, 1)

        self.label_10 = QLabel(self.verticalLayoutWidget_2)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 3, 0, 1, 1)

        self.label_8 = QLabel(self.verticalLayoutWidget_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)

        self.label_9 = QLabel(self.verticalLayoutWidget_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)

        self.lineEdit_trennzeichen2 = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_trennzeichen2.setObjectName(u"lineEdit_trennzeichen2")

        self.gridLayout_2.addWidget(self.lineEdit_trennzeichen2, 2, 1, 1, 1)

        self.lineEdit_trennzeichen1 = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_trennzeichen1.setObjectName(u"lineEdit_trennzeichen1")

        self.gridLayout_2.addWidget(self.lineEdit_trennzeichen1, 1, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_2)


        self.checkBox = QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox.setObjectName(u"checkBox")

        spacer = QWidget(self)
        spacer.setFixedSize(1, 10)

        spacer2 = QWidget(self)
        spacer2.setFixedSize(1, 10)

        self.verticalLayout_2.addWidget(spacer)
        self.verticalLayout_2.addWidget(self.checkBox)
        self.verticalLayout_2.addWidget(spacer2)



        self.label_trennzeichen_beispiele = QLabel(self.verticalLayoutWidget_2)
        self.label_trennzeichen_beispiele.setObjectName(u"label_trennzeichen_beispiele")
        self.label_trennzeichen_beispiele.setWordWrap(True)

        scroll_area_2 = QScrollArea()
        scroll_area_2.setWidgetResizable(True)

        # Erstellen eines Widgets für das Layout innerhalb der Scroll Area
        self.scroll_widget_2 = QWidget()
        scroll_layout_2 = QVBoxLayout(self.scroll_widget_2)
        scroll_layout_2.addWidget(self.label_trennzeichen_beispiele)

        # Das Scroll-Widget der Scroll Area zuweisen
        scroll_area_2.setWidget(self.scroll_widget_2)

        # Das Scroll-Widget zum Layout hinzufügen
        self.verticalLayout_2.addWidget(scroll_area_2)


        #self.scroll_widget_2 = QWidget()
        #scroller = QVBoxLayout(self.scroll_widget_2)
        #scroller.addWidget(self.label_trennzeichen_beispiele)


        #scroll_area = QScrollArea(self)



        #scroll_area.setWidget(self.label_trennzeichen_beispiele)
        #self.verticalLayout_2.addWidget(self.label_trennzeichen_beispiele)
        #self.verticalLayout_2.addWidget(scroll_area)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.button_trennzeichenauswahl_speichern = QPushButton(self.verticalLayoutWidget_2)
        self.button_trennzeichenauswahl_speichern.setObjectName(u"button_trennzeichenauswahl_speichern")

        self.horizontalLayout_5.addWidget(self.button_trennzeichenauswahl_speichern)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.tabwidg_inhalt.addTab(self.tab_trennzeichen, "")
        self.tab_codes_auswahl = QWidget()
        self.tab_codes_auswahl.setObjectName(u"tab_codes_auswahl")
        self.tab_codes_auswahl.setEnabled(False)
        self.verticalLayoutWidget_7 = QWidget(self.tab_codes_auswahl)
        self.verticalLayoutWidget_7.setObjectName(u"verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(10, 10, 441, 461))
        self.verticalLayout_6 = QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.verticalLayoutWidget_7)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setWordWrap(True)
        self.label_5.setMinimumSize(0, 70)
        myFont = QFont()
        myFont.setBold(True)
        self.label_5.setFont(myFont)
        self.verticalLayout_6.addWidget(self.label_5)

        self.verticalLayout_codes_liste = QVBoxLayout()
        self.verticalLayout_codes_liste.setObjectName(u"verticalLayout_codes_liste")
        self.verticalLayout_codes_liste.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.verticalLayout_6.addLayout(self.verticalLayout_codes_liste)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.button_codeauswahl_speichern = QPushButton(self.verticalLayoutWidget_7)
        self.button_codeauswahl_speichern.setObjectName(u"button_codeauswahl_speichern")

        self.horizontalLayout_11.addWidget(self.button_codeauswahl_speichern)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)

        self.tabwidg_inhalt.addTab(self.tab_codes_auswahl, "")
        self.tab_codieren = QWidget()
        self.tab_codieren.setObjectName(u"tab_codieren")
        self.tab_codieren.setEnabled(False)
        self.verticalLayoutWidget_5 = QWidget(self.tab_codieren)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(10, 10, 442, 131))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.verticalLayoutWidget_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label_7)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lbl_codetext = QLabel(self.verticalLayoutWidget_5)
        self.lbl_codetext.setObjectName(u"lbl_codetext")
        self.lbl_codetext.setWordWrap(True)

        self.horizontalLayout_4.addWidget(self.lbl_codetext)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.checkBox_codieren_codierteanzeigen = QCheckBox(self.verticalLayoutWidget_5)
        self.checkBox_codieren_codierteanzeigen.setObjectName(u"checkBox_codieren_codierteanzeigen")
        self.checkBox_codieren_codierteanzeigen.setChecked(True)

        self.verticalLayout_3.addWidget(self.checkBox_codieren_codierteanzeigen)

        self.checkBox_codieren_uncodierteanzeigen = QCheckBox(self.verticalLayoutWidget_5)
        self.checkBox_codieren_uncodierteanzeigen.setObjectName(u"checkBox_codieren_uncodierteanzeigen")
        self.checkBox_codieren_uncodierteanzeigen.setChecked(True)

        self.verticalLayout_3.addWidget(self.checkBox_codieren_uncodierteanzeigen)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.verticalLayoutWidget_3 = QWidget(self.tab_codieren)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 140, 444, 291))
        self.verticalLayout_codierung_ersteebene = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_codierung_ersteebene.setObjectName(u"verticalLayout_codierung_ersteebene")
        self.verticalLayout_codierung_ersteebene.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_codierung_ersteebene.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.verticalLayout_codierung_ersteebene.addLayout(self.horizontalLayout_3)

        self.horizontalLayoutWidget_3 = QWidget(self.tab_codieren)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(10, 430, 440, 41))
        self.horizontalLayout_13 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.button_zumersten = QPushButton(self.horizontalLayoutWidget_3)
        self.button_zumersten.setObjectName(u"button_zumersten")

        self.horizontalLayout_13.addWidget(self.button_zumersten)

        self.button_rueckwaerts = QPushButton(self.horizontalLayoutWidget_3)
        self.button_rueckwaerts.setObjectName(u"button_rueckwaerts")

        self.horizontalLayout_13.addWidget(self.button_rueckwaerts)

        self.line_codeakt_num = QLineEdit(self.horizontalLayoutWidget_3)
        self.line_codeakt_num.setObjectName(u"line_codeakt_num")
        self.line_codeakt_num.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.line_codeakt_num.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.line_codeakt_num)

        self.lbl_codieren_gesamtzahl = QLabel(self.horizontalLayoutWidget_3)
        self.lbl_codieren_gesamtzahl.setObjectName(u"lbl_codieren_gesamtzahl")

        self.horizontalLayout_13.addWidget(self.lbl_codieren_gesamtzahl)

        self.button_vorwaerts = QPushButton(self.horizontalLayoutWidget_3)
        self.button_vorwaerts.setObjectName(u"button_vorwaerts")

        self.horizontalLayout_13.addWidget(self.button_vorwaerts)

        self.button_zumletzten = QPushButton(self.horizontalLayoutWidget_3)
        self.button_zumletzten.setObjectName(u"button_zumletzten")

        self.horizontalLayout_13.addWidget(self.button_zumletzten)

        self.tabwidg_inhalt.addTab(self.tab_codieren, "")
        self.gridLayoutWidget = QWidget(fenster_codieren)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 40, 231, 116))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)

        self.fortschritt_codieren = QProgressBar(self.gridLayoutWidget)
        self.fortschritt_codieren.setObjectName(u"fortschritt_codieren")
        self.fortschritt_codieren.setValue(0)
        self.fortschritt_codieren.setTextVisible(False)

        self.gridLayout.addWidget(self.fortschritt_codieren, 3, 0, 1, 1)

        self.fortschritt_details = QProgressBar(self.gridLayoutWidget)
        self.fortschritt_details.setObjectName(u"fortschritt_details")
        self.fortschritt_details.setValue(0)
        self.fortschritt_details.setTextVisible(False)

        self.gridLayout.addWidget(self.fortschritt_details, 1, 0, 1, 1)

        self.fortschritt_spalte = QProgressBar(self.gridLayoutWidget)
        self.fortschritt_spalte.setObjectName(u"fortschritt_spalte")
        self.fortschritt_spalte.setValue(0)
        self.fortschritt_spalte.setTextVisible(False)

        self.gridLayout.addWidget(self.fortschritt_spalte, 0, 0, 1, 1)

        self.lbl_fort_daten_cod = QLabel(self.gridLayoutWidget)
        self.lbl_fort_daten_cod.setObjectName(u"lbl_fort_daten_cod")

        self.gridLayout.addWidget(self.lbl_fort_daten_cod, 3, 1, 1, 1)

        self.label_13 = QLabel(self.gridLayoutWidget)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 1, 1, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)

        self.fortschritt_codes = QProgressBar(self.gridLayoutWidget)
        self.fortschritt_codes.setObjectName(u"fortschritt_codes")
        self.fortschritt_codes.setValue(0)
        self.fortschritt_codes.setTextVisible(False)

        self.gridLayout.addWidget(self.fortschritt_codes, 2, 0, 1, 1)

        self.horizontalLayoutWidget_2 = QWidget(fenster_codieren)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(20, 10, 471, 31))
        self.horizontalLayout_12 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_codierung_ueberschrift = QLabel(self.horizontalLayoutWidget_2)
        self.label_codierung_ueberschrift.setObjectName(u"label_codierung_ueberschrift")

        self.horizontalLayout_12.addWidget(self.label_codierung_ueberschrift)

        self.button_OK = QPushButton(self.horizontalLayoutWidget_2)
        self.button_OK.setObjectName(u"button_OK")

        self.horizontalLayout_12.addWidget(self.button_OK)

        QWidget.setTabOrder(self.tabwidg_inhalt, self.lineEdit_trennzeichen1)
        QWidget.setTabOrder(self.lineEdit_trennzeichen1, self.lineEdit_trennzeichen2)
        QWidget.setTabOrder(self.lineEdit_trennzeichen2, self.lineEdit_trennzeichen3)
        QWidget.setTabOrder(self.lineEdit_trennzeichen3, self.checkBox_codieren_uncodierteanzeigen)
        QWidget.setTabOrder(self.checkBox_codieren_uncodierteanzeigen, self.checkBox_codieren_codierteanzeigen)
        QWidget.setTabOrder(self.checkBox_codieren_codierteanzeigen, self.button_trennzeichenauswahl_speichern)
        QWidget.setTabOrder(self.button_trennzeichenauswahl_speichern, self.checkBox)
        QWidget.setTabOrder(self.checkBox, self.listWidget_Spalten)
        QWidget.setTabOrder(self.listWidget_Spalten, self.button_spaltenauswahl_speichern)
        QWidget.setTabOrder(self.button_spaltenauswahl_speichern, self.check_Spalte_genannt)
        QWidget.setTabOrder(self.check_Spalte_genannt, self.radio_genannt_nichtleer)
        QWidget.setTabOrder(self.radio_genannt_nichtleer, self.radio_genannt_zeichen)
        QWidget.setTabOrder(self.radio_genannt_zeichen, self.line_genannt_zeichen)
        QWidget.setTabOrder(self.line_genannt_zeichen, self.radio_genannt_nichtzeichen)
        QWidget.setTabOrder(self.radio_genannt_nichtzeichen, self.line_genannt_nichtzeichen)
        QWidget.setTabOrder(self.line_genannt_nichtzeichen, self.button_genannt_markierung_speichern)

        self.retranslateUi(fenster_codieren)

        self.tabwidg_inhalt.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(fenster_codieren)
    # setupUi

    def retranslateUi(self, fenster_codieren):
        myFont = QFont()
        myFont.setBold(True)
        fenster_codieren.setWindowTitle(QCoreApplication.translate("fenster_codieren", u"Kategorien zuordnen", None))
        self.label.setTextFormat(Qt.RichText)  # Specify that the text is in HTML format

        self.label.setText('<b>Bitte wählen Sie alle Spalten aus, in denen die Informationen gespeichert sind.</b>'
                           '<br/>\tMehrere Spalten untereinander können Sie mit gedrückter Shift-Taste auswählen.'
                           '<br/>\tUm einzelne Spalten auszuwählen, halten Sie die STRG-Taste gedrückt.')
        self.label_2.setTextFormat(Qt.RichText)  # Specify that the text is in HTML format

        self.label_2.setText('<b>Wenn in den einzelnen Spalten Mehrfachantworten m\u00f6glich sind, mit welchen Trennzeichen werden die einzelnen Antworten getrennt?</b>\n'
                           '\n<p>Beispiel: <i>Rassismus, Geschlecht, Lebensalter</i></p>'
                           '<p>&#8594; Trennzeichen ist das Komma.</p>')

        self.text_spaltenauswahl.setText(QCoreApplication.translate("fenster_codieren", u"Folgende Spalten sind ausgew\u00e4hlt:", None))
        self.check_Spalte_genannt.setText(QCoreApplication.translate("fenster_codieren", u"Die Spalte(n) funktionieren nach dem Prinzip genannt/nicht genannt.", None))
        self.button_spaltenauswahl_speichern.setText(QCoreApplication.translate("fenster_codieren", u"Weiter", None))
        self.tabwidg_inhalt.setTabText(self.tabwidg_inhalt.indexOf(self.tab_spalten), QCoreApplication.translate("fenster_codieren", u"Spalten", None))
        self.tabwidg_inhalt.setTabText(self.tabwidg_inhalt.indexOf(self.tab_details), QCoreApplication.translate("fenster_codieren", u"Details", None))
        self.label_11.setText(QCoreApplication.translate("fenster_codieren", u"Bitte geben Sie an, wie in den Spalten die genannt Markierung zu erkennen ist.", None))
        self.label_genannt_beispiele.setText(QCoreApplication.translate("fenster_codieren", u"Wenn in den ", None))
        self.radio_genannt_nichtleer.setText(QCoreApplication.translate("fenster_codieren", u"Sobald die Spalte nicht leer ist, gilt die Spalte als genannt", None))
        self.radio_genannt_zeichen.setText(QCoreApplication.translate("fenster_codieren", u"Sobald die Spalte folgende Zeichenfolge enth\u00e4lt, \n"
"gilt die Spalte als genannt", None))
        self.radio_genannt_nichtzeichen.setText(QCoreApplication.translate("fenster_codieren", u"Sobald die Spalte folgende Zeichenfolge nicht\n"
"enth\u00e4lt, gilt die Spalte als genannt", None))
        self.button_genannt_markierung_speichern.setText(QCoreApplication.translate("fenster_codieren", u"Weiter", None))
        self.tabwidg_inhalt.setTabText(self.tabwidg_inhalt.indexOf(self.tab_genannt_markierungen), QCoreApplication.translate("fenster_codieren", u"Genannt-Markierung", None))
        self.label_10.setText(QCoreApplication.translate("fenster_codieren", u"Trennzeichen 3", None))
        self.label_8.setText(QCoreApplication.translate("fenster_codieren", u"Trennzeichen 1", None))
        self.label_9.setText(QCoreApplication.translate("fenster_codieren", u"Trennzeichen 2", None))
        self.checkBox.setText(QCoreApplication.translate("fenster_codieren", u"Es gibt keine Trennzeichen", None))
        self.label_trennzeichen_beispiele.setText(QCoreApplication.translate("fenster_codieren", u"Wenn in den ", None))
        self.button_trennzeichenauswahl_speichern.setText(QCoreApplication.translate("fenster_codieren", u"Weiter", None))
        self.tabwidg_inhalt.setTabText(self.tabwidg_inhalt.indexOf(self.tab_trennzeichen), QCoreApplication.translate("fenster_codieren", u"Trennzeichen", None))
        self.label_5.setText(QCoreApplication.translate("fenster_codieren", u"Welche Informationen k\u00f6nnen Sie mit den angegebenen Spalten auslesen?", None))
        self.button_codeauswahl_speichern.setText(QCoreApplication.translate("fenster_codieren", u"Weiter", None))
        self.tabwidg_inhalt.setTabText(self.tabwidg_inhalt.indexOf(self.tab_codes_auswahl), QCoreApplication.translate("fenster_codieren", u"Kategorien wählen", None))
        self.label_7.setText(QCoreApplication.translate("fenster_codieren", u"Bitte codieren Sie hier die Werte aus ihrer Dokumentation anhand der Mindeststandards zur AD-Beratungsdokumentation.", None))
        self.lbl_codetext.setText(QCoreApplication.translate("fenster_codieren", u"Noch nicht ausgew\u00e4hlt", None))
        self.checkBox_codieren_codierteanzeigen.setText(QCoreApplication.translate("fenster_codieren", u"Zeige zugeordnete Daten", None))
        self.checkBox_codieren_uncodierteanzeigen.setText(QCoreApplication.translate("fenster_codieren", u"Zeige nicht zugeordnete Daten", None))
        self.button_zumersten.setText(QCoreApplication.translate("fenster_codieren", u"|<", None))
        self.button_rueckwaerts.setText(QCoreApplication.translate("fenster_codieren", u"<", None))
        self.lbl_codieren_gesamtzahl.setText(QCoreApplication.translate("fenster_codieren", u"/nan         ", None))
        self.button_vorwaerts.setText(QCoreApplication.translate("fenster_codieren", u">", None))
        self.button_zumletzten.setText(QCoreApplication.translate("fenster_codieren", u">|", None))
        self.tabwidg_inhalt.setTabText(self.tabwidg_inhalt.indexOf(self.tab_codieren), QCoreApplication.translate("fenster_codieren", u"Daten zuordnen", None))
        self.label_3.setText(QCoreApplication.translate("fenster_codieren", u"Kategorien wählen", None))
        self.lbl_fort_daten_cod.setText(QCoreApplication.translate("fenster_codieren", u"Daten zuordnen", None))
        self.label_13.setText(QCoreApplication.translate("fenster_codieren", u"Details kl\u00e4ren", None))
        self.label_4.setText(QCoreApplication.translate("fenster_codieren", u"Spalte ausw\u00e4hlen", None))
        self.label_codierung_ueberschrift.setText(QCoreApplication.translate("fenster_codieren", u"Codierung:", None))
        self.button_OK.setText(QCoreApplication.translate("fenster_codieren", u"Bearbeitung abschlie\u00dfen", None))
    # retranslateUi

