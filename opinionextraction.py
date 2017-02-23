import dbaccess
import os

con = dbaccess.getcon("other")
cursor1 = con.cursor()
cursor2 = con.cursor()
cursor3 = con.cursor()
sql1 = "SELECT p.id,p.reviewsentementid FROM postag p,reviewsentiment r,featureclass f,koubei k " \
       "WHERE p.reviewsentementid = r.id AND r.featureclassid = f.id AND f.reviewid = k.id AND k.category = %s AND p.word = %s"
sql2 = "SELECT word,id FROM postag WHERE reviewsentementid = %s AND " \
       "(postag = 'a' OR postag = 'an' OR postag = 'al')"
sql3 = "INSERT INTO potentialfeature (feature,opinionword,category,reviewsentence_id,posTagId) VALUES (%s, %s, %s, %s,%s)"
for filename in os.listdir("./featuresetafterfpgrowth"):
    category = filename.split(".")[0]
    f = open(os.path.join("./featuresetafterfpgrowth", filename), "r", encoding="utf8")
    features = f.readlines()
    for fea in features:
        feature = fea.split(":")[0]
        if feature == "人" or feature == "车":
            print("continue")
            continue
        print(category+":"+feature+" is processing")
        cursor1.execute(sql1, (category, feature))
        while True:
            row1 = cursor1.fetchone()
            if row1 is None:
                break
            tagid = row1[0]
            sentenceid = row1[1]
            cursor2.execute(sql2, sentenceid)
            mindistanceid = 9999999
            while True:
                postagrow = cursor2.fetchone()
                if postagrow is None:
                    break
                opinionword = postagrow[0]
                opinionwordid = postagrow[1]
                if abs(opinionwordid-tagid) <= 6:
                    if abs(opinionwordid - tagid)< abs(mindistanceid-tagid):
                        nearestopinin = opinionword
                        mindistanceid = opinionwordid
            if mindistanceid != 9999999:
                cursor3.execute(sql3, (feature, opinionword, category, sentenceid, mindistanceid))
    con.commit()



