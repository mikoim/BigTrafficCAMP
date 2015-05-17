import csv
import MySQLdb
import MySQLdb.cursors

conn = MySQLdb.connect(user='root', passwd='hoge', host='localhost', db='camp', charset="utf8",
                       cursorclass=MySQLdb.cursors.DictCursor)

list_box = []
list_category = []

dict_category = {}

with open('raw/box.tsv', mode='r') as tsv:
    for line in csv.reader(tsv, dialect="excel-tab"):
        if line[0] == '#boxId':
            continue

        cardId = line[0]
        category = line[1]
        priority = int(line[2])

        list_box.append((cardId, category, priority))

        if category not in list_category:
            list_category.append(category)

for i in range(len(list_category)):
    cur = conn.cursor()

    cur.execute('INSERT INTO category VALUE (%s, %s);', (i + 1, list_category[i]))

    cur.close()

    dict_category[list_category[i]] = i + 1

conn.commit()

for i in range(len(list_box)):
    cur = conn.cursor()

    cur.execute('INSERT INTO box VALUE (%s, %s, %s);',
                (list_box[i][0], dict_category[list_box[i][1]], list_box[i][2])
                )

    cur.close()

conn.commit()
