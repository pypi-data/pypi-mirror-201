import pymysql
import yaml
import sshtunnel
import pandas as pd
import telegram
import clickhouse_driver
import sqlalchemy
from google.cloud import bigquery
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SSHFinanceTunnel:
    def __init__(self, credential_path: str):
        self.credentials = yaml.safe_load(open(credential_path, "r"))
        self.host = self.credentials['SSH_ABACUS']['SSH_HOST']
        self.port = self.credentials['SSH_ABACUS']['SSH_PORT']
        self.path = self.credentials['SSH_ABACUS']['SSH_PATH']
        self.username = self.credentials['SSH_ABACUS']['SSH_USER']
        self.key_phrase = self.credentials['SSH_ABACUS']['SSH_KEYPHRASE']
        self.client = None
        self.__connect()
        self.__start()

    def __connect(self):
        self.client = sshtunnel.SSHTunnelForwarder(
            (self.host, self.port),
            ssh_username=self.username,
            ssh_pkey=self.path,
            ssh_private_key_password=self.key_phrase,
            remote_bind_address=('127.0.0.1', 3306))
        return self.client

    def __start(self):
        self.client.start()

    def disconnect(self):
        self.client.stop()
        print("Client disconnected")


class SSHTunnel:
    def __init__(self, credential_path: str, datamart: bool = True):
        self.credentials = yaml.safe_load(open(credential_path, "r"))
        self.datamart = datamart
        if self.datamart:
            self.host = self.credentials['SSH_DATAMART']['SSH_HOST']
            self.port = self.credentials['SSH_DATAMART']['SSH_PORT']
            self.path = self.credentials['SSH_DATAMART']['SSH_PATH']
            self.username = self.credentials['SSH_DATAMART']['SSH_USER']
            self.key_phrase = self.credentials['SSH_DATAMART']['SSH_KEYPHRASE']
        else:
            self.host = self.credentials['SSH_PREDICT']['SSH_HOST']
            self.port = self.credentials['SSH_PREDICT']['SSH_PORT']
            self.path = self.credentials['SSH_PREDICT']['SSH_PATH']
            self.username = self.credentials['SSH_PREDICT']['SSH_USER']
            self.key_phrase = self.credentials['SSH_PREDICT']['SSH_KEYPHRASE']
        self.client = None
        self.__connect()
        self.__start()

    def __connect(self):
        if self.datamart:
            self.client = sshtunnel.SSHTunnelForwarder(
                (self.host, self.port),
                ssh_username=self.username,
                ssh_pkey=self.path,
                ssh_private_key_password=self.key_phrase,
                remote_bind_address=('127.0.0.1', 3306))
        else:
            self.client = sshtunnel.SSHTunnelForwarder(
                (self.host, self.port),
                ssh_username=self.username,
                ssh_pkey=self.path,
                ssh_private_key_password=self.key_phrase,
                remote_bind_address=('127.0.0.1', 9000))
        return self.client

    def __start(self):
        self.client.start()

    def disconnect(self):
        self.client.stop()
        print("Client disconnected")


class ClickConnection:
    def __init__(self, db_name: str, credential_path: str, ssh_tunnel: SSHTunnel):
        self.credentials = yaml.safe_load(open(credential_path, "r"))
        self.host = self.credentials['CLICK_CREDENTIALS']['HOST']
        self.user = self.credentials['CLICK_CREDENTIALS']['USER']
        self.password = self.credentials['CLICK_CREDENTIALS']['PASSWORD']
        self.ssh_tunnel = ssh_tunnel
        self.port = ssh_tunnel.client.local_bind_port
        self.dbname = db_name
        self.connector = None
        self.coursor = None
        self.client = None
        self.__connection()
        self.engine = sqlalchemy.create_engine(
            """clickhouse+native://{user}:{password}@localhost:{port}/{dbname}""".format(user=self.user,
                                                                                         password=self.password,
                                                                                         port=self.port,
                                                                                         dbname=self.dbname)
        )

    def __connection(self):
        connection_string = """clickhouse://{user}:{password}@localhost:{port}/{dbname}""".format(user=self.user,
                                                                                                  password=self.password,
                                                                                                  port=self.port,
                                                                                                  dbname=self.dbname)
        self.connector = clickhouse_driver.connect(connection_string)
        self.client = clickhouse_driver.Client(host='127.0.0.1', port=self.port, database=self.dbname,
                                               password=self.password,
                                               settings={"use_numpy": True})
        self.coursor = self.connector.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self.connector

    @property
    def cursor(self):
        return self.coursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()
        print("Connection disconnected")

    def close_with_ssh(self, commit=True):
        if commit:
            self.commit()
        self.ssh_tunnel.disconnect()
        self.connection.close()
        print("Connection disconnected")

    def query_pandas(self, sql: str):
        return pd.read_sql_query(sql, self.connector)

    def write_pandas(self, data: pd.DataFrame, table_name: str):
        self.client.insert_dataframe("INSERT INTO {table} VALUES".format(table=table_name),
                                     data)

    def query(self, sql: str):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def execute(self, sql: str, params=None):
        self.cursor.execute(sql, params or ())


class MySqlConnection:
    def __init__(self, db_name: str, credential_path: str, ssh_tunnel: SSHTunnel):
        self.credentials = yaml.safe_load(open(credential_path, "r"))
        self.host = self.credentials['DATAMART_CREDENTIALS']['HOST']
        self.user = self.credentials['DATAMART_CREDENTIALS']['USER']
        self.password = self.credentials['DATAMART_CREDENTIALS']['PASSWORD']
        self.ssh_tunnel = ssh_tunnel
        self.port = ssh_tunnel.client.local_bind_port
        self.dbname = db_name
        self.connector = None
        self.coursor = None
        self.__connection()
        self.engine = sqlalchemy.create_engine(
            'mysql+pymysql://' + self.user + ':' + self.password + '@' + self.host + ':' + str(self.port) + '/' \
            + self.dbname + '?charset=utf8mb4')

    def __connection(self):
        self.connector = pymysql.connect(
            host='127.0.0.1',
            user=self.user,
            passwd=self.password,
            db=self.dbname,
            port=self.port)
        self.coursor = self.connector.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self.connector

    @property
    def cursor(self):
        return self.coursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()
        print("Connection disconnected")

    def close_with_ssh(self, commit=True):
        if commit:
            self.commit()
        self.ssh_tunnel.disconnect()
        self.connection.close()

    def query(self, sql: str, params=None):
        self.coursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def query_pandas(self, sql: str):
        return pd.read_sql_query(sql, self.connector)

    def execute(self, sql: str, params=None):
        self.coursor.execute(sql, params or ())


class MySqlFinanceConnection:
    def __init__(self, db_name: str, credential_path: str, ssh_tunnel: SSHTunnel):
        self.credentials = yaml.safe_load(open(credential_path, "r"))
        self.host = self.credentials['ABACUS_CREDENTIALS']['HOST']
        self.user = self.credentials['ABACUS_CREDENTIALS']['USER']
        self.password = self.credentials['ABACUS_CREDENTIALS']['PASSWORD']
        self.ssh_tunnel = ssh_tunnel
        self.port = ssh_tunnel.client.local_bind_port
        self.dbname = db_name
        self.connector = None
        self.coursor = None
        self.__connection()
        self.engine = sqlalchemy.create_engine(
            'mysql+pymysql://' + self.user + ':' + self.password + '@' + self.host + ':' + str(self.port) + '/' \
            + self.dbname + '?charset=utf8mb4')

    def __connection(self):
        self.connector = pymysql.connect(
            host='127.0.0.1',
            user=self.user,
            passwd=self.password,
            db=self.dbname,
            port=self.port)
        self.coursor = self.connector.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self.connector

    @property
    def cursor(self):
        return self.coursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()
        print("Connection disconnected")

    def close_with_ssh(self, commit=True):
        if commit:
            self.commit()
        self.ssh_tunnel.disconnect()
        self.connection.close()

    def query(self, sql: str, params=None):
        self.coursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def query_pandas(self, sql: str):
        return pd.read_sql_query(sql, self.connector)

    def execute(self, sql: str, params=None):
        self.coursor.execute(sql, params or ())


class TgConnection:
    def __init__(self, credential_path: str, chat_id: str):
        self.credentials = yaml.safe_load(open(credential_path, "r"))
        self.bot_token = self.credentials['TELEGRAM_CREDENTIALS']['BOT_TOKEN']
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=self.bot_token)

    def send_telegram_photo(self, path: str):
        self.bot.send_photo(chat_id=self.chat_id, photo=open(path, 'rb'))

    def send_telegram_message(self, text: str):
        self.bot.send_message(chat_id=self.chat_id, text=text, parse_mode='HTML')

    def send_telegram_media_group(self, paths: list, text: str):
        media_group = []
        for i in range(len(paths)):
            media_group.append(telegram.InputMediaPhoto(open(paths[i], "rb"),
                                                        caption=text if i == 0 else ''))
        self.bot.send_media_group(chat_id=self.chat_id, media=media_group)


class SlackConnection:
    def __init__(self, credential_path: str):
        self.credentials = yaml.safe_load(open(credential_path, "r"))
        self.bot_token = self.credentials['SLACK_CREDENTIALS']['BOT_TOKEN']
        self.client = WebClient(token=self.bot_token)

    # Channels go with coma-separators
    def send_file(self, channels: str, filepath: str) -> None:
        try:
            response = self.client.files_upload(channels=channels, file=filepath)
            assert response["file"]  # the uploaded file
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")

    def send_message(self, channels: str, text: str) -> None:
        try:
            response = self.client.chat_postMessage(channel=channels, text=text)
        except SlackApiError as e:
            print(f"Got an error: {e.response['error']}")


class BigQueryConnection:
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.client = None
        self.__connection()

    def __connection(self):
        self.client = bigquery.Client.from_service_account_json(json_credentials_path=self.credentials_path)
        return self.client

    def query(self, sql: str):
        query_job = self.client.query(sql)
        results = query_job.result()
        return results

    def query_pandas(self, sql_query: str) -> pd.DataFrame:
        return self.query(sql_query).to_dataframe()
