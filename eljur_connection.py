from eljur.Eljur.auth import Authorization
from eljur.Eljur.journal import Journal, Journal2
from eljur.Eljur.portfolio import Portfolio


class Eljur():
    def __init__(self) -> None:
        self.authorisation = Authorization()
        self.subdomain = "englium"


def auth(login, password):
    authorisation = Authorization()
    data = {
        "username": login,
        "password": password
    }
    subdomain = "englium"

    try:
        authorisation.login(subdomain, data)
        return True
    except:
        return False


async def journal(login, password, week=0):
    authorisation = Authorization()
    data = {
        "username": login,
        "password": password,
    }
    subdomain = "englium"

    answer = await authorisation.login(subdomain, data)
    if "session" not in answer:
        return

    journal = Journal2()

    # В ответ получает нынешнюю неделю или ошибку.
    answ = await journal.journal2(subdomain, answer["session"], week=week)
    await answer["session"].close()

    return answ


def reportCard(login, password, week=0):
    authorisation = Authorization()
    data = {
        "username": login,
        "password": password
    }
    subdomain = "englium"

    answer = authorisation.login(subdomain, data)
    if "session" not in answer:
        print(answer)
        return
    portfolio = Portfolio()
    # В ответ получает оценки ученика или ошибку.
    answ = portfolio.reportCard(
        subdomain, answer["session"], answer["answer"]["user"]["uid"])
    return answ


async def quart(login, password, week=0):
    authorisation = Authorization()
    data = {
        "username": login,
        "password": password,
    }
    subdomain = "englium"

    answer = await authorisation.login(subdomain, data)
    if "session" not in answer:
        print(answer)
        return

    journal = Journal2()
    # В ответ получает нынешнюю неделю или ошибку.
    answ = []
    current_week = await journal.journal2(subdomain, answer["session"], week=week)
    while current_week != "Задание на каникулы":
        week -= 1
        current_week = await journal.journal2(subdomain, answer["session"], week=week)
        answ.append(current_week)
    await answer["session"].close()
    return answ


if __name__ == "__main__":
    print(journal("fygguri", "Neskazu1"))
