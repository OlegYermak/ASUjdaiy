import sqlite3
import datetime as dt
import random

FIELDS = [
    'date',
    'human',
    'tank',
    'helicopter',
    'armored_car',
    'artillery_system',
    'drone',
    'mlrs',
    'cruise_missile',
    'anti_aircraft',
    'warship',
    'special_technique',
    'aircraft',
    'tanker_trucks'
]

DATE_TIME_FORMAT = "%d.%m.%Y"

# штамп в дата.час об'єкт
def toDateTimeObj(timestamp: float) -> dt.datetime:
    return dt.datetime.fromtimestamp(timestamp)

# дата.час об'єкт в рядок
def toDateTimeStr(dt_obj: dt.datetime) -> str:
    return dt_obj.strftime(DATE_TIME_FORMAT)

# рядок в штамп
def strToTimestamp(dt_str: str) -> float:
    return dt.datetime.strptime(dt_str, DATE_TIME_FORMAT).timestamp()

def strToDateTime(dt_str: str) -> dt.datetime:
    return dt.datetime.strptime(dt_str, DATE_TIME_FORMAT)


class DB:
    def __init__(self, path: str) -> None:
        self.path = path
        query = """ 
            CREATE TABLE IF NOT EXISTS damage (
                date REAL UNIQUE,
                human INTEGER,
                tank INTEGER,
                helicopter INTEGER,
                armored_car INTEGER,
                artillery_system INTEGER,
                drone INTEGER,
                mlrs INTEGER,
                cruise_missile INTEGER,
                anti_aircraft INTEGER,
                warship INTEGER,
                special_technique INTEGER,
                aircraft INTEGER,
                tanker_trucks INTEGER
            )
        """
        connect = sqlite3.connect(path)
        cursor = connect.cursor()
        cursor.execute(query)
        cursor.close()
        connect.commit()
        connect.close()

    def addRecord(self, values: dict) -> None:
        query = """ 
            INSERT INTO damage (
                date, human, tank, helicopter, armored_car, artillery_system, drone, mlrs, cruise_missile,
                anti_aircraft, warship, special_technique, aircraft, tanker_trucks
            )
            VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})
        """.format(*values.values())
        print(query)
        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        cursor.execute(query)
        cursor.close()
        connect.commit()
        connect.close()

    def getRecord(self, date: float) -> dict | None:
        query = """ 
            SELECT 
                date, human, tank, helicopter, armored_car, artillery_system, drone, mlrs, cruise_missile,
                anti_aircraft, warship, special_technique, aircraft, tanker_trucks
            FROM damage
            WHERE date = {}
            LIMIT 1
        """.format(date)
        print(query)
        
        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        cursor.execute(query)
        values = cursor.fetchone()
        cursor.close()
        connect.close()

        if values:
            return dict(zip(FIELDS, values))
        else:
            return None

    def updateRecord(self, values: dict) -> None:
        query = """ 
            UPDATE damage SET
                date = {}, human = {}, tank = {}, helicopter = {}, armored_car = {}, artillery_system = {}, 
                drone = {}, mlrs = {}, cruise_missile = {},
                anti_aircraft = {}, warship = {}, special_technique = {}, aircraft = {}, tanker_trucks = {}           
            WHERE date = {}
        """.format(*values.values(), values['date'])
        print(query)

        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        cursor.execute(query)
        cursor.close()
        connect.commit()
        connect.close()

    def getTotal(self, dateStart: float, dateEnd: float) -> dict:
        query = """ 
            SELECT NULL, SUM(human), SUM(tank), SUM(helicopter), SUM(armored_car), SUM(artillery_system), 
                SUM(drone), SUM(mlrs), SUM(cruise_missile),SUM(anti_aircraft), SUM(warship), SUM(special_technique), 
                SUM(aircraft), SUM(tanker_trucks)
            FROM damage
            WHERE date >= {} AND date <= {}
        """.format(dateStart, dateEnd)

        print(query)

        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        cursor.execute(query)
        values = cursor.fetchone()
        cursor.close()
        connect.close()

        if len(tuple(filter(lambda x: x == None, values))) == 14:
            return None

        return dict(zip(FIELDS, values))

    def getReport(self, dateStart: float, dateEnd: float) -> list[dict] | None:
        query = """ 
            SELECT * FROM damage
            WHERE date >= {} AND date <= {}
            ORDER BY date
        """.format(dateStart, dateEnd)
        print(query)

        connect = sqlite3.connect(self.path)
        cursor = connect.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connect.close()

        if results:
            values = []
            for row in results:
                dict_row = dict(zip(FIELDS, row))
                dict_row['date'] = toDateTimeObj(dict_row['date'])
                values.append(dict_row)
            return values
        return None


if __name__ == "__main__":
    db = DB('damage.db')
    # рандомні дані
    empty_dict = dict(zip(FIELDS, [0]*14))
    for month in range(1, 4):
        for day in range(1, 28):
            today = dict(empty_dict)
            for k in today.keys():
                today[k] = random.randint(5, 15)
            today['date'] = strToTimestamp(f'{day}.{month}.2023')
            db.addRecord(today)

