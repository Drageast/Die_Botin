# Import
from .ErrorHandler import DatabasePreconditioning
import discord
from .Util import WrapperDecorator


class Sterilization_Uccount:
    def __init__(self, _id, Reports):
        self._id = _id
        self.Reports = Reports


class DBPreconditioning:
    def __init__(self, client):
        self.client = client


    @staticmethod
    @WrapperDecorator.TimeLogger
    def sterilize(data):

        _id = data["_id"]
        _Reports = data["Reports"]

        Sterilized_Data = Sterilization_Uccount(_id, _Reports)

        return Sterilized_Data

    @staticmethod
    @WrapperDecorator.TimeLogger
    async def POST_Uccount(self, user: discord.Member, Reports: int = 0):
        _data = self.client.Uccount.find_one({"_id": user.id})

        if _data is None:

            data = \
                {
                    "_id": user.id,
                    "Reports": Reports
                }

            self.client.Uccount.insert_one(data)

        elif _data is not None and Reports != 0:

            data_ = await DBPreconditioning.GET_Uccount(self, user)

            CurrentReports = int(data_.Reports)
            NewReports = CurrentReports + 1

            self.client.Uccount.update_one({"_id": user.id}, {"$set": {"Report": NewReports}})


    @staticmethod
    @WrapperDecorator.TimeLogger
    async def GET_Uccount(self, user: discord.Member):
        _data = self.client.Uccount.find_one({"_id": user.id})

        if _data is None:

            await DBPreconditioning.POST_Uccount(self, user)

            data_ = self.client.Uccount.find_one({"_id": user.id})

            Sterilized_Data = DBPreconditioning.sterilize(data_)

            return Sterilized_Data

        else:

            Sterilized_Data = DBPreconditioning.sterilize(_data)

            return Sterilized_Data


    @staticmethod
    @WrapperDecorator.TimeLogger
    async def DEL_Uccount(self, user: discord.Member):
        _data = DBPreconditioning.GET_Uccount(self, user)

        if _data is None:
            raise DatabasePreconditioning(f"Der Uccount mit der _id: {user.id} existiert nicht")

        else:
            self.client.ticket.delete_one({"_id": user.id})
