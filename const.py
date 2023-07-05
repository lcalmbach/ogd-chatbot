FIRST_PROMPT = """Frag mich etwas zu den Themen "Fischfang im Rhein, Birs, Wiese" oder zu den "Vornamen der Baselstädtischen Bevölkerung" oder zu täglichen Wetterdaten
"""

INTENT_LIST = [
    "Vornamen",
    "Fische",
    "Tägliche Wetter oder Klimadaten",
]

INTENT_PROMPT = f"""In welche Kategorie gehört folgende Frage: ###{{}}###. Wähle aus folgenden Kategorien aus: {'|'.join(INTENT_LIST)}
Antwort Format: Index der passenden Kategorie. Wenn keine Kategorie zutrifft dann antworte mit -99
Mögliche Antworten: [0, 1, 2, -99]
Beispiele: 
Beispiel 1: Frage: "Wieviele Fische wurden total in 2011 gefangen und im welchen Monat waren es die meisten?" Antwort: 1
Beispiel 2: Frage: "Welches war der häufigste männliche Vorname im Jahr 2015?" Antwort: 0
Beispiel 3: Frage: "Wieviele Brücken gibt es in Basel" Antwort: -99

"""

THEME_PROMPT = "Zu welchem Thema möchtest du denn gerne etwas wissen, ich kann dir folgendes bieten: Vornamen, Fischfang in Basel oder tägliche Klimadaten"

# unused as it confuses the model and always tries to reproduce one of the examples
INTENT_DICT = {
    0: """{{}}. Verwende Tabelle vornamen. Wenn nach Anzahl eines Vornamens gefragt wird, summiere die Spalte 'Anzahl'
    """,
    1: """{{}}. Wenn kein Gewässer-Kriterium genannt wird, verwende keinen Filter auf die gewaesser-Spalte
    Wenn nach laenge sortiert wird, sortiere in der desc Reihenfolge: ###order by laenge desc limit 1###
    Wenn nach längstem Fisch gefragt wird, setze Kriterium ###laenge is not not null###
    Wenn nach Fischart gefragt wird, setze Kriterium ###fischart is not not null###
    """,
}
