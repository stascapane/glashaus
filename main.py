import json
import os
import pandas as pd


def remove_if_exists(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def export_json_to_sql(filename: str, result_filename: str):
    remove_if_exists(result_filename)

    with open(filename, encoding='utf-8') as data:
        data = json.load(data)
        features = data["features"]

        with open(result_filename, "w", encoding="utf-8") as result:
            for part in features:
                attributes_ = part["attributes"]
                strasse = attributes_["strasse"]
                hausnummer = attributes_["hausnr"]
                postleitzahl = attributes_["postleitzahlgebiet"]
                stimmbezirk = attributes_["stimmbezirk"]
                insert = f"INSERT INTO adressen (strasse,hausnummer,postleitzahl,stimmbezirk) VALUES ('{strasse}','{hausnummer}',{postleitzahl}, {stimmbezirk});"
                result.write(insert + "\n")


def export_cvs1_to_sql(filename: str, result_filename: str):
    remove_if_exists(result_filename)
    df = pd.read_csv(filename)

    d_columns = [x for x in df.columns if "D" in x and x not in ["D", "D1", "D2", "D3", "D4", "D5", "D6"]]
    df["sonstige"] = df[d_columns].sum(axis=1)

    df_neu = df[["gebiet-nr", "D1", "D2", "D3", "D4", "D5", "D6", "sonstige"]]
    df_neu = df_neu.rename(
        {"gebiet-nr": "stimmbezirk", "D1": "cdu", "D2": "spd", "D3": "fdp", "D4": "afd", "D5": "gruene", "D6": "linke"},
        axis="columns")

    df_csv = df_neu.to_csv(index=False)

    with open(result_filename, "w", encoding="utf-8") as result:
        for line in df_csv.splitlines():
            insert = f"INSERT INTO ergebnisse (stimmbezirk, cdu, spd, fdp, afd, gruene, linke, sonstige) VALUES ({line});"
            result.write(insert + "\n")


def export_cvs2_to_sql(filename: str, result_filename: str):
    remove_if_exists(result_filename)
    df = pd.read_csv(filename)

    f_columns = [x for x in df.columns if "F" in x and x not in ["F", "F1", "F2", "F3", "F4", "F5", "F6"]]
    df["sonstige"] = df[f_columns].sum(axis=1)

    df_neu = df[["gebiet-nr", "F1", "F2", "F3", "F4", "F5", "F6", "sonstige"]]
    df_neu = df_neu.rename(
        {"gebiet-nr": "stimmbezirk", "F1": "cdu", "F2": "spd", "F3": "fdp", "F4": "afd", "F5": "gruene", "F6": "linke"},
        axis="columns")

    df_csv = df_neu.to_csv(index=False)

    with open(result_filename, "w", encoding="utf-8") as result:
        for line in df_csv.splitlines():
            insert = f"INSERT INTO ergebnisse2 (stimmbezirk, cdu, spd, fdp, afd, gruene, linke, sonstige) VALUES ({line});"
            result.write(insert + "\n")


if __name__ == '__main__':
    open_data = r"C:\Users\roxam\Documents\Arbeit\Datenshit_Work\OpenDataJSON.json"
    result_open_data = open_data.replace("json", "sql")
    export_json_to_sql(open_data, result_open_data)

    ergebnisse = r"C:\Users\roxam\Documents\Arbeit\Datenshit_Work\StimmbezirkeKoelncsvtoxlstocsv.csv"

    result_ergebnisse_1 = ergebnisse.replace(".csv", "1.sql")
    export_cvs1_to_sql(ergebnisse, result_ergebnisse_1)

    result_ergebnisse_2 = ergebnisse.replace(".csv", "2.sql")
    export_cvs2_to_sql(ergebnisse, result_ergebnisse_2)