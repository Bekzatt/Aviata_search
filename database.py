import sqlite3

conn = sqlite3.connect('dbms.db')
cursor = conn.cursor()
'''
create table customers(
 id bigint primary key,
 name varchar(30),
 one_direction bool,
 source_city varchar(30),
 dest_city varchar(30),
 flight_date date,
 return_date date
)
'''
def getUser(id):
    sql = f"select * from customers where id={id}"
    cursor.execute(sql)
    return cursor.fetchone()

def setUser(id,data):
    one_direction = False
    if 'reg' in data.keys():
        sql = f"delete from customers where id={id}"
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
    if data['type'] == 'one':
        one_direction = True
        sql = f"INSERT INTO customers(id, name, one_direction, source_city, dest_city, flight_date) " \
              f"VALUES ({id}, '{data['name']}',{one_direction}, '{data['source']}', '{data['dest']}', '{data['flight_date']}'); "
    else:
        return_date = data['return_date']
        sql = f"INSERT INTO customers(id, name, one_direction, source_city, dest_city, flight_date, return_date) " \
              f"VALUES ({id}, '{data['name']}',{one_direction}, '{data['source']}', '{data['dest']}', '{data['flight_date']}', '{return_date}'); "

    cursor.execute(sql)
    conn.commit()