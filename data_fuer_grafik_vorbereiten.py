import numpy as np
import pandas as pd

class Data_Fuer_Grafik_Vorbereiten:
    
    def data_erstellen(self, df, datentyp, abs_rel, ausgangsliste, reihenfolge='dict', kreuzung = False, reihenfolge_letzte = ""):
        print("df!", df)
        if datentyp == "dummies":
            if abs_rel == "relativ":
                df['relativ'] = np.where((df['genannt'] + df['nicht genannt']) == 0, 0, df['genannt'] * 100 / np.where((df['genannt'] + df['nicht genannt']) == 0, 1, df['genannt'] + df['nicht genannt']))
                data = df[["Wert", "relativ", "genannt"]]
                data = self.reihenfolge_daten_festlegen(data, reihenfolge, datentyp, kreuzung = kreuzung, reihenfolge_letzte = reihenfolge_letzte, ausgangsliste = ausgangsliste)
                data = data.dropna(subset=['Wert'])
                daten_labels = (data.Wert).tolist()
                daten = data['relativ'].to_frame().to_dict(orient='list')
            if abs_rel == "absolut":
                data = df
                data = self.reihenfolge_daten_festlegen(data, reihenfolge, datentyp, kreuzung = kreuzung, reihenfolge_letzte = reihenfolge_letzte, ausgangsliste = ausgangsliste)
                data = data.dropna(subset=['Wert'])
                
                print(data)
                daten_labels = (data.Wert).tolist()
                daten = data['genannt'].to_frame().to_dict(orient='list')
            df2 = data
            df2['gesamt'] = df2['genannt'] + df2['nicht genannt']
            print(df2)
            erste_zeile = df2.iloc[0]
            fallzahl = str(erste_zeile['gesamt'])

            
        if datentyp == "ausprägungen":

            haufigkeiten = {}
            if kreuzung != True:
                df['gesamt'] = df.drop('Wert', axis=1).sum(axis=1)
            fallzahl = str(int(df.at[df.index[-1], 'gesamt']))
            if kreuzung == True:
                df = df.drop('N', axis=1)
            data = pd.DataFrame()
            spalten = df.columns.difference(['gesamt', 'Wert'])
            daten_labels = df["Wert"].tolist()
            if abs_rel == "absolut":
                for spalte in spalten:
                    data[spalte] = df[spalte]
            if abs_rel == "relativ":
                for spalte in spalten:
                    data[spalte] = df[spalte] / df['gesamt'] * 100
            for column in df.columns:
                if kreuzung != True:
                    if column in tmp_dict:
                        data = data.rename(columns={column: tmp_dict[column]})                

                if kreuzung == True:
                    for spaltenname in tmp_dict_spalte:
                        if column == self.tmp_vorsilbe_spalte + "_" + spaltenname:
                            data = data.rename(columns={column: tmp_dict_spalte[spaltenname]})                
            if kreuzung != True:        
                data = self.reihenfolge_daten_festlegen(data, reihenfolge, datentyp, kreuzung = kreuzung, reihenfolge_letzte = reihenfolge_letzte, ausgangsliste = ausgangsliste)
            daten = data.to_dict(orient='list')
        print(daten, daten_labels, fallzahl)
        return daten, daten_labels, fallzahl


    def reihenfolge_daten_festlegen(self, data, reihenfolge, datentyp, ausgangsliste, kreuzung = True, reihenfolge_letzte = ""):
        
        if reihenfolge == "aufsteigend":
            if datentyp == "dummies":
                data = data.sort_values('genannt', ascending=False, ignore_index=True)
            if datentyp == "ausprägungen":
                sortierte_spalten = data.iloc[-1].sort_values(ascending=True).index  
                data = data[sortierte_spalten] 
        elif  reihenfolge == "absteigend":
            if datentyp == "dummies":
                data = data.sort_values('genannt', ascending=True, ignore_index=True)
            if datentyp == "ausprägungen":
                sortierte_spalten = data.iloc[-1].sort_values(ascending=False).index  
                data = data[sortierte_spalten] 
        elif  reihenfolge == "alphabetisch":
            if datentyp == "dummies":
                data = data.sort_values('Wert', ascending=True, ignore_index=True)
            if datentyp == "ausprägungen":
                data = data.sort_index(axis=1)
        else: 
            print('data1', data)
            if datentyp == "dummies":
                data['Wert'] = pd.Categorical(data['Wert'], categories=ausgangsliste, ordered=True)
                # Sortiere die Daten basierend auf der kategorialen Reihenfolge
                data = data.sort_values('Wert')
            if datentyp == "ausprägungen":
                print('ausgangsliste', ausgangsliste)
                if kreuzung != True: 
                    sortierte_spalten = [col for col in ausgangsliste if col in data.rows]
                if kreuzung == True: 
                    sortierte_spalten = [col for col in ausgangsliste_spalte.values() if col in data.rows]
                data = data[sortierte_spalten]
            print('data2',data)
        if reihenfolge_letzte != "" :
            
            if datentyp == "dummies":
                # Indexnummern der Werte in 'reihenfolge_letzte' ermitteln
                indexnummern_reihenfolge_letzte = data[data['Spalte'].isin(reihenfolge_letzte)].index.tolist()
                # Indexnummern der anderen Zeilen ermitteln
                andere_zeilen = data[~data['Spalte'].isin(reihenfolge_letzte)].index.tolist()
                # Indexnummern der Werte in 'reihenfolge_letzte' an das Ende setzen
                neue_reihenfolge = indexnummern_reihenfolge_letzte + andere_zeilen  
                data = data.loc[neue_reihenfolge]    
            if datentyp == "ausprägungen":
                andere_spalten = [col for col in data.columns if col not in reihenfolge_letzte]
                neue_reihenfolge = andere_spalten[:1] + reihenfolge_letzte + andere_spalten[1:]
                data = data[neue_reihenfolge]
        
        return data