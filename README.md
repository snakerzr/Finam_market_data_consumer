# Simple rabbit_mq consumer for saving depth of market data to clickhouse

## Brief instructions

To test:
1. run rabbit mq `docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management `
2. run clickhouse server ` docker run -d --name docker_sandbox -p 8123:8123 -p 9000:9000 clickhouse/clickhouse-server:latest`
3. start main.py `python main.py`

Producer repo: https://github.com/snakerzr/Finam_market_data_producer

## .env file

`CLICKHOUSE_HOST` - clickhouse_host  
`CLICKHOUSE_PORT` - 9000  
`CLICKHOUSE_DB` - your_db_in_ch  
`CLICKHOUSE_TABLE` - your_table_in_db  
`RABBIT_MQ_HOST` - rabbit_mq_host  
`RABBIT_MQ_QUEUE_NAME` - rabbit_mq_queue_name  

## Docker build
Create consumer image example:
```commandline
docker build -t consumer:1 -f ./docker/Dockerfile .
```
or force fresh build with `--no-cache`

Start docker image
```commandline
docker run -it --rm --name consumer_test --env-file .env consumer:1 
```



