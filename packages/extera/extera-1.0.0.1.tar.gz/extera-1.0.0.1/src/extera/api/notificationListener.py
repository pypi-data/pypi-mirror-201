from .config import Config
import websockets
import asyncio
from typing import Callable
from threading import Thread

class NotificationListener(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NotificationListener, cls).__new__(cls)
        return cls.instance
  
    def __init__(self) -> None:
        self.__routers = []
        self.ws = None
        self.thread = None

    def addListener(self, route: Callable[[str], None]):
        self.__routers.append(route)

    def removeListener(self, route: Callable[[str], None]):
        self.__routers.remove(route)

    async def __route__(self, message: str):
        for router in self.__routers:
            # await router(message)
            thread = Thread(target = router, args = (message, ), daemon = False)
            thread.start()

    async def __listen__(self, accessToken: str):
        url = Config.notificationUrl
        async with websockets.connect(url) as ws:
            self.ws = ws
            await self.ws.send('{{ "subscribe": true, "auth": "{accessToken}" }}'.format(accessToken = accessToken))
            async for message in self.ws:
                await self.__route__(message)

    def __start_listening__(self, accessToken):
        asyncio.run(self.__listen__(accessToken))

    def listen(self, accessToken: str):
        self.thread = Thread(target=self.__start_listening__, args=(accessToken,), daemon=True)
        self.thread.start()

    async def stop_listening(self):
        await self.ws.close()
        self.ws = None

    def __del__(self):
        if self.ws != None:
            self.ws.close()
