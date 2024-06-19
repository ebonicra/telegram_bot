from database.load_map import map_create_tables
from database.load_data import data_create_tables
from database.load_quest import quest_create_tables


def main() -> None:
    """
    Функция для загрузки таблиц карты, данных персонажей и квестов.
    """
    map_create_tables()
    data_create_tables()
    quest_create_tables()


if __name__ == "__main__":
    main()
