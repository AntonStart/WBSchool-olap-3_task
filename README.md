# WBSchool-olap-3_task
KAFKA+ZOOKEEPER+CLICKHOUSE

* Задание:
1. поднять в docker-compose, из репозитория + sasl. выложить в свой git
2. создать топик, создаётся автоматически при записи данных
3. написать python скрипт для заливки данных из небольшой таблицы клика (пегас) в топик кафка в формате json. Всю таблицу не нужно пушить, достаточно limit 100. выложить скрипт в свой git
4. программа Offset Explorer, просмотреть данные в топике. выложить скрины с результатами в свой git
5. чтение из топика питоном. выложить в свой git
!!!!! не выкладывать логопасы в репозиторий

* Решение:
1. Написал [docker-compose.yml](https://github.com/AntonStart/WBSchool-olap-3_task/blob/main/docker-compose.yml) И добавил в единый каталог с ним файлы с конфигурациями для SASL аутентификации.
   [client.properties](https://github.com/AntonStart/WBSchool-olap-3_task/blob/main/client.properties)  - для кафка-клиента,
   [kafka_server_jaas.conf](https://github.com/AntonStart/WBSchool-olap-3_task/blob/main/kafka_server_jaas.conf) - для кафка-сервера,
   [zookeeper_jaas.conf](https://github.com/AntonStart/WBSchool-olap-3_task/blob/main/zookeeper_jaas.conf) - для zookeeper.

   Запустил, используя wsl консоль (docker-compose up -d), предварительно открыв docker-desktop.

2. Открыл [Offset Explorer 3.0](https://www.kafkatool.com/) настроил подключение. Создал топик.
3. Написал скрипт для отправки сообщений в топик [kafka_producer.py](https://github.com/AntonStart/WBSchool-olap-3_task/blob/main/kafka_producer.py)
4. Проверил результ [тут скрин](https://github.com/AntonStart/WBSchool-olap-3_task/blob/main/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202024-06-18%20164846.jpg)
5. Взял готовый скрипт из репы на чтение из kafka, поменяв только имя топика. [kafka_consumer](https://github.com/AntonStart/WBSchool-olap-3_task/blob/main/kafka_consumer.py)   
