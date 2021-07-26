import psycopg2
import os
import json
import asyncio
from time import time

class ConnectionBase():
    """"Class connection base"""
    
    count_connect = 0

    def __init__(self) -> None:
        self.__load_config()
        ConnectionBase.count_connect +=1 
        self.numer_connect = ConnectionBase.count_connect
        self.connection = psycopg2.connect(
                                host="localhost",
                                database = self.__db_name,
                                user = self.__user_db,
                                password = self.__pass_db)
        self.cursor = self.connection.cursor()
        

    def __del__(self) -> None:
        self.cursor.close()
        self.connection.close()
        ConnectionBase.count_connect -=1 

    def __load_config(self) -> None:
        """Load config parameters"""

        if os.path.isfile('config.ini'):
             with open('config.ini', 'r') as outfile:
                data = json.load(outfile)
                self.__db_name = data['db_name']
                self.__user_db = data['user_db']
                self.__pass_db = data['pass_db']
        else:
            print('Configuration file not found')
            raise NameError('No configuration file')


class ConnectionPool():
    """Class connection Pool"""

    def __init__(self) -> None:
        self._start_user_connect = 10
        self.list_connection = {ConnectionBase(): False for _ in range(self._start_user_connect)}
        self.__max_user_connect = 100
        self.__max_free_connect = 5
        self.time_start = time()
        #self.loop()

    def loop(self) -> None:
        while True:
            pass
            #self.__add_new_connect()
            #self.__del_connect()

    def __add_new_connect(self):
        """"Add new connect to data base"""

        if self.__count_free_connect() < self.__max_free_connect and not len(self.list_connection) == self.__max_user_connect:
            self.list_connection[ConnectionBase()] = [False]
            return True
        else:
            return False

    def __del_connect(self):
        """Delete not use connect"""

        while self.__count_free_connect() > self.__max_free_connect:
            print('usuwam')
            del self.list_connection[self.__check_no_busy_connect()]


    def __check_no_busy_connect(self) -> int:
        """Check no busy connect - return index"""

        for value in self.list_connection.items():
            if value[1] == False:
                return value[0]
        return -1

    def __count_free_connect(self) -> int:
        """Count free connect"""

        return sum(value == False for value in self.list_connection.values())


    def get_connect(self) -> ConnectionBase:
        """Get connect to data base"""

        free_socket = self.__check_no_busy_connect()
        if free_socket != -1:
            self.list_connection[free_socket] = True
            return free_socket
        else:
            return None

    def put_connect(self, connect:ConnectionBase) -> None:
        """Put connection"""

        self.list_connection[connect] = False
        


k = ConnectionPool()
print(k.list_connection)
print(k.del_connect())
print(k.list_connection)

#print(k.list_connection.values())

#g = k.get_connect()
#print(k.list_connection)

#print(k.put_connect(g))
#print(k.list_connection)

#print(k.count_free_connect())