from confluent_kafka import Producer
from Utils.Connect_DB import connect_CH
from bson import json_util
import json

# Конфиги Kafka
kafka_config = {
    'bootstrap.servers': 'localhost:9093',
    'client.id': 'simple-producer',
    'sasl.mechanism':'PLAIN',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.username': 'admin',
    'sasl.password': 'admin-secret'
}

# Экземпляр продюсера
producer = Producer(**kafka_config)

# Экземпляр клиента CH для запроса
clickhouse_client = connect_CH()

# Функция для обработки результата запроса в КХ -> JSON

def execute_clickhouse_query(query):
    try:
        with clickhouse_client as client:
            result = client.execute(query, with_column_types=True)
            columns = [column[0] for column in result[1]]  # Получаем имена столбцов
            rows = [dict(zip(columns, row)) for row in result[0]]  # Преобразуем результат в список словарей
            return json.dumps(rows, default=json_util.default)  # Преобразуем в JSON
    except Exception as e:
        print(f"Error executing ClickHouse query: {e}")
        return None

# Callback функция, вызываемая при доставке сообщения в Kafka
def delivery_report(err, msg):
    """Callback функция, вызываемая при доставке сообщения в Kafka."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# Отправка сообщения в топик
def send_to_kafka(topic, data):
    try:
        producer.produce(topic, data, callback=delivery_report)
        producer.flush()
    except BufferError:
        print(f"Local producer queue is full ({len(producer)} messages awaiting delivery): try again")

# Точка входа в скрипт
if __name__ == '__main__':
    topic = 'tareLoad_topic'
    result = execute_clickhouse_query(f"""
                                select tare_id
                                    , is_load
                                    , dt
                                    , tare_sticker
                                    , tare_type
                                    , office_id
                                    , dst_office_id
                                    , wh_tare_entry
                                    , dt_reported
                                    , task_id
                                    , licence_plate        
                                from tareLoad
                                where dt > now() - interval 3 hour
                                    and tare_id > 1000000
                                order by dt desc
                                limit 100 
                                FORMAT JSONEachRow
                             """)
    if result is not None:
        send_to_kafka(topic, result)
    else:
        print("Failed to fetch data from ClickHouse.")
