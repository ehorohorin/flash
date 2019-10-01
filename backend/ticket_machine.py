class Data():
    dict = {'Абхазия':['Одному', 'Вдвоем', 'Пятером', 'С бомжами'],
            'Сочи':['Одному', 'С бомжами', 'Куртизанки'],
            'Горы':['Помидоры', 'Лоси', 'Кони']}

    steps = ['greeting', 'parkzone', 'route_type', 'trip_dates', 'client_data', 'purchase', 'finished']

    questions = [ """ Шаг 1. Привет! Меня зовут Лева, я буду твоим гидом :) Давай выберем, что посетить:
1 - Кавказский национальный заповедник
2 - Сочинский национальный парк 
3 - Абхазская горная трасса
4 - Эверест""",
"""Шаг 2. Отличный выбор! Погрузиться в атмосферу парка тебе поможет:
1 - Экскурсия по самым непроходимым и проходимым местам
2 - Свободное путешествие 
3 - Увлекательный туристический маршрут 
4 - Фотосессия в  живописных уголках парка""",
"""Шаг 3. А теперь давай определимся с датой. Пришли в формате ДД.ММ.ГГГГ желаемый день посещения""",
"""Шаг 4. Уже столько всего обсудили, а толком не познакомились…
Введи свои данные Ф.И.О., серию и номер паспорта без пробела.
Пример: Иванов Иван Андреевич, 1635109854"""]
    custom_messages = {"sendqr":"""Шаг 5. Осталось перевести мешок золота на этот счет - 4536 3121 3131 3213.
    Шучу, это же PoC. Сейчас прилетит билет"""}




class ReacreationInfo:
    def __init__(self):
        self.step = 0
        self.state = Data().steps[self.step]
        self.question = Data().questions[self.step]
        self.answers = []
        self.user = ""

    def nextstate(self):
        try:
            self.step += 1
            self.state = Data().steps[self.step]
            self.question = Data().questions[self.step]
        except IndexError:
            return False
        



# for i in range(0, 3):
#     print(a.question)
#     user_input = input("Ну давай, жги: ")
#     a.answers.append(user_input)
#     a.nextstate()



d = Data()

# print(d.dict['Сочи'])
# print(d.states[5])
