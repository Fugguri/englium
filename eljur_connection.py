from eljur.Eljur.auth import Authorization
from eljur.Eljur.journal import Journal, Journal2
from eljur.Eljur.profile import Profile
from eljur.Eljur.portfolio import Portfolio


class Eljur():
    def __init__(self) -> None:
        self.authorisation = Authorization()

        self.subdomain = "englium"


def is_login(login, password):
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
    profile = Profile()
    # В ответ возвращает информацию о профиле пользователя.
    answ = profile.getProfile(subdomain, answer["session"])
    result = []
    for i in answ:
        i, answ[i]
        result.append(i)
        result.append(answ[i])
    return result


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


def journal(login, password, week=0):
    authorisation = Authorization()
    data = {
        "username": login,
        "password": password,
    }
    subdomain = "englium"

    answer = authorisation.login(subdomain, data)
    if "session" not in answer:
        print(answer)
        return

    journal = Journal2()

    # В ответ получает нынешнюю неделю или ошибку.
    answ = journal.journal2(subdomain, answer["session"], week=week)
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


def quart(login, password, week=0):
    authorisation = Authorization()
    data = {
        "username": login,
        "password": password,
    }
    subdomain = "englium"

    answer = authorisation.login(subdomain, data)
    if "session" not in answer:
        print(answer)
        return

    journal = Journal2()
    # В ответ получает нынешнюю неделю или ошибку.
    answ = []
    while journal.journal2(subdomain, answer["session"], week=week) != "Задание на каникулы":
        week -= 1
        answ.append(journal.journal2(subdomain, answer["session"], week=week))

    return answ


if __name__ == "__main__":
    print(journal("fygguri", "Neskazu1"))
