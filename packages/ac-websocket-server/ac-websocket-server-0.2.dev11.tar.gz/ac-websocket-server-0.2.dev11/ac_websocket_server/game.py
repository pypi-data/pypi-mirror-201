'''Assetto Corsa Game Server Class'''

import asyncio
import configparser
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List

from ac_websocket_server.child import ChildServer
from ac_websocket_server.entries import EntryList
from ac_websocket_server.error import WebsocketsServerError
from ac_websocket_server.grid import Grid
from ac_websocket_server.objects import (DriverInfo, EntryInfo, SessionInfo)
from ac_websocket_server.lobby import Lobby
from ac_websocket_server.protocol import Protocol
from ac_websocket_server.watcher import Watcher


@dataclass
class GameServer(ChildServer):
    '''Represents an Assetto Corsa Server.'''
    # pylint: disable=logging-fstring-interpolation, invalid-name

    directory: str
    child_ini_file: str = field(default='cfg/server_cfg.ini')
    child_title: str = field(default='AC Server')
    child_short: str = field(default='AC Server')
    is_optional: bool = False

    version: str = field(default='n/a', init=False)
    timestamp: str = field(default='n/a', init=False)
    name: str = field(init=False)
    track: str = field(init=False)
    cars: str = field(init=False)
    http_port: int = field(init=False)
    tcp_port: int = field(init=False)
    udp_port: int = field(init=False)
    drivers: Dict[str, DriverInfo] = field(init=False)
    entries: Dict[int, EntryInfo] = field(init=False)
    sessions: Dict[str, SessionInfo] = field(init=False)
    lobby: Lobby = field(init=False)
    running: int = field(init=False, default=False)

    def __post_init__(self):

        super().__post_init__()

        self._logger = logging.getLogger('ac-ws.game')
        self._args = ()

        if os.path.exists(f'{self.directory}/acServer.py'):
            self._cwd = None
            self._exe = f'{self.directory}/acServer.py'
            self._hash = None
        else:
            self._cwd = self.directory
            if sys.platform == 'linux':
                self._exe = f'{self.directory}/acServer'
                self._hash = 'f781ddfe02e68adfa170b28d0eccbbdc'
            else:
                self._exe = f'{self.directory}/acServer.exe'
                self._hash = '357e1f1fd8451eac2d567e154f5ee537'

        self.drivers = {}
        self.entries = {}
        self.sessions = {}

        self.parse_server_cfg()
        self.parse_entry_list()

        self.grid = Grid(server_directory=self.directory,
                         track=self.track,
                         entry_list=self.entry_list)

        self.lobby = Lobby()

        self._watcher_stdout: Watcher

    async def consumer(self, message_words: List[str], connection: id = None):
        '''Consume args destined for the server'''

        message_funcs = {'drivers': self.__drivers,
                         'entries': self.__entries,
                         'info': self.__info,
                         'sessions': self.__sessions,
                         'start': self.start,
                         'stop': self.stop,
                         'restart': self.restart}

        if message_funcs.get(message_words[0]):
            await message_funcs[message_words[0]]()

    async def __drivers(self):
        '''Show game drivers info as part of a JSON reply'''
        await self.put(Protocol.success({'drivers': self.drivers}))

    async def __entries(self):
        '''Show game entries info as part of a JSON reply'''
        await self.put(Protocol.success({'entries': self.entries}))

    async def __info(self):
        '''Show game server info as a JSON string'''
        await self.put(Protocol.success({'server': self}))

    async def notify(self, notifier):
        '''Receive a notification of a new message from log watcher or lobby.'''

        message = await notifier.get(self)

        try:
            item = json.loads(message)

            if not item.get('type', None):
                if item.get('data', None):
                    await self.put(Protocol.success(item['data']))
                if item.get('error', None):
                    await self.put(Protocol.error(item['error']))
                return

            if item['type'] == 'LobbyInfo':
                await self.lobby.update(item['body'])
                await self.put(Protocol.success({'lobby': item['body']}))

            if item['type'] == 'ServerInfo':
                self.version = item['body']['version']
                self.timestamp = item['body']['timestamp']
                self.track = item['body']['track']
                self.cars = item['body']['cars']

                await self.put(Protocol.success({'server': item['body']}))

            if item['type'] == 'DriverInfo' and item['body']['msg'] == 'joining':

                body = item['body']
                name = body['name']

                driver_info = DriverInfo()

                driver_info.name = name
                driver_info.host = body['host']
                driver_info.port = body['port']
                driver_info.car = body['car']
                driver_info.guid = body['guid']
                driver_info.ballast = body['ballast']
                driver_info.restrictor = body['restrictor']
                driver_info.msg = body['msg']

                self.drivers[driver_info.name] = driver_info

                self._logger.debug(f'Driver {name} joining')
                await self.put(Protocol.success({'driver': item['body']}))

            if item['type'] == 'DriverInfo' and item['body']['msg'] == 'leaving':
                body = item['body']
                name = body['name']
                del self.drivers[name]

                self._logger.debug(f'Driver {name} leaving')
                await self.put(Protocol.success({'driver': item['body']}))

            if item['type'] == 'SessionInfo':

                body = item['body']
                session_type = body['type']

                session_info = SessionInfo()

                session_info.type = session_type
                session_info.laps = body['laps']
                session_info.time = body['time']

                self.sessions[session_type] = session_info

                await self.put(Protocol.success({'sessions': session_info}))

        except json.JSONDecodeError:
            pass

        # await self.put(message)

    def parse_entry_list(self):
        '''Parse entry list file and update attributes'''

        entry_list_file_name = f'{self.directory}/cfg/entry_list.ini'

        if not os.path.exists(entry_list_file_name):
            error_message = f'Missing entry_list.ini file in {self.directory}'
            self._logger.error(error_message)
            raise WebsocketsServerError(error_message)

        self.entry_list = EntryList(entry_list_file_name)
        self.entries = self.entry_list.entries

    def parse_server_cfg(self):
        '''Parse server config file and update attributes'''

        server_cfg_file_name = f'{self.directory}/{self.child_ini_file}'

        if not os.path.exists(server_cfg_file_name):
            error_message = f'Missing server_cfg.ini file in {self.directory}'
            self._logger.error(error_message)
            raise WebsocketsServerError(error_message)

        cfg = configparser.ConfigParser()
        try:
            cfg.read(server_cfg_file_name)

            self.name = cfg['SERVER']['NAME']
            self.cars = cfg['SERVER']['CARS']
            self.track = cfg['SERVER']['TRACK']
            self.http_port = cfg['SERVER']['HTTP_PORT']
            self.tcp_port = cfg['SERVER']['TCP_PORT']
            self.udp_port = cfg['SERVER']['UDP_PORT']

            for session in ['PRACTICE', 'QUALIFY', 'RACE']:
                if cfg.has_section(session):
                    name = cfg[session].get('NAME')
                    time = cfg[session].get('TIME', 0)
                    laps = cfg[session].get('LAPS', 0)
                    self.sessions[name] = SessionInfo(
                        name, laps=laps, time=time)

        except configparser.Error as e:
            raise WebsocketsServerError(e) from e

    def pre_start_hook(self):
        '''Parse and update status before start (for re-start post __init__)'''

        super().pre_start_hook()

        self._debug_transaction.open('game-start')
        self._debug_transaction.save_file(
            f'{self.directory}/{self.child_ini_file}')
        self._debug_transaction.save_file(
            f'{self.directory}/cfg/entry_list.ini')

        try:
            self.parse_server_cfg()
            self.parse_entry_list()
            self.grid.track = self.track
        except WebsocketsServerError as e:
            self._logger.error('Command failed - configuration error')
            raise e

    async def post_start_hook(self):

        super().post_start_hook()

        await self.put(Protocol.success(
            msg='Assetto Corsa server started'))

        self.lobby.subscribe(self)

        self._watcher_stdout = Watcher(self._logfile_stdout)
        self._watcher_stdout.subscribe(self)
        await self._watcher_stdout.start()

        self._debug_transaction.close()

    async def post_stop_hook(self):

        self._debug_transaction.open('game-stop')
        self._debug_transaction.save_file(
            f'{self.directory}/{self.child_ini_file}')
        self._debug_transaction.save_file(
            f'{self.directory}/cfg/entry_list.ini')

        await self.put(Protocol.success(
            msg='Assetto Corsa server stopped'))

        await self._watcher_stdout.stop()
        self._watcher_stdout.unsubscribe(self)

        self.lobby.unsubscribe(self)

    async def __sessions(self):
        '''Show game sessions info as a JSON string'''
        await self.put(Protocol.success({'sessions': self.sessions}))
