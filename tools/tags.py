import csv
import mysql.connector

conn = mysql.connector.connect(user='root', password='', host='localhost', database='camp')

list_tag = []
dict_tag = {}

with open('raw/card.tsv', mode='r') as tsv:
    for line in csv.reader(tsv, dialect="excel-tab"):
        if line[0] == '#cardId':
            continue

        for tag in line[3].split(','):
            if tag not in list_tag:
                list_tag.append(tag)

for i in range(len(list_tag)):
    cur = conn.cursor()

    cur.execute('INSERT INTO tag VALUE (%s, %s);', (i + 1, list_tag[i]))

    dict_tag[list_tag[i]] = i + 1

conn.commit()

with open('raw/card.tsv', mode='r') as tsv:
    for line in csv.reader(tsv, dialect="excel-tab"):
        if line[0] == '#cardId':
            continue

        cardId = line[0]

        cur = conn.cursor()

        for tag in line[3].split(','):
            cur.execute('INSERT INTO tag_rel VALUE (%s, %s);', (
                dict_tag[tag],
                cardId
            ))

        cur.close()

conn.commit()
conn.disconnect()
