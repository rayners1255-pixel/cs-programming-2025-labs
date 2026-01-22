import json
import datetime
import os
from typing import Dict, List, Optional, Tuple

# =============================================
# КОНСТАНТЫ И НАСТРОЙКИ
# =============================================
DATA_FILE = "gas_station_data.json"
FUEL_TYPES = ["АИ-92", "АИ-95", "АИ-98", "ДТ"]
FUEL_PRICES = {
    "АИ-92": 57.50,
    "АИ-95": 58.30,
    "АИ-98": 64.20,
    "ДТ": 56.80
}

# Схема подключения цистерн к колонкам (цистерна -> список колонок)
CISTERN_TO_COLUMNS = {
    "АИ-95 №1": [1, 2, 3, 4],
    "АИ-95 №2": [5, 6, 7, 8],
    "АИ-92 №1": [1, 2, 3, 4, 5, 6],
    "АИ-98 №1": [3, 4, 5, 6],
    "ДТ №1": [3, 4, 5, 6, 7, 8]
}

# Максимальные объемы цистерн (литры)
CISTERN_MAX_VOLUMES = {
    "АИ-92 №1": 20000,
    "АИ-95 №1": 20000,
    "АИ-95 №2": 20000,
    "АИ-98 №1": 15000,
    "ДТ №1": 25000
}

# Минимальные уровни (% от максимального объема)
MIN_LEVEL_PERCENT = 10


# =============================================
# КЛАССЫ ДЛЯ ХРАНЕНИЯ ДАННЫХ
# =============================================
class Cistern:
    def __init__(self, name: str, fuel_type: str, max_volume: float, current_volume: float = None):
        self.name = name
        self.fuel_type = fuel_type
        self.max_volume = max_volume
        self.current_volume = current_volume if current_volume is not None else max_volume * 0.5
        self.enabled = True
        self.min_level = max_volume * (MIN_LEVEL_PERCENT / 100)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "fuel_type": self.fuel_type,
            "max_volume": self.max_volume,
            "current_volume": self.current_volume,
            "enabled": self.enabled,
            "min_level": self.min_level
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Cistern':
        cistern = cls(
            data["name"],
            data["fuel_type"],
            data["max_volume"],
            data["current_volume"]
        )
        cistern.enabled = data["enabled"]
        return cistern

    def check_low_level(self) -> bool:
        """Проверяет, опустился ли уровень ниже минимального"""
        return self.current_volume < self.min_level

    def can_dispense(self, amount: float) -> Tuple[bool, str]:
        """Проверяет возможность отпуска указанного количества топлива"""
        if not self.enabled:
            return False, f"Цистерна {self.name} отключена"
        if self.current_volume < amount:
            return False, f"Недостаточно топлива в цистерне {self.name}"
        return True, ""

    def dispense(self, amount: float) -> bool:
        """Отпускает топливо из цистерны"""
        if self.current_volume >= amount:
            self.current_volume -= amount
            # Автоматически отключаем цистерну при низком уровне
            if self.check_low_level():
                self.enabled = False
            return True
        return False

    def refuel(self, amount: float) -> Tuple[bool, str]:
        """Пополняет цистерну"""
        if self.current_volume + amount > self.max_volume:
            available = self.max_volume - self.current_volume
            return False, f"Превышение максимального объема. Доступно для залива: {available:.1f} л"

        self.current_volume += amount
        return True, ""

    def get_info(self) -> str:
        status = "ВКЛ" if self.enabled else "ВЫКЛ"
        warning = ""
        if not self.enabled and self.check_low_level():
            warning = " (ниже порога)"
        elif not self.enabled:
            warning = " (отключена вручную)"

        return (f"{self.name:10} | {self.current_volume:7.1f} / {self.max_volume:7.1f} л | "
                f"{status}{warning}")


class FuelColumn:
    def __init__(self, number: int):
        self.number = number
        # Определяем доступные виды топлива на основе схемы подключения
        self.available_fuels = {}
        for cistern_name, columns in CISTERN_TO_COLUMNS.items():
            if self.number in columns:
                # Извлекаем тип топлива из имени цистерны
                for fuel_type in FUEL_TYPES:
                    if cistern_name.startswith(fuel_type):
                        self.available_fuels[fuel_type] = cistern_name
                        break

    def get_available_fuels(self, cisterns: Dict[str, Cistern]) -> List[Tuple[str, str]]:
        """Возвращает список доступных видов топлива с учетом состояния цистерн"""
        available = []
        for fuel_type, cistern_name in self.available_fuels.items():
            cistern = cisterns.get(cistern_name)
            if cistern and cistern.enabled:
                available.append((fuel_type, cistern_name))
        return available

    def get_info(self, cisterns: Dict[str, Cistern]) -> str:
        """Возвращает информацию о колонке"""
        info = f"Колонка {self.number}\n"
        info += "Доступные виды топлива:\n"

        fuels = self.get_available_fuels(cisterns)
        if not fuels:
            info += "  Нет доступного топлива (все цистерны отключены)\n"
        else:
            for i, (fuel_type, cistern_name) in enumerate(fuels, 1):
                cistern = cisterns[cistern_name]
                status = "✓" if cistern.enabled else "✗"
                info += f"  {i}) {fuel_type:6} (цистерна {cistern_name}) {status}\n"

        return info


class Transaction:
    def __init__(self, trans_type: str, details: str, amount: float = 0, fuel_type: str = None):
        self.timestamp = datetime.datetime.now()
        self.trans_type = trans_type  # "sale", "refuel", "transfer", "cistern_toggle", "emergency"
        self.details = details
        self.amount = amount
        self.fuel_type = fuel_type

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "type": self.trans_type,
            "details": self.details,
            "amount": self.amount,
            "fuel_type": self.fuel_type
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        trans = cls(
            data["type"],
            data["details"],
            data.get("amount", 0),
            data.get("fuel_type")
        )
        trans.timestamp = datetime.datetime.fromisoformat(data["timestamp"])
        return trans

    def get_display_string(self) -> str:
        time_str = self.timestamp.strftime("%d.%m.%Y %H:%M:%S")
        return f"[{time_str}] {self.details}"


class Statistics:
    def __init__(self):
        self.total_income = 0.0
        self.cars_served = 0
        self.fuel_stats = {fuel: {"liters": 0.0, "income": 0.0, "transactions": 0} for fuel in FUEL_TYPES}
        self.transactions: List[Transaction] = []

    def to_dict(self) -> dict:
        return {
            "total_income": self.total_income,
            "cars_served": self.cars_served,
            "fuel_stats": self.fuel_stats,
            "transactions": [t.to_dict() for t in self.transactions[-100:]]  # Храним только последние 100
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Statistics':
        stats = cls()
        stats.total_income = data.get("total_income", 0.0)
        stats.cars_served = data.get("cars_served", 0)
        stats.fuel_stats = data.get("fuel_stats",
                                    {ft: {"liters": 0.0, "income": 0.0, "transactions": 0} for ft in FUEL_TYPES})

        transactions_data = data.get("transactions", [])
        stats.transactions = [Transaction.from_dict(t) for t in transactions_data]
        return stats

    def add_sale(self, fuel_type: str, liters: float, amount: float):
        """Добавляет информацию о продаже"""
        self.total_income += amount
        self.cars_served += 1

        if fuel_type in self.fuel_stats:
            self.fuel_stats[fuel_type]["liters"] += liters
            self.fuel_stats[fuel_type]["income"] += amount
            self.fuel_stats[fuel_type]["transactions"] += 1

    def add_transaction(self, transaction: Transaction):
        """Добавляет транзакцию в историю"""
        self.transactions.append(transaction)
        # Ограничиваем размер истории
        if len(self.transactions) > 100:
            self.transactions = self.transactions[-100:]


class GasStation:
    def __init__(self):
        self.cisterns: Dict[str, Cistern] = {}
        self.columns: List[FuelColumn] = []
        self.stats = Statistics()
        self.emergency_mode = False
        self._initialize()

    def _initialize(self):
        """Инициализация АЗС с начальными данными"""
        # Создаем цистерны
        for cistern_name, max_volume in CISTERN_MAX_VOLUMES.items():
            for fuel_type in FUEL_TYPES:
                if cistern_name.startswith(fuel_type):
                    self.cisterns[cistern_name] = Cistern(cistern_name, fuel_type, max_volume)
                    break

        # Создаем колонки
        for i in range(1, 9):
            self.columns.append(FuelColumn(i))

    def save_state(self):
        """Сохраняет состояние АЗС в файл"""
        data = {
            "cisterns": {name: c.to_dict() for name, c in self.cisterns.items()},
            "stats": self.stats.to_dict(),
            "emergency_mode": self.emergency_mode
        }

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_state(self) -> bool:
        """Загружает состояние АЗС из файла"""
        if not os.path.exists(DATA_FILE):
            return False

        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Загружаем цистерны
            self.cisterns.clear()
            for cistern_data in data["cisterns"].values():
                cistern = Cistern.from_dict(cistern_data)
                self.cisterns[cistern.name] = cistern

            # Загружаем статистику
            self.stats = Statistics.from_dict(data["stats"])

            # Загружаем режим аварии
            self.emergency_mode = data.get("emergency_mode", False)

            return True
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            return False


# =============================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С МЕНЮ
# =============================================
def clear_screen():
    """Очищает экран консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(station: GasStation):
    """Выводит заголовок АЗС"""
    clear_screen()
    print("=" * 50)
    print("АЗС <<СеверНефть>>")
    print("Система управления заправочной станцией")
    print("=" * 50)
    print()

    # Проверяем отключенные цистерны
    disabled_cisterns = []
    for cistern in station.cisterns.values():
        if not cistern.enabled:
            disabled_cisterns.append(cistern)

    if disabled_cisterns:
        print("ВНИМАНИЕ!")
        print("Обнаружены отключённые цистерны:")
        for cistern in disabled_cisterns:
            reason = "низкий уровень топлива" if cistern.check_low_level() else "отключена вручную"
            print(f" - {cistern.name} ({reason})")
        print()


def wait_for_enter():
    """Ожидание нажатия Enter"""
    input("\nНажмите Enter для продолжения...")


def show_main_menu():
    """Отображает главное меню"""
    print("-" * 40)
    print("Выберите действие:")
    print("1) Обслужить клиента (касса)")
    print("2) Проверить состояние цистерн")
    print("3) Оформить пополнение топлива")
    print("4) Баланс и статистика")
    print("5) История операций")
    print("6) Перекачка топлива между цистернами")
    print("7) Включение / отключение цистерн")
    print("8) Состояние колонок")
    print("9) EMERGENCY - аварийная ситуация")
    print("0) Выход")
    print("-" * 40)


def serve_customer(station: GasStation):
    """Обслуживание клиента"""
    print("\n--- Обслуживание клиента ---\n")

    if station.emergency_mode:
        print("АВАРИЙНЫЙ РЕЖИМ! Заправка невозможна.")
        wait_for_enter()
        return

    print("Доступные колонки:")
    for i, column in enumerate(station.columns, 1):
        print(f"{i}) Колонка {column.number}")

    try:
        col_choice = int(input("\nВыберите колонку: "))
        if col_choice < 1 or col_choice > len(station.columns):
            print("Неверный выбор колонки!")
            wait_for_enter()
            return

        column = station.columns[col_choice - 1]
        print(f"\n{column.get_info(station.cisterns)}")

        available_fuels = column.get_available_fuels(station.cisterns)
        if not available_fuels:
            print("На этой колонке нет доступного топлива!")
            wait_for_enter()
            return

        print("\nДоступные виды топлива:")
        for i, (fuel_type, cistern_name) in enumerate(available_fuels, 1):
            print(f"{i}) {fuel_type} (цистерна {cistern_name})")

        fuel_choice = int(input("\nВыберите тип топлива: "))
        if fuel_choice < 1 or fuel_choice > len(available_fuels):
            print("Неверный выбор топлива!")
            wait_for_enter()
            return

        fuel_type, cistern_name = available_fuels[fuel_choice - 1]
        cistern = station.cisterns[cistern_name]

        # Проверяем возможность отпуска
        can_dispense, message = cistern.can_dispense(0)
        if not can_dispense:
            print(f"\nОШИБКА: {message}")
            wait_for_enter()
            return

        # Запрашиваем количество литров
        try:
            liters = float(input("\nВведите количество литров: "))
            if liters <= 0:
                print("Количество должно быть положительным!")
                wait_for_enter()
                return
        except ValueError:
            print("Некорректное значение!")
            wait_for_enter()
            return

        # Проверяем возможность отпуска конкретного объема
        can_dispense, message = cistern.can_dispense(liters)
        if not can_dispense:
            print(f"\nОШИБКА: {message}")
            wait_for_enter()
            return

        # Рассчитываем стоимость
        price_per_liter = FUEL_PRICES.get(fuel_type, 0)
        total_price = liters * price_per_liter

        print(f"\nСтоимость:")
        print(f"{liters:.1f} л × {price_per_liter:.2f} ₽ = {total_price:.2f} ₽")

        # Подтверждение оплаты
        confirm = input("\nПодтвердить оплату? (y/n): ").lower()
        if confirm != 'y':
            print("Операция отменена.")
            wait_for_enter()
            return

        # Выполняем продажу
        if cistern.dispense(liters):
            # Обновляем статистику
            station.stats.add_sale(fuel_type, liters, total_price)

            # Добавляем транзакцию
            details = f"Продажа {liters:.1f} л {fuel_type} на колонке {column.number} за {total_price:.2f} ₽"
            transaction = Transaction("sale", details, liters, fuel_type)
            station.stats.add_transaction(transaction)

            station.save_state()

            print("\nОперация выполнена успешно.")
            print("Спасибо за покупку!")
        else:
            print("\nОшибка при отпуске топлива!")

    except ValueError:
        print("Некорректный ввод!")

    wait_for_enter()


def check_cisterns(station: GasStation):
    """Проверка состояния цистерн"""
    print("\n--- Состояние цистерн ---\n")

    print("Доступные цистерны:")
    for i, (name, cistern) in enumerate(station.cisterns.items(), 1):
        print(f"{i}) {cistern.get_info()}")

    wait_for_enter()


def refuel_cistern(station: GasStation):
    """Пополнение цистерны"""
    print("\n--- Оформление пополнения топлива ---\n")

    if station.emergency_mode:
        print("АВАРИЙНЫЙ РЕЖИМ! Пополнение невозможно.")
        wait_for_enter()
        return

    print("Доступные цистерны:")
    cistern_list = list(station.cisterns.values())
    for i, cistern in enumerate(cistern_list, 1):
        available = cistern.max_volume - cistern.current_volume
        print(f"{i}) {cistern.name:10} | Заполнена на {cistern.current_volume / cistern.max_volume * 100:.1f}% "
              f"(можно залить {available:.1f} л)")

    try:
        choice = int(input("\nВыберите цистерну: "))
        if choice < 1 or choice > len(cistern_list):
            print("Неверный выбор!")
            wait_for_enter()
            return

        cistern = cistern_list[choice - 1]

        liters = float(input("Введите количество литров для залива: "))
        if liters <= 0:
            print("Количество должно быть положительным!")
            wait_for_enter()
            return

        # Пробуем залить топливо
        success, message = cistern.refuel(liters)

        if success:
            # Добавляем транзакцию
            details = f"Пополнение цистерны {cistern.name} на {liters:.1f} л"
            transaction = Transaction("refuel", details, liters, cistern.fuel_type)
            station.stats.add_transaction(transaction)

            station.save_state()
            print(f"\nЦистерна {cistern.name} успешно пополнена на {liters:.1f} л")
            print(f"Текущий уровень: {cistern.current_volume:.1f} / {cistern.max_volume:.1f} л")
        else:
            print(f"\nОШИБКА: {message}")

    except ValueError:
        print("Некорректный ввод!")

    wait_for_enter()


def show_statistics(station: GasStation):
    """Отображение статистики"""
    print("\n--- Баланс и статистика ---\n")

    stats = station.stats

    print(f"Обслужено автомобилей: {stats.cars_served}")
    print(f"Общий доход: {stats.total_income:,.2f} ₽\n")

    print("Продано топлива:")
    for fuel_type in FUEL_TYPES:
        fuel_stat = stats.fuel_stats.get(fuel_type, {"liters": 0, "income": 0, "transactions": 0})
        if fuel_stat["liters"] > 0:
            print(f"  {fuel_type:6} - {fuel_stat['liters']:7.1f} л ({fuel_stat['income']:9,.2f} ₽)")
        else:
            print(f"  {fuel_type:6} - {0:7.1f} л ({0:9,.2f} ₽)")

    wait_for_enter()


def show_history(station: GasStation):
    """Отображение истории операций"""
    print("\n--- История операций ---\n")

    if not station.stats.transactions:
        print("История операций пуста.")
    else:
        print("Последние операции:")
        for i, trans in enumerate(reversed(station.stats.transactions[-20:]), 1):  # Показываем последние 20
            print(f"{i:2}. {trans.get_display_string()}")

    wait_for_enter()


def transfer_fuel(station: GasStation):
    """Перекачка топлива между цистернами"""
    print("\n--- Перекачка топлива между цистернами ---\n")

    if station.emergency_mode:
        print("АВАРИЙНЫЙ РЕЖИМ! Перекачка невозможна.")
        wait_for_enter()
        return

    # Группируем цистерны по типу топлива
    cisterns_by_type = {}
    for cistern in station.cisterns.values():
        if cistern.fuel_type not in cisterns_by_type:
            cisterns_by_type[cistern.fuel_type] = []
        cisterns_by_type[cistern.fuel_type].append(cistern)

    # Выбираем тип топлива
    print("Доступные типы топлива:")
    fuel_types = list(cisterns_by_type.keys())
    for i, fuel_type in enumerate(fuel_types, 1):
        print(f"{i}) {fuel_type}")

    try:
        fuel_choice = int(input("\nВыберите тип топлива: "))
        if fuel_choice < 1 or fuel_choice > len(fuel_types):
            print("Неверный выбор!")
            wait_for_enter()
            return

        selected_fuel = fuel_types[fuel_choice - 1]
        cisterns = cisterns_by_type[selected_fuel]

        if len(cisterns) < 2:
            print(f"Для топлива {selected_fuel} доступна только одна цистерна.")
            wait_for_enter()
            return

        print(f"\nЦистерны с топливом {selected_fuel}:")
        for i, cistern in enumerate(cisterns, 1):
            print(f"{i}) {cistern.get_info()}")

        # Выбираем источник
        source_idx = int(input("\nВыберите цистерну-источник: ")) - 1
        if source_idx < 0 or source_idx >= len(cisterns):
            print("Неверный выбор!")
            wait_for_enter()
            return

        # Выбираем приемник
        target_idx = int(input("Выберите цистерну-приемник: ")) - 1
        if target_idx < 0 or target_idx >= len(cisterns) or target_idx == source_idx:
            print("Неверный выбор!")
            wait_for_enter()
            return

        source = cisterns[source_idx]
        target = cisterns[target_idx]

        # Проверяем источник
        if not source.enabled:
            print(f"Цистерна-источник {source.name} отключена!")
            wait_for_enter()
            return

        # Запрашиваем объем
        liters = float(input("\nВведите количество литров для перекачки: "))
        if liters <= 0:
            print("Количество должно быть положительным!")
            wait_for_enter()
            return

        # Проверяем достаточность топлива
        if source.current_volume < liters:
            print(f"Недостаточно топлива в цистерне-источнике!")
            print(f"Доступно: {source.current_volume:.1f} л")
            wait_for_enter()
            return

        # Проверяем вместимость приемника
        if target.current_volume + liters > target.max_volume:
            available = target.max_volume - target.current_volume
            print(f"Цистерна-приемник не вмещает указанное количество!")
            print(f"Доступно для залива: {available:.1f} л")
            wait_for_enter()
            return

        # Выполняем перекачку
        source.current_volume -= liters
        target.current_volume += liters

        # Проверяем и обновляем статусы цистерн
        if source.check_low_level():
            source.enabled = False

        # Добавляем транзакцию
        details = (f"Перекачка {liters:.1f} л {selected_fuel} из {source.name} в {target.name}")
        transaction = Transaction("transfer", details, liters, selected_fuel)
        station.stats.add_transaction(transaction)

        station.save_state()

        print("\nПерекачка выполнена успешно!")
        print(f"Источник: {source.name} - {source.current_volume:.1f} л")
        print(f"Приемник: {target.name} - {target.current_volume:.1f} л")

    except ValueError:
        print("Некорректный ввод!")

    wait_for_enter()


def manage_cisterns(station: GasStation):
    """Управление цистернами (включение/отключение)"""
    print("\n--- Управление цистернами ---\n")

    print("Доступные действия:")
    print("1) Включить цистерну")
    print("2) Отключить цистерну")

    try:
        action = int(input("\nВыберите действие: "))

        cistern_list = list(station.cisterns.values())

        if action == 1:  # Включение
            # Показываем только отключенные цистерны
            disabled = [c for c in cistern_list if not c.enabled]

            if not disabled:
                print("\nНет отключенных цистерн для включения.")
                wait_for_enter()
                return

            print("\nЦистерны, доступные для включения:")
            for i, cistern in enumerate(disabled, 1):
                print(f"{i}) {cistern.get_info()}")

            choice = int(input("\nВыберите цистерну: ")) - 1
            if choice < 0 or choice >= len(disabled):
                print("Неверный выбор!")
                wait_for_enter()
                return

            cistern = disabled[choice]

            # Проверяем уровень топлива
            if cistern.check_low_level():
                print(f"Внимание! Уровень топлива в цистерне ниже минимального ({cistern.min_level:.1f} л)")
                confirm = input("Всё равно включить цистерну? (y/n): ").lower()
                if confirm != 'y':
                    print("Операция отменена.")
                    wait_for_enter()
                    return

            cistern.enabled = True

            # Добавляем транзакцию
            details = f"Включение цистерны {cistern.name}"
            transaction = Transaction("cistern_toggle", details)
            station.stats.add_transaction(transaction)

            station.save_state()

            print(f"\nЦистерна {cistern.name} успешно включена.")

        elif action == 2:  # Отключение
            # Показываем только включенные цистерны
            enabled = [c for c in cistern_list if c.enabled]

            if not enabled:
                print("\nНет включенных цистерн для отключения.")
                wait_for_enter()
                return

            print("\nЦистерны, доступные для отключения:")
            for i, cistern in enumerate(enabled, 1):
                print(f"{i}) {cistern.get_info()}")

            choice = int(input("\nВыберите цистерну: ")) - 1
            if choice < 0 or choice >= len(enabled):
                print("Неверный выбор!")
                wait_for_enter()
                return

            cistern = enabled[choice]
            cistern.enabled = False

            # Добавляем транзакцию
            details = f"Отключение цистерны {cistern.name}"
            transaction = Transaction("cistern_toggle", details)
            station.stats.add_transaction(transaction)

            station.save_state()

            print(f"\nЦистерна {cistern.name} успешно отключена.")

        else:
            print("Неверный выбор действия!")

    except ValueError:
        print("Некорректный ввод!")

    wait_for_enter()


def show_columns(station: GasStation):
    """Отображение состояния колонок"""
    print("\n--- Состояние колонок ---\n")

    for column in station.columns:
        print(column.get_info(station.cisterns))
        print("-" * 40)

    wait_for_enter()


def emergency_procedure(station: GasStation):
    """Аварийная процедура"""
    print("\n=== EMERGENCY - АВАРИЙНАЯ СИТУАЦИЯ ===\n")

    if station.emergency_mode:
        print("Текущий статус: АВАРИЙНЫЙ РЕЖИМ АКТИВЕН")
        print("\nДоступные действия:")
        print("1) Отключить аварийный режим")
        print("2) Вернуться в меню")

        try:
            choice = int(input("\nВыберите действие: "))

            if choice == 1:
                print("\nОтключение аварийного режима...")
                station.emergency_mode = False
                station.save_state()
                print("Аварийный режим отключен.")
                print("ВНИМАНИЕ: Цистерны не разблокированы автоматически!")
            elif choice == 2:
                return
            else:
                print("Неверный выбор!")

        except ValueError:
            print("Некорректный ввод!")

    else:
        print("ВНИМАНИЕ: Активация аварийного режима приведет к:")
        print("1) Блокировке всех цистерн")
        print("2) Прекращению заправки")
        print("3) Фиксации аварийного события")
        print("4) Имитации вызова аварийных служб")

        confirm = input("\nВы уверены, что хотите активировать аварийный режим? (y/n): ").lower()

        if confirm == 'y':
            print("\nАктивация аварийного режима...")

            # Блокируем все цистерны
            for cistern in station.cisterns.values():
                cistern.enabled = False

            station.emergency_mode = True

            # Добавляем транзакцию
            details = "АКТИВАЦИЯ АВАРИЙНОГО РЕЖИМА"
            transaction = Transaction("emergency", details)
            station.stats.add_transaction(transaction)

            station.save_state()

            print("\n!!! АВАРИЙНЫЙ РЕЖИМ АКТИВИРОВАН !!!")
            print("Все цистерны заблокированы.")
            print("Заправка прекращена.")
            print("\nИмитация вызова аварийных служб...")
            print("Службы оповещены. Ожидайте прибытия.")

    wait_for_enter()


# =============================================
# ГЛАВНАЯ ФУНКЦИЯ
# =============================================
def main():
    """Главная функция программы"""
    # Создаем АЗС
    station = GasStation()

    # Пытаемся загрузить сохраненное состояние
    if station.load_state():
        print("Состояние АЗС загружено из файла.")
    else:
        print("Инициализирована новая АЗС.")

    wait_for_enter()

    # Главный цикл программы
    while True:
        print_header(station)
        show_main_menu()

        try:
            choice = int(input("> "))

            if choice == 0:
                print("\nСохранение данных...")
                station.save_state()
                print("Выход из программы.")
                break

            elif choice == 1:
                serve_customer(station)
            elif choice == 2:
                check_cisterns(station)
            elif choice == 3:
                refuel_cistern(station)
            elif choice == 4:
                show_statistics(station)
            elif choice == 5:
                show_history(station)
            elif choice == 6:
                transfer_fuel(station)
            elif choice == 7:
                manage_cisterns(station)
            elif choice == 8:
                show_columns(station)
            elif choice == 9:
                emergency_procedure(station)
            else:
                print("Неверный выбор! Попробуйте снова.")
                wait_for_enter()

        except ValueError:
            print("Пожалуйста, введите число!")
            wait_for_enter()
        except KeyboardInterrupt:
            print("\n\nЭкстренное завершение...")
            station.save_state()
            break


if __name__ == "__main__":
    main()