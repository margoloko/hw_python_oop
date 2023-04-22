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

    def add_record(self, record: Record) -> None:
        """Функция для сохранения новых записей в словарь."""
        self.records.append(record)

    def get_today_stats(self) -> float:
        """Функция рассчитывает сколько денег/каллорий потрачено за сегодня."""
        return (sum(spent_today.amount for spent_today in self.records
                if spent_today.date == self.today))

    def get_week_stats(self) -> float:
        """Функция расчитывает сколько денег/каллорий потрачено
        за последние 7 дней."""
        return (sum(spent_week.amount for spent_week in self.records
                if self.week < spent_week.date <= self.today))

    def balance_today(self) -> float:
        """Функция расчитывает остаток денег/каллорий на сегодня."""
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    """Класс CaloriesCalculator используется для подсчета каллорий."""

    def get_calories_remained(self) -> str:
        remains = self.balance_today()
        if self.balance_today() > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {remains} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Класс CashCalculator для подсчета денег."""
    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency: str) -> str:
        """В функции расчитывается сколько ещё денег
        можно потратить сегодня в рублях, долларах или евро."""
        currencies = {'rub': (self.RUB_RATE, 'руб'),
                      'eur': (self.EURO_RATE, 'Euro'),
                      'usd': (self.USD_RATE, 'USD')}
        if currency not in currencies:
            raise KeyError(f'В базе отсутствует валюта {currency}. '
                           'Используйте другую валюту')
        if not self.balance_today():
            return 'Денег нет, держись'
        cur_rate, cur_name = currencies[currency]
        cur = round(self.balance_today() / cur_rate, 2)
        if self.balance_today() > 0:
            return f'На сегодня осталось {cur} {cur_name}'
        return f'Денег нет, держись: твой долг - {abs(cur)} {cur_name}'


if __name__ == "__main__":
    cc_calc = CaloriesCalculator(2000)
    cc_calc.add_record(Record(amount=820, date='07.10.2021',
                              comment='Breakfast'))
    cc_calc.add_record(Record(amount=560))
    cc_calc.add_record(Record(amount=280, comment='chocolate'))
    cc_calc.add_record(Record(amount=860, comment='lunch'))
    print(cc_calc.get_calories_remained())

    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    cash_calculator.add_record(Record(amount=3000,
                                      comment='бар в Танин др',
                                      date='08.11.2019'))
    cash_calculator.add_record(Record(amount=555))
    print(cash_calculator.get_today_cash_remained('rub'))

