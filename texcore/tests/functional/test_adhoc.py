from texcore.tests import *

class TestAdhocController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='adhoc', action='index'))
        # Test response...
