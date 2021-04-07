# Import
from .ErrorHandler import DatabasePreconditioning
import discord


class Sterilization_Ticket:
    def __init__(self, _id, RequiredParticipants, MessageID, ChannelID):
        self._id = _id
        self.RequiredParticipants = RequiredParticipants
        self.ChannelID = ChannelID
        self.MessageID = MessageID


class Sterilization_Uccount:
    def __init__(self, _id, Reports, TicketEntry):
        self._id = _id
        self.Reports = Reports
        self.TicketEntry = TicketEntry


class DBPreconditioning:
    def __init__(self, client):
        self.client = client


    @staticmethod
    def sterilize(data, _type):

        if _type is Sterilization_Ticket:
            _id = data["_id"]
            _RequiredParticipants = data["RequiredParticipants"]
            _ChannelID = data["IDs"]["ChannelID"]
            _MessageID = data["IDs"]["MessageID"]

            Sterilized_Data = _type(_id, _RequiredParticipants, _MessageID, _ChannelID)

            return Sterilized_Data

        elif _type is Sterilization_Uccount:
            _id = data["_id"]
            _Reports = data["Reports"]
            _TicketEntry = data["TicketEntry"]

            Sterilized_Data = _type(_id, _Reports, _TicketEntry)

            return Sterilized_Data


    @staticmethod
    def POST_Ticket(self, user: discord.Member, RequiredParticipants: int, ChannelID: int, MessageID: int):
        _data = self.client.ticket.find_one({"_id": user.id})

        if _data is None and RequiredParticipants is not None:

            data = \
                {
                    "_id": user.id,
                    "RequiredParticipants": RequiredParticipants,
                    "IDs":
                        {
                            "ChannelID": ChannelID,
                            "MessageID": MessageID,
                        }
                }

            self.client.ticket.insert_one(data)

        elif _data["IDs"]["ChannelID"] is None and RequiredParticipants is None and ChannelID is not None and MessageID is not None:

            self.client.ticket.update_one({"_id": user.id}, {"$set": {"IDs.ChannelID": ChannelID}})
            self.client.ticket.update_one({"_id": user.id}, {"$set": {"IDs.MessageID": MessageID}})

        else:
            raise DatabasePreconditioning(f"Das Ticket für _id: {user.id} existiert bereits."
                                          f"\nWenn du dies für einen Fehler in der Datenbank hältst, gebe: `!debug ticket` ein")


    @staticmethod
    def GET_Ticket(self, user: discord.Member):
        _data = self.client.ticket.find_one({"_id": user.id})

        if _data is None:
            return None

        else:
            Sterilized_Data = DBPreconditioning.sterilize(_data, Sterilization_Ticket)
            return Sterilized_Data


    @staticmethod
    async def DEL_Ticket(self, user: discord.Member):
        _data = DBPreconditioning.GET_Ticket(self, user)

        if _data is None:
            raise DatabasePreconditioning(f"Das Ticket mit der _id: {user.id} existiert nicht")

        elif _data.ChannelID is None or _data.MessageID is None:
            self.client.ticket.delete_one({"_id": user.id})

        else:
            self.client.ticket.delete_one({"_id": user.id})
            try:
                channel = self.client.get_channel(_data.ChannelID)
                m = await channel.fetch_message(_data.MessageID)
                await m.delete()
            except:
                pass


    @staticmethod
    def POST_Uccount(self, user: discord.Member, Reports: int = None, TicketEntry: bool = False):
        _data = self.client.Uccount.find_one({"_id": user.id})

        if _data is None:

            data = \
                {
                    "_id": user.id,
                    "TicketEntry": TicketEntry,
                    "Reports": Reports
                }

            self.client.Uccount.insert_one(data)

        elif _data is not None and Reports is not None:

            data_ = DBPreconditioning.GET_Uccount(self, user)

            CurrentReports = int(data_.Reports)
            NewReports = CurrentReports + 1

            self.client.Uccount.update_one({"_id": user.id}, {"$set": {"Report": NewReports}})

        elif _data is not None and Reports is None:

            self.client.Uccount.update_one({"_id": user.id}, {"$set": {"TicketEntry": TicketEntry}})


    @staticmethod
    def GET_Uccount(self, user: discord.Member):
        _data = self.client.Uccount.find_one({"_id": user.id})

        if _data is None:
            DBPreconditioning.POST_Uccount(self, user)

        data_ = self.client.Uccount.find_one({"_id": user.id})

        Sterilized_Data = DBPreconditioning.sterilize(data_, Sterilization_Uccount)
        return Sterilized_Data


    @staticmethod
    def DEL_Uccount(self, user: discord.Member):
        _data = DBPreconditioning.GET_Uccount(self, user)

        if _data is None:
            raise DatabasePreconditioning(f"Der Uccount mit der _id: {user.id} existiert nicht")

        else:
            self.client.ticket.delete_one({"_id": user.id})
