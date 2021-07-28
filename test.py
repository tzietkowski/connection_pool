from connect_box import ConnectionPool
import threading



pool = ConnectionPool()

def quest_to_sql():
    
    
    command = """
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
    conn = pool.get_connect()
    conn.cursor.execute(command)
    conn.connection.commit()
    return conn.cursor.fetchone()


class TestConnectionPool(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        ans = quest_to_sql()
        print(ans)
        print(pool.count
        )


#Test 1 - Utworzenie 50 połaczeń - OK

lista_1 = [TestConnectionPool() for _ in range(98)]
for element in lista_1:
    element.start()
for element in lista_1:
    element.join()
pass
