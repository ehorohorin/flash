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

from api import create_text_message
from api import subscribe_to_messages
from api import create_image_message



from api import ImageFormat
from api import ApiKeys
from api import ApiResult

import gzip



OPAQUE = 0

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
    OPAQUE += 1

    key_file = open("private_key.rsa", "rb")
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

    key_file.close()
    

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

                        

                        person_ticket = Ticket(signature="")
                        
                        ticket_data_json = json.dumps(
                            person_ticket.__dict__, indent=4, sort_keys=True, default=str, ensure_ascii=False)

                        print("-----------------json---------------")
                        print(ticket_data_json)
                        ticket_bytes = bytearray(ticket_data_json, 'utf-8')
                        signature = private_key.sign(
                        ticket_bytes,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256())
                        person_ticket.signature = signature.hex()
                        ticket_data_json = json.dumps(
                            person_ticket.__dict__, indent=4, sort_keys=True, default=str, ensure_ascii=False)
                            
                        echo_msg = create_text_message(
                            auth_token, ticket_data_json, msg[ApiKeys.Sender], OPAQUE)
                        print(echo_msg)
                        sock.sendall(bytes(echo_msg, 'utf-8'))
                        OPAQUE += 1
                        ticket_data_json = gzip.compress(bytes(ticket_data_json, 'utf-8'))
                        # make qr code
                        qr_code_bytes = io.BytesIO()
                        qr_code_image = qrcode.make(ticket_data_json)
                        qr_code_image.save(qr_code_bytes, format='PNG')
                        qr_code_bytes = qr_code_bytes.getvalue()

                        # make thubmnail for qr code
                        qr_code_thumbnail = io.BytesIO()
                        size = 512, 512
                        qr_code_image.thumbnail(size)
                        qr_code_image.save(qr_code_thumbnail, format='PNG')
                        qr_code_thumbnail = qr_code_thumbnail.getvalue()

                        echo_image = create_image_message(auth_token, msg[ApiKeys.Sender], OPAQUE, qr_code_bytes,
                                                          qr_code_thumbnail, ImageFormat.Png)
                        
                        OPAQUE += 1
                        sock.sendall(bytes(echo_image, 'utf-8'))
                    # результат выполнения запроса
                    elif msg.__contains__(ApiKeys.OpaqueData):
                        # здесь можно обработать ошибки
                        if int(msg[ApiKeys.Result]) != ApiResult.Ok:
                            print("error :", msg[ApiKeys.Result])
        print("sleeping 1 sec")
        time.sleep(1)