import datetime


class Ticket:
    def __init__(self, name="Василий Иванович Сидоров",
                 valid_after=datetime.datetime.now(), valid_before=datetime.datetime.now() + datetime.timedelta(days=3),
                 parkzone="Волшебная дубрава", signature="f9fb00138b33c7387b7809c9610a0290d50de48e2aeedcebd1373cb6c8a403e8", 
                 passport="1234567890"):
        self.name = name
        self.valid_after = valid_after
        self.valid_before = valid_before
        self.parkzone = parkzone
        self.signature = signature
        self.passport = passport


# class Ticket:
#     def __init__(self, name="Вася", surname="Сидоров", patronymic="Иванович",
#         valid_after=datetime.datetime.now(), valid_before=datetime.datetime.now() + datetime.timedelta(days=3),
#         parkzone="Волшебная дубрава", signature="f9fb00138b33c7387b7809c9610a0290d50de48e2aeedcebd1373cb6c8a403e8"):
#         self.name = name
#         self.surname = surname
#         self.patronymic = patronymic
#         self.valid_after = valid_after
#         self.valid_before = valid_before
#         self.parkzone = parkzone
#         self.signature = signature
