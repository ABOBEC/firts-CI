import psycopg2  # Библиотека для работы с PostgreSQL
import os  # Модуль для работы с переменными окружения
import time  # Модуль для работы с временем (для задержек)
from flask import Flask, jsonify  # Flask для создания веб-приложения, jsonify для возврата JSON-ответов
from healthcheck import HealthCheck  # Импортируем библиотеку healthcheck

app = Flask(__name__)  # Создаем экземпляр Flask

# Глобальная переменная для отслеживания состояния готовности
is_ready = False

# Функция для подключения к базе данных
def connect_db():
    global is_ready  # Используем глобальную переменную is_ready
    try:
        time.sleep(40)  # Задержка в 40 секунд для ожидания готовности базы данных
        connection = psycopg2.connect(  
            user=os.environ["DB_USER"],  
            password=os.environ["DB_PASS"],  
            host=os.environ["DB_HOST"],  
            port=os.environ["DB_PORT"],  
            database=os.environ["DB_NAME"]  
        )
        cursor = connection.cursor()  # Создаем курсор для выполнения SQL-запросов

        # Создаем таблицу, если она еще не существует
        create_table_query = '''CREATE TABLE IF NOT EXISTS mobile
                              (ID INT PRIMARY KEY NOT NULL,
                              MODEL TEXT NOT NULL,
                              PRICE REAL);'''
        cursor.execute(create_table_query)  
        connection.commit()  
        print("Таблица успешно создана в PostgreSQL")

        # Вставляем данные в таблицу
        insert_query = """INSERT INTO mobile (ID, MODEL, PRICE) VALUES
                          (1, 'IPhone 12', 1000),
                          (2, 'Google Pixel 2', 700),
                          (3, 'Samsung Galaxy S21', 900),
                          (4, 'Nokia', 800)
                          ON CONFLICT (ID) DO NOTHING;"""
        cursor.execute(insert_query)  
        connection.commit()  

        # Устанавливаем флаг готовности
        is_ready = True

        cursor.close()  # Закрываем курсор
        connection.close()  # Закрываем соединение с базой данных
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)  # Выводим ошибку, если возникла проблема
        is_ready = False

# Запуск функции подключения к базе данных в фоновом режиме
connect_db()

# Создаем экземпляр HealthCheck
health = HealthCheck(app, "/healthz")
readiness = HealthCheck(app, "/readiness")

# Функция для проверки живости
def liveness_check():
    return True, "alive"

# Функция для проверки готовности
def readiness_check():
    if is_ready:
        return True, "ready"
    else:
        return False, "not ready"

# Добавляем проверки в HealthCheck
health.add_check(liveness_check)
readiness.add_check(readiness_check)

@app.route('/count')
def count():
    try:
        connection = psycopg2.connect(  # Подключаемся к базе данных PostgreSQL
            user=os.environ["DB_USER"],  
            password=os.environ["DB_PASS"],  
            host=os.environ["DB_HOST"],  
            port=os.environ["DB_PORT"], 
            database=os.environ["DB_NAME"]  
        )
        cursor = connection.cursor()  # Создаем курсор для выполнения SQL-запросов
        cursor.execute("SELECT COUNT(*) FROM mobile")  
        count = cursor.fetchone()[0]  
        cursor.close()  
        connection.close()  
        return jsonify(count=count), 200  # Возвращаем количество записей и статус 200
    except (Exception, psycopg2.Error) as error:
        return jsonify(error=str(error)), 500  # Возвращаем ошибку и статус 500, если возникла проблема

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  # Запускаем Flask приложение на порту 8000
