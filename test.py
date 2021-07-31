from os import truncate
from connect_box import ConnectionPool
import threading
import random
import time 

licznik = 0
lock = threading.Lock()
pool = ConnectionPool()

def quest_to_sql():
    
    global licznik

    command1 = """
            SELECT
                1 
            WHERE EXISTS (
                SELECT 
                    name 
                FROM 
                    users 
                WHERE 
                    name='admin');
        """ 
    command2 = """
                SELECT
                id_user
            FROM
                users
            WHERE
                name='admin';
            """
    command3 = """
                SELECT
                *
            FROM
                users;
            """       
    list_command = [command3, command2, command1]
    command = list_command[random.randrange(2)]
    conn = pool.get_connect()
    if conn:
        conn.cursor.execute(command)
        conn.connection.commit()
        print(conn.cursor.fetchone())
        pool.put_connect(conn)
        licznik += 1


class TestConnectionPool(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        quest_to_sql()


timer_start = time.time() + 50

def main():
    while True:
        time_finish = round(time.time(), 2)
        for element in [TestConnectionPool() for _ in range(50)]:
            element.start()
        if time_finish > timer_start:
            
            print(licznik)
            return

main()