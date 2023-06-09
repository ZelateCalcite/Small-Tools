import datetime
import re
from time import localtime


class Check:
    def __init__(self, dictionary=None):
        if dictionary is None:
            dictionary = {}
        self.data = []
        self.dictionary = dictionary

    @staticmethod
    def date_check(current: str, start='19000101',
                   end=str(localtime().tm_year) + str(localtime().tm_mon).zfill(2) + str(localtime().tm_mday).zfill(
                       2)) -> str:
        current_year, current_month, current_day = map(int, (current[0:4], current[4:6], current[6:8]))
        start_year, start_month, start_day = map(int, (start[0:4], start[4:6], start[6:8]))
        end_year, end_month, end_day = map(int, (end[0:4], end[4:6], end[6:8]))

        try:
            datetime.datetime(current_year, current_month, current_day)
            current_date = datetime.date(current_year, current_month, current_day)
            start_date = datetime.date(start_year, start_month, start_day)
            end_date = datetime.date(end_year, end_month, end_day)
            if start_date <= current_date <= end_date:
                return 'checked'
            else:
                return 'date not in range'
        except ValueError:
            return 'wrong date'

    @staticmethod
    def __length_check(string: str, minlength: int, maxlength: int) -> bool:
        return minlength <= len(string) <= maxlength

    def pid_check(self, pid: str) -> str:
        if not self.__length_check(pid, 18, 18):
            return 'wrong length'
        if re.match(r'^[0-9]{17}[0-9xX]$', pid) is None:
            return 'wrong character'
        return self.date_check(pid[6:14])

    def phone_check(self, phone: str) -> str:
        if not self.__length_check(phone, 11, 11):
            return 'wrong length'
        if phone.isdigit():
            return 'checked'
        else:
            return 'wrong character'

    def dict_check(self, dict_name: str, value: str) -> bool:
        return value in self.dictionary[dict_name]

    @staticmethod
    def uniq_check(current: dict, check_key) -> bool:
        return current.get(check_key) is None or current[check_key] == 1


if __name__ == '__main__':
    print(Check().pid_check('123456202402300000'))
