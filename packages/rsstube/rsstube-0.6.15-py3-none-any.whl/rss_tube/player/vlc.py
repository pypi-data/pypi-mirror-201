import subprocess

from .base import BasePlayer


class VlcPlayerInstance(BasePlayer):
    def _run(self):        
        retcode = subprocess.call([self.path, *self.args, self.url])
        if retcode != 0:
            self.failed.emit(retcode)
