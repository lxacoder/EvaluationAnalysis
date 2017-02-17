import pymysql
from configparser import ConfigParser

CONFIGFILE = "CONFIG.txt"
config = ConfigParser()
config.read(CONFIGFILE)

host = config.get("mysqlConfig", "host")
username = config.get("mysqlConfig", "username")
passwd = config.get("mysqlConfig", "passwd")


def getcon(database):
    try:
        dbcon = pymysql.connect(host=host, username=username, password=passwd, database=database)
    except Exception as e:
        print(e)
    return dbcon

