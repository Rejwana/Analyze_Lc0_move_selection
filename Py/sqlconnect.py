from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
from mysql.connector.constants import SQLMode




def connect_sql():
    DB_NAME = 'EGTB'

    config = {
      'user': 'root',
      'password': '123456ab',
      'host': '127.0.0.1',
      'database': 'EGTB',
      'raise_on_warnings': True
    }

    cnx = mysql.connector.connect(**config)
    cnx.sql_mode = SQLMode.STRICT_ALL_TABLES
    cursor = cnx.cursor()
    return cnx,cursor


def create_table(TB_name):
    TABLES = {}
    Table_name = 'positions_'+TB_name
    TABLES[Table_name] = (
        "CREATE TABLE `"+Table_name+"` ("
        "  `position` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,"
        "  `winning_moves` varchar (400),"
        "  `loosing_moves` varchar (400),"
        "  `drawing_moves` varchar (400),"
        "  `best_moves` varchar (400),"
        "  `WDL` enum('W','L','D') NOT NULL,"
        "  `WDL_score` integer NOT NULL,"
        "  `dtz_score` integer NOT NULL,"
        "  PRIMARY KEY (`position`)"
        ") ENGINE=InnoDB")

    cnx,cursor = connect_sql()


    for table_name in TABLES:
        table_description = TABLES[table_name]
    
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        
def insert_into(TB_name,psn,winning_moves,loosing_moves,drawing_moves,best_moves,WDL,WDL_score,dtz_score):
    cnx,cursor = connect_sql()
    add_psn = ("INSERT IGNORE INTO `positions_"+TB_name+"` "
                   "(`position`,`winning_moves`, `loosing_moves`, `drawing_moves`, `best_moves`, `WDL`,`WDL_score`, `dtz_score`)"
                   "VALUES (%(position)s,%(winning_moves)s,%(loosing_moves)s,%(drawing_moves)s,%(best_moves)s, %(WDL)s, %(WDL_score)s, %(dtz_score)s); ")

    
    psn_info = {
      'position': psn,
      'WDL': WDL,
      'winning_moves':winning_moves,
      'loosing_moves':loosing_moves,
      'drawing_moves':drawing_moves,
      'best_moves':best_moves,
      'WDL_score': WDL_score,
      'dtz_score': dtz_score
    }


    try:

        cursor.execute(add_psn, psn_info)
    except mysql.connector.Error as err:
        if err.errno == 1062:
            print("already exists."+psn)
        else:
            print(err.msg)



    cnx.commit()
    cursor.close()
    cnx.close()

