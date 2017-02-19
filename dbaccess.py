import pymysql
from configparser import ConfigParser

CONFIGFILE = "CONFIG.txt"
config = ConfigParser()
config.read(CONFIGFILE)

host = config.get("mysqlConfig", "host")
port = config.get("mysqlConfig", "port")
username = config.get("mysqlConfig", "username")
passwd = config.get("mysqlConfig", "passwd")
charset = config.get("mysqlConfig", "charset")


def getcon(database):
    try:
        dbcon = pymysql.connect(host=host, user=username, password=passwd, database=database, charset=charset)
    except Exception as e:
        print(e)
    return dbcon

