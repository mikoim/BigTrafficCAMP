import ujson

from flask import Flask, request, Response
import MySQLdb
import MySQLdb.cursors

from support import *


class DB:
    def __init__(self):
        self._db = None
        self.connect()

    def connect(self):
        self._db = MySQLdb.connect(user='root', passwd='hoge', host='localhost', db='camp', charset="utf8",
                                   cursorclass=MySQLdb.cursors.DictCursor)

    def query(self, sql, error_limit=3, error=0):
        if error > error_limit:
            raise Exception("Can't connect to DB server")

        try:
            cursor = self._db.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except (AttributeError, MySQLdb.OperationalError):
            print('Error')
            self.connect()
            return self.query(sql, error + 1)


app = Flask(__name__)
db = DB()


@app.route('/listCardsInBox')
def list_cards_inbox():
    parameters = dict(request.args.items())
    sql = 'SELECT `card`.`cardId`, `card`.`cardMessage` AS message, `card_type`.`cardType` AS type, `card`.`cardTags` AS tags, `card`.`cardMetrics` AS metrics, `box_card_rel`.`boxId` AS owner FROM `box_card_rel` INNER JOIN `card` USING(`cardId`) INNER JOIN `box` USING(`boxId`) INNER JOIN `category` USING(`categoryId`) INNER JOIN `card_type` USING(`cardTypeId`)'

    '''
    Generate WHERE query
    '''

    where = []

    if 'findByBoxIdEqual' in parameters:
        where.append('`box_card_rel`.`boxId` = "{:s}"'.format(parameters['findByBoxIdEqual']))

    if 'findByBoxCategoryEqual' in parameters:
        where.append('`category`.`category` = "{:s}"'.format(parameters['findByBoxCategoryEqual']))

    if 'findByBoxPriorityGTE' in parameters:
        where.append('`box`.`priority` <= {:d}'.format(int(parameters['findByBoxPriorityGTE'])))

    if 'findByBoxPriorityLTE' in parameters:
        where.append('`box`.`priority` >= {:d}'.format(int(parameters['findByBoxPriorityLTE'])))

    if 'findByCardTypeEqual' in parameters:
        where.append('`card_type`.`cardType` = "{:s}"'.format(parameters['findByCardTypeEqual']))

    if 'findByCardTagsIncludeAll' in parameters:
        tags_and = []
        for tag in parameters['findByCardTagsIncludeAll'].split(','):
            tags_and.append('`card`.`cardTags` LIKE "%|{:s}|%"'.format(tag))
        where.append(' AND '.join(tags_and))

    if 'findByCardTagsIncludeAny' in parameters:
        tags_and = []
        for tag in parameters['findByCardTagsIncludeAny'].split(','):
            tags_and.append('`card`.`cardTags` LIKE "%|{:s}|%"'.format(tag))
        where.append(' (' + ' OR '.join(tags_and) + ' ) ')

    if 'findByCardMetricsGTE' in parameters:
        where.append('`card`.`cardMetrics` >= {:d}'.format(int(parameters['findByCardMetricsGTE'])))

    if 'findByCardMetricsLTE' in parameters:
        where.append('`card`.`cardMetrics` <= {:d}'.format(int(parameters['findByCardMetricsLTE'])))

    if len(where) > 0:
        sql += ' WHERE ' + ' AND '.join(where)

    '''
    Generate ORDER query
    '''

    order = []

    if 'sortByBoxCategory' in parameters:
        order.append('`category`.`category` {:s}'.format(convert_order(parameters['sortByBoxCategory'])))

    if 'sortByBoxPriority' in parameters:
        order.append('`box`.`priority` {:s}'.format(convert_order(parameters['sortByBoxPriority'], inverse=True)))

    if 'sortByCardType' in parameters:
        order.append('`card_type`.`cardType` {:s}'.format(convert_order(parameters['sortByCardType'])))

    if 'sortByCardMatchedTagsNum' in parameters:
        pass

    if 'sortByCardMetrics' in parameters:
        order.append('`card`.`cardMetrics` {:s}'.format(convert_order(parameters['sortByCardMetrics'])))

    if len(order) > 0:
        sql += ' ORDER BY ' + ','.join(order)

    '''
    Generate LIMIT query
    '''

    if 'limit' in parameters:
        sql += ' LIMIT {:d}'.format(int(parameters['limit']))

    '''
    Fetch data from DB
    '''

    print(sql)

    data = db.query(sql)

    '''
    Convert to list from comma separated tags
    '''

    for i in range(len(data)):
        data[i]['tags'] = list(filter(None, data[i]['tags'].split('|')))

    return Response(ujson.dumps({
        'result': True,
        'data': data
    }), mimetype='application/json', status=200)


if __name__ == '__main__':
    app.run(debug=False)
