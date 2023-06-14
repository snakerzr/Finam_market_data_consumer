import pika, sys, os, datetime
from clickhouse_driver import Client
import json
from pytz import timezone
import src.config as config

def main():
    # clickhouse connection
    clickhouse_client = Client(host=config.CLICKHOUSE_HOST, port=config.CLICKHOUSE_PORT)

    clickhouse_client.execute(f'''
    CREATE DATABASE IF NOT EXISTS {config.CLICKHOUSE_DB};
    ''')

    # 'ask - минимальная цена покупки, bid - максимальная цена продажи'
    clickhouse_client.execute(f"""
        CREATE TABLE IF NOT EXISTS {config.CLICKHOUSE_DB}.{config.CLICKHOUSE_TABLE} (        
            datetime DateTime(6, 'Europe/Moscow'),
            type Enum8('ask' = 1, 'bid' = 2),
            price Float32,
            volume Int32
        )
        ENGINE = MergeTree()
        ORDER BY (datetime)
    """)


    # rabbit connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(config.RABBIT_MQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=config.RABBIT_MQ_QUEUE_NAME)

    def process_market_data(ch, method, properties, body):
        # Deserialize the JSON message back to a dictionary
        market_data = json.loads(body)

        receive_time = market_data['receive_time']

        timezone_name = 'Europe/Moscow'
        timezone_obj = timezone(timezone_name)
        receive_time = timezone_obj.localize(datetime.datetime.strptime(receive_time, '%Y-%m-%d %H:%M:%S.%f'))



        asks = market_data['asks']
        bids = market_data['bids']

        asks = [{**d, 'type': 'ask', 'datetime': receive_time} for d in asks]
        bids = [{**d, 'type': 'bid', 'datetime': receive_time} for d in bids]

        market_data = asks + bids

        market_data = [{**dict_, 'volume':int(dict_['quantity'])} for dict_ in market_data]

        columns = ['datetime','type','price','volume']

        market_data = [{key: dict_[key] for key in columns} for dict_ in market_data]
        print(market_data)
        print(columns)



        # Insert the market data into ClickHouse
        query = f'INSERT INTO {config.CLICKHOUSE_DB}.{config.CLICKHOUSE_TABLE} ({",".join(columns)}) VALUES'
        clickhouse_client.execute(query,
                                  market_data)

        print(' [x] Processed market data:', market_data)

    channel.basic_consume(queue=config.RABBIT_MQ_QUEUE_NAME,
                          auto_ack=True,
                          on_message_callback=process_market_data)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)