class TeXOperationError(Exception):
    def __init__(self, code, error):
        self.code = code
        self.error = error

    def __unicode__(self):
        return u'TeX returned code %d, log:\n%s' % (self.code, self.error.decode('EUC-JP', 'replace'))

    def __str__(self):
        return self.__unicode__().encode('utf-8')
