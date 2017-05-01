import csv
for line in open("samples/sample.csv"):
    title, year, director = line.split(",")
    print(year, title)
