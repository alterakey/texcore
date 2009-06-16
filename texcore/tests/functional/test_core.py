from texcore.tests import *

class TestCoreController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='core', action='index'))
        # Test response...
        assert 'Hello world' in response
