import psycopg2
import os
import json
import threading


lock = threading.Lock()

class ConnectionBase():
    """"Class connection base"""
    
    def __init__(self) -> None:
        self.__load_config()
        try:
            self.connection = psycopg2.connect(
                                    host="localhost",
                                    database = self.__db_name,
                                    user = self.__user_db,
                                    password = self.__pass_db)
            self.cursor = self.connection.cursor()
        except psycopg2.OperationalError:
             self.connection = None
             self.cursor = None


    def __del__(self) -> None:
        self.cursor.close()
        self.connection.close()

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
        self.count = self.__count_free_connect()

    def __add_new_connect(self) -> None:
        """"Add new connect to data base"""

        if self.__count_free_connect() < self.__max_free_connect and not len(self.list_connection) == self.__max_user_connect:
            self.list_connection[ConnectionBase()] = False

    def __del_connect(self) -> None:
        """Delete not use connect"""

        while self.__count_free_connect() > self.__max_free_connect:
            print('usuwam')
            del self.list_connection[self.__check_no_busy_connect()]


    def __check_no_busy_connect(self) -> int:
        """Check no busy connect - return index"""

        for value in self.list_connection.items():
            if value[0].connection == None:
                print('ok')
            
            if value[1] == False and value[0].connection != None:
                return value[0]
        return None

    def __count_free_connect(self) -> int:
        """Count free connect"""

        return sum(value == False for value in self.list_connection.values())


    def get_connect(self) -> ConnectionBase:
        """Get connect to data base"""
        global lock

        lock.acquire()
        
        free_socket = self.__check_no_busy_connect()
        if free_socket != -1:
            self.list_connection[free_socket] = True
       
        self.count = self.__count_free_connect()
        if self.__count_free_connect()  < self.__max_free_connect:
            self.__add_new_connect()
        lock.release()
        return free_socket


    def put_connect(self, connect:ConnectionBase) -> None:
        """Put connection"""

        self.list_connection[connect] = False
        while self.__count_free_connect()  > self.__max_free_connect:
            self.__del_connect()
        