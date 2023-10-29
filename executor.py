import time


def unpack(a):
    if a != {}:
        result = ""

        for date in a:
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
                    result += "<b>Оценки за урок: </b>" + \
                        str(a[date]["lessons"][lesson]['mark']) + "\n"
                result += "\n"
        return result
    else:
        return "Выходные"


def weeks(data, is_next=False):

    out = []
    if data == "Задание на каникулы":
        return "Каникулы"
    for a in data:
        if data[a] != {}:
            for date in data[a]:
                result = ""
                try:
                    date = data[a][date]
                except:
                    continue
                result += "<b>Дата: </b>" + date["date"] + "\n"
                result += "<u>" + a + "</u>\n"

                try:
                    for lesson in date["lessons"]:
                        names = [i[0]
                                 for i in date["lessons"][lesson]["degrees"]]
                        result += "<b>" + lesson + "</b>\n"
                        for i in date["lessons"][lesson]["hometask"]:
                            result += f"<b>Домашнее задание: </b>{i}\n"
                        if is_next == False:
                            # if "Homework" not in names:
                            #     result += "<b>Homework</b> ❗️\n"
                            # if "quiz" not in names and lesson == "Английский язык":
                            #     result += "<b>quiz</b> ❗️\n"
                            for d in date["lessons"][lesson]["degrees"]:
                                name = d[0]
                                value = d[1]
                                comm = d[2]
                                if name in ["Classwork", "classwork"] and value == "2":
                                    name += "❗️"
                                if name in ["Homework", "Test", "test", "quiz", "homework", "Quiz"] and value in ["2", "Н", " ", ""]:
                                    name += "❗️"
                                result += "<b>" + name + "</b> "
                                result += value + " "
                                result += comm + " "
                                result += "\n"
                        result += "" + "-----------------------\n"
                except:
                    # continue
                    result += "Нет занятий"
                if "Нет занятий" not in result:
                    out.append(result)
    return " ".join(out)


def degrees(asd):   
    out = []
    for data in asd:
        for a in data:
            if type(data) != str and data[a] != {}:
                for date in data[a]:
                    result = ""
                    result += "<b>Дата: </b>" + \
                        data[a][date]["date"] + "\n"
                    result += "<u>" + a + "</u>\n"
                    try:
                        for lesson in data[a][date]["lessons"]:
                            names = [i[0]
                                     for i in data[a][date]["lessons"][lesson]["degrees"]]
                            result += "<b>" + lesson + "</b>\n"
                            for i in data[a][date]["lessons"][lesson]["hometask"]:
                                result += f"<b>Домашнее задание: </b>{i}\n"
                            # if "Homework" not in names:
                            #     result += "<b>Homework</b> ❗️\n"
                            # if "quiz" not in names and lesson == "Английский язык":
                            #     result += "<b>quiz</b> ❗️\n"
                            for d in data[a][date]["lessons"][lesson]["degrees"]:
                                name = d[0]
                                value = d[1]
                                comm = d[2]
                                if name in ["Classwork", "classwork"] and value == "2":
                                    name += "❗️"
                                if name in ["Homework", "Test", "test", "quiz", "homework", "Quiz"] and value in ["2", "Н", " ", ""]:
                                    name += "❗️"
                                result += "<b>" + name + "</b> "
                                result += value + " "
                                result += comm + " "
                                result += "\n"
                            result += "" + "-----------------------\n"
                    except:
                        result = ""
                        continue
                        # result += "<u>" + "Выходной" + "</u>\n"
                    if result not in out:
                        out.append(result)
        out.sort(key=lambda x: time.mktime(
            time.strptime(x[13:18].replace(".", "-"), "%d-%m")))
    return out
    try:
        res = []
        for i in range(10, len(out)+10, 10):
            res.append("\n".join(out[i-10:i]))
        return res
    except:
        return "\n".join(out)
