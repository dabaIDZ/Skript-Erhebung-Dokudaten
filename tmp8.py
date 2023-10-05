version = '1.0'

import sys
import copy
import docx
import os
import openpyxl
import pandas as pd
import numpy as np
import zipfile

import itertools
from PySide6 import QtCore
from PySide6.QtCore import Qt, QSignalBlocker
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import re
import pickle
import seaborn as sns
from IPython.display import display
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QCheckBox, QVBoxLayout, QHBoxLayout, QWidget, \
    QScrollArea, QGridLayout, QDialogButtonBox, QVBoxLayout, QDialog, QLabel, QSizePolicy, QRadioButton, QLineEdit, \
    QPlainTextEdit, QLineEdit, QTextEdit, QFileDialog, QTreeWidgetItem, QMessageBox
# import PyQt6.QtWidgets
from PySide6.QtGui import QIntValidator
from UI.Windows.gui_mainwindow import Ui_MainWindow
from UI.Windows.gui_fenster_datengrundlage_einfach import Ui_fenster_datengrundlage_einfach
from UI.Windows.gui_codierfenster import Ui_fenster_codieren
from UI.Windows.gui_zeitraum_festlegen import Ui_fenster_zeitraum_festlegen
from UI.Windows.gui_ausfuellhinweise import Ui_fenster_ausfuellhinweise
from UI.Windows.gui_fenster_datenausgabe import Ui_fenster_datenausgabe
from data_fuer_grafik_vorbereiten import Data_Fuer_Grafik_Vorbereiten

data_vorbereiten = Data_Fuer_Grafik_Vorbereiten()
from grafik_erstellen import Grafik_Erstellen

# ohne Funktion im Moment
testbetrieb = False

# Wenn True, werden die UI-Dateien neu eingelesen
UI_neueinlesen = False

data_vorbereiten = Data_Fuer_Grafik_Vorbereiten()

# Pfad individuell anpassen
code = '''
os.chdir(r"/Users/felixbajus/Desktop/Arbeit/IDZ")
os.system("pyside6-uic UI/gui_mainwindow.ui -o UI/Windows/gui_mainwindow.py")
os.system("pyside6-uic UI/gui_fenster_datengrundlage_einfach.ui -o UI/Windows/gui_fenster_datengrundlage_einfach.py")
os.system("pyside6-uic UI/gui_codierfenster.ui -o UI/Windows/gui_codierfenster.py")
os.system("pyside6-uic UI/gui_zeitraum_festlegen.ui -o UI/Windows/gui_zeitraum_festlegen.py")
os.system("pyside6-uic UI/gui_ausfuellhinweise.ui -o UI/Windows/gui_ausfuellhinweise.py")
os.system("pyside6-uic UI/gui_fenster_datenausgabe.ui -o UI/Windows/gui_fenster_datenausgabe.py")
'''

# wenn oben True, dann wird hier die UI-Datei neu eingelesen
if UI_neueinlesen:
    exec(code)

# Objekt erstellen
grafik_erstell = Grafik_Erstellen()

# Pandas-Optionen setzen
pd.set_option('display.max_columns', None)


# Klasse zum Speichern der Daten
class Datenspeicher:
    def __init__(self):
        self.pfad_datengrundlage_einfach = ""  # Ort der Datengrundlage, wenn es sich nur um eine Datei handelt

        # Speicher wird mit leeren Werten initialisiert
        self.datengrundlage_eingelesen = False
        self.df = pd.DataFrame()
        self.df_original = pd.DataFrame()  # Dataframe vor Codierung und vor Einschränkung des Zeitraumes

        self.zeitraum_ausgewaehlt = False

        self.aktuell_codiert = ""

        self.spalten_gesamt = []

        self.codierfenster_initialisieren()
        self.eintraege_liste = []

        self.spalten_lebensbereich = []
        self.trennzeichen_liste_lebensbereich = []
        self.genannt_lebensbereich = False
        self.dict_code_checkboxes_auswahl_lebensbereich = {}
        self.lebensbereich_codiert = False
        self.fortschritt_lebensbereiche = 0
        self.codierliste_dict_lebensbereich = {}
        self.dict_lebensbereiche_vorgabe = {
            # dict mit den Vorgaben für die Codierung, Key: Oberbegriff, Value: Liste mit Unterpunkten
            "Arbeit": ["Durchführung des Beschäftigungsverhältnisses",
                       "Anbahnung/ Zugang zu einem Beschäftigungsverhältnis", "Arbeitsalltag",
                       "Beendigung des Arbeitsverhältnisses", "anderes - Arbeit", "keine Angabe - Arbeit",
                       "ignorieren - Arbeit"],
            "Bildung": ["Kita", "Schule", "Sonderpädagogischer Förderbedarf", "Hochschule", "Weiterbildung",
                        "private Bildungseinrichtung", "anderes - Bildung", "keine Angabe - Bildung",
                        "ignorieren - Bildung"],
            "Ämter und Behörden": ["Jobcenter/ Arbeitsagentur", "Ausländerbehörde", "Finanzamt", "Jugendamt",
                                   "Standesamt", "Ordnungsamt", "Gewerbeamt", "Bürgeramt/ Einwohnermeldeamt",
                                   "anderes - Behörden", "keine Angabe - Behörden", "ignorieren - Behörden"],
            "Justiz und Polizei": ["Justiz", "Polizei", "anderes - Justiz und Polizei",
                                   "keine Angabe - Justiz und Polizei", "ignorieren - Justiz und Polizei"],
            "Güter und Dienstleistungen": ["Geschäft", "Gastronomie", "Fitnessstudio", "Kultureinrichtung",
                                           "Nachtleben/ Bar/ Disko", "Finanzdienstleistung", "Hotel",
                                           "Post/ Lieferdienste", "ÖPNV und Fernverkehr",
                                           "anderes - Güter und Dienstleistungen",
                                           "keine Angabe - Güter und Dienstleistungen",
                                           "ignorieren - Güter und Dienstleistungen"],
            "Wohnen": ["Wohnungssuche", "bestehendes Wohnverhältnis", "anderes - Wohnen", "keine Angabe - Wohnen",
                       "ignorieren - Wohnen"],
            "Gesundheit und Pflege": ["Krankenhaus", "Ärzt*innenpraxis", "Psychosoziale Einrichtung",
                                      "Pflegeeinrichtung", "Krankenversicherung", "anderes - Gesundheit und Pflege",
                                      "keine Angabe - Gesundheit und Pflege", "ignorieren - Gesundheit und Pflege"],
            "Öffentlichkeit und Freizeit": ["persönliches Umfeld", "öffentlicher Raum", "Verein",
                                            "religiöse Einrichtung", "anderes - Öffentlichkeit und Freizeit",
                                            "keine Angabe - Öffentlichkeit und Freizeit",
                                            "ignorieren - Öffentlichkeit und Freizeit"],
            "Medien": ["Soziale Medien/ soziale Netzwerke", "Onlinemedien", "Printmedien", "Fernsehen/ Radio",
                       "Internet", "Werbung", "anderes - Medien", "keine Angabe - Medien", "ignorieren - Medien"],
            "anderes - Lebensbereich": [],
            "keine Angabe - Lebensbereich": [],
            "ignorieren - Lebensbereich": []
        }
        self.dict_lebensbereiche_codierung = {}
        self.spalten_diskriminierungsmerkmale = []
        self.trennzeichen_liste_diskriminierungsmerkmale = []
        self.genannt_diskriminierungsmerkmale = False
        self.dict_code_checkboxes_auswahl_diskriminierungsmerkmale = {}
        self.diskriminierungsmerkmale_codiert = False
        self.fortschritt_diskriminierungsmerkmale = 0
        self.codierliste_dict_diskriminierungsmerkmal = {}
        self.dict_diskriminierungsmerkmale_vorgabe = {
            # dict mit den Vorgaben für die Codierung, Key: Oberbegriff, Value: Liste mit Unterpunkten
            "Geschlecht": ["Frausein / Sexismus", "Mannsein", "Trans*sein/ Trans*Hintergrund", "Inter*sein",
                           "Non-Binary", "anderes-Geschlecht"],
            "Sexuelle Identität": ["lesbisch", "schwul", "bisexuell", "queer", "asexuell",
                                   "anderes-Sexuelle Identität"],
            "Lebensalter": ["hohes Alter", "geringes Alter", "anderes-Lebensalter"],
            "Behinderung/ Chronische Erkrankung": ["Behinderung", "Chronische Erkrankung",
                                                   "anderes - Behinderung/ Chronische Erkrankung",
                                                   "keine Angabe - Behinderung/ Chronische Erkrankung",
                                                   "ignorieren - Behinderung/ Chronische Erkrankung"],
            "Religion/ Weltanschauung": ["Buddhismus", "Christentum", "Hinduismus", "Islam", "Judentum",
                                         "konfessionslos", "Weltanschauung", "anderes - Religion/ Weltanschauung",
                                         "keine Angabe - Religion/ Weltanschauung",
                                         "ignorieren - Religion/ Weltanschauung"],
            "Antisemitismus, rassistische Zuschreibungen und (ethnische) Herkunft": ["Antimuslimischer Rassismus",
                                                                                     "Antischwarzer Rassismus",
                                                                                     "Rassismus gegen Rom*nja / Sinti*zze (Antiziganismus)",
                                                                                     "Antiasiatischer Rassismus",
                                                                                     "Antislawischer Rassismus",
                                                                                     "Fluchterfahrung",
                                                                                     "Aufenthaltsstatus",
                                                                                     "(zugeschriebene) Ethnische Herkunft",
                                                                                     "Staatsangehörigkeit", "Sprache",
                                                                                     "Antisemitismus",
                                                                                     "anderes - Antisemitismus, Rassismus, (ethnische) Herkunft",
                                                                                     "keine Angabe - Antisemitismus, rassistische Zuschreibungen und (ethnische) Herkunft",
                                                                                     "ignorieren - Antisemitismus, rassistische Zuschreibungen und (ethnische) Herkunft"],
            "Sozialer Status": ["Bildung", "Einkommen", "Wohnsituation", "anderes - Sozialer Status",
                                "keine Angabe - Sozialer Status", "ignorieren - Sozialer Status"],
            "anderes - Diskriminierungsmerkmal": [],
            "keine Angabe - Diskriminierungsmerkmal": [],
            "ignorieren - Diskriminierungsmerkmal": []
        }
        self.spalten_interventionsformen = []
        self.trennzeichen_liste_interventionsformen = []
        self.genannt_interventionsformen = False
        self.dict_code_checkboxes_auswahl_interventionsformen = {}
        self.interventionsformen_codiert = False
        self.fortschritt_interventionsform = 0
        self.codierliste_dict_interventionsform = {}
        self.dict_interventionsformen_vorgabe = {
            # dict mit den Vorgaben für die Codierung, Key: Oberbegriff; keine Unterpunkte
            "Nicht-rechtliche Interventionen(über Beratung hinaus)": [],
            "Rechtliche, aber außergerichtliche Interventionen": [],
            "gerichtliche Interventionen": [],
            "anderes - Interventionsformen": [],
            "keine Angabe - Interventionsformen": [],
            "ignorieren - Interventionsformen": []
        }
        self.spalten_diskriminierungsform = []
        self.trennzeichen_liste_diskriminierungsform = []
        self.genannt_diskriminierungsform = False
        self.dict_code_checkboxes_auswahl_diskriminierungsform = {}
        self.diskriminierungsform_codiert = False
        self.fortschritt_diskriminierungsform = 0
        self.codierliste_dict_diskriminierungsform = {}
        self.dict_diskriminierungsform_vorgabe = {
            # dict mit den Vorgaben für die Codierung, Key: Oberbegriff; keine Unterpunkte
            "Verwehr von Zugang / Ausschluss von bestehender Teilhabe": [],
            "Verwehr von gleichwertiger Behandlung, Bewertung und Leistung": [],
            "Belästigung": [],
            "Sexualisierte Belästigung": [],
            "Anweisung zur Diskriminierung": [],
            "Benachteiligung wegen einer Diskriminierungsbeschwerde/ Viktiminisierung": [],
            "Starftatbestand": [],
            "Grenzüberschreitungen / Alltagsdiskriminierung / Mikroagressionen / Othering": [],
            "anderes - Diskriminierungsform": [],
            "keine Angabe - Diskriminierungsform": [],
            "ignorieren - Diskriminierungsform": []
        }
        self.spalten_agg_relevanz = []
        self.trennzeichen_liste_agg_relevanz = []
        self.genannt_agg_relevanz = False
        self.dict_code_checkboxes_auswahl_agg_relevanz = {}
        self.agg_relevanz_codiert = False
        self.fortschritt_agg_relevanz = 0
        self.codierliste_dict_agg_relevanz = {}
        self.dict_agg_relevanz_vorgabe = {
            # dict mit den Vorgaben für die Codierung, Key: Oberbegriff; keine Unterpunkte
            "AGG-relevant": [],
            "nicht AGG-relevant": [],
            "anderes - AGG-Relevanz": [],
            "keine Angabe - AGG-Relevanz": [],
            "ignorieren - AGG-Relevanz": []
        }

        self.spalten_gesamt = self.df.columns.tolist()

        self.zeitraum_beginn = False
        self.zeitraum_ende = False
        self.zeitraum_inhalt = False
        self.zeitraum_genau = False
        self.zeitraum_irgendwas = False
        self.zeitraum_beginn_txt = ""
        self.zeitraum_ende_txt = ""
        self.zeitraum_inhalt_txt = ""
        self.zeitraum_genau_txt = ""
        self.pfad_datenausgabe = ""
        self.spalte_zeitraum = ""

        self.codierdict_export = {}

        self.codierung_dict_export_lebensbereich = {}
        self.codierung_dict_export_diskriminierungsmerkmale = {}
        self.codierung_dict_export_interventionsformen = {}
        self.codierung_dict_export_diskriminierungsform = {}
        self.codierung_dict_export_agg_relevanz = {}
        self.dict_code_checkboxes_auswahl_gesamt = {}

        self.genannt_markierung_leer_lebensbereich = True
        self.genannt_markierung_leer_diskriminierungsmerkmale = True
        self.genannt_markierung_leer_interventionsformen = True
        self.genannt_markierung_leer_diskriminierungsform = True
        self.genannt_markierung_leer_agg_relevanz = True

        self.genannt_markierung_zeichen_lebensbereich = False
        self.genannt_markierung_zeichen_diskriminierungsmerkmale = False
        self.genannt_markierung_zeichen_interventionsformen = False
        self.genannt_markierung_zeichen_diskriminierungsform = False
        self.genannt_markierung_zeichen_agg_relevanz = False

        self.genannt_markierung_zeichen_text_lebensbereich = ""
        self.genannt_markierung_zeichen_text_diskriminierungsmerkmale = ""
        self.genannt_markierung_zeichen_text_interventionsformen = ""
        self.genannt_markierung_zeichen_text_diskriminierungsform = ""
        self.genannt_markierung_zeichen_text_agg_relevanz = ""

        self.genannt_markierung_nichtzeichen_lebensbereich = False
        self.genannt_markierung_nichtzeichen_diskriminierungsmerkmale = False
        self.genannt_markierung_nichtzeichen_interventionsformen = False
        self.genannt_markierung_nichtzeichen_diskriminierungsform = False
        self.genannt_markierung_nichtzeichen_agg_relevanz = False

        self.genannt_markierung_nichtzeichen_text_lebensbereich = ""
        self.genannt_markierung_nichtzeichen_text_diskriminierungsmerkmale = ""
        self.genannt_markierung_nichtzeichen_text_interventionsformen = ""
        self.genannt_markierung_nichtzeichen_text_diskriminierungsform = ""
        self.genannt_markierung_nichtzeichen_text_agg_relevanz = ""

    def codierfenster_initialisieren(self):
        self.elemente_vollstaendig_getrennt_einfach = []
        self.liste_anzeige = {}


# Klasse für die GUI des Hauptfensters
class FRM_main(QMainWindow, Ui_MainWindow):

    # Initialisierung des Fensters ohne Daten
    def __init__(self, datenspeicher, app):
        super().__init__()
        self.app = app
        self.setupUi(self)
        self.datenspeicher = datenspeicher
        self.gui_datengrundlage_einfach = None
        self.gui_codierfenster = None
        self.gui_zeitraum = None
        self.gui_datenausgabe = None
        self.funktionalitaet()
        self.fortschritt_aktualisieren()
        self.version.setText(f"Version: {version}")

    # On-Klick-Events der Buttons definieren
    def funktionalitaet(self):
        self.button_datengrundlage_bearbeiten.clicked.connect(self.oeffnen_gui_datengrundlage_einfach)
        self.button_zeitraum_bearbeiten.clicked.connect(self.oeffnen_gui_zeitraum)

        self.button_lebensbereich_bearbeiten.clicked.connect(self.oeffnen_gui_codierfenster_lebensbereich)
        self.button_dismerkmal_bearbeiten.clicked.connect(self.oeffnen_gui_codierfenster_diskriminierungsmerkmale)
        self.button_intervform_bearbeiten.clicked.connect(self.oeffnen_gui_codierfenster_interventionsformen)
        self.button_disform_bearbeiten.clicked.connect(self.oeffnen_gui_codierfenster_diskriminierungsform)
        self.button_aggrelevanz_bearbeiten.clicked.connect(self.oeffnen_gui_codierfenster_agg_relevanz)
        self.button_skript_schliessen.clicked.connect(self.skript_schliessen)

        self.button_auswertungen.clicked.connect(self.öffnen_gui_datenausgabe)
        self.button_template_speichern.clicked.connect(self.template_speichern)
        self.button_template_bearbeiten.clicked.connect(self.template_laden)

    def skript_schliessen(self):
        self.app.quit()

    # Verhalten beim Schließen der Fenster definieren
    def on_datengrundlage_einfach_closed(self):
        self.gui_datengrundlage_einfach = None

    # Verhalten beim Schließen der Fenster definieren
    def on_gui_codierfenster_closed(self):
        self.gui_codierfenster = None

    # Verhalten beim Schließen der Fenster definieren
    def on_gui_zeitraum_closed(self):
        self.gui_zeitraum = None

    # Verhalten beim Schließen der Fenster definieren
    def on_datenausgabe_closed(self):
        self.gui_datenausgabe = None

    # Verhalten beim Öffnen der Fenster definieren
    def oeffnen_gui_codierfenster_lebensbereich(self, datenspeicher):
        self.datenspeicher.aktuell_codiert = "Lebensbereich"
        self.oeffnen_gui_codierfenster()

    # Verhalten beim Öffnen der Fenster definieren
    def oeffnen_gui_codierfenster_diskriminierungsmerkmale(self, datenspeicher):
        self.datenspeicher.aktuell_codiert = "Diskriminierungsmerkmale"
        self.oeffnen_gui_codierfenster()

    # Verhalten beim Öffnen der Fenster definieren
    def oeffnen_gui_codierfenster_interventionsformen(self, datenspeicher):
        self.datenspeicher.aktuell_codiert = "Interventionsformen"
        self.oeffnen_gui_codierfenster()

    # Verhalten beim Öffnen der Fenster definieren
    def oeffnen_gui_codierfenster_diskriminierungsform(self, datenspeicher):
        self.datenspeicher.aktuell_codiert = "Diskriminierungsform"
        self.oeffnen_gui_codierfenster()

    # Verhalten beim Öffnen der Fenster definieren
    def oeffnen_gui_codierfenster_agg_relevanz(self, datenspeicher):
        self.datenspeicher.aktuell_codiert = "AGG_Relevanz"
        self.oeffnen_gui_codierfenster()

    # Aktualisieren der Fortschrittsbalken
    # Kann man so machen, suggeriert aber bei fehlerhaftem Einlesen, dass alles ok ist
    def fortschritt_aktualisieren(self):
        if self.datenspeicher.pfad_datengrundlage_einfach != "":
            self.fortschritt_datenauswahl.setValue(50)
            if self.datenspeicher.datengrundlage_eingelesen == True:
                self.fortschritt_datenauswahl.setValue(100)
                self.button_template_bearbeiten.setEnabled(True)
            else:
                self.button_template_bearbeiten.setEnabled(False)
        else:
            self.button_template_bearbeiten.setEnabled(False)
        if self.datenspeicher.zeitraum_ausgewaehlt == True:
            self.fortschritt_zeitraum.setValue(100)
        else:
            self.fortschritt_zeitraum.setValue(0)
        self.fortschritt_lebensbereich.setValue(self.datenspeicher.fortschritt_lebensbereiche)
        self.fortschritt_dismerkmal.setValue(self.datenspeicher.fortschritt_diskriminierungsmerkmale)
        self.fortschritt_disform.setValue(self.datenspeicher.fortschritt_diskriminierungsform)
        self.fortschritt_intervform.setValue(self.datenspeicher.fortschritt_interventionsform)
        self.fortschritt_aggrelevanz.setValue(self.datenspeicher.fortschritt_agg_relevanz)

    def template_speichern(self):

        # create a dummy Datenspeicher which copies the attributes which get read in template_bearbeiten
        temp_speicher_save = Datenspeicher()
        temp_speicher_save.lebensbereich_codiert = self.datenspeicher.lebensbereich_codiert
        temp_speicher_save.spalten_lebensbereich = self.datenspeicher.spalten_lebensbereich
        temp_speicher_save.trennzeichen_liste_lebensbereich = self.datenspeicher.trennzeichen_liste_lebensbereich
        temp_speicher_save.genannt_lebensbereich = self.datenspeicher.genannt_lebensbereich
        temp_speicher_save.dict_code_checkboxes_auswahl_lebensbereich = self.datenspeicher.dict_code_checkboxes_auswahl_lebensbereich
        temp_speicher_save.dict_lebensbereiche_vorgabe = self.datenspeicher.dict_lebensbereiche_vorgabe
        temp_speicher_save.codierung_dict_export_lebensbereich = self.datenspeicher.codierung_dict_export_lebensbereich
        temp_speicher_save.diskriminierungsmerkmale_codiert = self.datenspeicher.diskriminierungsmerkmale_codiert
        temp_speicher_save.spalten_diskriminierungsmerkmale = self.datenspeicher.spalten_diskriminierungsmerkmale
        temp_speicher_save.trennzeichen_liste_diskriminierungsmerkmale = self.datenspeicher.trennzeichen_liste_diskriminierungsmerkmale
        temp_speicher_save.genannt_diskriminierungsmerkmale = self.datenspeicher.genannt_diskriminierungsmerkmale
        temp_speicher_save.dict_code_checkboxes_auswahl_diskriminierungsmerkmale = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsmerkmale
        temp_speicher_save.dict_diskriminierungsmerkmale_vorgabe = self.datenspeicher.dict_diskriminierungsmerkmale_vorgabe
        temp_speicher_save.codierung_dict_export_diskriminierungsmerkmale = self.datenspeicher.codierung_dict_export_diskriminierungsmerkmale
        temp_speicher_save.interventionsformen_codiert = self.datenspeicher.interventionsformen_codiert
        temp_speicher_save.spalten_interventionsformen = self.datenspeicher.spalten_interventionsformen
        temp_speicher_save.trennzeichen_liste_interventionsformen = self.datenspeicher.trennzeichen_liste_interventionsformen
        temp_speicher_save.genannt_interventionsformen = self.datenspeicher.genannt_interventionsformen
        temp_speicher_save.dict_code_checkboxes_auswahl_interventionsformen = self.datenspeicher.dict_code_checkboxes_auswahl_interventionsformen
        temp_speicher_save.dict_interventionsformen_vorgabe = self.datenspeicher.dict_interventionsformen_vorgabe
        temp_speicher_save.codierung_dict_export_interventionsformen = self.datenspeicher.codierung_dict_export_interventionsformen
        temp_speicher_save.diskriminierungsform_codiert = self.datenspeicher.diskriminierungsform_codiert
        temp_speicher_save.spalten_diskriminierungsform = self.datenspeicher.spalten_diskriminierungsform
        temp_speicher_save.trennzeichen_liste_diskriminierungsform = self.datenspeicher.trennzeichen_liste_diskriminierungsform
        temp_speicher_save.genannt_diskriminierungsform = self.datenspeicher.genannt_diskriminierungsform
        temp_speicher_save.dict_code_checkboxes_auswahl_diskriminierungsform = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsform
        temp_speicher_save.dict_diskriminierungsform_vorgabe = self.datenspeicher.dict_diskriminierungsform_vorgabe
        temp_speicher_save.codierung_dict_export_diskriminierungsform = self.datenspeicher.codierung_dict_export_diskriminierungsform
        temp_speicher_save.agg_relevanz_codiert = self.datenspeicher.agg_relevanz_codiert
        temp_speicher_save.spalten_agg_relevanz = self.datenspeicher.spalten_agg_relevanz
        temp_speicher_save.trennzeichen_liste_agg_relevanz = self.datenspeicher.trennzeichen_liste_agg_relevanz
        temp_speicher_save.genannt_agg_relevanz = self.datenspeicher.genannt_agg_relevanz
        temp_speicher_save.dict_code_checkboxes_auswahl_agg_relevanz = self.datenspeicher.dict_code_checkboxes_auswahl_agg_relevanz
        temp_speicher_save.dict_agg_relevanz_vorgabe = self.datenspeicher.dict_agg_relevanz_vorgabe
        temp_speicher_save.codierung_dict_export_agg_relevanz = self.datenspeicher.codierung_dict_export_agg_relevanz
        temp_speicher_save.zeitraum_beginn = self.datenspeicher.zeitraum_beginn
        temp_speicher_save.zeitraum_ende = self.datenspeicher.zeitraum_ende
        temp_speicher_save.zeitraum_inhalt = self.datenspeicher.zeitraum_inhalt
        temp_speicher_save.zeitraum_genau = self.datenspeicher.zeitraum_genau
        temp_speicher_save.zeitraum_irgendwas = self.datenspeicher.zeitraum_irgendwas
        temp_speicher_save.zeitraum_beginn_txt = self.datenspeicher.zeitraum_beginn_txt
        temp_speicher_save.zeitraum_ende_txt = self.datenspeicher.zeitraum_ende_txt
        temp_speicher_save.zeitraum_inhalt_txt = self.datenspeicher.zeitraum_inhalt_txt
        temp_speicher_save.zeitraum_genau_txt = self.datenspeicher.zeitraum_genau_txt
        temp_speicher_save.zeitraum_ausgewaehlt = self.datenspeicher.zeitraum_ausgewaehlt
        temp_speicher_save.spalte_zeitraum = self.datenspeicher.spalte_zeitraum
        temp_speicher_save.codierdict_export = self.datenspeicher.codierdict_export

        # copy all values genannt_markierung_leer_lebensbereich, genannt_markierung_leer_diskriminierungsmerkmale, genannt_markierung_leer_interventionsformen, genannt_markierung_leer_diskriminierungsform, genannt_markierung_leer_agg_relevanz
        temp_speicher_save.genannt_markierung_leer_lebensbereich = self.datenspeicher.genannt_markierung_leer_lebensbereich
        temp_speicher_save.genannt_markierung_leer_diskriminierungsmerkmale = self.datenspeicher.genannt_markierung_leer_diskriminierungsmerkmale
        temp_speicher_save.genannt_markierung_leer_interventionsformen = self.datenspeicher.genannt_markierung_leer_interventionsformen
        temp_speicher_save.genannt_markierung_leer_diskriminierungsform = self.datenspeicher.genannt_markierung_leer_diskriminierungsform
        temp_speicher_save.genannt_markierung_leer_agg_relevanz = self.datenspeicher.genannt_markierung_leer_agg_relevanz

        # copy all values genannt_markierung_zeichen_lebensbereich, genannt_markierung_zeichen_diskriminierungsmerkmale, genannt_markierung_zeichen_interventionsformen, genannt_markierung_zeichen_diskriminierungsform, genannt_markierung_zeichen_agg_relevanz
        temp_speicher_save.genannt_markierung_zeichen_lebensbereich = self.datenspeicher.genannt_markierung_zeichen_lebensbereich
        temp_speicher_save.genannt_markierung_zeichen_diskriminierungsmerkmale = self.datenspeicher.genannt_markierung_zeichen_diskriminierungsmerkmale
        temp_speicher_save.genannt_markierung_zeichen_interventionsformen = self.datenspeicher.genannt_markierung_zeichen_interventionsformen
        temp_speicher_save.genannt_markierung_zeichen_diskriminierungsform = self.datenspeicher.genannt_markierung_zeichen_diskriminierungsform
        temp_speicher_save.genannt_markierung_zeichen_agg_relevanz = self.datenspeicher.genannt_markierung_zeichen_agg_relevanz

        # copy all values genannt_markierung_zeichen_text_lebensbereich, genannt_markierung_zeichen_text_diskriminierungsmerkmale, genannt_markierung_zeichen_text_interventionsformen, genannt_markierung_zeichen_text_diskriminierungsform, genannt_markierung_zeichen_text_agg_relevanz
        temp_speicher_save.genannt_markierung_zeichen_text_lebensbereich = self.datenspeicher.genannt_markierung_zeichen_text_lebensbereich
        temp_speicher_save.genannt_markierung_zeichen_text_diskriminierungsmerkmale = self.datenspeicher.genannt_markierung_zeichen_text_diskriminierungsmerkmale
        temp_speicher_save.genannt_markierung_zeichen_text_interventionsformen = self.datenspeicher.genannt_markierung_zeichen_text_interventionsformen
        temp_speicher_save.genannt_markierung_zeichen_text_diskriminierungsform = self.datenspeicher.genannt_markierung_zeichen_text_diskriminierungsform
        temp_speicher_save.genannt_markierung_zeichen_text_agg_relevanz = self.datenspeicher.genannt_markierung_zeichen_text_agg_relevanz

        # copy all values genannt_markierung_nichtzeichen_lebensbereich, genannt_markierung_nichtzeichen_diskriminierungsmerkmale, genannt_markierung_nichtzeichen_interventionsformen, genannt_markierung_nichtzeichen_diskriminierungsform, genannt_markierung_nichtzeichen_agg_relevanz
        temp_speicher_save.genannt_markierung_nichtzeichen_lebensbereich = self.datenspeicher.genannt_markierung_nichtzeichen_lebensbereich
        temp_speicher_save.genannt_markierung_nichtzeichen_diskriminierungsmerkmale = self.datenspeicher.genannt_markierung_nichtzeichen_diskriminierungsmerkmale
        temp_speicher_save.genannt_markierung_nichtzeichen_interventionsformen = self.datenspeicher.genannt_markierung_nichtzeichen_interventionsformen
        temp_speicher_save.genannt_markierung_nichtzeichen_diskriminierungsform = self.datenspeicher.genannt_markierung_nichtzeichen_diskriminierungsform
        temp_speicher_save.genannt_markierung_nichtzeichen_agg_relevanz = self.datenspeicher.genannt_markierung_nichtzeichen_agg_relevanz

        # copy all values genannt_markierung_nichtzeichen_text_lebensbereich, genannt_markierung_nichtzeichen_text_diskriminierungsmerkmale, genannt_markierung_nichtzeichen_text_interventionsformen, genannt_markierung_nichtzeichen_text_diskriminierungsform, genannt_markierung_nichtzeichen_text_agg_relevanz
        temp_speicher_save.genannt_markierung_nichtzeichen_text_lebensbereich = self.datenspeicher.genannt_markierung_nichtzeichen_text_lebensbereich
        temp_speicher_save.genannt_markierung_nichtzeichen_text_diskriminierungsmerkmale = self.datenspeicher.genannt_markierung_nichtzeichen_text_diskriminierungsmerkmale
        temp_speicher_save.genannt_markierung_nichtzeichen_text_interventionsformen = self.datenspeicher.genannt_markierung_nichtzeichen_text_interventionsformen
        temp_speicher_save.genannt_markierung_nichtzeichen_text_diskriminierungsform = self.datenspeicher.genannt_markierung_nichtzeichen_text_diskriminierungsform
        temp_speicher_save.genannt_markierung_nichtzeichen_text_agg_relevanz = self.datenspeicher.genannt_markierung_nichtzeichen_text_agg_relevanz

        # generates a string to get a readable representation of temp_speicher_save
        textual_representation = str(temp_speicher_save.__dict__)

        options = QFileDialog.Options()
        dateipfad_zum_speichern, _ = QFileDialog.getSaveFileName(self, "Speichern unter", "", "Pickle-Dateien (*.pkl)",
                                                                 options=options)

        if dateipfad_zum_speichern:
            # Der Benutzer hat einen Speicherort ausgewählt
            with open(dateipfad_zum_speichern, 'wb') as datei:
                pickle.dump(temp_speicher_save, datei)
                # save textual representation of temp_speicher_save in a txt file
                with open(dateipfad_zum_speichern[:-4] + ".txt", "w") as text_file:
                    text_file.write(textual_representation)
            # open dialog to inform the user that the template was saved
            msg = QMessageBox()
            msg.setWindowTitle("Speichern erfolgreich")
            msg.setText(
                "Das Template wurde erfolgreich unter\n" + dateipfad_zum_speichern + "\ngespeichert.\nEine lesbare Textdatei wurde ebenfalls gespeichert.")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()


        else:
            # Der Benutzer hat den Speicherort nicht ausgewählt
            print("Speichern abgebrochen")

    def template_laden(self):

        options = QFileDialog.Options()
        dateipfad_zum_oeffnen, _ = QFileDialog.getOpenFileName(self, "Datei öffnen", "", "Pickle-Dateien (*.pkl)",
                                                               options=options)
        with open(dateipfad_zum_oeffnen, 'rb') as datei:
            temp_speicher: Datenspeicher = pickle.load(datei)
        if (temp_speicher.lebensbereich_codiert):
            self.datenspeicher.lebensbereich_codiert = True
            self.datenspeicher.spalten_lebensbereich = temp_speicher.spalten_lebensbereich
            self.datenspeicher.trennzeichen_liste_lebensbereich = temp_speicher.trennzeichen_liste_lebensbereich
            self.datenspeicher.genannt_lebensbereich = temp_speicher.genannt_lebensbereich
            self.datenspeicher.dict_code_checkboxes_auswahl_lebensbereich = temp_speicher.dict_code_checkboxes_auswahl_lebensbereich
            self.datenspeicher.dict_lebensbereiche_vorgabe = temp_speicher.dict_lebensbereiche_vorgabe
            self.datenspeicher.codierung_dict_export_lebensbereich = temp_speicher.codierung_dict_export_lebensbereich
            self.datenspeicher.genannt_markierung_nichtzeichen_text_lebensbereich = temp_speicher.genannt_markierung_nichtzeichen_text_lebensbereich
            self.datenspeicher.genannt_markierung_nichtzeichen_lebensbereich = temp_speicher.genannt_markierung_nichtzeichen_lebensbereich
            self.datenspeicher.genannt_markierung_zeichen_text_lebensbereich = temp_speicher.genannt_markierung_zeichen_text_lebensbereich
            self.datenspeicher.genannt_markierung_zeichen_lebensbereich = temp_speicher.genannt_markierung_zeichen_lebensbereich
            self.datenspeicher.genannt_markierung_leer_lebensbereich = temp_speicher.genannt_markierung_leer_lebensbereich
        if (temp_speicher.diskriminierungsmerkmale_codiert):
            self.datenspeicher.diskriminierungsmerkmale_codiert = True
            self.datenspeicher.spalten_diskriminierungsmerkmale = temp_speicher.spalten_diskriminierungsmerkmale
            self.datenspeicher.trennzeichen_liste_diskriminierungsmerkmale = temp_speicher.trennzeichen_liste_diskriminierungsmerkmale
            self.datenspeicher.genannt_diskriminierungsmerkmale = temp_speicher.genannt_diskriminierungsmerkmale
            self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsmerkmale = temp_speicher.dict_code_checkboxes_auswahl_diskriminierungsmerkmale
            self.datenspeicher.dict_diskriminierungsmerkmale_vorgabe = temp_speicher.dict_diskriminierungsmerkmale_vorgabe
            self.datenspeicher.codierung_dict_export_diskriminierungsmerkmale = temp_speicher.codierung_dict_export_diskriminierungsmerkmale
            self.datenspeicher.genannt_markierung_nichtzeichen_text_diskriminierungsmerkmale = temp_speicher.genannt_markierung_nichtzeichen_text_diskriminierungsmerkmale
            self.datenspeicher.genannt_markierung_nichtzeichen_diskriminierungsmerkmale = temp_speicher.genannt_markierung_nichtzeichen_diskriminierungsmerkmale
            self.datenspeicher.genannt_markierung_zeichen_text_diskriminierungsmerkmale = temp_speicher.genannt_markierung_zeichen_text_diskriminierungsmerkmale
            self.datenspeicher.genannt_markierung_zeichen_diskriminierungsmerkmale = temp_speicher.genannt_markierung_zeichen_diskriminierungsmerkmale
            self.datenspeicher.genannt_markierung_leer_diskriminierungsmerkmale = temp_speicher.genannt_markierung_leer_diskriminierungsmerkmale
        if (temp_speicher.agg_relevanz_codiert):
            self.datenspeicher.agg_relevanz_codiert = True
            self.datenspeicher.spalten_agg_relevanz = temp_speicher.spalten_agg_relevanz
            self.datenspeicher.trennzeichen_liste_agg_relevanz = temp_speicher.trennzeichen_liste_agg_relevanz
            self.datenspeicher.genannt_agg_relevanz = temp_speicher.genannt_agg_relevanz
            self.datenspeicher.dict_code_checkboxes_auswahl_agg_relevanz = temp_speicher.dict_code_checkboxes_auswahl_agg_relevanz
            self.datenspeicher.dict_agg_relevanz_vorgabe = temp_speicher.dict_agg_relevanz_vorgabe
            self.datenspeicher.codierung_dict_export_agg_relevanz = temp_speicher.codierung_dict_export_agg_relevanz
            self.datenspeicher.genannt_markierung_nichtzeichen_text_agg_relevanz = temp_speicher.genannt_markierung_nichtzeichen_text_agg_relevanz
            self.datenspeicher.genannt_markierung_nichtzeichen_agg_relevanz = temp_speicher.genannt_markierung_nichtzeichen_agg_relevanz
            self.datenspeicher.genannt_markierung_zeichen_text_agg_relevanz = temp_speicher.genannt_markierung_zeichen_text_agg_relevanz
            self.datenspeicher.genannt_markierung_zeichen_agg_relevanz = temp_speicher.genannt_markierung_zeichen_agg_relevanz
            self.datenspeicher.genannt_markierung_leer_agg_relevanz = temp_speicher.genannt_markierung_leer_agg_relevanz
        if (temp_speicher.interventionsformen_codiert):
            self.datenspeicher.interventionsformen_codiert = True
            self.datenspeicher.spalten_interventionsformen = temp_speicher.spalten_interventionsformen
            self.datenspeicher.trennzeichen_liste_interventionsformen = temp_speicher.trennzeichen_liste_interventionsformen
            self.datenspeicher.genannt_interventionsformen = temp_speicher.genannt_interventionsformen
            self.datenspeicher.dict_code_checkboxes_auswahl_interventionsformen = temp_speicher.dict_code_checkboxes_auswahl_interventionsformen
            self.datenspeicher.dict_interventionsformen_vorgabe = temp_speicher.dict_interventionsformen_vorgabe
            self.datenspeicher.codierung_dict_export_interventionsformen = temp_speicher.codierung_dict_export_interventionsformen
            self.datenspeicher.genannt_markierung_nichtzeichen_text_interventionsformen = temp_speicher.genannt_markierung_nichtzeichen_text_interventionsformen
            self.datenspeicher.genannt_markierung_nichtzeichen_interventionsformen = temp_speicher.genannt_markierung_nichtzeichen_interventionsformen
            self.datenspeicher.genannt_markierung_zeichen_text_interventionsformen = temp_speicher.genannt_markierung_zeichen_text_interventionsformen
            self.datenspeicher.genannt_markierung_zeichen_interventionsformen = temp_speicher.genannt_markierung_zeichen_interventionsformen
            self.datenspeicher.genannt_markierung_leer_interventionsformen = temp_speicher.genannt_markierung_leer_interventionsformen
        if (temp_speicher.diskriminierungsform_codiert):
            self.datenspeicher.diskriminierungsform_codiert = True
            self.datenspeicher.spalten_diskriminierungsform = temp_speicher.spalten_diskriminierungsform
            self.datenspeicher.trennzeichen_liste_diskriminierungsform = temp_speicher.trennzeichen_liste_diskriminierungsform
            self.datenspeicher.genannt_diskriminierungsform = temp_speicher.genannt_diskriminierungsform
            self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsform = temp_speicher.dict_code_checkboxes_auswahl_diskriminierungsform
            self.datenspeicher.dict_diskriminierungsform_vorgabe = temp_speicher.dict_diskriminierungsform_vorgabe
            self.datenspeicher.codierung_dict_export_diskriminierungsform = temp_speicher.codierung_dict_export_diskriminierungsform
            self.datenspeicher.genannt_markierung_nichtzeichen_text_diskriminierungsform = temp_speicher.genannt_markierung_nichtzeichen_text_diskriminierungsform
            self.datenspeicher.genannt_markierung_nichtzeichen_diskriminierungsform = temp_speicher.genannt_markierung_nichtzeichen_diskriminierungsform
            self.datenspeicher.genannt_markierung_zeichen_text_diskriminierungsform = temp_speicher.genannt_markierung_zeichen_text_diskriminierungsform
            self.datenspeicher.genannt_markierung_zeichen_diskriminierungsform = temp_speicher.genannt_markierung_zeichen_diskriminierungsform
            self.datenspeicher.genannt_markierung_leer_diskriminierungsform = temp_speicher.genannt_markierung_leer_diskriminierungsform
        if (temp_speicher.zeitraum_ausgewaehlt):
            self.datenspeicher.zeitraum_ausgewaehlt = True
            self.datenspeicher.zeitraum_beginn = temp_speicher.zeitraum_beginn
            self.datenspeicher.zeitraum_ende = temp_speicher.zeitraum_ende
            self.datenspeicher.zeitraum_inhalt = temp_speicher.zeitraum_inhalt
            self.datenspeicher.zeitraum_genau = temp_speicher.zeitraum_genau
            self.datenspeicher.zeitraum_irgendwas = temp_speicher.zeitraum_irgendwas
            self.datenspeicher.zeitraum_beginn_txt = temp_speicher.zeitraum_beginn_txt
            self.datenspeicher.zeitraum_ende_txt = temp_speicher.zeitraum_ende_txt
            self.datenspeicher.zeitraum_inhalt_txt = temp_speicher.zeitraum_inhalt_txt
            self.datenspeicher.zeitraum_genau_txt = temp_speicher.zeitraum_genau_txt
            self.datenspeicher.spalte_zeitraum = temp_speicher.spalte_zeitraum

        self.datenspeicher.codierdict_export = temp_speicher.codierdict_export

        self.fortschritt_template.setValue(100)

        self.fortschritt_aktualisieren()

    # Wenn das Fenster noch nicht existiert, wird es erstellt und geöffnet; ansonsten nur geöffnet
    def oeffnen_gui_datengrundlage_einfach(self):
        if self.gui_datengrundlage_einfach is None:
            self.gui_datengrundlage_einfach = FRM_datengrundlage_einfach(self.datenspeicher, self)
            self.gui_datengrundlage_einfach.show()
            self.gui_datengrundlage_einfach.closeEvent = lambda event: self.on_datengrundlage_einfach_closed()
            self.setEnabled(False)
        else:
            self.gui_datengrundlage_einfach.activateWindow()

    def öffnen_gui_datenausgabe(self):
        if self.gui_datenausgabe is None:
            self.gui_datenausgabe = FRM_datenausgabe(self.datenspeicher, self)
            self.gui_datenausgabe.show()
            self.gui_datenausgabe.closeEvent = lambda event: self.on_datenausgabe_closed()
            self.setEnabled(False)
        else:
            self.gui_datenausgabe.activateWindow()

    def oeffnen_gui_zeitraum(self, datenspeicher):
        if self.gui_zeitraum is None:
            self.gui_zeitraum = FRM_zeitraumfenster(self.datenspeicher, self)
            self.gui_zeitraum.show()
            self.gui_zeitraum.closeEvent = lambda event: self.on_gui_zeitraum_closed()
            self.setEnabled(False)
        else:
            self.gui_codierfenster.activateWindow()

    def oeffnen_gui_codierfenster(self):
        if self.gui_codierfenster is None:
            self.gui_codierfenster = FRM_codierfenster(self.datenspeicher, self)
            self.gui_codierfenster.show()
            self.gui_codierfenster.closeEvent = lambda event: self.on_gui_codierfenster_closed()
            self.setEnabled(False)
        else:
            self.gui_codierfenster.activateWindow()

    def enable_frm_main(self):
        self.setEnabled(True)


# Klasse für die GUI des Einlesefensters
class FRM_datengrundlage_einfach(QMainWindow, Ui_fenster_datengrundlage_einfach):

    # Initialisierung des Fensters
    def __init__(self, datenspeicher, frm_main):  # frm_main als Argument hinzugefügt
        super().__init__()
        self.setupUi(self)
        self.datenspeicher = datenspeicher
        self.frm_main = frm_main
        self.tmp_vars_erstellen()
        self.funktionalitaet()
        self.werte_füllen(datenspeicher)

    # dummy Pfad erstellen
    def tmp_vars_erstellen(self):
        self.tmp_pfad_datengrundlage_einfach = ""

    # Wenn das Fenster geschlossen wird, wird das Main-Fenster wieder aktiviert
    def event(self, event):
        if event.type() == QtCore.QEvent.Close:
            self.frm_main.enable_frm_main()
        return super().event(event)

    # On-Klick-Events der Buttons definieren
    def funktionalitaet(self):
        self.button_datengrundlage_einfach_durchsuchen.clicked.connect(self.datei_auswahl_einfach)
        self.button_speichern.clicked.connect(self.speichern)
        self.button_abbrechen.clicked.connect(self.abbrechen)

    # Wenn der Dateienpfad bereits im Speicher ist, wird er in das Textfeld geschrieben,
    # sonst wird der soeben ausgewählte Pfad eingetragen
    def werte_füllen(self, datenspeicher):
        if self.datenspeicher.pfad_datengrundlage_einfach != "":
            self.textfeld_datengrundlage_einfach_speicherort.setText(datenspeicher.pfad_datengrundlage_einfach)
        if self.tmp_pfad_datengrundlage_einfach != "":
            self.textfeld_datengrundlage_einfach_speicherort.setText(self.tmp_pfad_datengrundlage_einfach)

    # Dateiauswahl; anschließend wird der Pfad in das Textfeld geschrieben
    def datei_auswahl_einfach(self):
        self.dateiname_einfach, _ = QFileDialog.getOpenFileName(self, "Datei wählen", "",
                                                                "Excel-Dateien (*.xlsx);;CSV-Dateien (*.csv);;Alle Dateien (*)")  # Warum alle Typen zulassen?
        self.tmp_pfad_datengrundlage_einfach = self.dateiname_einfach
        self.werte_füllen(self.datenspeicher)

    # Speichern der Daten in den Speicher
    def speichern(self):
        self.datenspeicher.pfad_datengrundlage_einfach = self.tmp_pfad_datengrundlage_einfach
        self.frm_main.fortschritt_aktualisieren()
        self.datenspeicher.df_original = pd.read_excel(self.datenspeicher.pfad_datengrundlage_einfach, dtype=str)
        self.datenspeicher.datengrundlage_eingelesen = True
        self.datenspeicher.spalten_gesamt = self.datenspeicher.df_original.columns.tolist()
        self.datenspeicher.df = copy.deepcopy(self.datenspeicher.df_original)
        self.frm_main.fortschritt_aktualisieren()
        self.close()

    # Abbrechen des Einlesens; Pfad wird geleert
    def abbrechen(self):
        self.tmp_pfad_datengrundlage_einfach = ""
        self.close()


# Muss mmn anders gelöst werden, mittels Datumskonvertierung
class FRM_zeitraumfenster(QMainWindow, Ui_fenster_zeitraum_festlegen):
    def __init__(self, datenspeicher, frm_main):
        super().__init__()
        self.setupUi(self)
        self.datenspeicher = datenspeicher
        self.frm_main = frm_main
        self.werte_füllen(datenspeicher)
        self.button_zeitraum_speichern.setEnabled(False)
        # Initialer Status des Speichern-Buttons
        self.template_werte_befüllen()
        self.funktionalitaet()

    ### Spaltenname ist noch nicht selected
    def template_werte_befüllen(self):
        for spalte in self.datenspeicher.spalten_gesamt:
            # compare wether string spalte is the same as string spalte_zeitraum
            try:
                if spalte == self.datenspeicher.spalte_zeitraum[0]:
                    # select the item in the listWidget_zeitraum_spalten
                    self.listWidget_zeitraum_spalten.setCurrentItem(
                        self.listWidget_zeitraum_spalten.findItems(spalte, QtCore.Qt.MatchExactly)[0])
                # depending on which zeitraum boolean is true select the radiobutton
                if self.datenspeicher.zeitraum_beginn:
                    self.radio_zeitraum_beginn.setChecked(True)
                elif self.datenspeicher.zeitraum_ende:
                    self.radio_zeitraum_ende.setChecked(True)
                elif self.datenspeicher.zeitraum_inhalt:
                    self.radio_zeitraum_inhalt.setChecked(True)
                elif self.datenspeicher.zeitraum_genau:
                    self.radio_zeitraum_genau.setChecked(True)
                elif self.datenspeicher.zeitraum_irgendwas:
                    self.radio_zeitraum_irgendwas.setChecked(True)
                self.button_zeitraum_speichern.setEnabled(True)

            except IndexError:
                pass

        self.text_zeitraum_beginn.setText(self.datenspeicher.zeitraum_beginn_txt)
        self.text_zeitraum_ende.setText(self.datenspeicher.zeitraum_ende_txt)
        self.text_zeitraum_inhalt.setText(self.datenspeicher.zeitraum_inhalt_txt)
        self.text_zeitraum_genau.setText(self.datenspeicher.zeitraum_genau_txt)
        self.beispiel_string_setzen(bool(self.listWidget_zeitraum_spalten.selectedItems()))

    def funktionalitaet(self):

        self.button_zeitraum_speichern.clicked.connect(self.speichern)
        self.pushButton.clicked.connect(self.abbrechen)

        # Verbinde die toggled-Signale der Radiobuttons mit der Methode on_radiobutton_toggled
        self.radio_zeitraum_beginn.toggled.connect(self.on_radiobutton_toggled)
        self.radio_zeitraum_ende.toggled.connect(self.on_radiobutton_toggled)
        self.radio_zeitraum_inhalt.toggled.connect(self.on_radiobutton_toggled)
        self.radio_zeitraum_genau.toggled.connect(self.on_radiobutton_toggled)
        self.radio_zeitraum_irgendwas.toggled.connect(self.on_radiobutton_toggled)
        # Verbinde die textChanged-Signale der Textfelder mit der Methode on_text_changed
        self.text_zeitraum_beginn.textChanged.connect(self.on_text_changed)
        self.text_zeitraum_ende.textChanged.connect(self.on_text_changed)
        self.text_zeitraum_inhalt.textChanged.connect(self.on_text_changed)
        self.text_zeitraum_genau.textChanged.connect(self.on_text_changed)
        # Verknüpfe die Auswahl-Änderungs-Events der Radio-Buttons mit der Methode zum Aktualisieren des Speichern-Buttons
        for radio_btn in [self.radio_zeitraum_beginn, self.radio_zeitraum_ende, self.radio_zeitraum_inhalt,
                          self.radio_zeitraum_genau, self.radio_zeitraum_irgendwas]:
            radio_btn.toggled.connect(self.aktualisiere_speichern_button)
        self.text_zeitraum_beginn.textChanged.connect(self.aktualisiere_speichern_button)
        self.text_zeitraum_ende.textChanged.connect(self.aktualisiere_speichern_button)
        self.text_zeitraum_inhalt.textChanged.connect(self.aktualisiere_speichern_button)
        self.text_zeitraum_genau.textChanged.connect(self.aktualisiere_speichern_button)

        # Verknüpfe das itemSelectionChanged-Signal des listWidget_zeitraum_spalten mit der Methode zum Aktualisieren des Speichern-Buttons
        self.listWidget_zeitraum_spalten.itemSelectionChanged.connect(self.aktualisiere_speichern_button)

    def werte_füllen(self, datenspeicher):
        self.listWidget_zeitraum_spalten.clear()
        self.listWidget_zeitraum_spalten.addItems(self.datenspeicher.spalten_gesamt)

    def event(self, event):
        if event.type() == QtCore.QEvent.Close:
            self.frm_main.enable_frm_main()
        return super().event(event)

    def on_text_changed(self):
        # Wenn in einem der Textfelder etwas geschrieben wird, wähle den zugehörigen Radiobutton aus
        sender = self.sender()
        text = sender.text().strip()

        if sender == self.text_zeitraum_beginn:
            self.radio_zeitraum_beginn.setChecked(bool(text))
        elif sender == self.text_zeitraum_ende:
            self.radio_zeitraum_ende.setChecked(bool(text))
        elif sender == self.text_zeitraum_inhalt:
            self.radio_zeitraum_inhalt.setChecked(bool(text))
        elif sender == self.text_zeitraum_genau:
            self.radio_zeitraum_genau.setChecked(bool(text))

    def on_radiobutton_toggled(self):
        # Wenn einer der Radiobuttons aktiviert wird, leere die nicht zugehörigen Textfelder
        sender = self.sender()

        if sender == self.radio_zeitraum_beginn and sender.isChecked():
            self.text_zeitraum_ende.clear()
            self.text_zeitraum_inhalt.clear()
            self.text_zeitraum_genau.clear()
        elif sender == self.radio_zeitraum_ende and sender.isChecked():
            self.text_zeitraum_beginn.clear()
            self.text_zeitraum_inhalt.clear()
            self.text_zeitraum_genau.clear()
        elif sender == self.radio_zeitraum_inhalt and sender.isChecked():
            self.text_zeitraum_beginn.clear()
            self.text_zeitraum_ende.clear()
            self.text_zeitraum_genau.clear()
        elif sender == self.radio_zeitraum_genau and sender.isChecked():
            self.text_zeitraum_beginn.clear()
            self.text_zeitraum_ende.clear()
            self.text_zeitraum_inhalt.clear()
        elif sender == self.radio_zeitraum_irgendwas and sender.isChecked():
            self.text_zeitraum_beginn.clear()
            self.text_zeitraum_ende.clear()
            self.text_zeitraum_inhalt.clear()
            self.text_zeitraum_genau.clear()

    def aktualisiere_speichern_button(self):
        # Überprüfe die Bedingungen, um den Speichern-Button zu aktivieren oder zu deaktivieren
        is_spalte_selected = bool(self.listWidget_zeitraum_spalten.selectedItems())
        is_radio_selected = any(
            [radio.isChecked() for radio in [self.radio_zeitraum_beginn, self.radio_zeitraum_ende,
                                             self.radio_zeitraum_inhalt, self.radio_zeitraum_genau,
                                             self.radio_zeitraum_irgendwas]]
        )

        # Prüfe, ob radio_zeitraum_irgendwas ausgewählt ist, und setze entsprechend is_text_filled
        if self.radio_zeitraum_irgendwas.isChecked():
            is_text_filled = True
        else:
            is_text_filled = any(
                [text.text().strip() != '' for text in [self.text_zeitraum_beginn, self.text_zeitraum_ende,
                                                        self.text_zeitraum_inhalt, self.text_zeitraum_genau]]
            )

        # Aktualisiere den Zustand des Speichern-Buttons entsprechend der Bedingungen
        self.button_zeitraum_speichern.setEnabled(is_spalte_selected and is_radio_selected and is_text_filled)

        self.beispiel_string_setzen(is_spalte_selected)

    def beispiel_string_setzen(self, is_spalte_selected: bool):
        if is_spalte_selected:
            spalte = self.listWidget_zeitraum_spalten.selectedItems()[0].text()
            beispiel = self.datenspeicher.df_original[spalte].iloc[0]
            self.label_3.setText('Spalte: ' + spalte + ' --- Beispieleintrag: ' + beispiel)
        else:
            self.label_3.setText('Bitte wählen Sie eine Spalte aus')

    def speichern(self):
        self.frm_main.fortschritt_aktualisieren()
        self.datenspeicher.spalte_zeitraum = [item.text() for item in self.listWidget_zeitraum_spalten.selectedItems()]
        if self.radio_zeitraum_beginn.isChecked():
            self.datenspeicher.zeitraum_beginn = True
            self.datenspeicher.zeitraum_ende = False
            self.datenspeicher.zeitraum_inhalt = False
            self.datenspeicher.zeitraum_genau = False
            self.datenspeicher.zeitraum_irgendwas = False
            self.datenspeicher.zeitraum_beginn_txt = self.text_zeitraum_beginn.text().strip()
            self.datenspeicher.zeitraum_ende_txt = ""
            self.datenspeicher.zeitraum_inhalt_txt = ""
            self.datenspeicher.zeitraum_genau_txt = ""
            self.datenspeicher.df = self.datenspeicher.df_original[
                self.datenspeicher.df_original[self.datenspeicher.spalte_zeitraum].astype(str).apply(
                    lambda x: x.str.startswith(self.datenspeicher.zeitraum_beginn_txt)).any(axis=1)]

        if self.radio_zeitraum_ende.isChecked():
            self.datenspeicher.zeitraum_beginn = False
            self.datenspeicher.zeitraum_ende = True
            self.datenspeicher.zeitraum_inhalt = False
            self.datenspeicher.zeitraum_genau = False
            self.datenspeicher.zeitraum_irgendwas = False
            self.datenspeicher.zeitraum_beginn_txt = ""
            self.datenspeicher.zeitraum_ende_txt = self.text_zeitraum_ende.text().strip()
            self.datenspeicher.zeitraum_inhalt_txt = ""
            self.datenspeicher.zeitraum_genau_txt = ""
            self.datenspeicher.df = self.datenspeicher.df_original[
                self.datenspeicher.df_original[self.datenspeicher.spalte_zeitraum].astype(str).apply(
                    lambda x: x.str.endswith(self.datenspeicher.zeitraum_ende_txt)).any(axis=1)]

        if self.radio_zeitraum_inhalt.isChecked():
            self.datenspeicher.zeitraum_beginn = False
            self.datenspeicher.zeitraum_ende = False
            self.datenspeicher.zeitraum_inhalt = True
            self.datenspeicher.zeitraum_genau = False
            self.datenspeicher.zeitraum_irgendwas = False
            self.datenspeicher.zeitraum_beginn_txt = ""
            self.datenspeicher.zeitraum_ende_txt = ""
            self.datenspeicher.zeitraum_inhalt_txt = self.text_zeitraum_inhalt.text().strip()
            self.datenspeicher.zeitraum_genau_txt = ""
            print("self.datenspeicher.spalte_zeitraum", self.datenspeicher.spalte_zeitraum)
            print("self.datenspeicher.dfspalte_zeitraum",
                  self.datenspeicher.df_original[self.datenspeicher.spalte_zeitraum])
            print("self.datenspeicher.zeitraum_inhalt_txt", self.datenspeicher.zeitraum_inhalt_txt)
            print("Datentyp der Spalte:", type(self.datenspeicher.df_original[self.datenspeicher.spalte_zeitraum]))
            self.datenspeicher.df = self.datenspeicher.df_original[
                self.datenspeicher.df_original[self.datenspeicher.spalte_zeitraum].astype(str).apply(
                    lambda x: x.str.contains(self.datenspeicher.zeitraum_inhalt_txt)).any(axis=1)]

        if self.radio_zeitraum_genau.isChecked():
            self.datenspeicher.zeitraum_beginn = False
            self.datenspeicher.zeitraum_ende = False
            self.datenspeicher.zeitraum_inhalt = False
            self.datenspeicher.zeitraum_genau = True
            self.datenspeicher.zeitraum_irgendwas = False
            self.datenspeicher.zeitraum_beginn_txt = ""
            self.datenspeicher.zeitraum_ende_txt = ""
            self.datenspeicher.zeitraum_inhalt_txt = ""
            self.datenspeicher.zeitraum_genau_txt = self.text_zeitraum_genau.text().strip()
            self.datenspeicher.df = self.datenspeicher.df_original[self.datenspeicher.df_original[
                                                                       self.datenspeicher.spalte_zeitraum] == self.datenspeicher.zeitraum_genau_txt].dropna()

        if self.radio_zeitraum_irgendwas.isChecked():
            self.datenspeicher.zeitraum_beginn = False
            self.datenspeicher.zeitraum_ende = False
            self.datenspeicher.zeitraum_inhalt = False
            self.datenspeicher.zeitraum_genau = False
            self.datenspeicher.zeitraum_irgendwas = True
            self.datenspeicher.zeitraum_beginn_txt = ""
            self.datenspeicher.zeitraum_ende_txt = ""
            self.datenspeicher.zeitraum_inhalt_txt = ""
            self.datenspeicher.zeitraum_genau_txt = ""
            self.datenspeicher.df = self.datenspeicher.df_original[
                self.datenspeicher.df_original[self.datenspeicher.spalte_zeitraum].notna()]
        self.datenspeicher.zeitraum_ausgewaehlt = True
        self.frm_main.fortschritt_aktualisieren()
        print(self.datenspeicher.df)
        self.close()

    def abbrechen(self):
        self.datenspeicher.zeitraum_beginn = False
        self.datenspeicher.zeitraum_ende = False
        self.datenspeicher.zeitraum_inhalt = False
        self.datenspeicher.zeitraum_genau = False
        self.datenspeicher.zeitraum_irgendwas = False
        self.datenspeicher.zeitraum_beginn_txt = ""
        self.datenspeicher.zeitraum_ende_txt = ""
        self.datenspeicher.zeitraum_inhalt_txt = ""
        self.datenspeicher.zeitraum_genau_txt = ""
        self.close()


# Klasse für die GUI des Codierfensters; Funktionen siehe FRM_datengrundlage_einfach
class FRM_codierfenster(QMainWindow, Ui_fenster_codieren):
    def __init__(self, codier_datenspeicher, frm_main):
        super().__init__()
        self.setupUi(self)
        self.datenspeicher = codier_datenspeicher
        self.frm_main = frm_main
        self.tmp_vars_erstellen()
        self.funktionalitaet()

        self.werte_auswahl(codier_datenspeicher)
        self.werte_füllen(codier_datenspeicher)
        self.scroll_widget = None
        self.adjust_horizontal_layout()
        self.kategorien_bereits_ausgewählt = self.bereits_ausgewählt(self.datenspeicher)
        self.trennzeichen_lesen()

    def bereits_ausgewählt(self, datenspeicher):
        if self.get_aktuelles_dict():
            return True
        return False

    def get_aktuelles_dict(self):
        temp_ds = self.datenspeicher
        codier_kategorie = self.datenspeicher.aktuell_codiert.lower()
        if codier_kategorie == "agg_relevanz":
            return temp_ds.dict_code_checkboxes_auswahl_agg_relevanz
        if codier_kategorie == "diskriminierungsform":
            return temp_ds.dict_code_checkboxes_auswahl_diskriminierungsform
        if codier_kategorie == "diskriminierungsmerkmale":
            return temp_ds.dict_code_checkboxes_auswahl_diskriminierungsmerkmale
        if codier_kategorie == "interventionsformen":
            return temp_ds.dict_code_checkboxes_auswahl_interventionsformen
        if codier_kategorie == "lebensbereich":
            return temp_ds.dict_code_checkboxes_auswahl_lebensbereich
        return {}

    # Dummy-Variablen initialisieren
    def tmp_vars_erstellen(self):
        self.key_value_mapping = {}
        self.value_checkboxes = []
        self.key_checkboxes = []
        self.position = ""
        self.layout = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.first_run = True
        self.spaltenauswahl_funktionalität = False
        self.tmp_spalten_auswahl = []  # Alle als Auswahl markierten Spalten (noch nicht gespeichert) in denen sich zu codierende Werte befinden
        self.spalten_auswahl = []  # Alle als Auswahl gespeicherten Spalten in denen sich zu codierende Werte befinden
        self.genannt = False  # Information, darüber, ob sich um genannt/nicht genannt Spalten handelt
        self.line_codeakt_num_autofill = False  # Markierung zum Überspringen von bestimmten Code-Abschnitten, wenn keine manuelle Änderung vorgenommen wurde
        self.line_codeakt_num_autofill2 = False  # Markierung zum Überspringen von bestimmten Code-Abschnitten, wenn keine manuelle Änderung vorgenommen wurde
        self.aufnullnachklick = False  # Sorgt dafür, dass nach einem Klick auf "codierte anzeigen"/"uncodierte anzeigen" ersteinmal die Liste auf null gesetzt wird
        self.trennzeichen_liste = []  # Liste aller Trennzeichen für Mehrfachnennung
        self.elemente_vollstaendig_getrennt_einfach = []
        self.spaltenelemente_vollstaendig = []
        self.spaltenelemente_vollstaendig_getrennt = []
        self.spaltenelemente_vollstaendig_getrennt_einfach = []

        self.spaltenelemente_vollstaendig = []
        self.spaltenelemente_vollstaendig_zusammen = []

        self.codieren_erstaufruf = True  # Markierung, dass bestimmte Code-Teile beim ersten Durchlauf im Codierwidget nicht aufgerufen werden müssen
        self.codierliste = []  # vollständige Liste aller zu codierenden Elemente
        self.codierliste_aktuell = {}  # aktuell anzuzeigende Elemente zum Codieren
        self.n_zucodieren_gesamt = 0  # Anzahl der zu codierenden Elemente
        self.codieren_aktuelle_nummer = 0  # aktuell ausgewähltes Codierelement der Liste codierliste_aktuell
        self.codieren_aktuelle_nummer_anzeige = self.codieren_aktuelle_nummer + 1  # Angezeigtes Codierelemt (Erhöhung um 1, damit Zählung nicht bei 0 startet)
        self.werte_uncodiert = []  # Liste der noch zu codierenden Elemente
        self.werte_codiert = []  # Liste der schon codierten Elemente
        self.element_auf_null_setzen = False
        self.relation = 0

        self.dict_code_checkboxes = {}
        self.dict_code_checkboxes_auswahl = self.dict_code_checkboxes

        index_tab_genannt_markierungen = self.tabwidg_inhalt.indexOf(self.tab_genannt_markierungen)
        self.tabwidg_inhalt.removeTab(index_tab_genannt_markierungen)
        index_tab_trennzeichen = self.tabwidg_inhalt.indexOf(self.tab_trennzeichen)
        self.tabwidg_inhalt.removeTab(index_tab_trennzeichen)

        self.neuer_spaltenname = ""  # Kurzzeitiger Speicher für neu zu erstellende Spalten im Dataframe
        self.element = ""  # kurzzeitiger Speicher von Zelleninhalten einer Spalte
        self.element2 = ""  # kurzzeitiger Speicher von einzelnen Elementen der Liste eines Zelleninhaltes einer Spalte
        self.element3 = ""  # kurzzeitiger Speicher von einzelnen Elementen der Liste eines Zelleninhaltes einer Spalte
        self.gesamtliste_aller_codes = []  # Alle Keys und Values von dict_code_checkboxes zu einer Liste zusammengefasst
        self.getrennte_code_elemente = ""  # Aufsplittung von Values aus dem Dictionaire dict_code_checkboxes
        self.spalteninhalt_als_liste = []  # kurzzeitiger Speicher des alten Spalteninhalts aber Mehrfachantworten als Liste codiert

        self.codierte_keys = [list(key) for key in self.datenspeicher.codierdict_export.keys()]

    def event(self, event):  # Aktivieren des Mainfensters beim Schließen
        if event.type() == QtCore.QEvent.Close:
            self.frm_main.enable_frm_main()
        return super().event(event)

    def funktionalitaet(self):
        self.listWidget_Spalten.itemSelectionChanged.connect(self.update_tmp_spalten_auswahl)
        self.button_spaltenauswahl_speichern.clicked.connect(self.button_spaltenauswahl_speichern_clicked)
        self.button_genannt_markierung_speichern.clicked.connect(self.genannt_markierung_speichern)
        self.button_trennzeichenauswahl_speichern.clicked.connect(self.trennzeichenauslesen)
        self.button_codeauswahl_speichern.clicked.connect(self.codeauswahl_speichern)
        self.checkBox_codieren_codierteanzeigen.stateChanged.connect(self.click_checkbox_codiertuncodiert)
        self.checkBox_codieren_uncodierteanzeigen.stateChanged.connect(self.click_checkbox_codiertuncodiert)
        # def init_widget_codieren(self):
        self.button_zumersten.clicked.connect(self.click_button_zumersten)
        self.button_rueckwaerts.clicked.connect(self.click_button_rueckwaerts)
        self.button_vorwaerts.clicked.connect(self.click_button_vorwaerts)
        self.button_zumletzten.clicked.connect(self.click_button_zumletzten)
        self.line_codeakt_num.textChanged.connect(self.on_line_codeakt_num_changed)

        self.button_OK.clicked.connect(self.click_OK)

        self.label_7.setTextFormat(Qt.RichText)
        self.label_7.setText(
            "<b>Bitte ordnen Sie die Daten aus Ihrer Dokumentation den ausgewählten Kategorien zu.</b><br>Das Skript hat alle in den ausgewählten Spalten ausgewählten Antworten ausgelesen. Sie finden sie in der folgenden Form angezeigt:<br>Name der Spalte: Antwort")

    # je nach aktueller Codiereung werden unterschiedliche Fenster angezeigt
    def werte_auswahl(self, datenspeicher):
        print("werte_auswahl anfang")
        if self.datenspeicher.aktuell_codiert == "Lebensbereich":  # siehe oeffnen_gui_codierfenster_lebensbereich()
            self.tmp_spalten_auswahl = self.datenspeicher.spalten_lebensbereich
            self.genannt = self.datenspeicher.genannt_lebensbereich
            self.dict_code_checkboxes = self.datenspeicher.dict_lebensbereiche_vorgabe
            self.trennzeichen_liste = self.datenspeicher.trennzeichen_liste_lebensbereich
            self.dict_code_checkboxes_auswahl = self.datenspeicher.dict_code_checkboxes_auswahl_lebensbereich
            self.label_codierung_ueberschrift.setText("<b>Kategorien zuordnen: Lebensbereich</b>")
            self.codierliste_dict = self.datenspeicher.codierliste_dict_lebensbereich
            self.label_codierung_ueberschrift.setTextFormat(Qt.RichText)
        if self.datenspeicher.aktuell_codiert == "Diskriminierungsmerkmale":
            self.tmp_spalten_auswahl = self.datenspeicher.spalten_diskriminierungsmerkmale
            self.genannt = self.datenspeicher.genannt_diskriminierungsmerkmale
            self.dict_code_checkboxes = self.datenspeicher.dict_diskriminierungsmerkmale_vorgabe
            self.trennzeichen_liste = self.datenspeicher.trennzeichen_liste_diskriminierungsmerkmale
            self.dict_code_checkboxes_auswahl = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsmerkmale
            self.label_codierung_ueberschrift.setText("<b>Kategorien zuordnen: Diskriminierungsmerkmale</b>")
            self.codierliste_dict = self.datenspeicher.codierliste_dict_diskriminierungsmerkmal
            self.label_codierung_ueberschrift.setTextFormat(Qt.RichText)
        if self.datenspeicher.aktuell_codiert == "Interventionsformen":
            self.tmp_spalten_auswahl = self.datenspeicher.spalten_interventionsformen
            self.genannt = self.datenspeicher.genannt_interventionsformen
            self.dict_code_checkboxes = self.datenspeicher.dict_interventionsformen_vorgabe
            self.trennzeichen_liste = self.datenspeicher.trennzeichen_liste_interventionsformen
            self.dict_code_checkboxes_auswahl = self.datenspeicher.dict_code_checkboxes_auswahl_interventionsformen
            self.label_codierung_ueberschrift.setText("<b>Kategorien zuordnen: Interventionsformen</b>")
            self.codierliste_dict = self.datenspeicher.codierliste_dict_interventionsform
            self.label_codierung_ueberschrift.setTextFormat(Qt.RichText)
        if self.datenspeicher.aktuell_codiert == "Diskriminierungsform":
            self.tmp_spalten_auswahl = self.datenspeicher.spalten_diskriminierungsform
            self.genannt = self.datenspeicher.genannt_diskriminierungsform
            self.dict_code_checkboxes = self.datenspeicher.dict_diskriminierungsform_vorgabe
            self.trennzeichen_liste = self.datenspeicher.trennzeichen_liste_diskriminierungsform
            self.dict_code_checkboxes_auswahl = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsform
            self.label_codierung_ueberschrift.setText("<b>Kategorien zuordnen: Diskriminierungsform(en)</b>")
            self.codierliste_dict = self.datenspeicher.codierliste_dict_diskriminierungsform
            self.label_codierung_ueberschrift.setTextFormat(Qt.RichText)
        if self.datenspeicher.aktuell_codiert == "AGG_Relevanz":
            self.tmp_spalten_auswahl = self.datenspeicher.spalten_agg_relevanz
            self.genannt = self.datenspeicher.genannt_agg_relevanz
            self.dict_code_checkboxes = self.datenspeicher.dict_agg_relevanz_vorgabe
            self.trennzeichen_liste = self.datenspeicher.trennzeichen_liste_agg_relevanz
            self.dict_code_checkboxes_auswahl = self.datenspeicher.dict_code_checkboxes_auswahl_agg_relevanz
            self.label_codierung_ueberschrift.setText("<b>Kategorien zuordnen: AGG-Relevanz</b>")
            self.codierliste_dict = self.datenspeicher.codierliste_dict_agg_relevanz
            self.label_codierung_ueberschrift.setTextFormat(Qt.RichText)
        self.spalten_auswahl = self.tmp_spalten_auswahl

        # print("werte_auswahl ende")

    # die aktuelle Auswahl wird aus dem Datenspeicher in die GUI übertragen
    def werte_füllen(self, datenspeicher):
        self.werte_auswahl(datenspeicher)
        self.listWidget_Spalten.clear()
        self.listWidget_Spalten.addItems(datenspeicher.spalten_gesamt)
        for index in range(self.listWidget_Spalten.count()):
            item = self.listWidget_Spalten.item(index)
            print("Spaltenauswahl", self.tmp_spalten_auswahl)
            for spalte in self.tmp_spalten_auswahl:
                print("suche", item.text(), "!=", spalte)
                if item.text() == spalte:
                    item.setSelected(True)
                    print("Spalte gefunden", spalte)
        self.checkbox_codierung_füllen()
        self.spaltenauswahl_funktionalität = True

    def trennzeichen_lesen(self):
        if self.trennzeichen_liste == []:
            return
        if not self.trennzeichen_liste == ["", "", ""]:
            self.lineEdit_trennzeichen1.setText(self.trennzeichen_liste[0])
            self.lineEdit_trennzeichen2.setText(self.trennzeichen_liste[1])
            self.lineEdit_trennzeichen3.setText(self.trennzeichen_liste[2])

    ### Hat keine Funktion? ###
    def adjust_horizontal_layout(self):
        # listWidget_Spalten und text_spaltenauswahl sollen konstant gleich gross bleiben
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)

    # Widget Spalten wird befüllt:
    #   Folgende Spalten sind zur Zeit ausgewählt:
    #   SpaltenName [längster Spalteninhalt]
    #   Dargestellt ist jeweils ein Spalteneintrag als Beispiel in eckigen Klammern.
    def update_tmp_spalten_auswahl(self):
        if self.spaltenauswahl_funktionalität == True:
            selected_items = self.listWidget_Spalten.selectedItems()
            self.tmp_spalten_auswahl = [item.text() for item in selected_items]

        self.laengste_auspraegungen_str_spalten = self.spalteninhalt_laengste(anzahl=1, oneline=True)
        self.text_spaltenauswahl.setTextFormat(Qt.RichText)
        self.text_spaltenauswahl.setText(
            "<p>Folgende Spalten sind zur Zeit ausgewählt:</p>" + self.laengste_auspraegungen_str_spalten + "<br><br>Dargestellt ist jeweils ein Spalteneintrag als Beispiel in eckigen Klammern.")
        self.text_spaltenauswahl.setWordWrap(True)
        self.text_spaltenauswahl.setFixedWidth(200)

        if self.first_run:  # Nur beim ersten Durchlauf eine Scroll Area erstellen
            # Erstellen einer Scroll Area
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            # Erstellen eines Widgets für das Layout innerhalb der Scroll Area
            self.scroll_widget = QWidget()
            scroll_layout = QVBoxLayout(self.scroll_widget)
            scroll_layout.addWidget(self.text_spaltenauswahl)

            # Das Scroll-Widget der Scroll Area zuweisen
            scroll_area.setWidget(self.scroll_widget)

            # Das Scroll-Widget zum Layout hinzufügen
            self.horizontalLayout.addWidget(scroll_area)

            self.first_run = False  # Markiere den ersten Durchlauf als abgeschlossen

        else:
            if self.scroll_widget is not None:
                scroll_layout = self.scroll_widget.layout()
                if scroll_layout is not None:
                    # Aktualisiere den Inhalt des vorhandenen Scroll-Widgets
                    scroll_layout.itemAt(0).widget().setText(self.text_spaltenauswahl.text())

    # Speichern der Spaltenauswahl
    def button_spaltenauswahl_speichern_clicked(self):
        self.spalten_auswahl = self.tmp_spalten_auswahl
        self.beispiele_trennzeichen_aktualisieren()

        if self.check_Spalte_genannt.isChecked():
            index_tab_details = self.tabwidg_inhalt.indexOf(self.tab_details)
            self.tabwidg_inhalt.removeTab(index_tab_details)
            index_tab_genannt_markierungen = self.tabwidg_inhalt.indexOf(self.tab_genannt_markierungen)
            self.tabwidg_inhalt.insertTab(1, self.tab_genannt_markierungen, "Genannt-Markierung")

            self.genannt = True
            self.tab_genannt_markierungen.setEnabled(True)
            self.tab_trennzeichen.setEnabled(False)
            self.beispiel_string_setzen_genannt()
            self.tabwidg_inhalt.setCurrentWidget(self.tab_genannt_markierungen)
        else:
            index_tab_details = self.tabwidg_inhalt.indexOf(self.tab_details)
            self.tabwidg_inhalt.removeTab(index_tab_details)
            index_tab_trennzeichen = self.tabwidg_inhalt.indexOf(self.tab_trennzeichen)
            self.tabwidg_inhalt.insertTab(1, self.tab_trennzeichen, "Trennzeichen")

            self.genannt = False
            self.tab_genannt_markierungen.setEnabled(False)
            self.tab_trennzeichen.setEnabled(True)
            self.tabwidg_inhalt.setCurrentWidget(self.tab_trennzeichen)
        self.fortschritt_spalte.setValue(100)

    # Methode, die den Namen der Spalte verknüpft mit dem längsten Spalteneintrag zurückgibt; anzahl hat keinen Effekt
    def spalteninhalt_laengste(self, anzahl, oneline):
        laengste_auspraegungen_str = ""
        unique_lengths = set()
        selected_indices = []

        for spalte in self.tmp_spalten_auswahl:
            lengths = self.datenspeicher.df[spalte].str.len()
            display("lengths", lengths)

            # Überprüfen Sie, ob es NaN-Werte oder den Wert 0 gibt
            if lengths.isna().all():
                # spalte should be set to bold in html
                laengste_auspraegungen_str += f'\n<b>{spalte}:</b> " "\n'

            else:
                max_lengths = lengths.nlargest(anzahl, keep='all').index.tolist()
                for index in max_lengths:
                    length = lengths[index]
                    if length not in unique_lengths:
                        selected_indices.append(index)
                        unique_lengths.add(length)
                        if len(selected_indices) == anzahl:
                            break

                if len(selected_indices) > anzahl:
                    selected_indices = selected_indices[:anzahl]

                laengste_auspraegungen = self.datenspeicher.df.loc[selected_indices, spalte].values.tolist()
                if oneline == True:
                    laengste_auspraegungen_str += '<br>\n<b>' + spalte + "</b><br> "
                    laengste_auspraegungen_str += str(laengste_auspraegungen) + "\n"
                if oneline == False:
                    laengste_auspraegungen_str += '<br>\n<b>' + spalte + ':</b><br>\n'
                    for auspraegung in laengste_auspraegungen:
                        laengste_auspraegungen_str += "  " + str(auspraegung) + "<br>\n"
        return laengste_auspraegungen_str

    # je nach Auswahl im Fenster Genannt-Markierung wird Codierung angepasst
    def genannt_markierung_speichern(self):
        self.genannt_markierung_leer = True
        self.genannt_markierung_zeichen = False
        self.genannt_markierung_zeichen_text = ""
        self.genannt_markierung_nichtzeichen = False
        self.genannt_markierung_nichtzeichen_text = ""

        if self.radio_genannt_nichtleer.isChecked():
            self.genannt_markierung_leer = False
        if self.radio_genannt_zeichen.isChecked():
            self.genannt_markierung_zeichen = True
            self.genannt_markierung_zeichen_text = self.line_genannt_zeichen
        if self.radio_genannt_nichtzeichen.isChecked():
            self.genannt_markierung_nichtzeichen = True
            self.genannt_markierung_nichtzeichen_text = self.line_genannt_nichtzeichen
        # self.init_widget_codieren()

        if self.datenspeicher.aktuell_codiert == "Lebensbereich":
            self.datenspeicher.genannt_markierung_leer_lebensbereich = self.genannt_markierung_leer
            self.datenspeicher.genannt_markierung_zeichen_lebensbereich = self.genannt_markierung_zeichen
            self.datenspeicher.genannt_markierung_zeichen_text_lebensbereich = self.genannt_markierung_zeichen_text
            self.datenspeicher.genannt_markierung_nichtzeichen_lebensbereich = self.genannt_markierung_nichtzeichen
            self.datenspeicher.genannt_markierung_nichtzeichen_text_lebensbereich = self.genannt_markierung_nichtzeichen_text
        if self.datenspeicher.aktuell_codiert == "Diskriminierungsmerkmale":
            self.datenspeicher.genannt_markierung_leer_diskriminierungsmerkmale = self.genannt_markierung_leer
            self.datenspeicher.genannt_markierung_zeichen_diskriminierungsmerkmale = self.genannt_markierung_zeichen
            self.datenspeicher.genannt_markierung_zeichen_text_diskriminierungsmerkmale = self.genannt_markierung_zeichen_text
            self.datenspeicher.genannt_markierung_nichtzeichen_diskriminierungsmerkmale = self.genannt_markierung_nichtzeichen
            self.datenspeicher.genannt_markierung_nichtzeichen_text_diskriminierungsmerkmale = self.genannt_markierung_nichtzeichen_text
        if self.datenspeicher.aktuell_codiert == "Interventionsformen":
            self.datenspeicher.genannt_markierung_leer_interventionsformen = self.genannt_markierung_leer
            self.datenspeicher.genannt_markierung_zeichen_interventionsformen = self.genannt_markierung_zeichen
            self.datenspeicher.genannt_markierung_zeichen_text_interventionsformen = self.genannt_markierung_zeichen_text
            self.datenspeicher.genannt_markierung_nichtzeichen_interventionsformen = self.genannt_markierung_nichtzeichen
            self.datenspeicher.genannt_markierung_nichtzeichen_text_interventionsformen = self.genannt_markierung_nichtzeichen_text
        if self.datenspeicher.aktuell_codiert == "Diskriminierungsform":
            self.datenspeicher.genannt_markierung_leer_diskriminierungsform = self.genannt_markierung_leer
            self.datenspeicher.genannt_markierung_zeichen_diskriminierungsform = self.genannt_markierung_zeichen
            self.datenspeicher.genannt_markierung_zeichen_text_diskriminierungsform = self.genannt_markierung_zeichen_text
            self.datenspeicher.genannt_markierung_nichtzeichen_diskriminierungsform = self.genannt_markierung_nichtzeichen
            self.datenspeicher.genannt_markierung_nichtzeichen_text_diskriminierungsform = self.genannt_markierung_nichtzeichen_text
        if self.datenspeicher.aktuell_codiert == "AGG_Relevanz":
            self.datenspeicher.genannt_markierung_leer_agg_relevanz = self.genannt_markierung_leer
            self.datenspeicher.genannt_markierung_zeichen_agg_relevanz = self.genannt_markierung_zeichen
            self.datenspeicher.genannt_markierung_zeichen_text_agg_relevanz = self.genannt_markierung_zeichen_text
            self.datenspeicher.genannt_markierung_nichtzeichen_agg_relevanz = self.genannt_markierung_nichtzeichen
            self.datenspeicher.genannt_markierung_nichtzeichen_text_agg_relevanz = self.genannt_markierung_nichtzeichen_text

        self.fortschritt_details.setValue(100)
        self.tab_codes_auswahl.setEnabled(True)
        self.tabwidg_inhalt.setCurrentWidget(self.tab_codes_auswahl)
        self.checkbox_anlegen_codes_keys(self.datenspeicher)

    # Benenne die ausgewählte Spalte und gebe ein Beispiel an
    def beispiel_string_setzen_genannt(self):
        spalte = self.tmp_spalten_auswahl[0]
        self.label_genannt_beispiele.setText(
            'Beispiel: \nSpalte: ' + spalte + '\nZelleninhalt: ' + self.datenspeicher.df_original[spalte].iloc[0])

    def beispiele_trennzeichen_aktualisieren(self):
        self.laengste_auspraegungen_str_spalten = self.spalteninhalt_laengste(anzahl=3, oneline=False)
        self.label_trennzeichen_beispiele.setTextFormat(Qt.RichText)

        self.label_trennzeichen_beispiele.setText(  # was soll hier effektiv stehen?
            "Beispiele für die ausgewählten Spalten;<br>Dargestellt sind bis zu drei Beispielangaben für jede Spalte.<br>" + self.laengste_auspraegungen_str_spalten)
        self.label_trennzeichen_beispiele.setWordWrap(True)

    # Methode, die die Zelleninhalte anhand der Trennzeichen in Listen umwandelt: [Spaltenname, Merkmal]
    def trennzeichenauslesen(self):
        # Trennzeichen einlesen
        self.lineEdit_trennzeichen1_text = self.lineEdit_trennzeichen1.text()
        self.lineEdit_trennzeichen2_text = self.lineEdit_trennzeichen2.text()
        self.lineEdit_trennzeichen3_text = self.lineEdit_trennzeichen3.text()

        # Trennzeichen zu liste zusammenfassen
        self.trennzeichen_liste = [self.lineEdit_trennzeichen1_text, self.lineEdit_trennzeichen2_text,
                                   self.lineEdit_trennzeichen3_text]
        #
        self.elemente_vollstaendig_getrennt_einfach = []
        # geht jede ausgewählte Spalte durch
        for spalte in self.spalten_auswahl:
            # speichert alle Elemente der Spalte in einer Liste
            self.spaltenelemente_vollstaendig = self.datenspeicher.df[spalte].values.tolist()
            # initialisiert eine Liste für die
            self.spaltenelemente_vollstaendig_zusammen = []
            # geht jedes Element der Elementenliste durch
            for sublist in self.spaltenelemente_vollstaendig:
                # check if sublist / Listenelement ist selbst eine Liste, falls nicht wird Element in Liste umgewandelt
                if not isinstance(sublist, list):
                    sublist = [sublist]
                # geht das einzige Element der Liste durch
                for element in sublist:  ### Diese ganze Methodik ist nicht sinnvoll, oben wird sichergestellt, dass es sich um eine Liste mit nur einem Element handelt
                    element_copy = str(element)
                    # geht jedes Trennzeichen durch
                    for trennzeichen in self.trennzeichen_liste:
                        # wenn es Trennzeichen gibt, dann wird das Element an den Trennzeichen gesplittet
                        if trennzeichen != "":
                            getrennte_elemente = element_copy.split(trennzeichen)
                            # die getrennten Elemente werden der Liste 'zusammen' hinzugefügt
                            self.spaltenelemente_vollstaendig_zusammen.extend(getrennte_elemente)
                        elif self.trennzeichen_liste == ["", "", ""]:
                            getrennte_elemente = [element_copy]
                            # das gesamte Elemente wird der Liste 'zusammen' hinzugefügt
                            self.spaltenelemente_vollstaendig_zusammen.extend(getrennte_elemente)
            # die Liste 'zusammen' wird in eine Liste 'getrennt' umgewandelt, es werden Leerzeichen entfernt
            self.spaltenelemente_vollstaendig_getrennt = [element.strip() for element in
                                                          self.spaltenelemente_vollstaendig_zusammen]
            self.spaltenelemente_vollstaendig_getrennt_einfach = []
            # die Liste 'getrennt' wird in eine Liste 'getrennt_einfach' umgewandelt, es werden Duplikate entfernt
            self.spaltenelemente_vollstaendig_getrennt_einfach = list(set(self.spaltenelemente_vollstaendig_getrennt))
            # die Liste 'getrennt_einfach' wird in eine Liste 'elemente_vollstaendig_getrennt_einfach' umgewandelt, Muster: [Spaltenname, Merkmal]
            self.elemente_vollstaendig_getrennt_einfach = self.elemente_vollstaendig_getrennt_einfach + [
                [spalte, element]
                for element in
                self.spaltenelemente_vollstaendig_getrennt_einfach]

        # fortschrittsbalken aktualisieren
        self.fortschritt_details.setValue(100)
        # erlaube den Klick auf den Tab Codierung
        self.tab_codes_auswahl.setEnabled(True)
        # wechsle zum Tab Codierung
        self.tabwidg_inhalt.setCurrentWidget(self.tab_codes_auswahl)
        # erstelle die Checkboxen für die Codierung
        self.checkbox_anlegen_codes_keys(self.datenspeicher)

    # Methode, die die Checkboxen für die Codierung erstellt
    def checkbox_anlegen_codes_keys(self,
                                    datenspeicher):  # Checkboxen für Auswahl der im Dokusystem Keys der Codes anlegen
        # Clear the contents of the layout first
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        self.schlüssel_checkboxes = []
        self.wert_checkboxes = []
        # Für jeden Oberbegriff wird iteriert

        if self.kategorien_bereits_ausgewählt:
            aktuelles_dict = self.get_aktuelles_dict()
            for key in self.dict_code_checkboxes.keys():
                checkbox_codes_festlegen1 = QCheckBox(key)
                if key in aktuelles_dict:
                    checkbox_codes_festlegen1.setChecked(True)  # Set the checkbox as checked initially
                else:
                    checkbox_codes_festlegen1.setChecked(False)
                checkbox_codes_festlegen1.stateChanged.connect(
                    self.aendere_werte_keyboxen)  # Verknüpfung zur Funktion hinzufügen
                self.schlüssel_checkboxes.append(checkbox_codes_festlegen1)
                self.layout.addWidget(checkbox_codes_festlegen1)

                # Call the method to add value checkboxes directly below the key checkbox
                self.checkbox_anlegen_codes_values(key)
        else:
            for key in self.dict_code_checkboxes.keys():
                checkbox_codes_festlegen1 = QCheckBox(key)
                checkbox_codes_festlegen1.setChecked(True)  # Set the checkbox as checked initially
                checkbox_codes_festlegen1.stateChanged.connect(
                    self.aendere_werte_keyboxen)  # Verknüpfung zur Funktion hinzufügen
                self.schlüssel_checkboxes.append(checkbox_codes_festlegen1)
                self.layout.addWidget(checkbox_codes_festlegen1)

                # Call the method to add value checkboxes directly below the key checkbox
                self.checkbox_anlegen_codes_values(key)

        # Set the layout as the central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout)

        # Create a scroll area and set the central widget as its content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)

        # Clear the contents of the vertical layout first
        while self.verticalLayout_codes_liste.count():
            item = self.verticalLayout_codes_liste.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        # Add the scroll area to the vertical layout
        self.verticalLayout_codes_liste.addWidget(scroll_area)

        print("checkbox_anlegen_codes_keys ende")

    # Methode, die die Checkboxen für die Codierung trackt und auf Änderungen reagiert

    # Wenn die Schlüssel-Checkbox aktiviert wird, aktiviere auch die zugehörigen Wert-Checkboxes, wenn sie aber durch eine Funktion geändert wird, sollen die zugehörigen Wert-Checkboxes nicht aktiviert werden
    def aendere_werte_keyboxen(self, state):
        sender_checkbox = self.sender()

        if state == QtCore.Qt.Checked:
            for checkbox in self.wert_checkboxes[self.schlüssel_checkboxes.index(sender_checkbox)]:
                checkbox.setChecked(True)
        elif state == QtCore.Qt.Unchecked:
            for checkbox in self.wert_checkboxes[self.schlüssel_checkboxes.index(sender_checkbox)]:
                checkbox.setChecked(False)

    # Wenn die übergeordnete Schlüsselbox noch nicht aktiviert ist, aktiviere sie, falls eine der Wertboxen aktiviert ist, falls keine Wertbox aktiviert ist, deaktiviere die Schlüsselbox
    def aendere_werte_detailbox(self, state):
        sender_checkbox = self.sender()
        keybox = self.get_keybox(sender_checkbox)
        self.aktualisiere_keybox(keybox)

    # Methode die zu einer checkbox die zugehörige keybox zurückgibt
    def get_keybox(self, checkbox):
        for keybox in self.schlüssel_checkboxes:
            if checkbox in self.wert_checkboxes[self.schlüssel_checkboxes.index(keybox)]:
                return keybox

    # Methode die die keybox aktualisiert, indem sie prüft, ob eine der zugehörigen Wertboxen aktiviert ist
    def aktualisiere_keybox(self, keybox):
        value_checkboxes = self.wert_checkboxes[self.schlüssel_checkboxes.index(keybox)]
        for checkbox in value_checkboxes:
            if checkbox.isChecked():
                with QSignalBlocker(keybox) as blocker:
                    keybox.setChecked(True)
                return
        keybox.setChecked(False)

    # Methode, die die einzelnen Checkboxen für die Codierung erstellt, z.B. für alle unter dem Key Arbeit#
    def checkbox_anlegen_codes_values(self, key):  # Checkboxen für Values der Key-Codes anlegen
        values = self.dict_code_checkboxes[key]
        layout = QVBoxLayout()
        value_checkboxes = []

        if self.kategorien_bereits_ausgewählt:
            aktuelles_dict = self.get_aktuelles_dict()
            dict_values = [val for values_list in aktuelles_dict.values() for val in values_list]
            for value in values:
                checkbox = QCheckBox(value)
                checkbox.setStyleSheet("QCheckBox { font-size: 12px; margin-left: 20px; }")
                if value in dict_values:
                    checkbox.setChecked(True)
                else:
                    checkbox.setChecked(False)
                checkbox.stateChanged.connect(self.aendere_werte_detailbox)  # Verknüpfung zur Funktion hinzufügen
                checkbox.stateChanged.connect(lambda state, key_checkbox=checkbox: self.update_key_checkbox(state,
                                                                                                            key_checkbox))  # Verknüpfung zur update_key_checkbox-Funktion hinzufügen
                layout.addWidget(checkbox)

                # Füge die Wert-Checkbox zur Liste hinzu
                value_checkboxes.append(checkbox)
        else:
            for value in values:
                checkbox = QCheckBox(value)
                checkbox.setStyleSheet("QCheckBox { font-size: 12px; margin-left: 20px; }")
                checkbox.setChecked(True)  # Set the value checkbox as  checked initially
                checkbox.stateChanged.connect(self.aendere_werte_detailbox)  # Verknüpfung zur Funktion hinzufügen
                checkbox.stateChanged.connect(lambda state, key_checkbox=checkbox: self.update_key_checkbox(state,
                                                                                                            key_checkbox))  # Verknüpfung zur update_key_checkbox-Funktion hinzufügen
                layout.addWidget(checkbox)

                # Füge die Wert-Checkbox zur Liste hinzu
                value_checkboxes.append(checkbox)

        # Füge die Liste value_checkboxes in self.wert_checkboxes hinzu
        self.wert_checkboxes.append(value_checkboxes)

        # Insert the value checkboxes widget below the key checkbox in the main layout
        self.layout.insertLayout(self.layout.indexOf(self.schlüssel_checkboxes[-1]) + 1, layout)

    # Wenn der Zustand der Wert-Checkbox geändert wird, aktiviere auch die zugehörige Schlüssel-Checkbox
    def update_key_checkbox(self, state, key_checkbox):
        if state == QtCore.Qt.Checked:
            key_checkbox.setChecked(True)

    def codeauswahl_speichern(self):
        self.checkbox_codeauswahl_auslesen()

        self.relation == 0
        self.erster_codieraufruf = True
        self.line_codeakt_num_autofill = True
        self.start_codierung()
        self.erster_codieraufruf = False
        self.line_codeakt_num_autofill = False
        self.datenspeicher.codierung_dict_export = self.codierliste_dict
        self.fortschritt_codes.setValue(100)
        self.tab_codieren.setEnabled(True)
        self.tabwidg_inhalt.setCurrentWidget(self.tab_codieren)

    #
    def checkbox_codeauswahl_auslesen(self):
        checkboxes = []
        for checkbox_list in self.schlüssel_checkboxes + self.wert_checkboxes:
            if isinstance(checkbox_list, list):
                for checkbox in checkbox_list:
                    if checkbox.isChecked():
                        checkboxes.append(checkbox.text())
            else:
                if checkbox_list.isChecked():
                    checkboxes.append(checkbox_list.text())

                    # Create a copy of the original dictionary and remove the labels of the unchecked checkboxes
        self.dict_code_checkboxes_auswahl = copy.deepcopy(self.dict_code_checkboxes)
        for key in list(self.dict_code_checkboxes_auswahl):
            if key not in checkboxes:
                self.dict_code_checkboxes_auswahl.pop(key)
        # Create a list of values to be removed
        values_to_remove = []
        for value in self.dict_code_checkboxes_auswahl.values():
            for value1 in value:
                if value1 not in checkboxes:
                    values_to_remove.append(value1)
        values_to_pop = []  # Liste, um die Werte zu sammeln, die entfernt werden sollen

        for key, value in self.dict_code_checkboxes_auswahl.items():
            for value1 in value:
                if value1 in values_to_remove:
                    values_to_pop.append((key, value1))

        # Entfernen Sie die Werte nach der Schleife
        for key, value1 in values_to_pop:
            self.dict_code_checkboxes_auswahl[key].remove(value1)

        print("4: self.dict_code_checkboxes_auswahl", self.dict_code_checkboxes_auswahl)

        # Print the new dictionary

    def click_button_zumersten(self):
        self.line_codeakt_num_autofill = True
        self.relation = 0
        self.codierung_speichern()
        self.line_codeakt_num_autofill = False
        print("click_button_zumersten")

    def click_button_rueckwaerts(self):
        self.line_codeakt_num_autofill = True
        self.relation = "-1"
        self.codierung_speichern()
        self.line_codeakt_num_autofill = False
        print("click_button_rueckwaerts")

    def click_button_vorwaerts(self):
        self.line_codeakt_num_autofill = True
        self.relation = "+1"
        self.codierung_speichern()
        self.line_codeakt_num_autofill = False
        print("click_button_vorwaerts")

    def click_button_zumletzten(self):
        self.line_codeakt_num_autofill = True
        self.relation = "ende"
        self.codierung_speichern()
        self.line_codeakt_num_autofill = False
        print("click_button_zumletzten")

    def click_checkbox_codiertuncodiert(self):
        if len(self.werte_uncodiert) == 0:
            self.checkBox_codieren_codierteanzeigen.setChecked(True)
        if len(self.werte_codiert) == 0:
            self.checkBox_codieren_uncodierteanzeigen.setChecked(True)

        print("click_checkbox_codiertuncodiert anfang")
        self.element_auf_null_setzen = True
        self.line_codeakt_num_autofill = True
        self.relation = 0
        self.codierung_speichern()
        self.line_codeakt_num_autofill = False
        self.element_auf_null_setzen = False
        print("click_checkbox_codiertuncodiert ende")

    def on_line_codeakt_num_changed(
            self):  # Beim manuellen Ändern der Nummer für den zu bearbeitenden Fall zur entsprechenden Funktion verlinken
        print("on_line_codeakt_num_changed anfang")
        if self.line_codeakt_num_autofill == False:
            self.line_codeakt_num_autofill = True
            self.relation = int(self.line_codeakt_num.text()) - 1
            print("self.relation", self.relation)
            self.codierung_speichern()
            self.line_codeakt_num_autofill = False
        print("on_line_codeakt_num_changed ende")

    def checkbox_codierung_füllen(self):  # Checkboxen für Keys der Codes anlegen
        print("checkbox_codierung_füllen anfang")
        # Clear the contents of the layout first
        while self.layout2.count():
            item = self.layout2.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        self.key_checkboxes = []
        self.value_checkboxes = []
        for key in self.dict_code_checkboxes_auswahl.keys():
            checkbox_codierung_ebene1 = QCheckBox(key)
            checkbox_codierung_ebene1.stateChanged.connect(
                self.show_values_for_key)  # Separate Methode für Key-Checkboxen
            self.key_checkboxes.append(checkbox_codierung_ebene1)
            self.layout2.addWidget(checkbox_codierung_ebene1)
            self.value_checkboxes = []

        self.value_checkboxes = []

        # Set the layout as the central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout2)

        # Create a scroll area and set the central widget as its content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)

        # Clear the contents of the vertical layout first
        while self.verticalLayout_codierung_ersteebene.count():
            item = self.verticalLayout_codierung_ersteebene.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        # Add the scroll area to the vertical layout
        self.verticalLayout_codierung_ersteebene.addWidget(scroll_area)
        print("checkbox_codierung_füllen ende")

    def show_values_for_key(self, state):  # Checkboxen für Values der Key-Codes anlegen
        print("show_values_for_key anfang")
        selected_checkbox = self.sender()
        selected_key = selected_checkbox.text()
        if state:
            values = self.dict_code_checkboxes_auswahl[selected_key]
            layout2 = QVBoxLayout()
            for value in values:
                print("value", value)
                checkbox = QCheckBox(value)
                ### auskommentiert
                # checkbox.stateChanged.connect(
                #   self.speichern_ausgewaehlter_checkboxen)  # Verbindung für Value-Checkboxen Das könnte ein Problem sein
                self.value_checkboxes.append(checkbox)
                checkbox.setStyleSheet("QCheckBox { font-size: 12px; margin-left: 20px; }")
                print("länge", len(self.value_checkboxes))
                layout2.addWidget(checkbox)
            selected_widget = QWidget()
            selected_widget.setLayout(layout2)
            self.key_value_mapping[selected_checkbox] = selected_widget
            # Insert the value checkboxes widget below the selected checkbox in the main layout
            self.layout2.insertWidget(self.layout2.indexOf(selected_checkbox) + 1, selected_widget)
        else:
            selected_widget = self.key_value_mapping.get(selected_checkbox)
            if selected_widget:
                selected_widget.setParent(None)
                selected_widget.deleteLater()
                self.key_value_mapping.pop(selected_checkbox)
                # Remove value checkboxes for the deselected key
                self.value_checkboxes = [checkbox for checkbox in self.value_checkboxes if
                                         checkbox not in selected_widget.children()]
        # Check which checkboxes are selected
        ### auskommentiert
        # self.speichern_ausgewaehlter_checkboxen()
        print("show_values_for_key ende")

    def checkboxen_markieren(self):  # Gespeicherte Auswahl der Checkboxen wieder anzeigen
        print("checkboxen_markieren anfang")
        bereits_codiertes_element = False
        try:
            aktueller_key = self.codierliste_aktuell[self.codieren_aktuelle_nummer]
            bereits_codiertes_element = aktueller_key in self.codierte_keys
        except:
            print('excption')
        position_n = self.codierliste_aktuell[self.codieren_aktuelle_nummer]
        if bereits_codiertes_element:
            checkboxes_toselect_gesamt = self.datenspeicher.codierdict_export[tuple(aktueller_key)]
            if len(checkboxes_toselect_gesamt) >= 1:
                # Mark checkboxes based on selected values
                for checkbox in self.key_checkboxes:
                    for checkbox_value in checkboxes_toselect_gesamt:
                        if checkbox.text() in checkbox_value:
                            checkbox.setChecked(True)
                            break  # Den inneren Schleifen-Durchlauf beenden, wenn ein Übereinstimmung gefunden wurde
                for checkbox in self.value_checkboxes:
                    for checkbox_value in checkboxes_toselect_gesamt:
                        if checkbox.text() in checkbox_value:
                            checkbox.setChecked(True)
                            break  # Den inneren Schleifen-Durchlauf beenden, wenn ein Übereinstimmung gefunden wurde
        else:
            # No value found in codierliste_dict, uncheck all checkboxes
            for checkbox in self.key_checkboxes + self.value_checkboxes:
                checkbox.setChecked(False)
        print("checkboxen_markieren ende")

    def start_codierung(self):
        print("start_codierung 1")
        validator = QIntValidator(1, 9999999)
        print("start_codierung 1a")
        if self.erster_codieraufruf == True:
            self.codierliste_gesamt_initialisieren()
            print("start_codierung 1b")
        print("start_codierung 2")
        self.erster_codieraufruf = False
        print("start_codierung 3")
        if self.element_auf_null_setzen == True:
            self.element_position_veraendern(position=0)
        print("start_codierung 4")
        self.codierliste_aktuell_erstellen()
        print("start_codierung 5")
        self.element_auswaehlen()
        print("start_codierung 6")
        self.checkbox_codierung_füllen()
        print("start_codierung 7")
        self.checkboxen_markieren()
        print("start_codierung 8")
        self.sprungbuttons_enablen()
        print("start_codierung 9")

    def codierung_speichern(self):
        self.speichern_ausgewaehlter_checkboxen()
        self.speichern_in_listen()
        self.fortschritt_codierung = 100 * len(self.werte_codiert) / self.n_zucodieren_gesamt
        self.fortschritt_codieren.setValue(self.fortschritt_codierung)
        self.start_codierung()
        self.frm_main.fortschritt_aktualisieren()

    def element_auswaehlen(self):
        if self.relation == "-1":
            self.nummer = self.codieren_aktuelle_nummer - 1
        elif self.relation == "+1":
            self.nummer = self.codieren_aktuelle_nummer + 1
        elif self.relation == "ende":
            self.nummer = len(self.codierliste_aktuell) - 1
        else:
            self.nummer = self.relation
        self.element_position_veraendern(position=self.nummer)

    def element_position_veraendern(self, position):
        self.codieren_aktuelle_nummer = int(position)
        self.codieren_aktuelle_nummer_anzeige = self.codieren_aktuelle_nummer + 1
        if self.genannt == True:
            self.lbl_codetext.setText("</b>" + str(self.codierliste_aktuell[self.codieren_aktuelle_nummer]) + "</b>")
        if self.genannt == False:
            try:
                if str(self.codierliste_aktuell[self.codieren_aktuelle_nummer][1]) == 'nan':
                    self.lbl_codetext.setText(
                        str(self.codierliste_aktuell[self.codieren_aktuelle_nummer][
                                0]) + "  :  \n" + "<b>" + "[leere Zelle]" + "</b>")
                else:
                    self.lbl_codetext.setText(
                        str(self.codierliste_aktuell[self.codieren_aktuelle_nummer][0]) + "  :  \n" + "<b>" + str(
                            self.codierliste_aktuell[self.codieren_aktuelle_nummer][1]) + "</b>")
            except:
                print('exception')
        self.lbl_codetext.setWordWrap(True)  # Aktivieren Sie den Zeilenumbruch, falls erforderlich
        self.lbl_codetext.setTextFormat(Qt.RichText)  # Setzen Sie die Rich-Text-Formatierung
        self.line_codeakt_num.setText(str(self.codieren_aktuelle_nummer_anzeige))

    def sprungbuttons_enablen(self):
        if self.codieren_aktuelle_nummer == len(self.codierliste_aktuell) - 1:
            self.button_vorwaerts.setEnabled(False)
            self.button_zumletzten.setEnabled(False)
        else:
            self.button_vorwaerts.setEnabled(True)
            self.button_zumletzten.setEnabled(True)
        if self.codieren_aktuelle_nummer == 0:
            self.button_zumersten.setEnabled(False)
            self.button_rueckwaerts.setEnabled(False)
        else:
            self.button_zumersten.setEnabled(True)
            self.button_rueckwaerts.setEnabled(True)

    def codierliste_gesamt_initialisieren(self):
        self.codierliste.extend(self.codierte_keys)
        for element in self.codierliste:
            if self.datenspeicher.codierdict_export.get(tuple(element)) == []:
                self.codierliste.remove(element)

        if self.genannt == True:
            self.codierliste = self.spalten_auswahl
            # self.werte_uncodiert = [element for element in self.spalten_auswahl if element not in keys_as_list]
            # self.werte_codiert = [element for element in self.spalten_auswahl if element in keys_as_list]
            codierliste_dict_appendix = {key: [] for key in self.spalten_auswahl}
            for key, value in codierliste_dict_appendix.items():
                if key not in self.codierliste_dict:
                    self.codierliste_dict[key] = value
            self.codierliste_dict2 = copy.deepcopy(self.codierliste_dict)
            print("codierliste_gesamt_initialisieren 2a")
            print("self.codierliste", self.codierliste)
        if self.genannt == False:
            self.codierliste = self.elemente_vollstaendig_getrennt_einfach
            self.werte_codiert = [element for element in self.elemente_vollstaendig_getrennt_einfach if
                                  element in self.codierte_keys and
                                  element not in self.werte_codiert]
            self.werte_uncodiert = [element for element in self.elemente_vollstaendig_getrennt_einfach if
                                    element not in self.werte_codiert and
                                    element not in self.werte_uncodiert]
            self.codierliste_dict = {tuple(key): [] for key in self.elemente_vollstaendig_getrennt_einfach}
            self.codierliste_dict2 = copy.deepcopy(self.codierliste_dict)
            print("codierliste_gesamt_initialisieren 2b")
            print("self.codierliste", self.codierliste)
        # self.werte_uncodiert = copy.deepcopy(self.codierliste)
        self.n_zucodieren_gesamt = len(self.codierliste)
        print("self.werte_codiert", self.werte_codiert)
        print("self.n_zucodieren_gesamt", self.n_zucodieren_gesamt)
        self.lbl_fort_daten_cod.setText(
            "Daten codieren (" + str(len(self.werte_codiert)) + "/" + str(self.n_zucodieren_gesamt) + ")")

    def codierliste_aktuell_erstellen(self):
        if self.checkBox_codieren_codierteanzeigen.isChecked() & self.checkBox_codieren_uncodierteanzeigen.isChecked():
            self.codierliste_aktuell = copy.deepcopy(self.codierliste)
        elif self.checkBox_codieren_codierteanzeigen.isChecked():
            self.codierliste_aktuell = copy.deepcopy(self.werte_codiert)
        elif self.checkBox_codieren_uncodierteanzeigen.isChecked():
            self.codierliste_aktuell = copy.deepcopy(self.werte_uncodiert)
        else:
            self.checkBox_codieren_uncodierteanzeigen.setChecked(True)
        n_zucodieren_auswahl = len(self.codierliste_aktuell)
        self.lbl_codieren_gesamtzahl.setText("/" + str(n_zucodieren_auswahl))
        validator = QIntValidator(1, len(self.codierliste_aktuell))
        self.line_codeakt_num.setValidator(validator)

    def speichern_ausgewaehlter_checkboxen(self):  # Ausgewählte Checkboxen speichern
        print("speichern_ausgewählter_checkboxen anfang")
        # Check which checkboxes are selected
        selected_key_checkboxes = [checkbox.text() for checkbox in self.key_checkboxes if checkbox.isChecked()]
        selected_value_checkboxes = [checkbox.text() for checkbox in self.value_checkboxes if checkbox.isChecked()]
        selected_checkboxes_gesamt = selected_key_checkboxes + selected_value_checkboxes
        position_n = self.codierliste_aktuell[self.codieren_aktuelle_nummer]
        if self.genannt == True:
            self.codierliste_dict[position_n] = [selected_checkboxes_gesamt]
            print("self.codierliste_dict", self.codierliste_dict)
        if self.genannt == False:
            self.codierliste_dict[tuple(position_n)] = [selected_checkboxes_gesamt]
            self.datenspeicher.codierdict_export[tuple(position_n)] = [selected_checkboxes_gesamt]
        print("speichern_ausgewählter_checkboxen ende")

    def speichern_in_listen(self):
        if any(checkbox.isChecked() for checkbox in self.key_checkboxes) or any(
                checkbox.isChecked() for checkbox in self.value_checkboxes):
            element = self.codierliste_aktuell[self.codieren_aktuelle_nummer]
            if element in self.werte_uncodiert:
                self.werte_uncodiert.remove(element)
            if not element in self.werte_codiert:
                self.werte_codiert.append(element)
        elif self.position != "":
            element = self.codierliste_aktuell[self.position]
            if element in self.werte_codiert:
                self.werte_codiert.remove(element)
            if not element in self.werte_uncodiert:
                self.werte_uncodiert.append(element)
        print("self.werte_codiert", self.werte_codiert)
        print("self.n_zucodieren_gesamt", self.n_zucodieren_gesamt)
        self.lbl_fort_daten_cod.setText(
            "Daten codieren (" + str(len(self.werte_codiert)) + "/" + str(self.n_zucodieren_gesamt) + ")")

    def click_OK(self):
        self.speichern_ausgewaehlter_checkboxen()
        self.speichern_in_listen()
        self.fortschritt_codierung = 100 * len(self.werte_codiert) / self.n_zucodieren_gesamt
        self.fortschritt_codieren.setValue(self.fortschritt_codierung)
        # Spalten anlegen für alle im Dictionaire potentiell vorkommenden Werte
        print("self.dict_code_checkboxes", self.dict_code_checkboxes)
        if self.datenspeicher.aktuell_codiert == "Lebensbereich":
            self.datenspeicher.spalten_lebensbereich = self.tmp_spalten_auswahl
            self.datenspeicher.genannt_lebensbereich = self.genannt
            self.datenspeicher.fortschritt_lebensbereiche = self.fortschritt_codierung
            self.datenspeicher.dict_lebensbereich_vorgabe = self.dict_code_checkboxes
            self.datenspeicher.trennzeichen_liste_lebensbereich = self.trennzeichen_liste
            self.datenspeicher.dict_code_checkboxes_auswahl_lebensbereich = self.dict_code_checkboxes_auswahl
            self.datenspeicher.codierung_dict_export_lebensbereich = self.codierliste_dict
            self.datenspeicher.lebensbereich_codiert = True
            self.datenspeicher.codierliste_dict_lebensbereich = self.codierliste_dict
        if self.datenspeicher.aktuell_codiert == "Diskriminierungsmerkmale":
            self.datenspeicher.spalten_diskriminierungsmerkmale = self.tmp_spalten_auswahl
            self.datenspeicher.genannt_diskriminierungsmerkmale = self.genannt
            self.datenspeicher.fortschritt_diskriminierungsmerkmale = self.fortschritt_codierung
            self.datenspeicher.dict_diskriminierungsmerkmalee_vorgabe = self.dict_code_checkboxes
            self.datenspeicher.trennzeichen_liste_diskriminierungsmerkmale = self.trennzeichen_liste
            self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsmerkmale = self.dict_code_checkboxes_auswahl
            self.datenspeicher.codierung_dict_export_diskriminierungsmerkmale = self.codierliste_dict
            self.datenspeicher.diskriminierungsmerkmale_codiert = True
            self.datenspeicher.codierliste_dict_diskriminierungsmerkmal = self.codierliste_dict
        if self.datenspeicher.aktuell_codiert == "Interventionsformen":
            self.datenspeicher.spalten_interventionsformen = self.tmp_spalten_auswahl
            self.datenspeicher.genannt_interventionsformen = self.genannt
            self.datenspeicher.fortschritt_interventionsform = self.fortschritt_codierung
            self.datenspeicher.dict_interventionsformen_vorgabe = self.dict_code_checkboxes
            self.datenspeicher.trennzeichen_liste_interventionsformen = self.trennzeichen_liste
            self.datenspeicher.dict_code_checkboxes_auswahl_interventionsformen = self.dict_code_checkboxes_auswahl
            self.datenspeicher.codierung_dict_export_interventionsformen = self.codierliste_dict
            self.datenspeicher.interventionsformen_codiert = True
            self.datenspeicher.codierliste_dict_interventionsform = self.codierliste_dict
        if self.datenspeicher.aktuell_codiert == "Diskriminierungsform":
            self.datenspeicher.spalten_diskriminierungsform = self.tmp_spalten_auswahl
            self.datenspeicher.genannt_diskriminierungsform = self.genannt
            self.datenspeicher.fortschritt_diskriminierungsform = self.fortschritt_codierung
            self.datenspeicher.dict_diskriminierungsform_vorgabe = self.dict_code_checkboxes
            self.datenspeicher.trennzeichen_liste_diskriminierungsform = self.trennzeichen_liste
            self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsform = self.dict_code_checkboxes_auswahl
            self.datenspeicher.codierung_dict_export_diskriminierungsform = self.codierliste_dict
            self.datenspeicher.diskriminierungsform_codiert = True
            self.datenspeicher.codierliste_dict_diskriminierungsform = self.codierliste_dict
        if self.datenspeicher.aktuell_codiert == "AGG_Relevanz":
            self.datenspeicher.spalten_agg_relevanz = self.tmp_spalten_auswahl
            self.datenspeicher.genannt_agg_relevanz = self.genannt
            self.datenspeicher.fortschritt_agg_relevanz = self.fortschritt_codierung
            self.datenspeicher.dict_agg_relevanz_vorgabe = self.dict_code_checkboxes
            self.datenspeicher.trennzeichen_liste_agg_relevanz = self.trennzeichen_liste
            self.datenspeicher.dict_code_checkboxes_auswahl_agg_relevanz = self.dict_code_checkboxes_auswahl
            self.datenspeicher.codierung_dict_export_agg_relevanz = self.codierliste_dict
            self.datenspeicher.agg_relevanz_codiert = True
            self.datenspeicher.codierliste_dict_agg_relevanz = self.codierliste_dict
        self.frm_main.fortschritt_aktualisieren()
        print(self.datenspeicher.df)
        self.close()


class FRM_datenausgabe(QMainWindow, Ui_fenster_datenausgabe):
    def __init__(self, datenspeicher, frm_main):  # frm_main als Argument hinzugefügt
        super().__init__()
        self.setupUi(self)
        self.datenspeicher = datenspeicher
        self.frm_main = frm_main
        self.tmp_vars_erstellen()
        self.funktionalitaet()
        self.werte_füllen(datenspeicher)
        self.gesamtliste_aller_codes = []
        self.button_speichern.setEnabled(False)

    def tmp_vars_erstellen(self):
        self.tmp_pfad_datenausgabe = ""

    def event(self, event):
        if event.type() == QtCore.QEvent.Close:
            self.frm_main.enable_frm_main()
        return super().event(event)

    def funktionalitaet(self):
        self.button_datenausgabe_durchsuchen.clicked.connect(self.datei_auswahl_einfach)
        self.button_speichern.clicked.connect(self.button_speichern_klicked)
        self.button_abbrechen.clicked.connect(self.abbrechen)

    def button_speichern_klicked(self):
        if (self.datenspeicher.lebensbereich_codiert):
            self.auswerten(self.datenspeicher.dict_code_checkboxes_auswahl_lebensbereich,
                           self.datenspeicher.codierung_dict_export_lebensbereich,
                           self.datenspeicher.genannt_lebensbereich,
                           self.datenspeicher.trennzeichen_liste_lebensbereich,
                           self.datenspeicher.genannt_markierung_leer_lebensbereich,
                           self.datenspeicher.genannt_markierung_zeichen_lebensbereich,
                           self.datenspeicher.genannt_markierung_zeichen_text_lebensbereich,
                           self.datenspeicher.genannt_markierung_nichtzeichen_lebensbereich,
                           self.datenspeicher.genannt_markierung_nichtzeichen_text_lebensbereich)
        if (self.datenspeicher.diskriminierungsmerkmale_codiert):
            self.auswerten(self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsmerkmale,
                           self.datenspeicher.codierung_dict_export_diskriminierungsmerkmale,
                           self.datenspeicher.genannt_diskriminierungsmerkmale,
                           self.datenspeicher.trennzeichen_liste_diskriminierungsmerkmale,
                           self.datenspeicher.genannt_markierung_leer_diskriminierungsmerkmale,
                           self.datenspeicher.genannt_markierung_zeichen_diskriminierungsmerkmale,
                           self.datenspeicher.genannt_markierung_zeichen_text_diskriminierungsmerkmale,
                           self.datenspeicher.genannt_markierung_nichtzeichen_diskriminierungsmerkmale,
                           self.datenspeicher.genannt_markierung_nichtzeichen_text_diskriminierungsmerkmale)
        if (self.datenspeicher.interventionsformen_codiert):
            self.auswerten(self.datenspeicher.dict_code_checkboxes_auswahl_interventionsformen,
                           self.datenspeicher.codierung_dict_export_interventionsformen,
                           self.datenspeicher.genannt_interventionsformen,
                           self.datenspeicher.trennzeichen_liste_interventionsformen,
                           self.datenspeicher.genannt_markierung_leer_interventionsformen,
                           self.datenspeicher.genannt_markierung_zeichen_interventionsformen,
                           self.datenspeicher.genannt_markierung_zeichen_text_interventionsformen,
                           self.datenspeicher.genannt_markierung_nichtzeichen_interventionsformen,
                           self.datenspeicher.genannt_markierung_nichtzeichen_text_interventionsformen)
        if (self.datenspeicher.diskriminierungsform_codiert):
            self.auswerten(self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsform,
                           self.datenspeicher.codierung_dict_export_diskriminierungsform,
                           self.datenspeicher.genannt_diskriminierungsform,
                           self.datenspeicher.trennzeichen_liste_diskriminierungsform,
                           self.datenspeicher.genannt_markierung_leer_diskriminierungsform,
                           self.datenspeicher.genannt_markierung_zeichen_diskriminierungsform,
                           self.datenspeicher.genannt_markierung_zeichen_text_diskriminierungsform,
                           self.datenspeicher.genannt_markierung_nichtzeichen_diskriminierungsform,
                           self.datenspeicher.genannt_markierung_nichtzeichen_text_diskriminierungsform)
        if (self.datenspeicher.agg_relevanz_codiert):
            self.auswerten(self.datenspeicher.dict_code_checkboxes_auswahl_agg_relevanz,
                           self.datenspeicher.codierung_dict_export_agg_relevanz,
                           self.datenspeicher.genannt_agg_relevanz, self.datenspeicher.trennzeichen_liste_agg_relevanz,
                           self.datenspeicher.genannt_markierung_leer_agg_relevanz,
                           self.datenspeicher.genannt_markierung_zeichen_agg_relevanz,
                           self.datenspeicher.genannt_markierung_zeichen_text_agg_relevanz,
                           self.datenspeicher.genannt_markierung_nichtzeichen_agg_relevanz,
                           self.datenspeicher.genannt_markierung_nichtzeichen_text_agg_relevanz)

        self.speichern()
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Danke")
        msgbox.setText(
            "Die Auswertung ist nun abgeschlossen.\nBitte speichern Sie nun die Vorlage.\nDanach können Sie das Programm beenden.\n\nIhre nächsten Schritte sind:\n"
            "(1) Senden Sie uns die zip.Datei \"An IDZ senden\" per Email zu.\n(2) Beantworten Sie bitte die Fragen in der Online-Befragen.\n\n"
            "Vielen Dank für Ihre Zeit und Mitarbeit.\n"
            "Das Studien-Team des IDZ.")
        msgbox.setStandardButtons(QMessageBox.Ok)

        msgbox.exec_()

    def auswerten(self, dict_code_checkboxes_auswahl, codierung_dict_export, genannt, trennzeichen_liste,
                  genannt_markierung_leer, genannt_markierung_zeichen, genannt_markierung_zeichen_text,
                  genannt_markierung_nichtzeichen, genannt_markierung_nichtzeichen_text):
        # fasse alle vorgabe dict zu einem zusammen
        self.datenspeicher.dict_code_checkboxes_auswahl_gesamt = {
            **self.datenspeicher.dict_code_checkboxes_auswahl_agg_relevanz,
            **self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsform,
            **self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsmerkmale,
            **self.datenspeicher.dict_code_checkboxes_auswahl_interventionsformen,
            **self.datenspeicher.dict_code_checkboxes_auswahl_lebensbereich}

        self.datenspeicher.codierung_dict_export_gesamt = {
            **self.datenspeicher.codierung_dict_export_agg_relevanz,
            **self.datenspeicher.codierung_dict_export_diskriminierungsform,
            **self.datenspeicher.codierung_dict_export_diskriminierungsmerkmale,
            **self.datenspeicher.codierung_dict_export_interventionsformen,
            **self.datenspeicher.codierung_dict_export_lebensbereich}

        for schlüssel, werte_liste in dict_code_checkboxes_auswahl.items():  # alle Kategorien, die ausgewählt wurden, werden dem df zugefügt
            self.neuer_spaltenname = f"XXX_XXX_{schlüssel}"
            self.datenspeicher.df[self.neuer_spaltenname] = np.nan
            for idx, value in enumerate(werte_liste):
                self.neuer_spaltenname = f"XXX_XXX_{value}"
                self.datenspeicher.df[self.neuer_spaltenname] = np.nan

        if genannt:
            for schlüssel, value_list in codierung_dict_export.items():
                value_list = list(itertools.chain.from_iterable(value_list))
                for value in value_list:
                    if genannt_markierung_leer == False:
                        self.datenspeicher.df.loc[self.datenspeicher.df[schlüssel].notna(), "XXX_XXX_" + value] = 1
                    if genannt_markierung_zeichen == True:
                        self.datenspeicher.df.loc[
                            self.datenspeicher.df[
                                schlüssel] == genannt_markierung_zeichen_text, "XXX_XXX_" + value] = 1
                    if genannt_markierung_nichtzeichen == True:
                        self.datenspeicher.df.loc[
                            self.datenspeicher.df[
                                schlüssel] != genannt_markierung_nichtzeichen_text, "XXX_XXX_" + value] = 1
        else:
            # Liste für Gesamtheit aller Schlüssel und Werte erstellen
            for schlüssel, value in codierung_dict_export.items():
                self.gesamtliste_aller_codes.append(schlüssel[0])

            self.gesamtliste_aller_codes = list(set(self.gesamtliste_aller_codes))

            # Umwandlung der Originalspalteninhalte in eine Liste
            for spalte in self.gesamtliste_aller_codes:
                self.datenspeicher.df['XXX_YYY_' + spalte] = ""
                for index, row in self.datenspeicher.df.iterrows():
                    self.element = row[spalte]
                    self.element = [self.element]
                    self.spalteninhalt_als_liste = []

                    if trennzeichen_liste == ["", "", ""]:
                        for self.element2 in self.element:
                            self.element3 = str(self.element2)
                            self.getrennte_code_elemente = [self.element3]
                            self.spalteninhalt_als_liste.extend(self.getrennte_code_elemente)
                        self.datenspeicher.df.at[index, 'XXX_YYY_' + spalte] = self.spalteninhalt_als_liste
                    else:
                        for self.element2 in self.element:
                            self.element3 = str(self.element2)
                            for trennzeichen in trennzeichen_liste:
                                if trennzeichen != "":
                                    self.getrennte_code_elemente = self.element3.split(trennzeichen)
                                    self.spalteninhalt_als_liste.extend(self.getrennte_code_elemente)
                            self.datenspeicher.df.at[index, 'XXX_YYY_' + spalte] = self.spalteninhalt_als_liste

            for spalte in self.gesamtliste_aller_codes:
                for index, row in self.datenspeicher.df.iterrows():
                    if not isinstance(self.datenspeicher.df.at[index, 'XXX_YYY_' + spalte], list):
                        self.datenspeicher.df.at[index, 'XXX_YYY_' + spalte] = [
                            self.datenspeicher.df.at[index, 'XXX_YYY_' + spalte]]
            # Übersetzung vonehmen und als 1 markieren, wenn genannt
            for spalte in self.gesamtliste_aller_codes:
                print("neuertestversuch: a")
                for index, row in self.datenspeicher.df.iterrows():
                    liste = self.datenspeicher.df.at[index, 'XXX_YYY_' + spalte]
                    if isinstance(liste, list):
                        for schlüssel, value in codierung_dict_export.items():
                            if schlüssel[0] == spalte:
                                for element8 in liste:
                                    element8 = str(element8)
                                    if schlüssel[1] == element8:
                                        einfache_liste = [elementx1 for liste in value for elementx1 in liste]
                                        for element9 in einfache_liste:
                                            self.datenspeicher.df.at[index, 'XXX_XXX_' + str(element9)] = 1
                                            print(self.datenspeicher.df['XXX_XXX_' + str(element9)])
            # Nullsetzen von Werten, wenn ein Wert aus dem Key genannt
            for schlüssel, werte_liste in dict_code_checkboxes_auswahl.items():
                for value2 in werte_liste:
                    for value in werte_liste:
                        self.datenspeicher.df.loc[(self.datenspeicher.df["XXX_XXX_" + value2] == 1) & (
                            self.datenspeicher.df["XXX_XXX_" + value].isnull()), "XXX_XXX_" + value] = 0
            # Nullsetzen von Keys, wenn ein Key genannt
            for schlüssel, werte_liste in dict_code_checkboxes_auswahl.items():
                for schlüssel2, werte_liste2 in dict_code_checkboxes_auswahl.items():
                    self.datenspeicher.df.loc[(self.datenspeicher.df["XXX_XXX_" + schlüssel] == 1) & (
                        self.datenspeicher.df["XXX_XXX_" + schlüssel2].isnull()), "XXX_XXX_" + schlüssel2] = 0
            # Auf 97-setzen, wenn Key genannt aber kein Wert ausgewählt
            for schlüssel, werte_liste in dict_code_checkboxes_auswahl.items():
                for value in werte_liste:
                    for value2 in werte_liste:
                        self.datenspeicher.df.loc[(self.datenspeicher.df["XXX_XXX_" + schlüssel] == 1) & (
                            self.datenspeicher.df["XXX_XXX_" + value].isnull()), "XXX_XXX_" + value2] = 97

    def werte_füllen(self, datenspeicher):
        if self.datenspeicher.pfad_datenausgabe != "":
            self.textfeld_datenausgabe.setText(datenspeicher.pfad_datenausgabe)
        if self.tmp_pfad_datenausgabe != "":
            self.textfeld_datenausgabe.setText(self.tmp_pfad_datenausgabe)
        self.haeufigkeit_null = 0  # kurzzeitiger Speicher für die Häufigkeit des Vorkommens von genannt
        self.haeufigkeit_eins = 0  # kurzzeitiger Speicher für die Häufigkeit des Vorkommens von nicht genannt
        self.haeufigkeit_keineAngabe = 0  # kurzzeitiger Speicher für die Häufigkeit des Vorkommens von fehlender Angabe (Key ist genannt aber keine Angabe zum Wert)
        self.haeufigkeit_tnz = 0  # kurzzeitiger Speicher für die Häufigkeit des Vorkommens von genannt
        self.df_ergebnis = {}  # Dataframe für Ergebnis einer Auswertung
        self.tmp_df = {}
        self.columns = []  # Für den Ergebnis Dataframe anzulegende Spalten

    def datei_auswahl_einfach(self):
        widget = QWidget()  # Erstellen Sie ein gültiges Widget-Objekt
        self.tmp_pfad_datenausgabe = QFileDialog.getExistingDirectory(widget, "Ordner auswählen")
        self.werte_füllen(self.datenspeicher)
        self.button_speichern.setEnabled(True)

    def speichern(self):
        self.datenspeicher.pfad_datenausgabe = self.tmp_pfad_datenausgabe
        self.zip_neu_erstellen = True
        self.zip_datei_name = "An IDZ senden.zip"

        self.ordner_pfad = self.datenspeicher.pfad_datenausgabe + "/" + "02 Daten für die Erhebung"
        if not os.path.exists(self.ordner_pfad):
            os.makedirs(self.ordner_pfad)
        self.ordner_pfad = self.datenspeicher.pfad_datenausgabe + "/" + "01 Informationen für die Beratungsstelle"
        if not os.path.exists(self.ordner_pfad):
            os.makedirs(self.ordner_pfad)

        self.gesamtzahl_grafiken = 0
        self.aktuelle_grafiken = 0
        if self.datenspeicher.lebensbereich_codiert == True:
            self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 2
            self.dict_code_checkboxes = self.datenspeicher.dict_code_checkboxes_auswahl_lebensbereich
            for bereich, values in self.dict_code_checkboxes.items():
                if values:
                    self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.diskriminierungsmerkmale_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.interventionsformen_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.diskriminierungsform_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.agg_relevanz_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1

        if self.datenspeicher.diskriminierungsmerkmale_codiert == True:
            self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 2
            self.dict_code_checkboxes = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsmerkmale
            for bereich, values in self.dict_code_checkboxes.items():
                if values:
                    self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.lebensbereich_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.interventionsformen_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.diskriminierungsform_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.agg_relevanz_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1

        if self.datenspeicher.interventionsformen_codiert == True:
            self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 2
            self.dict_code_checkboxes = self.datenspeicher.dict_code_checkboxes_auswahl_interventionsformen
            for bereich, values in self.dict_code_checkboxes.items():
                if values:
                    self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.lebensbereich_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.diskriminierungsmerkmale_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.diskriminierungsform_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.agg_relevanz_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1

        if self.datenspeicher.diskriminierungsform_codiert == True:
            self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 2
            self.dict_code_checkboxes = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsform
            for bereich, values in self.dict_code_checkboxes.items():
                if values:
                    self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.lebensbereich_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.interventionsformen_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.diskriminierungsmerkmale_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.agg_relevanz_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1

        if self.datenspeicher.agg_relevanz_codiert == True:
            self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 2
            self.dict_code_checkboxes = self.datenspeicher.dict_code_checkboxes_auswahl_agg_relevanz
            for bereich, values in self.dict_code_checkboxes.items():
                if values:
                    self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.lebensbereich_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.interventionsformen_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.diskriminierungsform_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1
            if self.datenspeicher.diskriminierungsmerkmale_codiert == True:
                self.gesamtzahl_grafiken = self.gesamtzahl_grafiken + 1

        if self.datenspeicher.lebensbereich_codiert == True:
            self.dict_code_checkboxes = self.datenspeicher.dict_code_checkboxes_auswahl_lebensbereich
            self.tmp_vorsilbe = 'Lebensbereiche'
            self.grafiktitel = 'Lebensbereiche'
            self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
            self.untertitel = 'Beratungsfälle nach Lebensbereichen, 2022'
            self.tabelle_univariat()
            self.ausgangsliste = list(self.dict_code_checkboxes.keys())
            self.df_ergebnis2 = copy.deepcopy(self.df_ergebnis)
            self.daten, self.daten_labels, self.fallzahl = data_vorbereiten.data_erstellen(self.df_ergebnis2, "dummies",
                                                                                           "absolut",
                                                                                           ausgangsliste=self.ausgangsliste)
            self.graph_univariat(daten=self.daten, daten_labels=self.daten_labels, fallzahl=self.fallzahl,
                                 dateiname=self.dateiname, datentyp="dummies", abs_rel="relativ", reihenfolge="",
                                 titel=self.grafiktitel, untertitel=self.untertitel, kreuzung=False)
            self.fortschrittbalken_grafiken()
            for bereich, values in self.dict_code_checkboxes.items():
                if values:
                    self.ausgangsliste = values
                    self.df_ergebnis2 = copy.deepcopy(self.df_ergebnis)
                    self.dateiname = self.saubere_dateinamen_string(bereich)
                    self.daten, self.daten_labels, self.fallzahl = data_vorbereiten.data_erstellen(self.df_ergebnis2,
                                                                                                   "dummies", "absolut",
                                                                                                   ausgangsliste=self.ausgangsliste)
                    self.graph_univariat(daten=self.daten, daten_labels=self.daten_labels, fallzahl=self.fallzahl,
                                         dateiname="Lebensbereich " + self.dateiname, datentyp="dummies",
                                         abs_rel="relativ", reihenfolge="", titel="Lebensbereich: " + bereich,
                                         untertitel="Beratungsfälle nach Lebensbereich, 2022", kreuzung=False)
                    self.fortschrittbalken_grafiken()

            self.dict_code_checkboxes_zeilen = self.dict_code_checkboxes
            self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
            self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                          self.dict_code_checkboxes_spalten)
            self.grafiktitel = "Mehrfachnennung von Lebensbereichen"
            self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
            self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                   dateiname=self.dateiname)
            self.fortschrittbalken_grafiken()
            if self.datenspeicher.diskriminierungsmerkmale_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsmerkmale
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Lebensbereiche nach Diskriminierungsmerkmalen"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.interventionsformen_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_interventionsformen
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Lebensbereiche nach Interventionsformen"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.diskriminierungsform_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsform
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Lebensbereiche nach Diskriminierungsform"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.agg_relevanz_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_agg_relevanz
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Lebensbereiche nach AGG-Relevanz"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()

        if self.datenspeicher.diskriminierungsmerkmale_codiert == True:
            self.dict_code_checkboxes = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsmerkmale
            self.tmp_vorsilbe = 'Diskriminierungsmerkmale'
            self.grafiktitel = 'Diskriminierungsmerkmale'
            self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
            self.untertitel = 'Beratungsfälle nach Diskriminierungsmerkmalen, 2022'
            self.tabelle_univariat()
            self.ausgangsliste = list(self.dict_code_checkboxes.keys())
            self.df_ergebnis2 = copy.deepcopy(self.df_ergebnis)
            display("fehler3", self.df_ergebnis)
            display("fehler2", self.df_ergebnis2)
            self.daten, self.daten_labels, self.fallzahl = data_vorbereiten.data_erstellen(self.df_ergebnis2, "dummies",
                                                                                           "absolut",
                                                                                           ausgangsliste=self.ausgangsliste)
            self.graph_univariat(daten=self.daten, daten_labels=self.daten_labels, fallzahl=self.fallzahl,
                                 dateiname=self.dateiname, datentyp="dummies", abs_rel="relativ", reihenfolge="",
                                 titel=self.grafiktitel, untertitel=self.untertitel, kreuzung=False)
            self.fortschrittbalken_grafiken()
            for bereich, values in self.dict_code_checkboxes.items():
                if values:
                    self.ausgangsliste = values
                    self.df_ergebnis2 = copy.deepcopy(self.df_ergebnis)
                    self.dateiname = self.saubere_dateinamen_string(bereich)
                    self.daten, self.daten_labels, self.fallzahl = data_vorbereiten.data_erstellen(self.df_ergebnis2,
                                                                                                   "dummies", "absolut",
                                                                                                   ausgangsliste=self.ausgangsliste)
                    self.graph_univariat(daten=self.daten, daten_labels=self.daten_labels, fallzahl=self.fallzahl,
                                         dateiname="Diskriminierungsmerkmale " + self.dateiname, datentyp="dummies",
                                         abs_rel="relativ", reihenfolge="", titel="Diskriminierungsmerkmal: " + bereich,
                                         untertitel="Beratungsfälle nach Diskriminierungsmerkmalen, 2022",
                                         kreuzung=False)
                    self.fortschrittbalken_grafiken()

            self.dict_code_checkboxes_zeilen = self.dict_code_checkboxes
            self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
            self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                          self.dict_code_checkboxes_spalten)
            self.grafiktitel = "Mehrfachnennung von Diskriminierungsmerkmalen"
            self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
            self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                   dateiname=self.dateiname)
            self.fortschrittbalken_grafiken()
            if self.datenspeicher.lebensbereich_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_lebensbereich
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Diskriminierungsmerkmale nach Lebensbereichen"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.interventionsformen_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_interventionsformen
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Diskriminierungsmerkmale nach Interventionsformen"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.diskriminierungsform_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsform
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Diskriminierungsmerkmale nach Diskriminierungsform"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.agg_relevanz_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_agg_relevanz
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Diskriminierungsmerkmale nach AGG-Relevanz"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()

        if self.datenspeicher.interventionsformen_codiert == True:
            self.dict_code_checkboxes = self.datenspeicher.dict_code_checkboxes_auswahl_interventionsformen
            self.tmp_vorsilbe = 'Interventionsformen'
            self.grafiktitel = 'Interventionsformen'
            self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
            self.untertitel = 'Beratungsfälle nach Interventionsformen, 2022'
            self.tabelle_univariat()
            self.ausgangsliste = list(self.dict_code_checkboxes.keys())
            self.df_ergebnis2 = copy.deepcopy(self.df_ergebnis)
            self.daten, self.daten_labels, self.fallzahl = data_vorbereiten.data_erstellen(self.df_ergebnis2, "dummies",
                                                                                           "absolut",
                                                                                           ausgangsliste=self.ausgangsliste)
            self.graph_univariat(daten=self.daten, daten_labels=self.daten_labels, fallzahl=self.fallzahl,
                                 dateiname=self.dateiname, datentyp="dummies", abs_rel="relativ", reihenfolge="",
                                 titel=self.grafiktitel, untertitel=self.untertitel, kreuzung=False)
            self.fortschrittbalken_grafiken()
            for bereich, values in self.dict_code_checkboxes.items():
                if values:
                    self.ausgangsliste = values
                    self.df_ergebnis2 = copy.deepcopy(self.df_ergebnis)
                    self.dateiname = self.saubere_dateinamen_string(bereich)
                    self.daten, self.daten_labels, self.fallzahl = data_vorbereiten.data_erstellen(self.df_ergebnis2,
                                                                                                   "dummies", "absolut",
                                                                                                   ausgangsliste=self.ausgangsliste)
                    self.graph_univariat(daten=self.daten, daten_labels=self.daten_labels, fallzahl=self.fallzahl,
                                         dateiname="Interventionsformen " + self.dateiname, datentyp="dummies",
                                         abs_rel="relativ", reihenfolge="", titel="Interventionsform: " + bereich,
                                         untertitel="Beratungsfälle nach Interventionsformen, 2022", kreuzung=False)
                    self.fortschrittbalken_grafiken()

            self.dict_code_checkboxes_zeilen = self.dict_code_checkboxes
            self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
            self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                          self.dict_code_checkboxes_spalten)
            self.grafiktitel = "Mehrfachnennung von Interventionsformen"
            self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
            self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                   dateiname=self.dateiname)
            self.fortschrittbalken_grafiken()
            if self.datenspeicher.lebensbereich_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_lebensbereich
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Interventionsformen nach Lebensbereichen"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.diskriminierungsmerkmale_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsmerkmale
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Interventionsformen nach Diskriminierungsmerkmalen"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.diskriminierungsform_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsform
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Interventionsformen nach Diskriminierungsform"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.agg_relevanz_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_agg_relevanz
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Interventionsformen nach AGG-Relevanz"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()

        if self.datenspeicher.diskriminierungsform_codiert == True:
            self.dict_code_checkboxes = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsform
            self.tmp_vorsilbe = 'Diskriminierungsform'
            self.grafiktitel = 'Diskriminierungsform'
            self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
            self.untertitel = 'Beratungsfälle nach Diskriminierungsform, 2022'
            self.tabelle_univariat()
            self.ausgangsliste = list(self.dict_code_checkboxes.keys())
            self.df_ergebnis2 = copy.deepcopy(self.df_ergebnis)
            self.daten, self.daten_labels, self.fallzahl = data_vorbereiten.data_erstellen(self.df_ergebnis2, "dummies",
                                                                                           "absolut",
                                                                                           ausgangsliste=self.ausgangsliste)
            self.graph_univariat(daten=self.daten, daten_labels=self.daten_labels, fallzahl=self.fallzahl,
                                 dateiname=self.dateiname, datentyp="dummies", abs_rel="relativ", reihenfolge="",
                                 titel=self.grafiktitel, untertitel=self.untertitel, kreuzung=False)
            self.fortschrittbalken_grafiken()
            for bereich, values in self.dict_code_checkboxes.items():
                if values:
                    self.ausgangsliste = values
                    self.df_ergebnis2 = copy.deepcopy(self.df_ergebnis)
                    self.dateiname = self.saubere_dateinamen_string(bereich)
                    self.daten, self.daten_labels, self.fallzahl = data_vorbereiten.data_erstellen(self.df_ergebnis2,
                                                                                                   "dummies", "absolut",
                                                                                                   ausgangsliste=self.ausgangsliste)
                    self.graph_univariat(daten=self.daten, daten_labels=self.daten_labels, fallzahl=self.fallzahl,
                                         dateiname="Diskriminierungsform " + self.dateiname, datentyp="dummies",
                                         abs_rel="relativ", reihenfolge="", titel="Diskriminierungsform: " + bereich,
                                         untertitel="Beratungsfälle nach Diskriminierungsform, 2022", kreuzung=False)
                    self.fortschrittbalken_grafiken()

            self.dict_code_checkboxes_zeilen = self.dict_code_checkboxes
            self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
            self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                          self.dict_code_checkboxes_spalten)
            self.grafiktitel = "Mehrfachnennung von Diskriminierungsformen"
            self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
            self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                   dateiname=self.dateiname)
            self.fortschrittbalken_grafiken()
            if self.datenspeicher.lebensbereich_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_lebensbereich
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Diskriminierungsformen nach Lebensbereichen"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.interventionsformen_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_interventionsformen
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Diskriminierungsformen nach Interventionsformen"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.diskriminierungsmerkmale_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsmerkmale
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Diskriminierungsformen nach Diskriminierungsmerkmal"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.agg_relevanz_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_agg_relevanz
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "Diskriminierungsformen nach AGG-Relevanz"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()

        if self.datenspeicher.agg_relevanz_codiert == True:
            self.dict_code_checkboxes = self.datenspeicher.dict_code_checkboxes_auswahl_agg_relevanz
            self.tmp_vorsilbe = 'AGG-Relevanz'
            self.grafiktitel = 'AGG-Relevanz'
            self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
            self.untertitel = 'Beratungsfälle nach AGG-Relevanz, 2022'
            self.tabelle_univariat()
            self.ausgangsliste = list(self.dict_code_checkboxes.keys())
            self.df_ergebnis2 = copy.deepcopy(self.df_ergebnis)
            self.daten, self.daten_labels, self.fallzahl = data_vorbereiten.data_erstellen(self.df_ergebnis2, "dummies",
                                                                                           "absolut",
                                                                                           ausgangsliste=self.ausgangsliste)
            self.graph_univariat(daten=self.daten, daten_labels=self.daten_labels, fallzahl=self.fallzahl,
                                 dateiname=self.dateiname, datentyp="dummies", abs_rel="relativ", reihenfolge="",
                                 titel=self.grafiktitel, untertitel=self.untertitel, kreuzung=False)
            self.fortschrittbalken_grafiken()
            for bereich, values in self.dict_code_checkboxes.items():
                if values:
                    self.ausgangsliste = values
                    self.df_ergebnis2 = copy.deepcopy(self.df_ergebnis)
                    self.dateiname = self.saubere_dateinamen_string(bereich)
                    self.daten, self.daten_labels, self.fallzahl = data_vorbereiten.data_erstellen(self.df_ergebnis2,
                                                                                                   "dummies", "absolut",
                                                                                                   ausgangsliste=self.ausgangsliste)
                    self.graph_univariat(daten=self.daten, daten_labels=self.daten_labels, fallzahl=self.fallzahl,
                                         dateiname="AGG Relevanz " + self.dateiname, datentyp="dummies",
                                         abs_rel="relativ", reihenfolge="", titel="AGG-Relevanz: " + bereich,
                                         untertitel="Beratungsfälle nach AGG-Relevanz, 2022", kreuzung=False)
                    self.fortschrittbalken_grafiken()

            self.dict_code_checkboxes_zeilen = self.dict_code_checkboxes
            self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
            self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                          self.dict_code_checkboxes_spalten)
            self.grafiktitel = "Mehrfachnennung nach AGG-Relevanz"
            self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
            self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                   dateiname=self.dateiname)
            self.fortschrittbalken_grafiken()
            if self.datenspeicher.lebensbereich_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_lebensbereich
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "AGG-Relevanz nach Lebensbereichen"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.interventionsformen_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_interventionsformen
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "AGG-Relevanz nach Interventionsformen"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.diskriminierungsform_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsform
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "AGG-Relevanz nach Diskriminierungsform"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
            if self.datenspeicher.diskriminierungsmerkmale_codiert == True:
                self.dict_code_checkboxes_zeilen = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsmerkmale
                self.dict_code_checkboxes_spalten = self.dict_code_checkboxes
                self.kreuztabelle = self.dummies_kreuztabelle(self.dict_code_checkboxes_zeilen,
                                                              self.dict_code_checkboxes_spalten)
                self.grafiktitel = "AGG-Relevanz nach Diskriminierungsmerkmalen"
                self.dateiname = self.saubere_dateinamen_string(self.grafiktitel)
                self.heatmap_erstellen(kreuztabelle=self.kreuztabelle, grafiktitel=self.grafiktitel,
                                       dateiname=self.dateiname)
                self.fortschrittbalken_grafiken()
        self.close()

    def fortschrittbalken_grafiken(self):
        self.aktuelle_grafiken = self.aktuelle_grafiken + 1
        self.fortschritt_grafiken = self.aktuelle_grafiken * 100 / self.gesamtzahl_grafiken
        # @Felix: Hier den Code für die Anpassung des Fortschrittbalkens einfügen

    def heatmap_erstellen(self, kreuztabelle, grafiktitel, dateiname):
        kreuztabelle2 = grafik_erstell.testdata_heatmap_erstellen(kreuztabelle)
        display("kreuztabelle2", kreuztabelle2)
        index_liste = kreuztabelle2.index.tolist()
        index_liste, mehrzeilige_labels, laengstes_zeilelaenge = grafik_erstell.label_trennen(index_liste,
                                                                                              zeilenlänge=22)
        kreuztabelle2.index = index_liste
        spalten_liste = kreuztabelle2.columns.tolist()
        spalten_liste = grafik_erstell.label_trennen(spalten_liste, zeilenlänge=22)[0]
        kreuztabelle2.columns = spalten_liste
        plt.figure(figsize=(12, 8))
        heatmap = sns.heatmap(kreuztabelle2, vmin=0, vmax=100, annot=True, fmt='.0f', cmap='YlOrBr')
        heatmap.set_title(grafiktitel, fontdict={'fontsize': 12}, pad=12);
        heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=45, ha='right')
        plt.savefig(
            self.datenspeicher.pfad_datenausgabe + "/" + "01 Informationen für die Beratungsstelle" + "/" + dateiname + '.png',
            bbox_inches='tight', dpi=300)

    def graph_univariat(self, daten, daten_labels, fallzahl, dateiname, datentyp="dummies", abs_rel="absolut",
                        reihenfolge="absteigend", titel="Titel", untertitel="Untertitel", kreuzung=False):
        graph_breite = 12

        df = pd.DataFrame()
        print('1')
        legende_vorhanden, label_yachse_vorhanden = grafik_erstell.elemente_festlegen(daten, datentyp, daten_labels)
        print('2')
        elemente_übereinander, elementezahl, reihenfolge_oben, reihenfolge_graph, reihenfolge_graph_yachse, reihenfolge_legende, reihenfolge_unten, reihenfolge_oben_vert, reihenfolge_graph_vert, reihenfolge_graph_yachse_vert, reihenfolge_graph_vert, reihenfolge_legende_vert, reihenfolge_unten_vert = grafik_erstell.reihenfolge_festlegen(
            label_yachse_vorhanden, legende_vorhanden)
        print('3')
        daten_labels = grafik_erstell.label_korrektur(daten_labels)
        print('4')
        daten_labels, y_mehrzeilige_labels, y_label_laengstes_zeilelaenge = grafik_erstell.label_trennen(daten_labels)
        print('5')
        key_labels = list(daten.keys())
        print('6')
        key_labels = grafik_erstell.label_korrektur(key_labels)
        print('7')
        key_labels, x_mehrzeilige_labels, x_label_laengstes_zeilelaenge = grafik_erstell.label_trennen(key_labels)
        print('8')
        daten = dict(zip(key_labels, daten.values()))
        print('9')
        if legende_vorhanden == True:
            legende_labels, n_legende_spalten, n_legende_labels_pro_spalte = grafik_erstell.legende_vorbereiten(
                graph_breite, daten, datentyp, x_label_laengstes_zeilelaenge)
            höhe_legende = .1 + .3 * n_legende_labels_pro_spalte
        print('10')
        höhe_oben = 1.4
        höhe_graph = grafik_erstell.graph_höhe_bestimmen(daten_labels, y_mehrzeilige_labels)
        print('11')

        höhe_unten = 0.8

        if legende_vorhanden == True:
            height_ratios = [höhe_oben, höhe_graph, höhe_legende, höhe_unten]
        print('12')
        if legende_vorhanden == False:
            height_ratios = [höhe_oben, höhe_graph, höhe_unten]
        print('13')

        fig, axes = plt.subplots(elementezahl, 1, figsize=(graph_breite, sum(height_ratios)), sharex=True)
        print('14')

        gs = gridspec.GridSpec(elemente_übereinander, 2, height_ratios=height_ratios, width_ratios=[0.01, 11.99],
                               wspace=0.0, hspace=0.0)
        print('15')

        if reihenfolge_oben > 0:
            axes[reihenfolge_oben - 1] = plt.subplot(gs[reihenfolge_oben_vert - 1, :])
        if reihenfolge_graph > 0:
            if label_yachse_vorhanden == False:
                axes[reihenfolge_graph - 1] = plt.subplot(gs[reihenfolge_graph_vert - 1, :])
            if label_yachse_vorhanden == True:
                axes[reihenfolge_graph_yachse - 1] = plt.subplot(gs[reihenfolge_graph_vert - 1, 0])
                axes[reihenfolge_graph_yachse - 1].axis('off')
                axes[reihenfolge_graph - 1] = plt.subplot(gs[reihenfolge_graph_yachse_vert - 1, 1])
        if reihenfolge_legende > 0:
            axes[reihenfolge_legende - 1] = plt.subplot(gs[reihenfolge_legende_vert - 1, :])
        if reihenfolge_unten > 0:
            axes[reihenfolge_unten - 1] = plt.subplot(gs[reihenfolge_unten_vert - 1, :])
        if reihenfolge_graph > 0:
            fig, axes[reihenfolge_graph - 1] = grafik_erstell.graph_einfügen(fig, axes[reihenfolge_graph - 1], daten,
                                                                             daten_labels, datentyp, abs_rel,
                                                                             label_yachse_vorhanden,
                                                                             x_mehrzeilige_labels,
                                                                             x_label_laengstes_zeilelaenge,
                                                                             y_mehrzeilige_labels,
                                                                             y_label_laengstes_zeilelaenge, kreuzung)
        if reihenfolge_oben > 0:
            fig, axes[reihenfolge_oben - 1] = grafik_erstell.deko_oben_einfügen(fig, axes[reihenfolge_oben - 1])
            fig, axes[reihenfolge_oben - 1] = grafik_erstell.titel_einfügen(fig, axes[reihenfolge_oben - 1], titel)
            fig, axes[reihenfolge_oben - 1] = grafik_erstell.untertitel_einfügen(fig, axes[reihenfolge_oben - 1],
                                                                                 untertitel)
        if reihenfolge_legende > 0:
            fig, axes[reihenfolge_legende - 1] = grafik_erstell.legende_einfügen(fig, axes[reihenfolge_legende - 1],
                                                                                 datentyp, daten, x_mehrzeilige_labels,
                                                                                 legende_labels, n_legende_spalten)
        if reihenfolge_unten > 0:
            fig, axes[reihenfolge_unten - 1] = grafik_erstell.caption_einfügen(fig, axes[reihenfolge_unten - 1],
                                                                               fallzahl, datentyp, kreuzung=kreuzung)
            fig, axes[reihenfolge_unten - 1] = grafik_erstell.deko_unten_einfügen(fig, axes[reihenfolge_unten - 1])
        fig = gs.tight_layout(fig, h_pad=0)
        print('20')

        plt.savefig(
            self.datenspeicher.pfad_datenausgabe + "/" + "01 Informationen für die Beratungsstelle" + "/" + dateiname + '.png',
            bbox_inches='tight', dpi=300)
        print('21')

        return dateiname

    def saubere_dateinamen_string(self, ungesaeuberter_string):
        # Erlaubte Zeichen in Dateinamen (Angepasst an das Betriebssystem)
        erlaubte_zeichen = "abcdefghijklmnopqrstuvwxyzöäüABCDEFGHIJKLMNOPQRSTUVWXYZÖÄÜ0123456789_-"

        # Ersetze alle Zeichen, die nicht in der erlaubten Zeichenliste sind, durch Leerzeichen
        gesaeuberter_string = re.sub(f"[^{erlaubte_zeichen}]", " ", ungesaeuberter_string)

        # Entferne doppelte Leerzeichen und führende/trailing Leerzeichen
        gesaeuberter_string = " ".join(gesaeuberter_string.split())

        return gesaeuberter_string

    def tabelle_univariat(self):
        self.columns = ['Wert', 'genannt', 'nicht genannt', 'keine Angabe', 'trifft nicht zu']
        self.df_ergebnis = pd.DataFrame(columns=self.columns)
        display("df in Datenspeicher", self.datenspeicher.df)
        display("self.dict_code_checkboxes", self.dict_code_checkboxes)
        for schlüssel, werte_liste in self.dict_code_checkboxes.items():
            self.haeufigkeit_null = self.datenspeicher.df["XXX_XXX_" + schlüssel].eq(0).sum()
            self.haeufigkeit_eins = self.datenspeicher.df["XXX_XXX_" + schlüssel].eq(1).sum()
            self.haeufigkeit_keineAngabe = self.datenspeicher.df["XXX_XXX_" + schlüssel].eq(97).sum()
            self.haeufigkeit_tnz = self.datenspeicher.df["XXX_XXX_" + schlüssel].isna().sum()
            self.tmp_df = pd.DataFrame({'Wert': [schlüssel],
                                        'genannt': [self.haeufigkeit_eins],
                                        'nicht genannt': [self.haeufigkeit_null],
                                        'keine Angabe': [self.haeufigkeit_keineAngabe],
                                        'trifft nicht zu': [self.haeufigkeit_tnz]})
            self.df_ergebnis = pd.concat([self.df_ergebnis, self.tmp_df], ignore_index=True)

            for value in werte_liste:
                self.haeufigkeit_null = self.datenspeicher.df["XXX_XXX_" + value].eq(0).sum()
                self.haeufigkeit_eins = self.datenspeicher.df["XXX_XXX_" + value].eq(1).sum()
                self.haeufigkeit_keineAngabe = self.datenspeicher.df["XXX_XXX_" + value].eq(97).sum()
                self.haeufigkeit_tnz = self.datenspeicher.df["XXX_XXX_" + value].isna().sum()
                self.tmp_df = pd.DataFrame({'Wert': [value],
                                            'genannt': [self.haeufigkeit_eins],
                                            'nicht genannt': [self.haeufigkeit_null],
                                            'keine Angabe': [self.haeufigkeit_keineAngabe],
                                            'trifft nicht zu': [self.haeufigkeit_tnz]})
                self.df_ergebnis = pd.concat([self.df_ergebnis, self.tmp_df], ignore_index=True)
        self.ausgabepfad = ""
        self.ausgabepfad = self.datenspeicher.pfad_datenausgabe + "/" + "02 Daten für die Erhebung" + "/" + self.grafiktitel + "_häufigkeit.xlsx"
        self.df_ergebnis.to_excel(self.ausgabepfad, index=True)
        self.zip_speicherpfad = self.datenspeicher.pfad_datenausgabe + "/" + self.zip_datei_name
        if self.zip_neu_erstellen == True:
            # Erstelle eine leere ZIP-Datei
            with zipfile.ZipFile(self.zip_speicherpfad, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Füge die Datei zur ZIP-Datei hinzu
                self.datei_zum_hinzufuegen = self.ausgabepfad  # Ersetze dies durch den richtigen Dateipfad
                datei_name_in_zip = self.grafiktitel + "_häufigkeit.xlsx"  # Ersetze dies durch den gewünschten Namen in der ZIP-Datei
                ds = self.template_speichern()
                textual_representation = str(ds.__dict__)

                zipf.write(self.datei_zum_hinzufuegen, datei_name_in_zip)
                zipf.writestr('/data.txt', textual_representation)
        if self.zip_neu_erstellen == False:
            # Öffne die vorhandene ZIP-Datei im Anhangsmodus
            with zipfile.ZipFile(self.zip_speicherpfad, 'a', zipfile.ZIP_DEFLATED) as zipf:
                # Füge die Datei zur ZIP-Datei hinzu
                self.datei_zum_hinzufuegen = self.ausgabepfad  # Ersetze dies durch den richtigen Dateipfad
                datei_name_in_zip = self.grafiktitel + "_häufigkeit.xlsx"  # Ersetze dies durch den gewünschten Namen in der ZIP-Datei
                ds = self.template_speichern()
                textual_representation = str(ds.__dict__)
                zipf.write(self.datei_zum_hinzufuegen, datei_name_in_zip)
                zipf.writestr('/data.txt', textual_representation)

        self.zip_neu_erstellen = False

    def template_speichern(self):

        # create a dummy Datenspeicher which copies the attributes which get read in template_bearbeiten
        temp_speicher_save = Datenspeicher()
        temp_speicher_save.lebensbereich_codiert = self.datenspeicher.lebensbereich_codiert
        temp_speicher_save.spalten_lebensbereich = self.datenspeicher.spalten_lebensbereich
        temp_speicher_save.trennzeichen_liste_lebensbereich = self.datenspeicher.trennzeichen_liste_lebensbereich
        temp_speicher_save.genannt_lebensbereich = self.datenspeicher.genannt_lebensbereich
        temp_speicher_save.dict_code_checkboxes_auswahl_lebensbereich = self.datenspeicher.dict_code_checkboxes_auswahl_lebensbereich
        temp_speicher_save.dict_lebensbereiche_vorgabe = self.datenspeicher.dict_lebensbereiche_vorgabe
        temp_speicher_save.codierung_dict_export_lebensbereich = self.datenspeicher.codierung_dict_export_lebensbereich
        temp_speicher_save.diskriminierungsmerkmale_codiert = self.datenspeicher.diskriminierungsmerkmale_codiert
        temp_speicher_save.spalten_diskriminierungsmerkmale = self.datenspeicher.spalten_diskriminierungsmerkmale
        temp_speicher_save.trennzeichen_liste_diskriminierungsmerkmale = self.datenspeicher.trennzeichen_liste_diskriminierungsmerkmale
        temp_speicher_save.genannt_diskriminierungsmerkmale = self.datenspeicher.genannt_diskriminierungsmerkmale
        temp_speicher_save.dict_code_checkboxes_auswahl_diskriminierungsmerkmale = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsmerkmale
        temp_speicher_save.dict_diskriminierungsmerkmale_vorgabe = self.datenspeicher.dict_diskriminierungsmerkmale_vorgabe
        temp_speicher_save.codierung_dict_export_diskriminierungsmerkmale = self.datenspeicher.codierung_dict_export_diskriminierungsmerkmale
        temp_speicher_save.interventionsformen_codiert = self.datenspeicher.interventionsformen_codiert
        temp_speicher_save.spalten_interventionsformen = self.datenspeicher.spalten_interventionsformen
        temp_speicher_save.trennzeichen_liste_interventionsformen = self.datenspeicher.trennzeichen_liste_interventionsformen
        temp_speicher_save.genannt_interventionsformen = self.datenspeicher.genannt_interventionsformen
        temp_speicher_save.dict_code_checkboxes_auswahl_interventionsformen = self.datenspeicher.dict_code_checkboxes_auswahl_interventionsformen
        temp_speicher_save.dict_interventionsformen_vorgabe = self.datenspeicher.dict_interventionsformen_vorgabe
        temp_speicher_save.codierung_dict_export_interventionsformen = self.datenspeicher.codierung_dict_export_interventionsformen
        temp_speicher_save.diskriminierungsform_codiert = self.datenspeicher.diskriminierungsform_codiert
        temp_speicher_save.spalten_diskriminierungsform = self.datenspeicher.spalten_diskriminierungsform
        temp_speicher_save.trennzeichen_liste_diskriminierungsform = self.datenspeicher.trennzeichen_liste_diskriminierungsform
        temp_speicher_save.genannt_diskriminierungsform = self.datenspeicher.genannt_diskriminierungsform
        temp_speicher_save.dict_code_checkboxes_auswahl_diskriminierungsform = self.datenspeicher.dict_code_checkboxes_auswahl_diskriminierungsform
        temp_speicher_save.dict_diskriminierungsform_vorgabe = self.datenspeicher.dict_diskriminierungsform_vorgabe
        temp_speicher_save.codierung_dict_export_diskriminierungsform = self.datenspeicher.codierung_dict_export_diskriminierungsform
        temp_speicher_save.agg_relevanz_codiert = self.datenspeicher.agg_relevanz_codiert
        temp_speicher_save.spalten_agg_relevanz = self.datenspeicher.spalten_agg_relevanz
        temp_speicher_save.trennzeichen_liste_agg_relevanz = self.datenspeicher.trennzeichen_liste_agg_relevanz
        temp_speicher_save.genannt_agg_relevanz = self.datenspeicher.genannt_agg_relevanz
        temp_speicher_save.dict_code_checkboxes_auswahl_agg_relevanz = self.datenspeicher.dict_code_checkboxes_auswahl_agg_relevanz
        temp_speicher_save.dict_agg_relevanz_vorgabe = self.datenspeicher.dict_agg_relevanz_vorgabe
        temp_speicher_save.codierung_dict_export_agg_relevanz = self.datenspeicher.codierung_dict_export_agg_relevanz
        temp_speicher_save.zeitraum_beginn = self.datenspeicher.zeitraum_beginn
        temp_speicher_save.zeitraum_ende = self.datenspeicher.zeitraum_ende
        temp_speicher_save.zeitraum_inhalt = self.datenspeicher.zeitraum_inhalt
        temp_speicher_save.zeitraum_genau = self.datenspeicher.zeitraum_genau
        temp_speicher_save.zeitraum_irgendwas = self.datenspeicher.zeitraum_irgendwas
        temp_speicher_save.zeitraum_beginn_txt = self.datenspeicher.zeitraum_beginn_txt
        temp_speicher_save.zeitraum_ende_txt = self.datenspeicher.zeitraum_ende_txt
        temp_speicher_save.zeitraum_inhalt_txt = self.datenspeicher.zeitraum_inhalt_txt
        temp_speicher_save.zeitraum_genau_txt = self.datenspeicher.zeitraum_genau_txt
        temp_speicher_save.zeitraum_ausgewaehlt = self.datenspeicher.zeitraum_ausgewaehlt
        temp_speicher_save.spalte_zeitraum = self.datenspeicher.spalte_zeitraum
        temp_speicher_save.codierdict_export = self.datenspeicher.codierdict_export

        # copy all values genannt_markierung_leer_lebensbereich, genannt_markierung_leer_diskriminierungsmerkmale, genannt_markierung_leer_interventionsformen, genannt_markierung_leer_diskriminierungsform, genannt_markierung_leer_agg_relevanz
        temp_speicher_save.genannt_markierung_leer_lebensbereich = self.datenspeicher.genannt_markierung_leer_lebensbereich
        temp_speicher_save.genannt_markierung_leer_diskriminierungsmerkmale = self.datenspeicher.genannt_markierung_leer_diskriminierungsmerkmale
        temp_speicher_save.genannt_markierung_leer_interventionsformen = self.datenspeicher.genannt_markierung_leer_interventionsformen
        temp_speicher_save.genannt_markierung_leer_diskriminierungsform = self.datenspeicher.genannt_markierung_leer_diskriminierungsform
        temp_speicher_save.genannt_markierung_leer_agg_relevanz = self.datenspeicher.genannt_markierung_leer_agg_relevanz

        # copy all values genannt_markierung_zeichen_lebensbereich, genannt_markierung_zeichen_diskriminierungsmerkmale, genannt_markierung_zeichen_interventionsformen, genannt_markierung_zeichen_diskriminierungsform, genannt_markierung_zeichen_agg_relevanz
        temp_speicher_save.genannt_markierung_zeichen_lebensbereich = self.datenspeicher.genannt_markierung_zeichen_lebensbereich
        temp_speicher_save.genannt_markierung_zeichen_diskriminierungsmerkmale = self.datenspeicher.genannt_markierung_zeichen_diskriminierungsmerkmale
        temp_speicher_save.genannt_markierung_zeichen_interventionsformen = self.datenspeicher.genannt_markierung_zeichen_interventionsformen
        temp_speicher_save.genannt_markierung_zeichen_diskriminierungsform = self.datenspeicher.genannt_markierung_zeichen_diskriminierungsform
        temp_speicher_save.genannt_markierung_zeichen_agg_relevanz = self.datenspeicher.genannt_markierung_zeichen_agg_relevanz

        # copy all values genannt_markierung_zeichen_text_lebensbereich, genannt_markierung_zeichen_text_diskriminierungsmerkmale, genannt_markierung_zeichen_text_interventionsformen, genannt_markierung_zeichen_text_diskriminierungsform, genannt_markierung_zeichen_text_agg_relevanz
        temp_speicher_save.genannt_markierung_zeichen_text_lebensbereich = self.datenspeicher.genannt_markierung_zeichen_text_lebensbereich
        temp_speicher_save.genannt_markierung_zeichen_text_diskriminierungsmerkmale = self.datenspeicher.genannt_markierung_zeichen_text_diskriminierungsmerkmale
        temp_speicher_save.genannt_markierung_zeichen_text_interventionsformen = self.datenspeicher.genannt_markierung_zeichen_text_interventionsformen
        temp_speicher_save.genannt_markierung_zeichen_text_diskriminierungsform = self.datenspeicher.genannt_markierung_zeichen_text_diskriminierungsform
        temp_speicher_save.genannt_markierung_zeichen_text_agg_relevanz = self.datenspeicher.genannt_markierung_zeichen_text_agg_relevanz

        # copy all values genannt_markierung_nichtzeichen_lebensbereich, genannt_markierung_nichtzeichen_diskriminierungsmerkmale, genannt_markierung_nichtzeichen_interventionsformen, genannt_markierung_nichtzeichen_diskriminierungsform, genannt_markierung_nichtzeichen_agg_relevanz
        temp_speicher_save.genannt_markierung_nichtzeichen_lebensbereich = self.datenspeicher.genannt_markierung_nichtzeichen_lebensbereich
        temp_speicher_save.genannt_markierung_nichtzeichen_diskriminierungsmerkmale = self.datenspeicher.genannt_markierung_nichtzeichen_diskriminierungsmerkmale
        temp_speicher_save.genannt_markierung_nichtzeichen_interventionsformen = self.datenspeicher.genannt_markierung_nichtzeichen_interventionsformen
        temp_speicher_save.genannt_markierung_nichtzeichen_diskriminierungsform = self.datenspeicher.genannt_markierung_nichtzeichen_diskriminierungsform
        temp_speicher_save.genannt_markierung_nichtzeichen_agg_relevanz = self.datenspeicher.genannt_markierung_nichtzeichen_agg_relevanz

        # copy all values genannt_markierung_nichtzeichen_text_lebensbereich, genannt_markierung_nichtzeichen_text_diskriminierungsmerkmale, genannt_markierung_nichtzeichen_text_interventionsformen, genannt_markierung_nichtzeichen_text_diskriminierungsform, genannt_markierung_nichtzeichen_text_agg_relevanz
        temp_speicher_save.genannt_markierung_nichtzeichen_text_lebensbereich = self.datenspeicher.genannt_markierung_nichtzeichen_text_lebensbereich
        temp_speicher_save.genannt_markierung_nichtzeichen_text_diskriminierungsmerkmale = self.datenspeicher.genannt_markierung_nichtzeichen_text_diskriminierungsmerkmale
        temp_speicher_save.genannt_markierung_nichtzeichen_text_interventionsformen = self.datenspeicher.genannt_markierung_nichtzeichen_text_interventionsformen
        temp_speicher_save.genannt_markierung_nichtzeichen_text_diskriminierungsform = self.datenspeicher.genannt_markierung_nichtzeichen_text_diskriminierungsform
        temp_speicher_save.genannt_markierung_nichtzeichen_text_agg_relevanz = self.datenspeicher.genannt_markierung_nichtzeichen_text_agg_relevanz

        return temp_speicher_save

    def dummies_kreuztabelle(self, dict_code_checkboxes_zeilen, dict_code_checkboxes_spalten):

        zeilen = list(dict_code_checkboxes_zeilen.keys())
        spalten = list(dict_code_checkboxes_spalten.keys())

        tmp_df = self.datenspeicher.df.copy()  # Erstellen einer unabhängigen Kopie des DataFrames
        print(tmp_df)
        for s1 in zeilen:
            s1_modifiziert = 'XXX_XXX_' + s1
            print("s1_modifiziert", s1_modifiziert)
            tmp_df = tmp_df.dropna(subset=[s1_modifiziert])
            print("hallo2")
            break
        print(tmp_df)
        for s2 in spalten:
            s2_modifiziert = 'XXX_XXX_' + s2
            tmp_df = tmp_df.dropna(subset=[s2_modifiziert])
            break
        print(tmp_df)

        spalten.append("N")
        df_kreuztabelle = pd.DataFrame(index=zeilen, columns=spalten, dtype=int)

        for s1 in zeilen:
            s1_modifiziert = 'XXX_XXX_' + s1
            for s2 in spalten:
                s2_modifiziert = 'XXX_XXX_' + s2
                if s2 == "N":
                    not_missing = tmp_df[altspalte].notnull() & tmp_df[s1_modifiziert].eq(True)
                    df_kreuztabelle.loc[s1, s2] = not_missing.sum()
                else:
                    print('tmp_df[s1_modifiziert]', tmp_df[s1_modifiziert])
                    print('tmp_df[s2_modifiziert]', tmp_df[s2_modifiziert])
                    print(' tmp_df', tmp_df)
                    df_kreuztabelle.loc[s1, s2] = sum((tmp_df[s1_modifiziert] == 1) & (tmp_df[s2_modifiziert] == 1))

                    altspalte = s2_modifiziert
        df_kreuztabelle = df_kreuztabelle.astype(int)

        self.ausgabepfad = ""
        self.ausgabepfad = self.datenspeicher.pfad_datenausgabe + "/" + "02 Daten für die Erhebung" + "/" + self.grafiktitel + "_kreuztabelle.xlsx"
        df_kreuztabelle.to_excel(self.ausgabepfad, index=True)

        with zipfile.ZipFile(self.zip_speicherpfad, 'a', zipfile.ZIP_DEFLATED) as zipf:
            # Füge die Datei zur ZIP-Datei hinzu
            self.datei_zum_hinzufuegen = self.ausgabepfad  # Ersetze dies durch den richtigen Dateipfad
            datei_name_in_zip = self.grafiktitel + "_kreuztabelle.xlsx"  # Ersetze dies durch den gewünschten Namen in der ZIP-Datei
            zipf.write(self.datei_zum_hinzufuegen, datei_name_in_zip)
        return df_kreuztabelle

        # self.standard_grafik_dummies()

    def abbrechen(self):
        self.tmp_pfad_datengrundlage_einfach = ""
        self.close()


class fehlerfenster(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hinweis")
        self.setFixedatenspeicherze(300, 100)  # Festlegen einer festen Größe für das Dialogfenster

        self.layout = QVBoxLayout()

        label = QLabel("Sie haben bereits alles fertig codiert")
        self.layout.addWidget(label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)  # Schließen des Dialogfensters beim Klicken auf den "OK"-Button
        self.layout.addWidget(ok_button)

        self.setLayout(self.layout)


class FRM_fenster_ausfuellhinweise(QMainWindow, Ui_fenster_ausfuellhinweise):
    def __init__(self, datenspeicher, frm_main):  # frm_main als Argument hinzugefügt
        super().__init__()
        self.setupUi(self)
        self.datenspeicher = datenspeicher
        self.frm_main = frm_main
        self.fill_tree_widget()
        self.treeWidget.itemClicked.connect(
            self.handle_tree_item_clicked)  # Verbinden Sie das Klick-Signal des TreeWidgets
        self.init_text_browser()

    def init_text_browser(self):
        # Setzen Sie den HTML-Text im TextBrowser auf leer
        self.textBrowser.setHtml("")

    def fill_text_browser(self, anchor_id):
        # Erstellen Sie den Text mit Anker im rechten TextBrowser basierend auf anchor_id
        if anchor_id == "Lebensbereiche":
            text = """
            <h1 id="Lebensbereiche">Lebensbereiche</h1>
            <p>Dies ist der Text für Anker 1. <a href="#Ämter und Behörden">Zum Lesezeichen Ämter und Behörden</a> Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. Maecenas nec odio et ante tincidunt tempus. Donec vitae sapien ut libero venenatis faucibus. Nullam quis ante. Etiam sit amet orci eget eros faucibus tincidunt. Duis leo. Sed fringilla mauris sit amet nibh. Donec sodales sagittis magna. Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, quis gravida magna mi a libero. Fusce vulputate eleifend sapien. Vestibulum purus quam, scelerisque ut, mollis sed, nonummy id, metus. Nullam accumsan lorem in dui. Cras ultricies mi eu turpis hendrerit fringilla. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; In ac dui quis mi consectetuer lacinia. Nam pretium turpis et arcu. Duis arcu tortor, suscipit eget, imperdiet nec, imperdiet iaculis, ipsum. Sed aliquam ultrices mauris. Integer ante arcu, accumsan a, consectetuer eget, posuere ut, mauris. Praesent adipiscing. Phasellus ullamcorper ipsum rutrum nunc. Nunc nonummy metus. Vestibulum volutpat pretium libero. Cras id dui. Aenean ut eros et nisl sagittis</p>
            <h2 id="Ämter und Behörden">Ämter und Behörden</h2>
            <p>Dies ist der Text für Anker 2. ...</p>
            <h2 id="Polizei">Polizei</h2>
            <p>Dies ist der Text für Anker 4. <a href="#Lebensbereiche">Zum Lesezeichen Lebensbereiche</a> ...</p>
            """
        elif anchor_id == "Diskriminierungsmerkmale":
            text = """
            <h1 id="Diskriminierungsmerkmale">Diskriminierungsmerkmale</h1>
            <p>Dies ist der Text für einen neuen Anker. 
            """
        else:
            text = ""  # Setzen Sie den Text auf leer, wenn das Lesezeichen nicht gefunden wird

        # Setzen Sie den HTML-Text im TextBrowser
        self.textBrowser.setHtml(text)

    def handle_tree_item_clicked(self, item, column):
        anchor_id = item.text(column)

        # Wenn eine H2-Überschrift ausgewählt wurde, setze die Textanzeige auf die entsprechende H2-Überschrift
        if anchor_id in ["Ämter und Behörden", "Polizei"]:
            self.fill_text_browser("Lebensbereiche")
            self.textBrowser.scrollToAnchor(anchor_id)
        elif anchor_id in ["Geschlecht"]:
            self.fill_text_browser("Diskriminierungsmerkmale")
            self.textBrowser.scrollToAnchor(anchor_id)
        else:
            # Wenn eine H1-Überschrift ausgewählt wurde, zeige die gesamte Textseite an
            self.fill_text_browser(anchor_id)

    def fill_tree_widget(self):
        new_item = QTreeWidgetItem(self.treeWidget)
        new_item.setText(0, "Lebensbereiche")

        sub_item = QTreeWidgetItem(new_item)
        sub_item.setText(0, "Ämter und Behörden")
        sub_item = QTreeWidgetItem(new_item)
        sub_item.setText(0, "Polizei")

        new_item = QTreeWidgetItem(self.treeWidget)
        new_item.setText(0, "Diskriminierungsmerkmale")


class Application:
    def __init__(self):
        self.app = QApplication([])
        self.datenspeicher = Datenspeicher()
        self.gui_MainWindow = FRM_main(self.datenspeicher, self.app)

    def run(self):
        self.gui_MainWindow.show()
        self.app.exec()

        print("Erfolg")


if __name__ == "__main__":
    application = Application()
    application.run()
