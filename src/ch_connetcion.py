from clickhouse_driver import Client
from jira_collector import get_json
from config import NAMES, DATABASE, TABLE, CH_HOST, PORT, USER, PASSWORD, DB

PROJECT_NAME = f"FP"
FILTER_NAME = f"filter=10007"


def update_table(client, id, data) -> None:
    delete_query = f"""
                ALTER TABLE {TABLE} DELETE WHERE {'id'} = '{id}'
            """
    client.execute(delete_query)
    client.execute(
        f"INSERT INTO {TABLE} (id, link, executor, start_data, type, creation_date, priority, resume) VALUES",
        [data],
    )


def update_ch_database() -> None:
    client = Client(
        host=CH_HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DB,
        verify=False,
        secure=True,
    )
    client.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
    client.execute(f"USE {DATABASE}")
    # Создание таблицы, если она не существует
    client.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            id String,
            link Nullable(String),
            executor Nullable(String),
            start_data Nullable(String),
            type Nullable(String),
            creation_date Nullable(String),
            priority Nullable(String),
            resume Nullable(String)
        ) ENGINE = MergeTree()
        ORDER BY id
    """
    )
    table_from_db = client.execute(f"SELECT * FROM {TABLE}")
    json_dict = get_json(NAMES, PROJECT_NAME, FILTER_NAME)
    values = []

    for values_list in list(json_dict.values()):
        values.append(tuple(list([i for i in values_list.values()])))
    # client.execute(f'INSERT INTO {TABLE} (id, link, executor, start_data, type, creation_date, priority, resume) VALUES', values)

    for i in values:
        if i not in table_from_db:
            if i[0] not in list([j[0] for j in table_from_db]):
                client.execute(
                    f"INSERT INTO {TABLE} (id, link, executor, start_data, type, creation_date, priority, resume) VALUES",
                    [i],
                )
            else:
                update_table(client, i[0], i)

    client.disconnect()


update_ch_database()
