class modifyDate:
    def __init__(self, date_string):
        # the key signifies the month 1 - 12
        # the value in the dictionary signify the day for the corresponding month
        self.__DAYINMONTHS = {
            1: 31,
            2: 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }
        self.date_string = date_string
        self.__day_str = self.__get_day()
        self.__month_str = self.__get_month()
        self.__year_str = self.__get_year()

    def __get_day(self):
        return self.date_string[-2:]

    def __get_year(self):
        return self.date_string[0:4]

    def __get_month(self):
        return self.date_string[4:6]

    def __is_leap_year(self):
        year_num = int(self.__year_str)
        return year_num % 4 == 0

    def incrment_date(self):
        day_increment = int(self.__day_str) + 7
        month_num = int(self.__month_str)
        year_num = int(self.__year_str)
        max_days = self.__DAYINMONTHS[month_num]

        if month_num == 2:
            if self.__is_leap_year():
                max_days += 1

        if day_increment > max_days:
            if month_num == 12:
                month_num = 1
                year_num += 1
                self.__year_str = str(year_num)
            else:
                month_num += 1
            next_month_day = self.__DAYINMONTHS[month_num]
            if self.__is_leap_year() and month_num == 2:
                day_increment = day_increment % 29
            else:
                day_increment = day_increment % next_month_day

            self.__month_str = (
                str(month_num) if month_num >= 10 else "0" + str(month_num)
            )

        self.__day_str = (
            str(day_increment) if day_increment >= 10 else "0" + str(day_increment)
        )

        self.date_string = self.__year_str + self.__month_str + self.__day_str

    def get_date(self):
        return self.date_string
