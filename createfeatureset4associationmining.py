import dbaccess
import os

con = dbaccess.getcon("other")
sqlcategory = "SELECT DISTINCT category FROM koubei"
sqlword = "SELECT p.word,f.feature FROM postag p, featureclass f, reviewsentiment r, koubei k" \
          " WHERE p.reviewsentementid = r.id AND r.featureclassid = f.id AND " \
          "f.reviewid = k.id AND k.category = %s AND p.postag='n'"
processnum = 0
total = str(805)
cursor1 = con.cursor()
cursor2 = con.cursor()
cursor1.execute(sqlcategory)
while True:
    category = cursor1.fetchone()
    if category is None:
        break
    categoryname = category[0]
    cursor2.execute(sqlword, categoryname)
    while True:
        try:
            oneclass = cursor2.fetchone()
            if oneclass is None:
                break
            word = oneclass[0]
            feature = oneclass[1]
            directory = "./featureset/"+categoryname
            file_ = directory+"/"+feature+".txt"
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(file_):
                f = open(file_, "a", encoding="utf8")
            f.write(word+"\n")
        except Exception as e:
            print("something wrong")
            open("./err.txt", "a").write(categoryname+"\n")
    f.close()
    processnum += 1
    print("processing:"+str(processnum)+"/"+total)
