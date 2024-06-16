import psycopg2
import os
import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/count')
def count():
    try:
        connection = psycopg2.connect(
                    user=os.environ["DB_USER"],
                    password=os.environ["DB_PASS"],
                    host=os.environ["DB_HOST"],
                    port=os.environ["DB_PORT"],
                    database=os.environ["DB_NAME"]
        )
        cur = conn.cursor()
        cur.execute('SELECT count(*) FROM mobile')
        result = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify(count=result[0])
    except Exception as e:
        return str(e), 500

@app.route('/healthz')
def healthz():
    return 'OK', 200

@app.route('/readiness')
def readiness():
    return 'READY', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    # Даем время базе данных запуститься
    time.sleep(40)
    
    # Подключение к базе данных и создание таблицы
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        create_table_query = '''CREATE TABLE IF NOT EXISTS mobile
                                (ID INT PRIMARY KEY NOT NULL,
                                 MODEL TEXT NOT NULL,
                                 PRICE REAL);'''
        cursor.execute(create_table_query)
        connection.commit()
        
        insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES
                            (1, 'IPhone 12', 1000),
                            (2, 'Google Pixel 2', 700),
                            (3, 'Samsung Galaxy S21', 900),
                            (4, 'Nokia', 800)
                            ON CONFLICT (ID) DO NOTHING;"""
        cursor.execute(insert_query)
        connection.commit()

        cursor.close()
        connection.close()
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    # Запуск Flask приложения
    app.run(host='0.0.0.0', port=8000)
