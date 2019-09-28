#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import time
import io
import qrcode
from ticket import Ticket
from os.path import dirname, realpath
from base64 import b64encode
from sys import argv, exit



# Взаимодействие с сервисом работы с сообщениями осуществляется по протоколу TCP
# Запросы, ответы и оповещения о новых сообщениях передаются в виде json, например

# Изображения передаются в кодировке base64

# В данный момент реализованы следующие функции:
# 1. Отправка текстовых сообщений
# 2. Отправка изображений
# 3. Получение текстовых сообщений

# Каждый запрос к сервису содержит поле OpaqueData, которое является идентификатором и добавляется сервисом в ответ
# Для получения сообщений от пользователя необходимо подписаться, отправив команду вида:
# {"subscribe": true, "auth": "1b190253fc80765a897f0d39b13d1774dd34ee77de2116e62bc7121ab6fb625b", "opaque": 0}
# При получении нового сообщения от пользователя сервис отправляет нотификацию вида:
# {"mimetype":"com.seraphim.textmessage","sender":"8bbaa91a3a8cbc6da326ff81b68acf3826ddbfd52839e7435f4b83d67d951653","text":"\xd0\x93"}\n
# Для отправки текстового сообщения необходимо отправить команду вида:
# {"text":"Привет","mimetype":"com.seraphim.textmessage","receiver":"8bbaa91a3a8cbc6da326ff81b68acf3826ddbfd52839e7435f4b83d67d951653","opaque":1,"receiverencoding":"hash","auth":"1b190253fc80765a897f0d39b13d1774dd34ee77de2116e62bc7121ab6fb625b"}
# Отправка изображения аналогична отправке текста, только вместо ключа "text" команда должна содержать ключи "image",
# "imagethumbnail" (изображения в кодировке base64) и "imageformat" (формат "jpg" или "png").
# {"mimetype":"com.seraphim.imagemessage","receiver":"c13c4f998a3495acc795ea7fc59ab54065c0a29ed6ecb203e8b1c509ba9dfc72","opaque":2,"receiverencoding":"hash","image":"IMAGE_DATA","imagethumbnail":"IMAGE_THUMBNAIL_DATA","imageformat":"jpg","auth":"1b190253fc80765a897f0d39b13d1774dd34ee77de2116e62bc7121ab6fb625b"}

# Ключи к запросам и ответам сервиса работы с сообщениями


class ApiKeys:
    MimeType = "mimetype"  # тип сообщения
    Receiver = "receiver"  # получатель
    Text = "text"  # текст
    OpaqueData = "opaque"  # идентификатор запроса
    ReceiverEncoding = "receiverencoding"  # кодирование получателя сообщения
    Image = "image"  # изображение
    ImageThumbnail = "imagethumbnail"  # миниатюра  изображения
    ImageFormat = "imageformat"  # формат изображения
    Sender = "sender"  # отправитель
    Result = "result"  # результат выполнения
    Auth = "auth"  # аутентификация
    Subscribe = "subscribe"  # подписка на информацию


# Результаты выполнения запроса к сервису работы с сообщениями
class ApiResult:
    Ok = 0  # Запрос выполнен успешно
    JsonFieldMissing = 100  # Не переданы все обязательные поля
    ParsePacketError = 101  # Некорректный пакет
    JsonSyntaxError = 102  # Ошибка парсинга. Не хватает закрывающей скобки или запятой
    # Сервис отправки сообщений не может обработать сообщение в данный момент
    SenderNotReady = 103
    FileNotExist = 104  # Файл с контентом не существует. Возможно не было передано изображение
    BadReceiver = 105  # Некорректный получатель сообщения
    Timeout = 106  # Сервер не дождался всех фрагментов команды
    Unauthorized = 107  # Не совпал token аутентификации


# Форматы изображений
class ImageFormat:
    Jpg = "jpg"
    Png = "png"


# Типы сообщений
class MimeTypes:
    Text = "com.seraphim.textmessage"  # Текстовое
    Image = "com.seraphim.imagemessage"  # Изображение


# Варианты кодирования получателя сообщения
class ReceiverEncodings:
    Hash = "hash"  # В виде sha-256 хэш-суммы


def create_text_message(auth_token, text, receiver, opaque):
    ''' Создание текстового сообщения
    :param auth_token: токен аутентификации бота
    :param text: Текст сообщения
    :param receiver: sha-256 хэш-сумма логина получателя
    :param opaque: идентификатор запроса к API. Число
    :return: json команды
    '''

    return json.dumps(
        {ApiKeys.Text: text,
         ApiKeys.MimeType: MimeTypes.Text,
         ApiKeys.Receiver: receiver,
         ApiKeys.OpaqueData: opaque,
         ApiKeys.ReceiverEncoding: ReceiverEncodings.Hash,
         ApiKeys.Auth: auth_token}, separators=(',', ':'))


def create_image_message(auth_token, receiver, opaque, image, image_thumbnail, image_format):
    ''' Создание сообщения с изображением
    :param auth_token: токен аутентификации бота
    :param receiver: sha-256 хэш-сумма логина получателя
    :param opaque: идентификатор запроса к API. Число
    :param image: изображение, закодированное в base64
    :param image_thumbnail: миниатюра изображения, закодированная в base64
    :param image_format: формат изображения
    :return: json команды
    '''

    return json.dumps(
        {ApiKeys.MimeType: MimeTypes.Image,
         ApiKeys.Receiver: receiver,
         ApiKeys.OpaqueData: opaque,
         ApiKeys.ReceiverEncoding: ReceiverEncodings.Hash,
         ApiKeys.Image: b64encode(image).decode(),
         ApiKeys.ImageThumbnail: b64encode(image_thumbnail).decode(),
         ApiKeys.ImageFormat: image_format,
         ApiKeys.Auth: auth_token}, separators=(',', ':'))


def subscribe_to_messages(auth_token, opaque):
    ''' Подписка на сообщение от пользователя
    :param auth_token: токен аутентификации бота
    :param opaque:
    :return: json команды
    '''
    return json.dumps(
        {
            ApiKeys.Subscribe: True,
            ApiKeys.Auth: auth_token,
            ApiKeys.OpaqueData: opaque
        }
    )



