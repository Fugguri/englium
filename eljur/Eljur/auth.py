from bs4 import BeautifulSoup
from requests import Session, post
from aiohttp import ClientSession
import json
from eljur.Eljur.errors import _checkStatus, _checkSubdomain, _findData


class Authorization:

    async def login(self, subdomain, data):
        """
        Подключение к пользователю eljur.ru.

        :param subdomain: Поддомен eljur.ru                             // str
        :param data:      Дата, состоящая из {"username": "ваш логин",
                                              "password": "ваш пароль"} // dict

        :return: Словарь с ошибкой или с положительным ответом:         // dict
                 answer // dict
                 session // Session
                 subdomain // str
                 result // bool
        """
        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain
        print(1)
        session = ClientSession()
        url = f"https://{subdomain}.eljur.ru/ajaxauthorize"
        err = await session.post(url=url, data=data)

        checkStatus = _checkStatus(err, url)
        if "error" in checkStatus:
            return checkStatus
        del checkStatus
        _json = await err.json()
        if not _json["result"]:
            return {"error": {"error_code": -103,
                              "error_msg": _json['error'],
                              "full_error": _json}}
        del err
        print(23)

        url = f"https://{subdomain}.eljur.ru/?show=home"
        account = await session.get(url=url)
        checkStatus = _checkStatus(account, url)
        if "error" in checkStatus:
            return checkStatus
        print(account.text)
        soup = BeautifulSoup(await account.text(), 'lxml')

        sentryData = _findData(soup)
        del soup
        if not sentryData:
            return {"error": {"error_code": -104,
                              "error_msg": "Данные о пользователе не найдены."}}

        return {"answer": json.loads(sentryData[17:-1]),
                "session": session,
                "subdomain": subdomain,
                "result": True}
