import dbaccess

con = dbaccess.getcon("other")

cursor1 = con.cursor()
cursor2 = con.cursor()
cursor3 = con.cursor()
cursor4 = con.cursor()

sql1 = "SELECT DISTINCT category FROM koubei"
sql2 = "select DISTINCT feature from findfeaturesentences WHERE category = %s"
sql3 = "SELECT positivescore,negativescore FROM featurewisescore WHERE category = %s AND " \
       "feature = %s"
sql4 = "SELECT sentence,orientation FROM findfeaturesentences " \
       "INNER JOIN reviewsentiment r ON r.id = sentenceid WHERE feature=%s " \
       "AND category=%s ORDER BY orientation DESC "

cursor1.execute(sql1)
while True:
    row = cursor1.fetchone()
    if row is None:
        break
    category = row[0]
    f = open("./finalresult/"+category+".txt", "w", encoding="utf-8")
    print(category)
    cursor2.execute(sql2, category)
    while True:
        row = cursor2.fetchone()
        if row is None:
            break
        feature = row[0]
        cursor3.execute(sql3, (category, feature))
        while True:
            row = cursor3.fetchone()
            if row is None:
                break
            positivescore = row[0]
            negativescore = row[1]
            cursor4.execute(sql4, (feature, category))

            f.write("\n")
            f.write("----------------------------------------------------------------------------------\n")
            f.write("feature:"+feature+"   positivescore:"+str(positivescore)+"   negativescore:"+str(negativescore)+"\n")
            f.write("----------------------------------------------------------------------------------\n")
            p = 0
            n = 0
            i = 1
            while True:
                one = cursor4.fetchone()
                if one is None:
                    break
                if one[1] == 1 and p == 0:
                    f.write("positive sentences:\n")
                    p += 1
                if one[1] == -1 and n == 0:
                    f.write("\n")
                    f.write("negative sentences:\n")
                    n += 1
                    i = 1
                f.write(str(i)+". "+one[0]+"\n")
                i += 1
    f.close()





