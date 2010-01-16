# -*- coding: utf-8 -*-
from nose.tools import *
from texcore.tests import *

class TestAdhocController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='adhoc', action='index'))
        assert_true(u'ちゃっかり作ってみたりする実験' in response)
