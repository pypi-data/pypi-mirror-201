'''Asyncio Debug Utilities.'''

import asyncio
from datetime import datetime
import os
import shutil

DELAY = 10


class DebugMonitor:
    '''Helper class to monitor async tasks'''

    @classmethod
    async def monitor_tasks(cls):
        '''
        Monitor tasks and print out every DELAY seconds.

        Call with:
        loop.create_task(monitor_tasks())
        '''
        # pylint: disable=expression-not-assigned

        while True:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            tasks = [
                t for t in asyncio.all_tasks()
                if t is not asyncio.current_task()
            ]
            [t.print_stack(limit=5) for t in tasks]
            await asyncio.sleep(DELAY)


class DebugTransaction():
    '''Super-class with methods to store debug files'''

    def __init__(self, server_directory: str):

        self._server_directory = server_directory

        if os.path.isdir(f'{self._server_directory}/debug'):
            self.debug_directory = f'{self._server_directory}/debug'
        else:
            self.debug_directory = None

        self.debug_transaction = None

    def close(self):
        '''Close a debug transaction'''
        self.debug_transaction = None

    def open(self, name: str = 'debug'):
        '''Open a debug transaction'''

        if not self.debug_transaction and self.debug_directory:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.debug_transaction = f'{self.debug_directory}/{timestamp}-{name}'
            os.mkdir(self.debug_transaction)

    def save_file(self, filename: str, new_filename: str = None):
        '''Save a file in the debug transaction'''

        if self.debug_transaction:
            if new_filename:
                shutil.copy2(
                    filename, '{self.debug_transaction}/{new_filename}')
            else:
                shutil.copy2(filename, self.debug_transaction)
