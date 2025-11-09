from threading import Thread

from krita_hook.watcher import Watcher, ChangeEvent
from krita_hook.zip import zip_directory
from krita_hook.export import export_directory
from krita_hook.config import config


def start_hook():
    if not config:
        print('No krita config file found')
        return

    watcher_thread = Thread(
        target=Watcher(
            config['Watch'], 
            [
                LogChanges(),
                # ZipProject(),
                # ExportDirectory(),
            ]
        ).run,
    )
    watcher_thread.start()
    print('Started krita hook')
    watcher_thread.join()


class ZipProject(ChangeEvent):
    def handle(self, root):
        zip_directory(config['ZipFrom'], f'{config["ExtensionName"]}.zip', ignored=['__pycache__'])


class ExportDirectory(ChangeEvent):
    def handle(self, root):
        export_directory(config['ExportFrom'], config['ExportTo'])


class LogChanges(ChangeEvent):
    def handle(self, root):
        print('Changes detected')
