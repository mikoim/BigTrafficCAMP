import csv
import MySQLdb
import MySQLdb.cursors

conn = MySQLdb.connect(user='root', passwd='hoge', host='localhost', db='camp', charset="utf8",
                       cursorclass=MySQLdb.cursors.DictCursor)

list_card = []

list_card_type = []
dict_card_type = {}

def tag_wrapper(tags:str)->str:
    result = ''

    for tag in tags.split(','):
        result += '|{:s}|'.format(tag)

    return result

with open('raw/card.tsv', mode='r') as tsv:
    for line in csv.reader(tsv, dialect="excel-tab"):
        if line[0] == '#cardId':
            continue

        cardId = line[0]
        cardMessage = line[1]
        cardType = line[2]
        cardTags = tag_wrapper(line[3])
        cardMetrics = int(line[4])

        if cardType not in list_card_type:
            list_card_type.append(cardType)

        list_card.append(
            (cardId, cardMessage, cardType, cardTags, cardMetrics)
        )

'''
cardTypeを正規化
'''
cur = conn.cursor()

for i in range(len(list_card_type)):
    cur.execute('INSERT INTO card_type VALUE (%s, %s);', (i + 1, list_card_type[i]))

    dict_card_type[list_card_type[i]] = i + 1

cur.close()
conn.commit()

'''
cardをインサート
'''
cur = conn.cursor()

for i in range(len(list_card)):
    cur.execute('INSERT INTO card VALUE (%s, %s, %s, %s, %s);', (
        list_card[i][0],
        list_card[i][1],
        dict_card_type[list_card[i][2]],
        list_card[i][3],
        list_card[i][4]
    ))

cur.close()
conn.commit()
