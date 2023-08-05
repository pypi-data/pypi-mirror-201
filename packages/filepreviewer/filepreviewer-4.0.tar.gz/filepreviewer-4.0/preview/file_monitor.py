import pathlib
from typing import Callable

class FileMonitor:
    def __init__(self, path : pathlib.Path ):
        self.__last_modified = None
        self.__path = path

    async def run_if_modified(self, func:Callable):
        '''Run the specified callable if the file being monitored has been modified.
        '''
        if self.__last_modified != self.__path.stat().st_mtime:
            self.__last_modified = self.__path.stat().st_mtime
            await func()




