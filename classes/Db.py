from classes.singleton import Singleton
import mysql.connector
from bot.creds import db_name, db_password, db_url, db_user_name
import functools
import logging
import time
import re
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


logger = logging.getLogger(__name__)

class Db(metaclass=Singleton):
    
    def __init__(self):
        self.db_name = db_name,
        self.db_password = db_password,
        self.db_url = db_url,
        self.user_name = db_user_name
        logger.info(f"action: {self}, context: {db_url}")

    def get_connection(func):
        @functools.wraps(func)
        def get_connection_wrapper(self, *args, **kwargs):
            try:
                with mysql.connector.connect(
                    host=db_url,
                    user=db_user_name,
                    password=db_password,
                    database=db_name
                    ) as connection:
                        logger.info(f"connection: {connection}, context: {self}")

                        return func(self, connection = connection, *args, **kwargs)
            except mysql.connector.Error as e:
                print(f"failed to connect to db: {e}")
        return get_connection_wrapper

    @get_connection
    def query(self, connection = None, query = ''):
        if not query or not connection:
            return False
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
            
    @get_connection
    def insert(self, connection = None, tb_name = '' , insert_model = None):
        if not insert_model or not connection or not tb_name:
            return False
        model_dict = insert_model.to_dict(reset=True)
        model_dict["last_update"] = str(time.time())
        fields = "("
        fields += ",".join(["`" + str(key) + "`" for key in model_dict.keys()])
        fields += ")"

        values = "("
        values += ",".join(["%s" for val in model_dict.values()])
        values += ")"

        query = f"INSERT INTO `{tb_name}` {fields} VALUES {values}"
        with connection.cursor() as cursor:
            cursor.execute(query, tuple(model_dict.values()))
            connection.commit()