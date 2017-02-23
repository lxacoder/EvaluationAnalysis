import dbaccess


sql = "select s1.*,s2.p2 from (select s.reviewsentence_id,s.category" \
      ",sum(s.ResultantPolarity) p1 from " \
      "(select  distinct r.opinionword,r.category,r.reviewsentence_id,(r.ResultantPolarity)" \
      "  from (select t2.id,t2.feature,t2.opinionWord,t2.category," \
      "t2.reviewsentence_id,t2.posTagId,t2.isNegateNear*t2.Polarity ResultantPolarity from" \
      " (select t.*,ifnull(p.Polarity,0) Polarity from " \
      "(select o.id,o.feature,o.opinionWord,o.category,o.reviewsentence_id,o.posTagId, ifnull(n.isNegateNear,1) isNegateNear" \
      " from potentialfeature o left join negateproximity n on o.posTagId = n.id) t " \
      "left join polarity p on p.word = t.opinionWord) t2)r)s group by s.reviewsentence_id) s1 " \
      "inner join (select s.reviewsentence_id,sum(s.ResultantPolarity) p2 from " \
      "(select  r.opinionword,r.reviewsentence_id,(r.ResultantPolarity) from " \
      "(select t2.id,t2.feature,t2.opinionWord,t2.category,t2.reviewsentence_id," \
      "t2.posTagId,t2.isNegateNear*t2.Polarity ResultantPolarity from (" \
      "select t.*,ifnull(p.Polarity,0) Polarity from " \
      "(select o.id,o.feature,o.opinionWord,o.category,o.reviewsentence_id,o.posTagId, ifnull(n.isNegateNear,1) " \
      "isNegateNear from potentialfeature o left join negateproximity n on o.posTagId = n.id) t " \
      "left join polarity p on p.word = t.opinionWord) t2)r)s group by s.reviewsentence_id) s2 " \
      "on s1.reviewsentence_id=s2.reviewsentence_id";
sql2 = "INSERT INTO sentencescore VALUES(%s,%s)"
con = dbaccess.getcon("other")
cursor1 = con.cursor()
cursor2 = con.cursor()
cursor1.execute(sql)
idscore = dict()
while True:
    onesentencescore = cursor1.fetchone()
    if onesentencescore is None:
        break
    sentenceid = onesentencescore[0]
    score1 = onesentencescore[2]
    score2 = onesentencescore[3]
    if score1 != 0:
        idscore[sentenceid] = score1
    elif score2 != 0:
        idscore[sentenceid] = score2
    else:
        if (sentenceid - 1) in idscore:
            idscore[sentenceid] = idscore[sentenceid-1]
enties = idscore.items()
lenth = str(len(enties))
print(lenth)
count = 0
for item in enties:
    count += 1
    print("processing:"+str(count)+"/"+lenth)
    cursor2.execute(sql2, item)
    if count % 1000 == 0:
        con.commit()
con.commit()
con.close()
