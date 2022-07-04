import json
import os


def export_json_to_sql(filename: str):
    result_filename = filename.replace("json", "sql")
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


if __name__ == '__main__':
    open_data = r"C:\Users\roxam\Documents\Arbeit\Datenshit_Work\OpenDataJSON.json"
    export_json_to_sql(open_data)
