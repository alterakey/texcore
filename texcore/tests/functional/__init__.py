import xmlrpclib

from texcore.tests import TestController

class XMLRPCControllerTestBase(TestController):
    def setUp(self):
        self.xc = xmlrpclib.ServerProxy('http://localhost:5000/RPC2')
