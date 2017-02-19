# -- coding: utf-8 --
import dbaccess
import re


def speratefeatures(inputstring):
    regex1 = "【(.*?)】"
    # 这里遇到的坑 http://www.crifan.com/python_re_search_vs_re_findall/
    regex2 = "】(.*?)(?:【|$)"
    pat1 = re.compile(regex1)
    pat2 = re.compile(regex2)
    reviewid = inputstring[0]
    reviewsentence = inputstring[1]
    para = reviewsentence.strip()
    # 两个模式让其分离出各种特性
    features = re.findall(pat1, para)
    features_details = re.findall(pat2, para)
    sqlinsertfeatureclass = "INSERT INTO featureclass (feature,detail,reviewid) VALUES (%s,%s,%s)"

    # 如果输入中不包含特性
    with con.cursor() as cursor:
        if len(features) == 0:
            feature = "无"
            features_detail = reviewsentence
            cursor.execute(sqlinsertfeatureclass, (feature, features_detail, reviewid))
            lastrowid = cursor.lastrowid
            breakintosentence(features_detail, lastrowid)
        else:
            for feature, features_detail in zip(features, features_details):
                cursor.execute(sqlinsertfeatureclass, (feature, features_detail, reviewid))
                lastrowid = cursor.lastrowid
                breakintosentence(features_detail, lastrowid)


def breakintosentence(inputstring, lastrowid):
    regex = "[。？！]+"
    pattern = re.compile(regex)
    sentences = re.split(pattern, inputstring)
    sql = "INSERT INTO reviewsentiment (sentence, featureclassid) VALUES (%s,%s)"
    with con.cursor() as cursor:
        for sentence in sentences:
            if sentence.strip() == "":
                continue
            cursor.execute(sql, (sentence, lastrowid))


con = dbaccess.getcon("other")
try:
    with con.cursor() as cursor:
        processnum = 0
        sqltotal = "SELECT count(*) FROM koubei"
        cursor.execute(sqltotal)
        total = cursor.fetchone()[0]
    with con.cursor() as cursor:
        sql = "SELECT id,neirong FROM koubei WHERE id > 76975"
        cursor.execute(sql)
        while True:
            one = cursor.fetchone()
            if one is None:
                break
            speratefeatures(one)
            if processnum % 5 == 0:
                con.commit()
            processnum += 1
            print("processing:" + str(processnum) + "/" + str(total))
except Exception as e:
    print(e)
finally:
    con.commit()
    con.close()


# file = open("test.txt", 'r', encoding="utf8")
# string = file.read()
# breakreviewintosentence(string)
