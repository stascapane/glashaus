import json
import os
import pandas as pd


def export_json_to_sql(filename: str, result_filename: str):
    try:
        os.remove(result_filename)
    except OSError:
        pass
    with open(filename, encoding='utf-8') as data:
        data = json.load(data)
        features = data["features"]
        with open(result_filename, "w", encoding="utf-8") as result:
            for part in features:
                strasse = part["attributes"]["strasse"]
                hausnummer = part["attributes"]["hausnr"]
                postleitzahl = part["attributes"]["postleitzahlgebiet"]
                stimmbezirk = part["attributes"]["stimmbezirk"]
                insert = f"INSERT INTO adressen (strasse,hausnummer,postleitzahl,stimmbezirk) VALUES ('{strasse}','{hausnummer}',{postleitzahl}, {stimmbezirk});"
                result.write(insert + "\n")

def export_cvs1_to_sql(filename: str, result_filename: str):
    try:
        os.remove(result_filename)
    except OSError:
        pass
    df = pd.read_csv(filename)
    d_columns = [x for x in df.columns if "D" in x and x not in ["D", "D1", "D2", "D3", "D4", "D5", "D6"]]

    df["sonstige"] = df[d_columns].sum(axis=1)
    print(d_columns)
    df_neu = df[["gebiet-nr", "D1", "D2", "D3", "D4", "D5", "D6", "sonstige"]]
    df_neu = df_neu.rename(
        {"gebiet-nr": "stimmbezirk", "D1": "cdu", "D2": "spd", "D3": "fdp", "D4": "afd", "D5": "gruene", "D6": "linke"},
        axis="columns")
    df_csv = df_neu.to_csv(index=False)
    with open(result_filename, "w", encoding="utf-8") as result:
        for line in df_csv.splitlines():
            insert = f"INSERT INTO ergebnisse (stimmbezirk, cdu, spd, fdp, afd, gruene, linke, sonstige) VALUES ({line});"
            result.write(insert + "\n")
            print(insert)

## mach die erste Funktion noch hübsch, dann kopier die zweite, Sara
## außerdem musst du noch eine Tabelle anlegen

def export_cvs2_to_sql(filename: str, result_filename: str):
    try:
        os.remove(result_filename)
    except OSError:
        pass
    df = pd.read_csv(filename)
    d_columns = [x for x in df.columns if "D" in x and x not in ["D", "D1", "D2", "D3", "D4", "D5", "D6"]]

    df["sonstige"] = df[d_columns].sum(axis=1)
    print(d_columns)
    df_neu = df[["gebiet-nr", "D1", "D2", "D3", "D4", "D5", "D6", "sonstige"]]
    df_neu = df_neu.rename(
        {"gebiet-nr": "stimmbezirk", "D1": "cdu", "D2": "spd", "D3": "fdp", "D4": "afd", "D5": "gruene", "D6": "linke"},
        axis="columns")

    df_csv = df_neu.to_csv(index=False)


    with open(result_filename, "w", encoding="utf-8") as result:
        for line in df_csv.splitlines():
            insert = f"INSERT INTO ergebnisse (stimmbezirk, cdu, spd, fdp, afd, gruene, linke, sonstige) VALUES ({line});"
            result.write(insert + "\n")
            print(insert)

if __name__ == '__main__':
    open_data = r"C:\Users\roxam\Documents\Arbeit\Datenshit_Work\OpenDataJSON.json"
    result_open_data = open_data.replace("json", "sql")
    ergebnisse = r"C:\Users\roxam\Documents\Arbeit\Datenshit_Work\StimmbezirkeKoelncsvtoxlstocsv.csv"
    result_ergebnisse_1 = ergebnisse.replace(".csv", "1.sql")
    result_ergebnisse_2 = ergebnisse.replace(".csv", "2.sql")
    export_json_to_sql(open_data, result_open_data)
    export_cvs1_to_sql(ergebnisse, result_ergebnisse_1)
    export_cvs2_to_sql(ergebnisse, result_ergebnisse_2)

