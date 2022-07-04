import json
import os


def load_json():
    filename = r"C:\Users\roxam\Documents\Arbeit\Datenshit_Work\OpenDataJSON.json"
    result_filename = filename.replace("json", "sql")
    try:
        os.remove(result_filename)
    except OSError:
        pass
    with open(filename, encoding='utf-8') as data:
        data = json.load(data)
        features = data["features"]
        with open(result_filename, "w", encoding="utf-8") as result:
            line = 0
            dict_unique_keys = {}
            for part in features:
                strasse = part["attributes"]["strasse"]
                hausnummer = part["attributes"]["hausnr"]
                postleitzahl = part["attributes"]["postleitzahlgebiet"]
                unique_key = f"{strasse},{hausnummer},{postleitzahl}"
                if unique_key not in dict_unique_keys:
                    dict_unique_keys[unique_key] = [line]
                else:
                    dict_unique_keys[unique_key].append(line)
                stimmbezirk = part["attributes"]["stimmbezirk"]
                insert = f"INSERT INTO adressen (strasse,hausnummer,postleitzahl,stimmbezirk) VALUES ('{strasse}','{hausnummer}',{postleitzahl}, {stimmbezirk});"
                result.write(insert + "\n")
                line += 1
            for key,lines in dict_unique_keys.items():
                if len(lines) > 1:
                    print(key, lines)

                ## if line == 100:
                    ## break

                # zeile = (strasse + ", " + hausnummer + ", " + postleitzahl + ", " + stimmbezirk)
                # print(zeile)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_json()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
