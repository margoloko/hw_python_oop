import datetime as dt

today = dt.datetime.today().date()


class Record:

    def __init__(self, amount: float, date=None,
                 comment: str = "Комментарий осутствует"):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = today
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:

    def __init__(self, limit) -> None:
        self.records = []
        self.limit = limit

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self) -> float:
        i_today = 0
        for i in self.records:
            if i.date == today:
                i_today += i.amount
        return i_today

    def get_week_stats(self) -> float:
        i_week = 0
        for i in self.records:
            self.week = today - dt.timedelta(weeks=1)
            print(self.week)
            if self.week < i.date <= today:
                i_week += i.amount
        return i_week


class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        if self.limit > self.get_today_stats():
            m = self.limit - self.get_today_stats()
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {m} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency: str) -> str:
        currencies = {'rub': [self.RUB_RATE, 'руб'],
                      'eur': [self.EURO_RATE, 'Euro'],
                      'usd': [self.USD_RATE, 'USD']}
        cur_rate = currencies[currency][0]
        cur_name = currencies[currency][1]
        m = self.limit - self.get_today_stats()
        cur = round(m / cur_rate, 2)
        if self.limit > self.get_today_stats():
            return f'На сегодня осталось {cur} {cur_name}'
        elif self.limit == self.get_today_stats():
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {abs(cur)} {cur_name}'


# создадим калькулятор каллорий с дневным лимитом 2000
cc_calc = CaloriesCalculator(2000)
cc_calc.add_record(Record(amount=820, date='07.10.2021', comment='Breakfast'))
cc_calc.add_record(Record(amount=560))
cc_calc.add_record(Record(amount=280, comment='chocolate'))
cc_calc.add_record(Record(amount=860, comment='lunch'))
print(cc_calc.get_calories_remained())


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))
# cash_calculator.add_record(Record(amount=945))
print(cash_calculator.get_today_cash_remained('rub'))
# должно напечататься
# На сегодня осталось 555 руб
