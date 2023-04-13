import pymysql

db_setting = {

    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "aa552300",
    "db": "test"

}


class _DataBase:
    def __init__(
            self,
            host,
            port,
            user,
            password,
            db_name,
    ):
        # Connect to the database
        self.__connection = pymysql.connect(host=host, port=port, user=user, password=password, db=db_name)
        self.__cursor = self.__connection.cursor()

    def _connect(self):
        """與資料庫開啟會話(連線)"""
        self.__connection.ping(reconnect=True)

    def _query(self, sql: str):
        """寫入sql查詢語法"""
        self.__cursor.execute(sql)

    def fetchone(self):
        """取得一筆資料"""
        return self.__cursor.fetchone()

    def fetchall(self):
        """取得全部資料"""
        return self.__cursor.fetchall()

    def update(self):
        """更新資料"""
        self._commit()

    def insert(self):
        """插入資料"""
        self._commit()

    def _commit(self):
        """提交"""
        self.__connection.commit()
        self.__connection.close()


class MySqlProxy:
    def __init__(self):
        self._db = _DataBase(**db_setting)

    @property
    def session(self):
        getattr(self._db, '_connect')()
        return self

    def query(self, sql: str) -> _DataBase:
        """寫入sql查詢語法"""
        getattr(self._db, '_query')(sql)
        return self._db


class MySqlConnection:

    def __init__(
            self,
            host,
            port,
            user,
            password,
            db_name,
    ):
        # Connect to the database
        self.connection = pymysql.connect(host=host, port=port, user=user, password=password, db=db_name)
        self.__cursor = self.connection.cursor()

    @property
    def session(self):
        """與資料庫開啟會話(連線)"""
        self.connection.ping(reconnect=True)
        return self

    def query(self, sql: str):
        """寫入sql查詢語法"""
        self.__cursor.execute(sql)
        return self

    def fetchone(self):
        """取得一筆資料"""
        return self.__cursor.fetchone()

    def fetchall(self):
        """取得全部資料"""
        return self.__cursor.fetchall()

    def update(self):
        """更新資料"""
        self._commit()

    def insert(self):
        """插入資料"""
        self._commit()

    def _commit(self):
        """提交"""
        self.connection.commit()
        self.connection.close()


db = MySqlProxy()
db.session.query('...').fetchall()
