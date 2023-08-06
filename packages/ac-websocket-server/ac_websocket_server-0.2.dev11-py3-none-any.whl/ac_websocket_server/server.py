'''Assetto Corsa Websocket Server Class'''

import asyncio
from datetime import datetime
import logging
import os
import socket
from typing import List
import websockets

from ac_websocket_server import logger
from ac_websocket_server.connection import WebSocketConnection
from ac_websocket_server.debug import DebugMonitor
from ac_websocket_server.constants import HOST, PORT
from ac_websocket_server.error import WebsocketsServerError
from ac_websocket_server.game import GameServer
from ac_websocket_server.grid import Grid
from ac_websocket_server.handlers import handler
from ac_websocket_server.observer import Observer
from ac_websocket_server.protocol import Protocol
from ac_websocket_server.tracker import TrackerServer

EXTRA_DEBUG = False


class WebsocketsServer():
    '''Represents an Assetto Corsa WebSocket Server.

    Allows control of an Assetto Corsa server with a websockets interface.'''
    # pylint: disable=logging-fstring-interpolation, invalid-name

    def __init__(self,
                 server_directory: str = None,
                 host: str = HOST,
                 port: int = PORT
                 ) -> None:

        self._logger = logging.getLogger('ac-ws.ws-server')

        if EXTRA_DEBUG:
            asyncio.get_event_loop().create_task(DebugMonitor.monitor_tasks())

        self._connections: List[WebSocketConnection] = []

        self.host = host
        self.port = port

        if not server_directory:
            self.server_directory = os.getcwd()
        else:
            self.server_directory = server_directory

        log_directory = f'{self.server_directory}/logs/acws'
        if not os.path.isdir(log_directory):
            os.mkdir(log_directory)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logging_filename = f'{log_directory}/messages-{timestamp}'
        file_handler = logging.FileHandler(logging_filename)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s'))
        logger.addHandler(file_handler)

        try:
            self.game = GameServer(directory=self.server_directory)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((self.host, int(self.game.http_port)))
            s.close()
            if result == 0:
                msg = f'Fatal error - Existing ACS process running on {self.host}:{self.game.http_port}'
                self._logger.error(msg)
                raise WebsocketsServerError(msg)
        except WebsocketsServerError as error:
            self._logger.error(f'Fatal error {error}')
            raise

        try:
            self.tracker = TrackerServer(f'{self.server_directory}/stracker')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex(
                (self.host, int(self.tracker.listening_port)))
            s.close()
            if result == 0:
                msg = f'Fatal error - Existing Tracker process running on {self.host}:{self.tracker.listening_port}'
                self._logger.error(msg)
                raise WebsocketsServerError(msg)
        except WebsocketsServerError as error:
            self._logger.error(f'Fatal error: {error}')

        self.stop_server: asyncio.Future = None

    async def broadcast(self, msg: str):
        '''Broadcast message to all connected websockets.'''

        for connection in self._connections:
            await connection.send(msg)

    async def handler(self, websocket):
        '''ACWS handler function for websocket connection'''

        connection = WebSocketConnection(server=self, websocket=websocket)

        self._connections.append(connection)

        await connection.send(Protocol.success(
            msg=f'Welcome to the Assetto Corsa WebSocket server running at {self.host}:{self.port}'))

        await handler(websocket, connection.consumer, connection.producer)

        connection.close()

    async def start(self):
        '''Start the websocket server'''

        try:

            self._logger.info('Starting websocket server')

            self.stop_server = asyncio.Future()

            async with websockets.serve(self.handler, self.host, self.port):
                await self.stop_server

            self._logger.info('Stopping websocket server')

        except KeyboardInterrupt:
            self._logger.info('Interupting the server')

    async def stop(self):
        '''Stop the websocket server'''

        self.stop_server.set_result(True)

    async def shutdown(self, message: str = None, connection: id = None):
        '''
        Shutdown the ACWS server.

        Note that running AC servers and trackers will NOT be stopped.
        '''

        await self.broadcast(Protocol.success(
            msg=f'Shutting down the WebSocket server running at {self.host}:{self.port}'))

        self._logger.info('Shutting down the server')
        await self.stop()
