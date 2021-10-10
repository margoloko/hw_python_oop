import datetime as dt
from typing import Optional


class Record:
    """Класс Record используется для создания данных."""
    def __init__(self, amount: float, date: Optional[str] = None,
                 comment: str = "Комментарий осутствует") -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    """Родительский класс Calculator."""
    def __init__(self, limit) -> None:
        self.records = []
        self.limit = limit
        self.today = dt.date.today()
        self.week = self.today - dt.timedelta(weeks=1)
    """Функция для сохранения новых записей в словарь."""
    def add_record(self, record: Record) -> None:
        self.records.append(record)
    """Функция рассчитывает сколько денег/каллорий потрачено за сегодня."""
    def get_today_stats(self) -> float:
        sum_for_today = 0
        return (sum(sum_for_today + i.amount for i in self.records
                if i.date == self.today))
    """Функция расчитывает сколько денег/каллорий потрачено
    за последние 7 дней."""
    def get_week_stats(self) -> float:
        sum_week = 0
        return (sum(sum_week + i.amount for i in self.records
                if self.week < i.date <= self.today))
    """Функция расчитывает остаток денег/каллорий на сегодня."""
    def balance_today(self) -> float:
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    """Класс CaloriesCalculator используется для подсчета каллорий."""
    def get_calories_remained(self) -> str:
        if self.limit > self.get_today_stats():
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {self.balance_today()} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Класс CashCalculator для подсчета денег."""
    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1.00
    """В функции расчитывается сколько ещё денег
    можно потратить сегодня в рублях, долларах или евро."""
    def get_today_cash_remained(self, currency: str) -> str:
        currencies = {'rub': (self.RUB_RATE, 'руб'),
                      'eur': (self.EURO_RATE, 'Euro'),
                      'usd': (self.USD_RATE, 'USD')}
        try:
            currency in currencies[currency]
        except KeyError:
            return (f'В базе отсутствует валюта {currency}. '
                    'Используйте другую валюту')
        cur_rate, cur_name = currencies[currency]
        cur = round(self.balance_today() / cur_rate, 2)
        if self.limit == self.get_today_stats():
            return 'Денег нет, держись'
        elif self.limit > self.get_today_stats():
            return f'На сегодня осталось {cur} {cur_name}'
        else:
            return f'Денег нет, держись: твой долг - {abs(cur)} {cur_name}'


if __name__ == "__main__":
    cc_calc = CaloriesCalculator(2000)
    cc_calc.add_record(Record(amount=820, date='07.10.2021',
                              comment='Breakfast'))
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
    print(cash_calculator.get_today_cash_remained('eur'))
# должно напечататься
# На сегодня осталось 555 руб
