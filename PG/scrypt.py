
import psycopg2 , os, time

from psycopg2 import Error

try:
    # Подключиться к существующей базе данных
    connection = psycopg2.connect(user=os.environ["DB_USER"],
                                  # пароль, который указали при установке PostgreSQL
                                  password=os.environ["DB_PASS"],
                                  host=os.environ["DB_HOST"],
                                  port=os.environ["DB_PORT"], 
                                  database=os.environ["DB_NAME"])
    
    cursor = connection.cursor()
#сюда делей
    time.sleep(1200)
    create_table_query = '''CREATE TABLE mobile
                          (ID INT PRIMARY KEY     NOT NULL,
                          MODEL           TEXT    NOT NULL,
                          PRICE         REAL); '''
    # Выполнение команды: это создает новую таблицу
    cursor.execute(create_table_query)
    connection.commit()
    print("Таблица успешно создана в PostgreSQL")



        
    # Выполнение SQL-запроса для вставки данных в таблицу
    insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES
                                          (1, 'IPhone 12', 1000),
                                          (2, 'Google Pixel 2', 700),
                                          (3, 'Samsung Galaxy S21', 900),
                                          (4, 'Nokia', 800)"""
    cursor.execute(insert_query)
    connection.commit()



    postgreSQL_select_Query = "select * from mobile"
    cursor.execute(postgreSQL_select_Query)
    print("Выбор строк из таблицы mobile с помощью cursor.fetchall")
    mobile_records = cursor.fetchall()
    print("Вывод каждой строки и ее столбцов")
    for row in mobile_records:
            print("Id =", row[0], )
            print("model =", row[1])
            print("price =", row[2], "\n")
        
except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")