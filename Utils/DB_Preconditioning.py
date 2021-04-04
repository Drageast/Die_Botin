from .ErrorHandler import DatabasePreconditioning


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

            return data if indicator == 1 else None

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

        elif exTicket["IDs"]["MessageID"] is None:
            raise DatabasePreconditioning("Das Ticket besitzt keine ID!")

        else:

            return exTicket
