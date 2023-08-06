"""Provides a multithreaded API notification listener.

The Extera API provides notifications to registered listeners that are specific to the logged in
user. The notifications are issued every time there is a change to data belonging to the logged
in user.

One example of using the notification is listening for the completion of runs. 

Example usage:
```python
from extera.api.notificationListener import NotificationListener
from extera.api.auth import login, logout
from threading import Event
import json

def handleSpecificMessage(message): str
    global event
    msg = json.loads(message)

    if msg["type"] == "Case" && msg["action"] == "Changed":
        print("Case {name} changed".format(name = msg["result"]["name"]))
        event.set()

if __name__ == "__main__"
    tokens = login("user@domain.com", "password")
    listener = NotificationListener()
    listener.listen(tokens["accessToken"])
    event = Event()

    # wait for a case to change
    event.wait()
    logout(tokens["accessToken"])
```

"""

from .config import Config
import websockets
import asyncio
from typing import Callable
from threading import Thread

class NotificationListener(object):
    """ Implements an API notifications listeners singleton class
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NotificationListener, cls).__new__(cls)
        return cls.instance
  
    def __init__(self) -> None:
        self.__routers = []
        self.ws = None
        self.thread = None

    def addListener(self, route: Callable[[str], None]):
        """Adds an event handler to be called when a notification is received
        Args:
            `route`: The `Callable` function to be invoked when a notification is received
        
        The handler is responsible for filtering the messages received and taking action for the
        relevant messages.

        Each handler is executed in its own separate thread.
        """
        self.__routers.append(route)

    def removeListener(self, route: Callable[[str], None]):
        """Removes an event handler from the list of handlers to be called
        Args:
            `route`: The `Callable` function to be removed.
        """
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
        """Initiates listening to messages from the API
        Args:
            `accessToken`: A string representing the access token of the logged in user for which
            to listen to messages. 
        
        The function starts the listener on its own thread. The thread is initialized with 
        `daemon = True`, which means that it will continue listening for as long as the script
        is running, and terminate when the main script is complete.
        """
        self.thread = Thread(target=self.__start_listening__, args=(accessToken,), daemon=True)
        self.thread.start()

    async def stop_listening(self):
        """Closes the notification session and terminates the listener thread.
        
        This is a manual termination of the listener thread, as opposed to the listener expiring
        with the main script.
        """
        await self.ws.close()
        self.ws = None

    def __del__(self):
        if self.ws != None:
            self.ws.close()

__all__ = ["NotificationListener"]