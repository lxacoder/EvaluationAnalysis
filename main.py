# -- coding: utf-8 --
import dbaccess
import re



def breakreviewintosentence(inputstring):
    regex1 = "【(.*?)】"
    # 这里遇到的坑 http://www.crifan.com/python_re_search_vs_re_findall/
    regex2 = "】(.*?)(?:【|$)"
    pat1 = re.compile(regex1)
    pat2 = re.compile(regex2)
    para = inputstring.strip()
    features = re.findall(pat1, para)
    features_details = re.findall(pat2, para)
    for feature in zip(features, features_details):


con = dbaccess.getcon("other")
cursor


file = open("test.txt", 'r', encoding="utf8")
string = file.read()
breakreviewintosentence(string)
