import csv
import pandas as pd

df = pd.read_csv(r"C:\Users\roxam\Documents\Arbeit\Datenshit_Work\StimmbezirkeKoelncsvtoxlstocsv.csv")
columns = list(df.columns)
d_columns = []
for clmn in columns:
    if "D" in clmn:
        d_columns.append(clmn)

df["sonstige"] = df[d_columns[:-26:-1]].sum(axis=1)
#  print(df["sonstige"])
df_neu = df[["gebiet-nr", "D1", "D2", "D3", "D4", "D5", "D6", "sonstige"]]
df_neu = df_neu.rename({"gebiet-nr":"stimmbezirk", "D1":"cdu", "D2":"spd", "D3":"fdp", "D4":"afd", "D5":"gruene", "D6":"linke"}, axis="columns")
df_csv = df_neu.to_csv(index=False)
print(df_csv)



