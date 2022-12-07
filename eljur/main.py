from Eljur.auth import Authorization
from Eljur.journal import Journal
from Eljur.profile import Profile


def run():
    authorisation = Authorization()

    data = {
        "username": "fygguri",
        "password": "Neskazu1"
    }
    subdomain = "englium"

    answer = authorisation.login(subdomain, data)
    if "session" not in answer:
        print(answer)
        return
    print(answer)
    profile = Profile()
    # В ответ возвращает информацию о профиле пользователя.
    answ = profile.getProfile(subdomain, answer["session"])
    for i in answ:
        yield i, answ[i]


if __name__ == "__main__":
    run()
