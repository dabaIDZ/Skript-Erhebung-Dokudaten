# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_ausfuellhinweise.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHeaderView, QLabel,
    QScrollArea, QSizePolicy, QTextBrowser, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_fenster_ausfuellhinweise(object):
    def setupUi(self, fenster_ausfuellhinweise):
        if not fenster_ausfuellhinweise.objectName():
            fenster_ausfuellhinweise.setObjectName(u"fenster_ausfuellhinweise")
        fenster_ausfuellhinweise.resize(480, 640)
        self.treeWidget = QTreeWidget(fenster_ausfuellhinweise)
        __qtreewidgetitem = QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(self.treeWidget)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(30, 50, 161, 561))
        self.scrollArea = QScrollArea(fenster_ausfuellhinweise)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(200, 50, 271, 561))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 269, 559))
        self.textBrowser = QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(0, 0, 251, 561))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label = QLabel(fenster_ausfuellhinweise)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 20, 151, 16))

        self.retranslateUi(fenster_ausfuellhinweise)

        QMetaObject.connectSlotsByName(fenster_ausfuellhinweise)
    # setupUi

    def retranslateUi(self, fenster_ausfuellhinweise):
        fenster_ausfuellhinweise.setWindowTitle(QCoreApplication.translate("fenster_ausfuellhinweise", u"Dialog", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("fenster_ausfuellhinweise", u"Inhalt", None));

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("fenster_ausfuellhinweise", u"Neues Element", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("fenster_ausfuellhinweise", u"Neues untergeordnetes Element", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("fenster_ausfuellhinweise", u"Neues untergeordnetes Element", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem1.child(2)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("fenster_ausfuellhinweise", u"Neues untergeordnetes Element", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem1.child(3)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("fenster_ausfuellhinweise", u"Neues untergeordnetes Element", None));
        ___qtreewidgetitem6 = self.treeWidget.topLevelItem(1)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("fenster_ausfuellhinweise", u"Neues Element", None));
        ___qtreewidgetitem7 = self.treeWidget.topLevelItem(2)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("fenster_ausfuellhinweise", u"Neues Element", None));
        ___qtreewidgetitem8 = self.treeWidget.topLevelItem(3)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("fenster_ausfuellhinweise", u"Neues Element", None));
        ___qtreewidgetitem9 = self.treeWidget.topLevelItem(4)
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("fenster_ausfuellhinweise", u"Neues Element", None));
        ___qtreewidgetitem10 = self.treeWidget.topLevelItem(5)
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("fenster_ausfuellhinweise", u"Neues Element", None));
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.label.setText(QCoreApplication.translate("fenster_ausfuellhinweise", u"Codierhinweise", None))
    # retranslateUi

