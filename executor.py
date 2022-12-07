import time


def unpack(a):
    if a != {}:
        result = ""
        for date in a:
            print(a)
            result += "<b>День недели: " + date + "</b> \n"
            result += "<b>Дата: </b>" + a[date]["date"] + "\n"
            for lesson in a[date]["lessons"]:
                result += "<b>Время занятия: </b>" + \
                    a[date]["lessons"][lesson]['time'] + "\n"
                result += "<b>Название предмета: </b>" + \
                    a[date]["lessons"][lesson]['name'] + "\n"
                if a[date]["lessons"][lesson]['hometask'] is None:
                    result += "<b>Домашняя работа: </b>" + "\n"
                else:
                    result += "<b>Домашняя работа: </b>" + \
                        a[date]["lessons"][lesson]['hometask'] + "\n"
                if a[date]["lessons"][lesson]['mark'] == None:

                    result += "<b>Оценки за урок: </b>" + "\n"
                else:
                    result += "<b>Оценки за урок: </b>" + ":" + \
                        str(a[date]["lessons"][lesson]['mark']) + "\n"
                result += "\n"
        return result
    else:
        return "Выходные"


def weeks(data, is_next=False):
    out = []
    for a in data:
        if a != {}:
            for date in a:
                try:
                    data[a]["date"]
                except:
                    break
                result = ""
                result += "<b>Дата: </b>" + data[a]["date"] + "\n"
                for lesson in data[a]["lessons"]:
                    names = [i[0]
                             for i in data[a]["lessons"][lesson]["degrees"]]
                    result += "<b>" + lesson + "</b>\n"
                    for i in data[a]["lessons"][lesson]["hometask"]:
                        result += f"<b>Домашнее задание: </b>{i}\n"
                    if is_next == False:
                        if "Homework" not in names:
                            result += "<b>Homework</b> ❗️\n"
                        if "quiz" not in names and lesson == "Английский язык":
                            result += "<b>quiz</b> ❗️\n"
                        for d in data[a]["lessons"][lesson]["degrees"]:
                            name = d[0]
                            value = d[1]
                            comm = d[2]

                            if name in ["Classwork", "classwork"] and value in ["2", "Н"]:
                                name += ":❗️"
                            if name in ["Homework", "Test", "test", "quiz", "homework", "Quiz"] and value in ["2", "Н", " ", ""]:
                                name += ":❗️"

                            result += "<b>" + name + "</b> "
                            if ":" not in name:
                                result += "<b>:</b> "
                            result += value + " "
                            result += comm + " "

                            result += "\n"

                    result += "\n"
            out.append(result)
    return " ".join(out)


def degrees(data):
    out = []

    for a in data:
        if a != {}:
            for date in a:
                try:
                    a[date]["date"]

                except:

                    break
                result = ""
                result += "<b>Дата: </b>" + a[date]["date"] + "\n"

                for lesson in a[date]["lessons"]:

                    names = [i[0]
                             for i in a[date]["lessons"][lesson]["degrees"]]
                    result += "<b>" + lesson + "</b>\n"
                    for i in a[date]["lessons"][lesson]["hometask"]:
                        result += f"<b>Домашнее задание: </b>{i}\n"
                    if "Homework" not in names:
                        result += "<b>Homework</b> ❗️\n"
                    if "quiz" not in names and lesson == "Английский язык":
                        result += "<b>quiz</b> ❗️\n"

                    for d in a[date]["lessons"][lesson]["degrees"]:
                        name = d[0]
                        value = d[1]
                        comm = d[2]

                        if name in ["Classwork", "classwork"] and value in ["2", "Н"]:
                            name += ":❗️"
                        if name in ["Homework", "Test", "test", "quiz", "homework", "Quiz"] and value in ["2", "Н", " ", ""]:
                            name += ":❗️"

                        result += "<b>" + name + ":</b> "
                        result += value + " "
                        result += comm + " "

                        result += "\n"

                    result += "\n"

                out.append(result)
    out.sort(key=lambda x: time.mktime(
        time.strptime(x[13:18].replace(".", "-"), "%d-%m")))

    return " ".join(out)
