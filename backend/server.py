import socket
import json
import time
import io
import qrcode
from ticket import Ticket
from os.path import dirname, realpath
from base64 import b64encode
from sys import argv, exit
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import datetime
from api import create_text_message
from api import subscribe_to_messages
from api import create_image_message


from api import ImageFormat
from api import ApiKeys
from api import ApiResult

import gzip
import threading
import sched
import time


from ticket_machine import Data
from ticket_machine import ReacreationInfo


OPAQUE = 0
KEEP_ALIVE_TIME = 120
resubber = sched.scheduler(time.time, time.sleep)


def resub(sock, token):
    msg = subscribe_to_messages(token, '7746655173')
    print(msg)
    print("subscribing another time")
    sock.sendall(bytes(msg, 'utf-8'))
    t = threading.Timer(KEEP_ALIVE_TIME, resub, [sock, token])
    t.start()


def sign_ticket(ticket, private_key):
    # ticket_data_json = json.dumps(
    #     ticket.__dict__, indent=4, sort_keys=True, default=str, ensure_ascii=False)
    ticket_data = f"{ticket.name};{ticket.parkzone};{ticket.valid_after};{ticket.valid_before};{ticket.passport}"
    print(ticket_data)
    ticket_bytes = bytearray(ticket_data, 'utf-8')
    signature = private_key.sign(
        ticket_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256())
    ticket.signature = signature.hex()
    return ticket


def get_ticket_qr_code(ticket):
    ticket_data_json = json.dumps(
        ticket.__dict__, indent=4, sort_keys=True, default=str, ensure_ascii=False)
    # ticket_data_json = gzip.compress(bytes(ticket_data_json, 'utf-8'))
    qr_code_bytes = io.BytesIO()
    qr_code_image = qrcode.make(ticket_data_json)
    qr_code_image.save(qr_code_bytes, format='PNG')
    qr_code_bytes = qr_code_bytes.getvalue()
    return qr_code_bytes, qr_code_image


def get_ticket_qr_code_thumbnail(full_image):
    qr_code_thumbnail = io.BytesIO()
    size = 512, 512
    full_image.thumbnail(size)
    full_image.save(qr_code_thumbnail, format='PNG')
    qr_code_thumbnail = qr_code_thumbnail.getvalue()
    return qr_code_thumbnail


def send_message(token, message, connection_socket, receiver, id):
    echo_msg = create_text_message(
        token, message, receiver, id)
    connection_socket.sendall(bytes(echo_msg, 'utf-8'))


def check_input(message, user_step):
    errMsg = ""
    if user_step == 0:
        return True
    elif user_step == 1:
        try:
            return message.isdigit() and int(message) < 5 and int(message) > 0
        except ValueError:
            return False
    elif user_step == 2:
        try:
            return message.isdigit() and int(message) < 5 and int(message) > 0
        except ValueError:
            return False
    elif user_step == 3:
        try:
            date = datetime.datetime.strptime(message, "%d.%m.%Y")
            if date.date() < datetime.datetime.now().date():
		errMsg="Выберите дату из будущего"
                return False
            return True
        except ValueError:
            return False
    elif user_step == 4:
        if message.count(',') != 2:
	    errMsg = "Используйте формат ввода (через запятую): Имя, паспортные данные"
            return False
        return True
    else:
        return True


if __name__ == '__main__':
    if (len(argv) < 4):
        print("Нужно передать параметры: IP адрес, порт, токен")
        exit(0)
    ip_addr = argv[1]  # IP адрес, например 127.0.0.1
    port = int(argv[2])  # порт, например 20000
    auth_token = argv[3]  # токен аутентификации бота
    print(auth_token)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip_addr, port))
    msg = subscribe_to_messages(auth_token, OPAQUE)
    print(msg)
    sock.sendall(bytes(msg, 'utf-8'))
    # OPAQUE += 1

    key_file = open("private_key.rsa", "rb")
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

    datafile = Data()
    user_statuses = {}

    key_file.close()
    t = threading.Timer(KEEP_ALIVE_TIME, resub, [sock, auth_token])
    t.start()
    while True:
        data = sock.recv(1024)

        if data:
            print('Received', data)
            # Так как мы вычитываем раз в секунду, у нас может накопиться несколько сообщений от сервера:
            # {"opaque": 2,  "result": 0}\n{"opaque": 3,  "result": 0}\n
            # необходимо их разделить перед передачей в парсер
            messages = data.split(b"\n")
            for encoded_msg in messages:
                if encoded_msg:
                    msg = json.loads(encoded_msg)
                    # входящее сообщение от пользователя
                    if msg.__contains__(ApiKeys.Sender):
                        user = msg[ApiKeys.Sender]
                        user_message = msg[ApiKeys.Text]
                        try:
                            user_step = len(user_statuses[user].keys())
                        except KeyError:
                            user_step = 0
                            user_statuses[user] = {}

                        if check_input(user_message, user_step):
                            try:
                                user_statuses[user].update(
                                    {user_step: user_message})
                                user_dialog = datafile.questions[user_step]
                                send_message(auth_token, user_dialog,
                                             sock, user, user_step)
                            except IndexError:

                                with open('data.txt', 'a', encoding='utf-8') as file:
                                    file.write(json.dumps(
                                        user_statuses, indent=4, sort_keys=True, default=str, ensure_ascii=False))
                                user_dialog = datafile.custom_messages['sendqr']
                                send_message(auth_token, user_dialog,
                                             sock, user, user_step)
                                parkname = user_statuses[user][1].replace("1", "Кавказский национальный заповедник").replace(
                                    "2", "Сочинский национальный парк").replace("3", "Абхазская горная трасса").replace("4", "Эверест")
                                user_ticket_choice = user_statuses[user][2].replace("1", "Экскурсия по самым непроходимым и проходимым местам").replace(
                                    "2", "Свободное путешествие").replace("3", "Увлекательный туристический маршрут").replace("4", "Фотосессия в  живописных уголках парка")
                                passport_parsed = user_statuses[user][4].split(',')[
                                    1].replace(' ', '')
                                person_ticket = Ticket(name=user_statuses[user][4],
                                                       valid_after=datetime.datetime.strptime(
                                    user_statuses[user][3], "%d.%m.%Y"),
                                    valid_before=datetime.datetime.strptime(
                                    user_statuses[user][3], "%d.%m.%Y") + datetime.timedelta(days=3),
                                    parkzone=parkname, passport=passport_parsed,
                                    ticket_type=user_ticket_choice)
                                qr_code, qr_image = get_ticket_qr_code(
                                    person_ticket)
                                qr_code_thumbnail = get_ticket_qr_code_thumbnail(
                                    qr_image)
                                echo_image = create_image_message(auth_token, msg[ApiKeys.Sender], OPAQUE, qr_code,
                                                                  qr_code_thumbnail, ImageFormat.Png)
                                sock.sendall(bytes(echo_image, 'utf-8'))
                                # user_dialog = """Шаг 5. Осталось перевести мешок золота на этот счет - 4536 3121 3131 3213.
                                # Шучу, это же PoC. Сейчас прилетит билет"""
                                # send_message(auth_token, user_dialog,
                                #              sock, user, user_step)
                                date_after = person_ticket.valid_after.strftime(
                                    "%m-%d-%Y")
                                date_before = person_ticket.valid_before.strftime(
                                    "%m-%d-%Y")
                                user_dialog = f"Ура, вы купили билет.\nВаши данные:\n{person_ticket.name}\nМесто: {person_ticket.parkzone}\nТип билета: {person_ticket.ticket_type}\nДаты поездки: {date_after} - {date_before}\nВозьмите билет еще и другу!"

                                send_message(auth_token, user_dialog,
                                             sock, user, user_step)
                                user_step = 0
                                user_statuses[user] = {}
                        else:
                            user_dialog = "Вы что-то вели неправильно, попробуйте еще раз"
                            send_message(auth_token, user_dialog,
                                         sock, user, user_step)
                    # результат выполнения запроса
                    elif msg.__contains__(ApiKeys.OpaqueData):
                        # здесь можно обработать ошибки
                        if int(msg[ApiKeys.Result]) != ApiResult.Ok:
                            print("error :", msg[ApiKeys.Result])
        print("sleeping 1 sec")
        time.sleep(1)
