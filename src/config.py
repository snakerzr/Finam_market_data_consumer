from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT")
CLICKHOUSE_DB = os.getenv("CLICKHOUSE_DB")
CLICKHOUSE_TABLE = os.getenv("CLICKHOUSE_TABLE")

RABBIT_MQ_HOST = os.getenv('RABBIT_MQ_HOST')
RABBIT_MQ_QUEUE_NAME = os.getenv('RABBIT_MQ_QUEUE_NAME')