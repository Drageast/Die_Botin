from .ErrorHandler import DatabasePreconditioning
from datetime import date
import discord


class Ticket:
    def __init__(self, client):
        self.client = client

    async def create_Ticket(self, user, activity, neededParticipants: int, description, indicator: int):

        exTicket = self.client.ticket.find_one({"_id": user.id})

        if exTicket is not None:
            raise DatabasePreconditioning("Das Ticket existiert schon! Lösche bitte dein vorheriges, falls vorhanden.")

        else:

            data = \
                {
                    "_id": user.id,
                    "Activity": activity,
                    "Description": description,
                    "NeededParticipants": neededParticipants,
                    "IDs": {"MessageID": None, "ChannelID": None}
                }

            self.client.ticket.insert_one(data)

            serialized1 = serialization(data["_id"])
            serialized1.NeededParticipants = data["NeededParticipants"]
            serialized1.activity = data["Activity"]
            serialized1.description = data["Description"]
            serialized1.MID = None
            serialized1.CID = None

            return data if indicator == 1 else serialized1

    async def delete_Ticket(self, user):

        exTicket = self.client.ticket.find_one({"_id": user.id})

        if exTicket is None:
            raise DatabasePreconditioning("Das Ticket existiert nicht!")

        else:

            self.client.ticket.delete_one({"_id": user.id})

    async def edit_Ticket(self, user, edit, index: int):

        exTicket = self.client.ticket.find_one({"_id": user.id})

        if exTicket is None:
            raise DatabasePreconditioning("Das Ticket existiert nicht!")

        elif exTicket["IDs"]["MessageID"] is not None and index == 1:
            raise DatabasePreconditioning("Das Ticket besitzt schon eine ID!")

        elif exTicket["IDs"]["ChannelID"] is not None and index == 2:
            raise DatabasePreconditioning("Das Ticket besitzt schon eine ID!")

        else:

            choice = "MessageID" if index == 1 else "ChannelID"
            self.client.ticket.update_one({"_id": user.id}, {"$set": {f"IDs.{choice}": edit}})

    async def get_Ticket(self, user):

        exTicket = self.client.ticket.find_one({"_id": user.id})

        if exTicket is None:
            raise DatabasePreconditioning("Das Ticket existiert nicht!")

        elif exTicket["IDs"]["MessageID"] is None or exTicket["IDs"]["ChannelID"] is None:
            raise DatabasePreconditioning("Das Ticket besitzt keine ID!")

        else:
            data = exTicket

            serialized2 = serialization(data["_id"])
            serialized2.NeededParticipants = data["NeededParticipants"]
            serialized2.activity = data["Activity"]
            serialized2.description = data["Description"]
            serialized2.MID = data["IDs"]["MessageID"]
            serialized2.CID = data["IDs"]["ChannelID"]

            return serialized2


class Spielverderber:
    def __init__(self, client):
        self.client = client

    async def file_report(self, user, mode: int):

        _report = await Spielverderber.get_report(self, user)

        if _report is None:
            today = date.today()

            data = \
                {
                    "_id": user.id,
                    "ReportCount": 1,
                    "FirstReport": today.strftime("%d.%m.%y")
                }

            self.client.Spielverderber.insert_one(data)

        else:

            OldCount = int(_report.reports)
            NewCount = OldCount + 1 if mode == 1 else OldCount - 1

            self.client.Spielverderber.update_one({"_id": user.id}, {"$set": {f"ReportCount": int(NewCount)}})




    async def get_report(self, user):

        _report = self.client.Spielverderber.find_one({"_id": user.id})

        if _report is None:
            return None

        else:

            serialized = serialization2(user.id)
            serialized.reports = _report["ReportCount"]
            serialized.first_report = _report["FirstReport"]

            return serialized

# Object Oriented Class


class serialization:
    def __init__(self, _id):
        self._id = _id

    description = None
    activity = None
    NeededParticipants = None
    MID = None
    CID = None


class serialization2:
    def __init__(self,_id):
        self._id = _id

    reports = None
    first_report = None
