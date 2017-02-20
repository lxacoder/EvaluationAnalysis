import os
# 获取目标文件夹的路径
for dirpath, dirnames, filenames in os.walk("./featureset"):
    for item in dirnames:
        meragefiledir = os.path.join(dirpath, item)
        # 获取当前文件夹中的文件名称列表
        filenames = os.listdir(meragefiledir)
        # 打开当前目录下的result.txt文件，如果没有则创建17,756
        # 文件也可以是其他类型的格式，如result.js
        file = open(os.path.join(dirpath, item+'.txt'), 'a', encoding="utf8")
        # 向文件中写入字符
        # file.write('python\n')
        # 先遍历文件名
        for filename in filenames:
            filepath = meragefiledir + '\\' + filename
            # 遍历单个文件，读取行数
            print(filepath)
            for line in open(filepath, encoding="utf8"):
                file.write(line)
        # 关闭文件
        file.close()