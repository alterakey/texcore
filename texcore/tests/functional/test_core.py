# -*- coding: utf-8 -*-
import xmlrpclib

from nose.tools import *

from texcore.tests import *
from texcore.tests.functional import XMLRPCControllerTestBase

class TestCoreController(XMLRPCControllerTestBase):
    def test_typeset(self):
        corps = r'''%
\documentclass{jsarticle}
\begin{document}
test!
\end{document}
'''
        pdf = self.xc.typeset(xmlrpclib.Binary(corps))
        assert 'PDF' in pdf.data

    @raises(xmlrpclib.Fault)
    def test_typeset__with_invalid_charset(self):
        corps = ur'''%
\documentclass{jsarticle}
\begin{document}
test!ふははははははあ
\end{document}
'''.encode('cp932')
        self.xc.typeset(xmlrpclib.Binary(corps))

    def test_typeset_with_encoding(self):
        corps = ur'''%
\documentclass{jsarticle}
\begin{document}
test!ふははははははあ
\end{document}
'''.encode('cp932')
        pdf = self.xc.typeset_with_encoding('cp932', xmlrpclib.Binary(corps))
        assert 'PDF' in pdf.data

