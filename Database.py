import pymysql
import json
import os
from utils.common_logs import _logger as logger
import logging
 
with open('conf/conf.json') as json_data_file:
    config_data = json.load(json_data_file)

MYSQL_HOST    = config_data['host']
MYSQL_PORT    = config_data['port']
MYSQL_USER    = config_data['user']
MYSQL_PASSWD  = config_data['passwd']
MYSQL_DB      = config_data['db']


class Database:
    def __enter__(self):
        logger.info("=========Database START==========") 
        return self

    def __init__(self):
        host = MYSQL_HOST
        port = int(MYSQL_PORT)
        user = MYSQL_USER
        password = MYSQL_PASSWD
        db = MYSQL_DB
        charset = 'utf8'
        try:
            self.con = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
            self.curs = self.con.cursor()
            self.curs_dict = self.con.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            logger.error("pymysql.connect : {}".format(e))  


    def select_user(self):
        try:
            query = """ SELECT NAME FROM USER;"""
            self.curs.execute(query)
            result = self.curs.fetchall()
            return result
        except Exception as e:
            logger.error("select_user : {}".format(e))


    def __exit__(self, type, value, traceback):
        if self.con:
            logger.info("==========connection END============") 
            self.curs.close()
            self.curs_dict.close()
            self.con.close()
