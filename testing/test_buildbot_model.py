from build_dashboard.model import BuildbotModel
from unittest import TestCase
from unittest.mock import patch, Mock
from asyncio import Future, coroutine

class TestBuildbotModel(TestCase):

    @patch('build_dashboard.model.BuildbotClient')
    def test_builders(self, mockClient):
        EXPECTED = [ { 'builderid': 1, 'name': 'builder' } ]
        mockClient.builders = Mock(side_effect=coroutine(Mock(return_value=EXPECTED)))
        model = BuildbotModel(mockClient)
        builders = model.builders()
        assert EXPECTED == builders

    @patch('build_dashboard.model.BuildbotClient')
    def test_builders(self, mockClient):
        BUILDERS = [ { 'builderid': 1, 'name': 'builder' } ]
        BUILDS = [ { 'builderid': 1, 'name': 'builder', 'buildid': 1 } ]
        EXPECTED = BUILDERS.copy()
        EXPECTED[0]['builds'] = BUILDS
        mockClient.builders = Mock(side_effect=coroutine(Mock(return_value=BUILDERS)))
        mockClient.builds = Mock(side_effect=coroutine(Mock(return_value=BUILDS)))
        model = BuildbotModel(mockClient)
        builders = model.builders_with_builds()
        assert EXPECTED == builders
