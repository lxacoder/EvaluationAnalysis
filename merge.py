import os

for dirpath, dirnames, filenames in os.walk("./featureset"):
    for item in dirnames:
        meragefiledir = os.path.join(dirpath, item)

        filenames = os.listdir(meragefiledir)

        file = open(os.path.join(dirpath, item+'.txt'), 'a', encoding="utf8")

        for filename in filenames:
            filepath = meragefiledir + '\\' + filename

            print(filepath)
            for line in open(filepath, encoding="utf8"):
                if line == "人" or line == "车":
                    continue
                file.write(line)
        file.close()