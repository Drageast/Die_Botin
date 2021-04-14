## **Projekt: Botin der Neun**

Dieser Bot ist für die Community: _Destiny 2 Deutschland Community ( PlayStation )_

###### Er wurde von [DrageastLP](https://github.com/Drageast) geschrieben und von folgenden Personen getestet:
1. _Qualitätskontrolle:_ TezzQu
2. _Funktionsverwaltung:_ killerbee_5000(Uli)

###### Sonstige Contributor:
1. Loki
2. AKAII96
3. Zerberus 
4. Virussumpf
5. _Notfall Qualitätskontrolle:_ K03gang 
6. _Networking:_ TheRealLaurinator
7. LooCrank 
8. _Notfall Qualitätskontrolle:_ Jonas R.
9. Ines-agn
10. _GitHub Manager:_ Eisenschild
11. Bristerus
12. Niclas Rapp

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
`Variablen: Universals: Emojis: CustomGuild`. *Die formatierung erreichen sie, indem sie vor dem Emoji ein* \ *schreiben und dies absenden.*

##### Mongo - Datenbank:

Stellen Sie sicher, dass Sie ein gültiges [MongoDB-Konto](https://www.mongodb.com/) besitzen. Erstellen sie daraufhin ein `Cluster`
und folgen sie den Anweisungen: `How to connect to your application`. Den erhaltenen Link fügen sie in der
`config.yaml` - Datei im passendem Bereich ein. Je nachdem, wie ihre `Collection` heißt, müssen sie in der 
`config.yaml` - Datei in dem Bereich `Variablen: ClientSide: MongoDB` eintragen. Den Collection-Namen als `Base`
eintragen, die Rubrik dann passend zu `Uccount` und `Config`.

##### Webhook - Fehlerbewältigung:

Sie können für einen Kanal ihrer Wahl einen Webhook anlegen. Dort sendet der Bot bei ungeklärter korrumption einen 
ausführlichen Fehlerbericht. Wenn sie einen Webhook erstellt haben, können sie einen Link zu diesem kopieren,
diesen fügen sie in dem korrespondierendem Bereich in der `config.yaml` - Datei ein.

##### Code - Veränderung:

Wenn sie möchten, könne sie den Code verändern, dies ist relativ einfach gestaltet, da der Bot größtenteils 
Objekt-Orientiert geschrieben ist und mit einem Python-Package ausgestattet ist, wodurch Funktionen von überall 
genutzt werden, solange die Funktion in der `__init__.py` - Datei gekennzeichnet ist.

### Funktionen:

##### Ticket - System:

Der Bot besitzt ein Ticket-System, welches es sehr einfach macht, Spieler für 
eine Aktivität zu suchen. Man muss lediglich in der Kategorie `Spielersuche`
eine Nachricht schreiben, den Rest managed der Bot selbst.

##### Report - System

Wenn Spieler während der Aktivität verlassen, beleidigen oder sonstige unangebrachte 
Dinge tun, kann man den Spieler melden (Befehl: `!report @Spieler`), das führt dazu, dass wenn der Spieler sich in ein Ticket
einträgt, der Ticket-Ersteller eine Warnung über den Spieler erhält.

##### Tweepy - BungieHelp Nachrichten

Der Bot schaut jede Minute, ob der Twitter-Kanal von `BungieHelp` etwas gepostet hat, wenn dies 
der Fall ist, sendet er diesen Tweet an einen Kanal, den sie über die `config.yaml` - Datei einstellen können. 
(Dies wird über einen Webhook bewältigt.)