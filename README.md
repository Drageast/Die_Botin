## **Projekt: Botin der Neun**

Dieser Bot ist für die Community: _Destiny 2 Deutschland Community ( PlayStation )_

###### Er wurde von [DrageastLP](https://github.com/Drageast) geschrieben und von folgenden Personen getestet:
1. _Qualitätskontrolle:_ TezzQu
2. _Funktionsverwaltung:_ killerbee_5000(Uli)
3. _Auftraggeber:_ papabaer29

##### Genutzte pip – Pakete sind:

- [Discord.py](https://pypi.org/project/discord.py/)
- [Requests](https://pypi.org/project/requests/)
- [PyYaml](https://pypi.org/project/PyYAML/)
- [PyMongo](https://pypi.org/project/pymongo/)
- [PyNaCl](https://pypi.org/project/PyNaCl/)
- [Dnspython](https://pypi.org/project/dnspython)

### Modularität:

Der Discord Bot ist extra modular gestaltet, damit man ihn sehr einfach auf einen
Server anpassen kann. Dazu verändert man die benötigten Informationen in der `config.yaml` - Datei.
Diese Datei finden sie in dem Ordner: `Utils`. Bitte beachten Sie, keine Codestücke zu
modifizieren, es sei denn, es wird zur Konfiguration verlangt.
Zu Beginn, fügen sie ihren Bot-Token in der `config.yaml` - Datei in dem Bereich:
`Variablen: ClientSide: Token` ein. *Diesen finden sie in ihrer [Applikation](https://discord.com/developers/applications)*. Sie können auch 
den Präfix in dem korrespondierendem Bereich ändern. Darauf hinaus, fügen sie Emojis auf dem Server
hinzu und setzten sie diese in der richtigen formatierung in den Bereich: 
`Variablen: UniversalEmoji`. *Die formatierung erreichen sie, indem sie vor dem Emoji ein* \ *schreiben und dies absenden.*

#### Mongo - Datenbank:

Stellen Sie sicher, dass Sie ein gültiges [MongoDB-Konto](https://www.mongodb.com/) besitzen. Erstellen sie daraufhin ein `Cluster`
und folgen sie den Anweisungen: `How to connect to your application`. Den erhaltenen Link fügen sie in der
`config.yaml` - Datei im passendem Bereich ein. Je nachdem, wie ihre `Collection` heißt, müssen sie in dem Skrip:
`Main.py` in **Zeile 27** unter `client.mongo["Cluster Name"]["Colection Name"]` die Namen anpassen.

##### Webhook - Fehlerbewältigung

Sie können für einen Kanal ihrer Wahl einen Webhook anlegen. Dort sendet der Bot bei ungeklärter korrumption einen 
ausführlichen Fehlerbericht. Wenn sie einen Webhook erstellt haben, können sie einen Link zu diesem kopieren,
diesen fügen sie in dem korrespondierendem Bereich in der `config.yaml` - Datei ein.