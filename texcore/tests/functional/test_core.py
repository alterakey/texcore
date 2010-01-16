import xmlrpclib

from texcore.tests import *
from texcore.tests.functional import XMLRPCControllerTestBase

class TestCoreController(XMLRPCControllerTestBase):
    def test_typeset(self):
        corps = '\relax'
        pdf = self.xc.typeset(xmlrpclib.Binary(corps))
        assert 'PDF' in pdf.data
