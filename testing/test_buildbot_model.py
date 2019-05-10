from build_dashboard.model import BuildbotModel
from unittest import TestCase
from unittest.mock import patch, Mock
from asyncio import Future, coroutine
import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

class TestBuildbotModel(TestCase):

    @patch('build_dashboard.model.BuildbotClient')
    def test_builders(self, mockClient):
        BUILDERS = [ { 'builderid': 1, 'name': 'builder' } ]
        BUILDS = [ { 'builderid': 1, 'name': 'builder', 'buildid': 1 } ]
        EXPECTED = BUILDERS.copy()
        EXPECTED[0]['builds'] = BUILDS
        mockClient.builders = Mock(side_effect=coroutine(Mock(return_value=BUILDERS)))
        mockClient.builds = Mock(side_effect=coroutine(Mock(return_value=BUILDS)))
        model = BuildbotModel(mockClient)
        builders = model.builders()
        assert EXPECTED == builders
