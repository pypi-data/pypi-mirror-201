import time
from watchdog.events import FileSystemEventHandler, LoggingEventHandler

from .delayqueue import DelayQueue

delayqueue = DelayQueue()
class TransferHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print (f"GOT {event}")



def watch_directories(session, args, fixedtags, tagitems):
    from watchdog.observers import Observer

    observer = Observer()
    handler = TransferHandler()

    for dirs in args.directories:
        observer.schedule(handler, dirs, recursive=True)

    observer.start()
    print("Observer started")

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
