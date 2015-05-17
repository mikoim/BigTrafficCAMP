def convert_order(parm: str, inverse=False) ->str:
    if parm == 'ascend':
        if not inverse:
            return 'ASC'
        else:
            return 'DESC'
    elif parm == 'descend':
        if not inverse:
            return 'DESC'
        else:
            return 'ASC'
    else:
        raise Exception('Unknown format: ' + parm)
