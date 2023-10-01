import pandas as pd
import numpy as np
import PySimpleGUI as sg
import sys
import os
import tempfile
import shutil
import re
import copy
import zipfile
import math
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import lines
from matplotlib import patches
from matplotlib.patheffects import withStroke
from IPython.display import display
#from docx import Document
#from docx.shared import Pt
#from docx.oxml.ns import nsdecls
#from docx.oxml import parse_xml
#from docx.enum.style import WD_STYLE_TYPE


BLAU = "#076fa2"
ROT = "#E3120B"
SCHWARZ = "#202020"
GRAU = "#a2a2a2"
GRAU_DUNKEL = "#A8BAC4"
GELB = "#FFA54F"
WEISS = "#FFFFFF"
SCHRIFT = "Calibri"

FARBE_DEKOELEMENTE = GELB
FARBE_SCHRIFT_ÜBERSCHRIFT = SCHWARZ
FARBE_SCHRIFT_ÜBERSCHRIFT2 = SCHWARZ
FARBE_BALKEN1 = BLAU
FARBE_SCHRIFT_INBALKEN = WEISS
FARBE_SCHRIFT_YACHSE = BLAU
FARBE_SCHRIFT_NEBENBALKEN = BLAU
FARBE_SCHRIFT_KOMMENTAR = GRAU
FARBE_SCHRIFT_ÜBERSCHRIFT= BLAU
FARBE_ACHSEN = GRAU_DUNKEL


BALKENFARBEN  = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd', '#ccebc5', '#ffed6f']

class Grafik_Erstellen:
        
    def testdata_heatmap_erstellen(self, df):
        tmp_dict_spalte = df.columns.tolist()[1:]
        tmp_dict_zeile = df.iloc[1:, 0].tolist()

        #df.columns = tmp_dict_spalte
        #df = df.iloc[1:, :]



        for index, row in df.iterrows():
            if index != 'N':
                if row['N'] != 0:
                    calculated_values = (row[df.columns != 'N'] / row['N']) * 100
                    calculated_values = calculated_values.round(1)
                    df.loc[index, df.columns != 'N'] = calculated_values
                else:
                    df.loc[index, df.columns != 'N'] = 0
            """if index != 'N':
                print("b")
                if index['N'] == 0:
                    print("c")
                    df.loc[index] = 0
                    df.loc[index] = df.loc[index].round(1)
                else:
                    print("d")
                    df.loc[index] = (df[index] / df['N']) * 100
                    df.loc[index] = df.loc[index].round(1)"""
        new_index = []

        for idx, row in df.iterrows():
            new_index.append(f'{idx} (N = {row["N"]})')

        df.index = new_index
        df.drop('N', axis=1, inplace=True)

        return df


        print("Hier")
        """
        for column in df.columns:
            for spaltenname in tmp_dict_spalte:
                if column == tmp_vorsilbe_spalte + "_" + spaltenname:
                    df = df.rename(columns={column: tmp_dict_spalte[spaltenname]})   
        df.set_index('Spalte', inplace=True)
        spalten = df.columns.difference(['gesamt', 'Wert'])
        for spalte in spalten:
            df[spalte] = df[spalte] / df['gesamt'] * 100
        df = df.round(1)
        columns_to_drop = ['gesamt', 'N']
        existing_columns = [col for col in columns_to_drop if col in df.columns]
        df = df.drop(existing_columns, axis=1)
        return df
        """


    def reihenfolge_festlegen(self, label_yachse_vorhanden, legende_vorhanden):
        if label_yachse_vorhanden == True:
            if legende_vorhanden == True:
                i = 1
                j = 1
                reihenfolge_oben = i
                reihenfolge_oben_vert = j
                i = i + 1
                j = j + 1
                reihenfolge_graph_yachse = i
                reihenfolge_graph_yachse_vert = j
                i = i + 1

                reihenfolge_graph = i
                reihenfolge_graph_vert = j
                i = i + 1
                j = j + 1
                reihenfolge_legende = i
                reihenfolge_legende_vert = j
                i = i + 1
                j = j + 1
                reihenfolge_unten = i
                reihenfolge_unten_vert = j
            elif legende_vorhanden == False:
                i = 1
                j = 1
                reihenfolge_oben = i
                reihenfolge_oben_vert = j
                i = i + 1
                j = j + 1
                reihenfolge_graph_yachse = i
                reihenfolge_graph_yachse_vert = j
                i = i + 1

                reihenfolge_graph = i
                reihenfolge_graph_vert = j
                i = i + 1
                j = j + 1
                reihenfolge_legende = 0
                reihenfolge_legende_vert = 0


                reihenfolge_unten = i
                reihenfolge_unten_vert = j
        elif label_yachse_vorhanden == False:
            if legende_vorhanden == True:
                i = 1
                j = 1
                reihenfolge_oben = i
                reihenfolge_oben_vert = j
                i = i + 1
                j = j + 1
                reihenfolge_graph_yachse = 0
                reihenfolge_graph_yachse_vert = 0


                reihenfolge_graph = i
                reihenfolge_graph_vert = j
                i = i + 1
                j = j + 1
                reihenfolge_legende = i
                reihenfolge_legende_vert = j
                i = i + 1
                j = j + 1
                reihenfolge_unten = i
                reihenfolge_unten_vert = j
            elif legende_vorhanden == False:
                i = 1
                j = 1
                reihenfolge_oben = i
                reihenfolge_oben_vert = j
                i = i + 1
                j = j + 1
                reihenfolge_graph_yachse = 0
                reihenfolge_graph_yachse_vert = 0


                reihenfolge_graph = i
                reihenfolge_graph_vert = j
                i = i + 1
                j = j + 1
                reihenfolge_legende = 0
                reihenfolge_legende_vert = 0


                reihenfolge_unten = i
                reihenfolge_unten_vert = j
        elemente_übereinander = sum(objekt != 0 for objekt in [reihenfolge_oben, reihenfolge_graph, reihenfolge_legende, reihenfolge_unten])

        elementezahl = max(
            reihenfolge_oben,
            reihenfolge_graph_yachse,
            reihenfolge_graph,
            reihenfolge_legende,
            reihenfolge_unten
        )
        return(elemente_übereinander, elementezahl, reihenfolge_oben, reihenfolge_graph, reihenfolge_graph_yachse, reihenfolge_legende, reihenfolge_unten, reihenfolge_oben_vert, reihenfolge_graph_vert, reihenfolge_graph_yachse_vert, reihenfolge_graph_vert, reihenfolge_legende_vert, reihenfolge_unten_vert)

    def label_korrektur(self, labels):
        for i in range(len(labels)):
            if 'tmp_dict_korrektur' in locals() or 'tmp_dict_korrektur' in globals():
                if labels[i] in tmp_dict_korrektur:
                    labels[i] = tmp_dict_korrektur[labels[i]]
        return labels

    def label_trennen(self, labels, zeilenlänge = 40):
        mehrzeilige_labels = "FALSE"
        for i in range(len(labels)):
            if len(labels[i]) > zeilenlänge:
                idx = len(labels[i]) // 2
                while idx < len(labels[i]) and labels[i][idx] not in [" ", ",", "/", ";", "-"]:
                    idx += 1
                if idx - len(labels[i]) // 2 < len(labels[i]) // 2 - idx + 1:
                    labels[i] = labels[i][:idx] + "\n" + labels[i][idx+1:]
                else:
                    labels[i] = labels[i][:idx] + "\n" + labels[i][idx:]
                mehrzeilige_labels = "TRUE"
        label_längstes_zeilelänge = 0
        for label in labels:
            if "\n" in label:
                zeilen_längen = [len(line) for line in label.split("\n")]
                max_zeilen_länge = max(zeilen_längen)
            else:
                max_zeilen_länge = len(label)
            if max_zeilen_länge > label_längstes_zeilelänge:
                label_längstes_zeilelänge = max_zeilen_länge  
        labels = [element.replace("\n ", "\n") if "\n " in element else element for element in labels]
        return labels, mehrzeilige_labels, label_längstes_zeilelänge

    def graph_höhe_bestimmen(self, daten_labels, y_mehrzeilige_labels):
        yachse_multiplikator = 1
        if y_mehrzeilige_labels == "TRUE":
            yachse_multiplikator = 1.3
        höhe = ((len(daten_labels) * 0.3) + 2)*yachse_multiplikator
        return höhe

    def balken_yposition_festlegen(self, daten, daten_labels, datentyp):
        if datentyp == "ausprägungen":
            liste_balken_y =  [i for i in range(len(daten_labels))]
        elif datentyp == "dummies":
            for key in daten:
                anzahl_werte = len(daten[key])
                max_anzahl_werte = 0
                if anzahl_werte > max_anzahl_werte:
                    max_anzahl_werte = anzahl_werte
            if max_anzahl_werte == 1: 
                anzahl_werte = sum(len(values) for values in daten.values())
                liste_balken_y =  [i * 0.9 for i in range(anzahl_werte)]
            if max_anzahl_werte > 1:
                # Bestimme die Anzahl der Werte im Dictionaire daten
                liste_balken_y = []
                start = 0  # Startwert auf 0 setzen
                while len(liste_balken_y) < len(daten_labels) * len(daten):
                    liste_balken_y.extend(range(start, start + len(daten_labels)))
                    start += len(daten_labels) + 1 
        return liste_balken_y

    def balken_einfügen(self, fig, axes, daten, daten_labels, datentyp, abs_rel):
        liste_balken_y = self.balken_yposition_festlegen(daten, daten_labels, datentyp)
        häufigkeiten = []
        if datentyp == "dummies":        
            for werte in daten.values():
                häufigkeiten.extend(werte)
            axes.barh(liste_balken_y, häufigkeiten, height=0.55, align="edge", color=FARBE_BALKEN1)
        if datentyp == "ausprägungen": 
            x_start = [0] * len((daten_labels))
            index_spalte = 0
            for spalte, werte in daten.items():
                index_werte = 0
                farbe = BALKENFARBEN[index_spalte % len(BALKENFARBEN)]
                #for i, wert in enumerate(werte):

                axes.barh(liste_balken_y, werte, height=0.55, align="edge", color=farbe, left=x_start)

                for i in range(len(x_start)):
                    x_start[i] = x_start[i] + werte[i]

                häufigkeiten.extend(werte)

                index_werte = (index_werte + 1)
                index_spalte = (index_spalte + 1)
        return fig, axes, liste_balken_y, häufigkeiten

    def xachse_anpassen(self, fig, axes, daten, abs_rel, datentyp):
        if abs_rel == "relativ":
            axes.xaxis.set_ticks([i * 10 for i in range(0, 21)])
            axes.xaxis.set_ticklabels([i * 10 for i in range(0, 21)], size=16, fontfamily=SCHRIFT, fontweight=100)
            axes.set_xlim((0, 100.5))
            xmax = 100
        if abs_rel == "absolut":
            list_xwerte_pot = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
            if datentyp == "dummies":            
                xmax = max(max(values) for values in daten.values())
            if datentyp == "ausprägungen":
                summen = {}
                for key, werte in daten.items():
                    for i, wert in enumerate(werte):
                        if i not in summen:
                            summen[i] = 0
                        summen[i] += wert
                xmax = max(summen.values())
            xmax_durch10 = xmax/10
            xintervall = min(list_xwerte_pot, key=lambda x: abs(x - xmax_durch10))
            xmax = round(xmax + 1) 
            while xmax % xintervall != 0: 
                xmax += 1  
            xachse_zahl_ticks = math.ceil((xmax + 1)/xintervall)
            axes.set_xlim((0, xmax+1))
            axes.xaxis.set_ticks([i * xintervall for i in range(0, xachse_zahl_ticks)])
            axes.xaxis.set_ticklabels([i * xintervall for i in range(0, xachse_zahl_ticks)], size=16, fontfamily=SCHRIFT, fontweight=100)  
        return fig, axes, xmax

    def yachse_anpassen(self, fig, axes, datentyp, daten, daten_labels, liste_balken_y):
        if datentyp == "dummies":
            axes.set_ylim((0, max(liste_balken_y)+.8))
        #fig_copy = copy.deepcopy(fig)
        #fig_copy
        if datentyp == "ausprägungen":
            for spalte, werte in daten.items():
                if len(werte) > 1:
                    axes.set_ylim((0, len(werte)))# * 0.9 - 0.2))
        #fig_copy = copy.deepcopy(fig)
        #fig_copy   
        axes.xaxis.set_tick_params(labelbottom=False, labeltop=True, length=0)
        axes.set_axisbelow(True)
        axes.grid(axis = "x", color=FARBE_ACHSEN, lw=1.2)
        axes.spines["right"].set_visible(False)
        axes.spines["top"].set_visible(False)
        axes.spines["bottom"].set_visible(False)
        axes.spines["left"].set_lw(0.5)
        axes.spines["left"].set_capstyle("butt")
        axes.yaxis.set_visible(False) 
        return fig, axes

    def ylabels_einfügen(self, fig, axes, daten_labels, liste_balken_y):
        path_effects = [withStroke(linewidth=6, foreground="white")]
        for label, y_pos in zip(daten_labels, liste_balken_y):
            x_value = -0.02
            axes.text(x_value, y_pos +0.25, label, horizontalalignment='right', color=FARBE_SCHRIFT_YACHSE, fontfamily=SCHRIFT, fontsize=18, va="center", path_effects=path_effects, transform=axes.get_yaxis_transform())  
        return fig, axes


    def werte_einfügen(self, fig, axes, datentyp, labels, daten, liste_balken_y, häufigkeiten, xmax, kreuzung = False):
        path_effects = [withStroke(linewidth=6, foreground="white")]
        häufigkeiten = [round(wert, 1) for wert in häufigkeiten]
        if datentyp == "dummies":
            for label, häufigkeit, y_pos in zip(labels, häufigkeiten, liste_balken_y):
                #for key in daten:
                    x_value = float(häufigkeit) + 0.01 * float(xmax)
                    häufigkeit_str = str(häufigkeit).replace('.', ',')
                    axes.text(
                        x_value, 
                        y_pos + 0.5 / 2, 
                        häufigkeit_str, 
                        color=FARBE_SCHRIFT_NEBENBALKEN,  
                        fontfamily=SCHRIFT, fontsize=18, va="center",
                        path_effects=path_effects)
        elif datentyp == "ausprägungen":
            if kreuzung == False:
                x_start = 0
                index_spalte = 0
                for spalte, werte in daten.items():
                    for wert, y_pos in zip(werte, liste_balken_y):            
                        wert_str = str(round(wert, 1)).replace('.', ',')
                        axes.text(
                                (x_start + x_start + wert)/2, 
                                y_pos + 0.5 / 2, 
                                wert_str, 
                                color=FARBE_SCHRIFT_NEBENBALKEN,  
                                fontfamily=SCHRIFT, fontsize=16, va="center", ha='center',
                                path_effects=path_effects)
                        x_start = x_start + wert
                                
            if kreuzung == True:
                x_start = [0] * len(daten_labels)
                for spalte, werte in daten.items():
                    i = 0
                    for wert, y_pos in zip(werte, liste_balken_y):   
                        wert_str = str(round(wert, 1)).replace('.', ',')
                        axes.text(
                                (x_start[i] + x_start[i] + wert)/2, 
                                y_pos + 0.5 / 2, 
                                wert_str, 
                                color=FARBE_SCHRIFT_NEBENBALKEN,  
                                fontfamily=SCHRIFT, fontsize=18, va="center", ha='center',
                                path_effects=path_effects)
                        x_start[i] = x_start[i] + wert
                        i = i + 1
        return fig, axes


    def graph_einfügen(self, fig, axes, daten, daten_labels, datentyp, abs_rel, label_yachse_vorhanden, x_mehrzeilige_labels, x_label_längstes_zeilelänge, y_mehrzeilige_labels, y_label_längstes_zeilelänge, kreuzung = False):
        #fig, axes = graph_grundgerüst_erstellen(fig, axes, daten_labels, y_mehrzeilige_labels)
        fig, axes, liste_balken_y, häufigkeiten = self.balken_einfügen(fig, axes, daten, daten_labels, datentyp, abs_rel)
        #fig_copy = copy.deepcopy(fig)
        #fig_copy
        fig, axes, xmax = self.xachse_anpassen(fig, axes, daten, abs_rel, datentyp)
        #fig_copy = copy.deepcopy(fig)
        #fig_copy
        fig, axes = self.yachse_anpassen(fig, axes, datentyp, daten, daten_labels, liste_balken_y)
        #fig_copy = copy.deepcopy(fig)
        #fig_copy
        if label_yachse_vorhanden == True:
            fig, axes = self.ylabels_einfügen(fig, axes, daten_labels, liste_balken_y)
        #fig_copy = copy.deepcopy(fig)
        #fig_copy
        fig, axes = self.werte_einfügen(fig, axes, datentyp, daten_labels, daten, liste_balken_y, häufigkeiten, xmax, kreuzung)
        #fig_copy = copy.deepcopy(fig)
        #fig_copy
        return fig, axes

    def legende_vorbereiten(self, graph_breite, daten, datentyp, x_label_längstes_zeilelänge):
        # Legende anzeigen^
        legende_labels = daten.keys()
        n_legende_labels_pro_zeile = int((graph_breite * 5) / (x_label_längstes_zeilelänge * 0.6))
        n_legende_spalten = n_legende_labels_pro_zeile
        n_legende_labels = len(legende_labels)
        n_legende_labels_pro_spalte = n_legende_labels // n_legende_labels_pro_zeile
        if n_legende_spalten > 0:
            n_legende_labels_pro_spalte += 1
        return legende_labels, n_legende_spalten, n_legende_labels_pro_spalte

    def legende_einfügen(self, fig, axes, datentyp, daten, x_mehrzeilige_labels, legende_labels, n_legende_spalten):
        legende_farben = BALKENFARBEN[:len(legende_labels)]
        legende_elemente = []
        for label, farbe in zip(legende_labels, legende_farben):
            patch = patches.Patch(facecolor=farbe, edgecolor='none')
            legende_elemente.append((patch, label))
        
        n_legende_reihen = (len(legende_elemente) + n_legende_spalten - 1) // n_legende_spalten
        neue_reihenfolge = []
        for j in range(n_legende_spalten):
            for i in range(n_legende_reihen):
                index = j + i * n_legende_spalten
                if index < len(legende_elemente):
                    neue_reihenfolge.append(legende_elemente[index])
        legende_elemente = neue_reihenfolge

        
        # Legende erstellen, aber nicht anzeigen, um die Größe zu bestimmen
        legende = axes.legend(handles=[patch for patch, _ in legende_elemente],
                            labels=[label for _, label in legende_elemente],
                            loc='center',
                            bbox_to_anchor=(0.5, 0.5),
                            fontsize=14,
                            frameon=False,
                            ncol=n_legende_spalten)
        axes.axis('off')
        return fig, axes


    def titel_einfügen(self, fig, axes,titel):
        axes.text(0, 0.5, titel, color=FARBE_SCHRIFT_ÜBERSCHRIFT,        fontsize=22, fontweight="bold", fontfamily=SCHRIFT)
        return fig, axes

    def untertitel_einfügen(self, fig, axes, untertitel):
        axes.text(0, 0.15, untertitel, color=FARBE_SCHRIFT_ÜBERSCHRIFT2, fontsize=20, fontfamily=SCHRIFT)
        return fig, axes


    def caption_einfügen(self, fig, axes, fallzahl, datentyp, kreuzung = True):
        if datentyp == 'dummies':
            quelle = 'N = ' + str(fallzahl) + ', Mehrfachnennung möglich' + '\nDokumentationsdaten 2022 im Rahmen der Erhebung des IDZ'
        elif kreuzung == True:
            quelle = 'Dokumentationsdaten 2022 im Rahmen der Erhebung des IDZ'
        else:
            quelle = 'N = ' + str(fallzahl) + '' + '\nDokumentationsdaten 2022 im Rahmen der Erhebung des IDZ'
        axes.text(0, 0.35, quelle, color=FARBE_SCHRIFT_KOMMENTAR, fontsize=14, fontfamily=SCHRIFT)
        return fig, axes

    def deko_oben_einfügen(self, fig, axes):
        axes.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color=FARBE_DEKOELEMENTE, solid_capstyle="butt"))
        axes.add_artist(patches.Rectangle((0, 0.8), 0.05, 0.8, color=FARBE_DEKOELEMENTE))
        axes.axis('off')
        axes.set_facecolor("white")
        return fig, axes

    def deko_unten_einfügen(self, fig, axes):
        axes.add_artist(lines.Line2D([0, 1], [0, 0], lw=3, color=FARBE_DEKOELEMENTE, solid_capstyle="butt"))
        axes.add_artist(patches.Rectangle((0.95, 0), 0.05, 0.35, color=FARBE_DEKOELEMENTE))
        axes.axis('off')
        axes.set_facecolor("white")
        return fig, axes

    def elemente_festlegen(self, daten, datentyp, daten_labels):
        if datentyp == "dummies":
            label_yachse_vorhanden = True
            if len(daten) > 1:
                legende_vorhanden = True
            else:
                legende_vorhanden = False
        elif datentyp == "ausprägungen":
            legende_vorhanden = True
            if len(daten_labels) > 1:
                label_yachse_vorhanden = True
            else:
                label_yachse_vorhanden = False
        return legende_vorhanden, label_yachse_vorhanden    

    def grafik(self, daten, daten_labels, fallzahl, dateiname, datentyp = "dummies", abs_rel = "absolut", reihenfolge ="absteigend", titel = "Titel", untertitel = "Untertitel", kreuzung = False):
        graph_breite = 12
        
        df = pd.DataFrame()
        legende_vorhanden, label_yachse_vorhanden = elemente_festlegen(daten, datentyp, daten_labels)
        elemente_übereinander, elementezahl, reihenfolge_oben, reihenfolge_graph, reihenfolge_graph_yachse, reihenfolge_legende, reihenfolge_unten, reihenfolge_oben_vert, reihenfolge_graph_vert, reihenfolge_graph_yachse_vert, reihenfolge_graph_vert, reihenfolge_legende_vert, reihenfolge_unten_vert = reihenfolge_festlegen(label_yachse_vorhanden, legende_vorhanden)
        daten_labels = label_korrektur(daten_labels)
        daten_labels, y_mehrzeilige_labels, y_label_längstes_zeilelänge = label_trennen(daten_labels)
        key_labels = list(daten.keys())
        key_labels = label_korrektur(key_labels)
        key_labels, x_mehrzeilige_labels, x_label_längstes_zeilelänge = label_trennen(key_labels)
        daten = dict(zip(key_labels, daten.values()))
        if legende_vorhanden == True:
            legende_labels, n_legende_spalten, n_legende_labels_pro_spalte = legende_vorbereiten(graph_breite, daten, datentyp, x_label_längstes_zeilelänge)
            höhe_legende = .1 + .3*n_legende_labels_pro_spalte

        höhe_oben = 1.4       
        höhe_graph = graph_höhe_bestimmen(daten_labels, y_mehrzeilige_labels)
        höhe_unten = 0.8

        # Höhenverhältnis der Subplots
        if legende_vorhanden == True:
            height_ratios = [höhe_oben, höhe_graph, höhe_legende, höhe_unten]
        if legende_vorhanden == False:
            height_ratios = [höhe_oben, höhe_graph, höhe_unten]

        # Erstellen der Figure und Subplots
        fig, axes = plt.subplots(elementezahl, 1, figsize=(graph_breite, sum(height_ratios)), sharex=True)
        #fig.set_size_inches(sum(height_ratios)*10, 12)

        # GridSpec erstellen
        gs = gridspec.GridSpec(elemente_übereinander, 2, height_ratios=height_ratios, width_ratios=[0.01, 11.99], wspace=0.0, hspace=0.0)
        #fig_copy = copy.deepcopy(fig)
        #fig_copy
        if reihenfolge_oben > 0:
            #axes[reihenfolge_oben-1].remove()
            axes[reihenfolge_oben-1] = plt.subplot(gs[reihenfolge_oben_vert-1, :])
        #fig_copy = copy.deepcopy(fig)
        #fig_copy
        if reihenfolge_graph > 0:
            if label_yachse_vorhanden == False:
                #axes[reihenfolge_graph-1].remove()
                axes[reihenfolge_graph-1] = plt.subplot(gs[reihenfolge_graph_vert-1, :])
            if label_yachse_vorhanden == True:
                #axes[reihenfolge_graph-1].remove()
                #axes[reihenfolge_graph_yachse-1].remove()
                axes[reihenfolge_graph_yachse-1] = plt.subplot(gs[reihenfolge_graph_vert-1, 0])
                axes[reihenfolge_graph_yachse-1].axis('off')
                axes[reihenfolge_graph-1] = plt.subplot(gs[reihenfolge_graph_yachse_vert-1, 1])
        if reihenfolge_legende > 0:
            axes[reihenfolge_legende-1] = plt.subplot(gs[reihenfolge_legende_vert-1, :])
        if reihenfolge_unten > 0:
            axes[reihenfolge_unten-1] = plt.subplot(gs[reihenfolge_unten_vert - 1, :])
        #fig_copy = copy.deepcopy(fig)
        #fig_copy    
        #Lege mit Matplotlib eine Grafik an, die soviele Subplots besitzt, wie in matplotlib gespeichert sind. Das Höhenverhältnis der Subplots zeinander soll 0.2, 0.3, 0.3, 2, 1, 0.3, 0.2 betragen
        if reihenfolge_graph > 0:
            fig, axes[reihenfolge_graph-1] = graph_einfügen(fig, axes[reihenfolge_graph-1], daten, daten_labels, datentyp, abs_rel, label_yachse_vorhanden, x_mehrzeilige_labels, x_label_längstes_zeilelänge, y_mehrzeilige_labels, y_label_längstes_zeilelänge, kreuzung)
        #fig_copy = copy.deepcopy(fig)
        #fig_copy
        if reihenfolge_oben > 0:
            fig, axes[reihenfolge_oben-1] = deko_oben_einfügen(fig, axes[reihenfolge_oben-1])
            fig, axes[reihenfolge_oben-1] = titel_einfügen(fig, axes[reihenfolge_oben-1], titel)
            fig, axes[reihenfolge_oben-1] = untertitel_einfügen(fig, axes[reihenfolge_oben-1], untertitel)
        #fig_copy = copy.deepcopy(fig)
        #fig_copy
        if reihenfolge_legende > 0:
            fig, axes[reihenfolge_legende-1] = legende_einfügen(fig, axes[reihenfolge_legende-1], datentyp, daten, x_mehrzeilige_labels, legende_labels, n_legende_spalten)
        #fig_copy = copy.deepcopy(fig)
        #fig_copy
        if reihenfolge_unten > 0:
            fig, axes[reihenfolge_unten-1] = caption_einfügen(fig, axes[reihenfolge_unten-1], fallzahl, datentyp, kreuzung = kreuzung) 
            fig, axes[reihenfolge_unten-1] = deko_unten_einfügen(fig, axes[reihenfolge_unten-1])
        fig = gs.tight_layout(fig, h_pad=0)
        #zahl = fig.dpi
        plt.savefig(output_pfad + "/" + dateiname + '.png', bbox_inches='tight', dpi=300)
        return dateiname
    #grafik(daten = daten, daten_labels = daten_labels, titel = titel, untertitel= "Untertitel2", datentyp = "dummies", fallzahl = fallzahl, abs_rel="relativ")
