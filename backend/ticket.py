import datetime

class Ticket:

    name = "Вася"
    surname = "Сидоров"
    patronymic = "Иванович"
    valid_before = datetime.datetime.now() + datetime.timedelta(days=3)
    valid_after = datetime.datetime.now()
    parkzone = "Волшебная дубрава"
    signature = "52a6eb687cd22e80d3342eac6fcc7f2e19209e8f83eb9b82e81c6f3e6f30743b"
    def __init__(self, name, surname, patronymic, valid_after, valid_before, parkzone, signature):
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.valid_after = valid_after
        self.valid_before = valid_before
        self.parkzone = parkzone
        self.signature = signature

    def __init__(self):
        self.name = "Вася"
        self.surname = "Сидоров"
        self.patronymic = "Иванович"
        self.valid_before = datetime.datetime.now() + datetime.timedelta(days=3)
        self.valid_after = datetime.datetime.now()
        self.parkzone = "Волшебная дубрава"
        self.signature = "52a6eb687cd22e80d3342eac6fcc7f2e19209e8f83eb9b82e81c6f3e6f30743b"