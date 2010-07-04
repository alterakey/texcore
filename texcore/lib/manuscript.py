# -*- coding: utf-8 -*-
import pylons

class Manuscript(object):
    def __init__(self, data, encoding='UTF-8'):
        self.data = data.decode(encoding)

    def __str__(self):
        return self.data.encode(pylons.config.get('texcore.ptex.encoding', 'UTF-8'), 'replace')

    def __unicode__(self):
        return self.data
