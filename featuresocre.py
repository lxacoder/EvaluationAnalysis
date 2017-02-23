import dbaccess

con = dbaccess.getcon("other")
cursor1 = con.cursor()
cursor2 = con.cursor()
cursor3 = con.cursor()
cursor4 = con.cursor()
cursor5 = con.cursor()
cursor6 = con.cursor()
cursor7 = con.cursor()
cursor8 = con.cursor()
cursor9 = con.cursor()

sql1 = "SELECT DISTINCT category FROM koubei"
sql2 = "SELECT p.feature,s.sentenceid,s.score FROM potentialfeature p,sentencescore s WHERE " \
       "p.reviewsentence_id = s.sentenceid AND p.category = %s"
sql3 = "INSERT INTO findfeaturesentences VALUES (NULL ,%s,%s,%s,%s)"
sql4 = "INSERT INTO featurewisescore VALUES (%s,%s,%s,%s)"
sql5 = "SELECT * FROM featurewisescore WHERE feature = %s AND category=%s"
sql6 = "UPDATE featurewisescore SET negativescore = %s WHERE feature = %s AND category = %s"

# 查询每个车型
cursor1.execute(sql1)
while True:
    categoryrow = cursor1.fetchone()
    if categoryrow is None:
        break
    category = categoryrow[0]

    # 查询该车型的feature,sentenceid,sentencecore
    cursor2.execute(sql2, category)

    featurescore = dict()
    while True:
        row = cursor2.fetchone()
        if row is None:
            break
        feature = row[0].lower()
        sentenceid = row[1]
        positivesocre = row[2]
        print(category+":"+feature)
        # 如果该sentence的分数>0,大于0和小于0执行不同的操作
        if positivesocre > 0:
            if feature in featurescore:
                featurescore[feature] = featurescore[feature] + positivesocre
            else:
                featurescore[feature] = positivesocre
            cursor3.execute(sql3, (category, feature, sentenceid, 1))
            con.commit()

    enties = featurescore.items()

    for item in enties:
        cursor4.execute(sql4, (category, item[0], item[1], 0))
        con.commit()

    featurescore.clear()

    cursor5.execute(sql2, category)
    while True:
        row = cursor5.fetchone()
        if row is None:
            break
        feature = row[0]
        sentenceid = row[1]
        negativescore = row[2]

        if negativescore < 0:
            if feature in featurescore:
                featurescore[feature] = featurescore[feature]+negativescore
            else:
                featurescore[feature] = negativescore
            cursor6.execute(sql3, (category, feature, sentenceid, -1))
            con.commit()

    enties = featurescore.items()

    for item in enties:
        cursor7.execute(sql5, (item[0], category))
        one = cursor7.fetchone()
        if one is None:
            cursor9.execute(sql4, (category, item[0], 0, item[1]))
            con.commit()
        else:
            cursor8.execute(sql6, (item[1], item[0], category))
            con.commit()
con.close()
