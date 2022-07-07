# how and why to use main.py

### Das sind die Datengrundlagen
Der hier gezeigte Code liest Daten in Form einer JSON- und einer CSV-Datei aus, entsprechend der angegebenen Grundlage.
Sowohl die hausnummernscharfe Zuordnung der Stadt Köln zu Stimbezirken, als auch die Wahlergebnisse der Landtagswahl enthalten einige Daten, die für unsere Zwecke unerheblich sind. 
Erste Aufgabe (um etwa Ladezeiten zu verringern) muss also die Pflege und Auswahl der Daten sein, die wir auch wirklich brauchen.

***Achtung:** Der Datensatz der Stadt Köln der alle Adressen zu ihrem entsprechenden Stimmbezirk zuordnen soll, ist **nicht** vollständig. Nicht alle Adressen sind enthalten. Nach erster Recherche scheint es sich um eine Zuordnung aller **Gebäude** um einen Stimmbezirk zu halten. 
Das CVS-Dokument mit den Stimmen pro Stimmbezirk ist außerdem nur mit einem externen Schlüssel lesbar, Kolumnen sind nicht sprechend benannt.* 
***
### Das macht der Code

1. Wir importieren die python directories, die wir brauchen
- **json:** Allgemeiner Umgang mit dem Dateiformat
- **os:** Allgemeine Funktionalität
- **pandas:** Statistische Datenaufbereitung und Visualisierung

2. Wir definieren die Funktionen, die wir brauchen um die Daten aufzubereiten, zu sortieren und in ein Datenbank-lesbares Format zu bringen.
- **export_json_to_sql:** Extrahiert die Daten, die für uns interessant sind: Straße, Hausnummer, Postleitzahlgebiet und Stimmbezirk. 
Schreibt dann die so ausgelesenen Informationen in eine SQL-Datei, sodass für jedes Set ein eigener Eintrag entsteht.
- **export_csv1_to_sql:**  Extrahiert die Daten, die für uns interessant sind: Stimmbezirk, Wahlergebnisse der Parteien cdu, spd, fdp, afd, gruene und linke. Rechnet dann die Ergebnisse der anderen Parteien zusammen. Schreibt alles in ein neues CSV-Format und schließlich in eine SQL-Datei, sodass für jedes Set ein neuer Eintrag entsteht.
- **export_csv2_to_sql:** Analog zu **export_csv1_to_sql**, nur für die Zweitstimmen der Parteien.
- **remove_if_exists:** Ersetzt eventuell schon vorhandene sql-Dateien durch neu generierte Version.

3. Wir zeigen, wo die Dateien liegen, mit denen wir arbeiten wollen. Wir speichern die Pfade in Variablen und geben diese als Parameter an die Funktionen. Wir generieren Dateinamen für die sql-Dateien aus den Datenquellen.
***
###Das soll mit den so erzeugten Dateien passieren
Die Erstellung von SQLite-Datenbanken stellt sicher, dass unsere Daten nicht nur inhaltlich, sondern auch formal bereinigt sind - doppelte oder nicht ausgefüllte Zeilen werden ausgeschlossen, die Formate einheitlich festgelegt.

Im openapi-Dokument beschreiben wir die Anforderungen, die wir an eine API haben. Diesen Prozess geben wir an jeweils eine/n Front- und eine/n Backendentwickler ab. 
Wir gehen davon aus, dass beide jeweils etwa einen bis zwei Tage beschäftigt werden müssten, um die API zu schreiben.
Wie in dem Dokument genauer erläutert, arbeiten wir mit zwei (bzw. drei) Abfragen: Der Leser oder die Leserin gibt ihre Adresse ein. 
Die API gibt dann den dazugehörigen Stimmbezirk zurück (Schritt 1). Dieser Stimmbezirk ist die Grundlage für die zweite Abfrage, die die Erststimmen-Ergebnisse zurück gibt, die dem Stimmbezirk zugeordnet sind (Schritt 2) - und entsprechend nochmal mit den Zweitstimmen-Ergebnissen (Schritt 3).
Zu klären mit dem Haus sind Serverkapazitäten sowie Einbindung im CMS. 
