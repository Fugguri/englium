from eljur.Eljur.errors import _fullCheck, _checkInstance


class Journal:

    def journal(self, subdomain, session, week=0):
        """
        Получение страницы дневника с расписанием, оценками и другой информации.
        :param subdomain: Поддомен eljur.ru                                                                           // str
        :param session:   Активная сессия пользователя                                                                // Session
        :param week:      Нужная вам неделя (0 - нынешняя, -1 - предыдущая, 1 - следующая). По умолчанию 0 (нынешняя) // str
        :return: Словарь с ошибкой или с расписанием пользователя:                                                    // dict
                 answer // dict
                 result // bool
        """
        checkWeek = _checkInstance(week, int)
        if "error" in checkWeek:
            return checkWeek
        del checkWeek

        url = f"https://{subdomain}.eljur.ru/journal-app/week.{week * -1}"

        soup = _fullCheck(subdomain, session, url)
        if "error" in soup:
            return soup
        if soup.find("h1", class_="page-title red"):
            return "Задание на каникулы"
        info = {}
        for day in soup.find_all("div", class_="dnevnik-day"):
            title = day.find("div", class_="dnevnik-day__title")
            week, date = title.contents[0].strip().replace(
                "\n", "").split(", ")

            # if day.find("div", class_="page-empty"):
            #     info.update(
            #         [(week, {"date": date, "isEmpty": True, "comment": "Нет уроков", "lessons": {}})])
            #     continue

            # if day.find("div", class_="dnevnik-day__holiday"):
            #     info.update(
            #         [(week, {"date": date, "isEmpty": True, "comment": "Выходной", "lessons": {}})])
            #     continue

            lessons = day.find_all("div", class_="dnevnik-lesson")
            lessonsDict = {}
            if lessons:
                for lesson in lessons:
                    lessonNumber = lesson.find(
                        "div", class_="dnevnik-lesson__number dnevnik-lesson__number--time")
                    if lessonNumber:
                        lessonNumber = lessonNumber.contents[0].replace("\n", "").strip()[
                            :-1]

                    lessonTime = lesson.find(
                        "div", class_="dnevnik-lesson__time").contents[0].strip().replace("\n", "")
                    lessonName = lesson.find(
                        "span", class_="js-rt_licey-dnevnik-subject").contents[0]

                    lessonHomeTask = lesson.find(
                        "div", class_="dnevnik-lesson__task")
                    if lessonHomeTask:
                        lessonHomeTask = lessonHomeTask.contents[2].replace(
                            "\n", "").strip()
                    marks = lesson.find_all("div", class_="dnevnik-mark")

                    if marks:
                        result_marks = "\n"
                        for mark in marks:
                            result_marks += mark.contents[1].attrs["mtype"] + "-"
                            if mark.contents[1].attrs["value"] in ["2", "Н", " "]:
                                result_marks += mark.contents[1].attrs["value"] + "❗️" " "
                            else:
                                result_marks += mark.contents[1].attrs["value"] + " "
                        result_marks += mark.contents[1].attrs["mcomm"] + "\n"
                        if "quiz" not in result_marks:
                            result_marks += "quiz" + "❗️"
                        if "Homework" not in result_marks:
                            result_marks += "\nHomework" + "❗️"
                        result_marks += "\n"
                    else:
                        result_marks = None

                    lessonsDict.update([(lessonNumber, {"time": lessonTime,
                                                        "name": lessonName,
                                                        "hometask": lessonHomeTask,
                                                        "mark": result_marks})])
                info.update(
                    [(week, {"date": date, "isEmpty": False, "comment": "Выходной", "lessons": lessonsDict})])
        return info


class Journal2:

    def journal2(self, subdomain, session, week=0):
        """
        Получение страницы дневника с расписанием, оценками и другой информации.
        :param subdomain: Поддомен eljur.ru                                                                           // str
        :param session:   Активная сессия пользователя                                                                // Session
        :param week:      Нужная вам неделя (0 - нынешняя, -1 - предыдущая, 1 - следующая). По умолчанию 0 (нынешняя) // str
        :return: Словарь с ошибкой или с расписанием пользователя:                                                    // dict
                 answer // dict
                 result // bool
        """
        print("Journal")
        checkWeek = _checkInstance(week, int)
        if "error" in checkWeek:
            return checkWeek

        del checkWeek

        url = f"https://{subdomain}.eljur.ru/journal-app/week.{week * -1}"
        soup = _fullCheck(subdomain, session, url)
        childs = soup.find(
            "div", class_="navigation-tabs__students")
        childs = childs.find_all("option")
        result = {}
        for i in childs:
            child_id = i.attrs["value"].replace("/journal-app/", "")
            child_name = i.contents[0]
            url = f"https://{subdomain}.eljur.ru/journal-app/{child_id}/week.{week * -1}"
            soup = _fullCheck(subdomain, session, url)
            if "error" in soup:
                return soup
            if soup.find("h1", class_="page-title red"):
                return "Задание на каникулы"
            info = {}
            for day in soup.find_all("div", class_="dnevnik-day"):
                title = day.find("div", class_="dnevnik-day__title")
                week_, date = title.contents[0].strip().replace(
                    "\n", "").split(", ")
                lessons = day.find_all("div", class_="dnevnik-lesson")
                lessonsDict = {}
                if lessons:
                    for lesson in lessons:
                        lessonNumber = lesson.find(
                            "div", class_="dnevnik-lesson__number dnevnik-lesson__number--time")
                        if lessonNumber:
                            lessonNumber = lessonNumber.contents[0].replace("\n", "").strip()[
                                : -1]
                        lessonTime = lesson.find(
                            "div", class_="dnevnik-lesson__time").contents[0].strip().replace("\n", "")
                        lessonName = lesson.find(
                            "span", class_="js-rt_licey-dnevnik-subject").contents[0]
                        lessonHomeTask = lesson.find(
                            "div", class_="dnevnik-lesson__task")
                        try:
                            lessonsDict[lessonName]
                        except:
                            lessonsDict[lessonName] = dict()
                            lessonsDict[lessonName]["degrees"] = []
                            lessonsDict[lessonName]["hometask"] = []
                        if lessonHomeTask:
                            lessonHomeTask = "".join([
                                str(i) for i in lessonHomeTask.contents[2:-2]]).replace("\n", "").strip().replace("<br/>", "\n")+"\n"
                            lessonsDict[lessonName]["hometask"].append(
                                lessonHomeTask)
                        marks = lesson.find_all("div", class_="dnevnik-mark")
                        if marks:
                            for mark in marks:
                                if mark.contents[1].attrs["value"]:
                                    val = mark.contents[1].attrs["value"]
                                elif "Н" in str(mark):
                                    val = "Н"
                                else:
                                    val = ""
                                try:
                                    cl = [mark.contents[1].attrs["mtype"],
                                          val,
                                          mark.contents[1].attrs["mcomm"],
                                          ]
                                    lessonsDict[lessonName]["degrees"] .append(
                                        cl)
                                except:
                                    pass
                    info.update(
                        [(week_, {"date": date, "isEmpty": False, "comment": "Выходной", "lessons": lessonsDict})])
                else:
                    info.update(
                        [(week_, {"date": date, "isEmpty": False, "comment": "Выходной"})])
                result[child_name] = info
        return result
