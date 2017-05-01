import csv


# 不用csv操作csv文件，输出内容
# for line in open("file/sample.csv"):
#     title, year, director = line.split(",")
#     print(title,year, title)


# 使用csv模块操作 csv文件，输出内容
with open('file/sample.csv','a') as file:
    # reader = csv.reader(file)
    # for title, year, director in reader:
    #     print(title, year, director)

    writer = csv.writer(file)
    writer.writerow(['title', 'summary', 'year'])

