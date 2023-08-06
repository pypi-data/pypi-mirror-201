def heavy_translate(string:str):
    '''
    returns string translated of any 'fancy' quotations or ellipses
    '''
    transl_table = dict([ (ord(x), ord(y)) for x,y in zip( u"‘’´“”–-―　",  u"'''\"\"--- ") ] )
    return string.translate(transl_table).replace('…', '...')