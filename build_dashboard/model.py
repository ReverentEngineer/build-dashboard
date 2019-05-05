from aiohttp import TCPConnector, UnixConnector, request, ClientSession
from json import loads
import asyncio

class BuildbotModel(object):

    def __init__(self, client):
        self.loop = asyncio.get_event_loop()
        self.client = client

    def __del__(self):
        self.loop.run_until_complete(self.client.close())

    async def __mergeBuilderAndBuild(self, builder):
        builds = await self.client.getBuilds(builder['builderid'])
        builder['builds'] = builds 
        return builder

    def getBuildersWithBuilds(self):
        builders = self.getBuilders()
        done, pending = self.loop.run_until_complete(
                asyncio.wait([self.__mergeBuilderAndBuild(builder) 
                    for builder in builders ])
                )
        return [ task.result() for task in done ]
    
    def getBuilders(self):
        builders = self.loop.run_until_complete(self.client.getBuilders())
        return builders

    def getBuilds(self, builderid):
        return self.loop.run_until_complete(self.client.getBuilds(builderid))

class BuildbotClient(object):
    def __init__(self, path=None, protocol='http', host='localhost'):
        if path is None:
            conn = TCPConnector(limit=30)
        else:
            conn = UnixConnector(path=path)
        self.session = ClientSession(connector=conn) 
        self.base_address = protocol + '://' + host + '/api/v2'

    async def get(self, address):
        response = await self.session.get(self.base_address + address)
        text = await response.text()
        result = loads(text)
        return result
    
    async def getBuilders(self):
        results = await self.get('/builders')
        return results['builders']

    async def getBuilds(self, builderid):
        results = await self.get('/builders/' + str(builderid) + '/builds')
        return results['builds']
    
    async def close(self):
        await self.session.close()
