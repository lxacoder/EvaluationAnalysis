import dbaccess


con = dbaccess.getcon("other")
cursor1 = con.cursor()
cursor2 = con.cursor()
cursor3 = con.cursor()
sql = "SELECT DISTINCT reviewsentence_id FROM potentialfeature"
sql2 = "SELECT id,word,postag FROM postag WHERE reviewsentementid = %s"
sql3 = "INSERT INTO negateproximity VALUES (%s,-1)"
neg_words = ["不", "不是"]
cursor1.execute(sql)
withneglist = list()

total = str(1819993)
count = 0

while(True):
    count += 1
    print("processing:"+str(count)+"/"+total)
    one = cursor1.fetchone()
    if one is None:
        break
    reviewsentence_id = one[0]
    cursor2.execute(sql2, reviewsentence_id)
    adjlist = list()

    curr_neg = -5
    while(True):
        antherone = cursor2.fetchone()
        if antherone is None:
            break
        id_ = antherone[0]
        word_ = antherone[1]
        postag = antherone[2]
        if postag == 'a' or postag == 'an' or postag == 'aj':
            if abs(id_-curr_neg) <= 3:
                withneglist.append(id_)
            else:
                adjlist.append(id_)
        elif word_ in neg_words:
            curr_neg = id_
            for negid in adjlist:
                if curr_neg - negid <= 3:
                    withneglist.append(negid)
                else:
                    adjlist.remove(negid)
f = open("back.txt", "w")
for id_ in list(set(withneglist)):
    f.write(str(id_))
    cursor3.execute(sql3, id_)
f.close()
con.commit()
