import os
import imp
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from importlib import reload
import logging

logger = logging.getLogger()

class FSHandler(FileSystemEventHandler):
    def __init__(self, plugins):
        self.plugins = plugins
    
    def dispatch(self, event):
        """Dispatches events to the appropriate methods.

            Parameters:	event (FileSystemEvent) – The event object representing the file system event.
        """
        src_path = event.src_path
        path = src_path
        basename = os.path.basename(path)
        while len(basename) > 0:
            plugin = self.plugins.get(basename)
            if plugin is None:
                path = os.path.dirname(path)
                basename = os.path.basename(path)
                continue
            
            logger.debug("plugin %s is reloaded " % basename)
            reload(plugin)
            break

class PluginLoader():
    def __init__(self, basepath, folder):
        self.basepath = basepath
        self.folder = folder
        self.plugins={}
    
    def load(self):
        res = {}
        # check subfolders
        fullPath = os.path.abspath(os.path.join(self.basepath, self.folder))
        lst = os.listdir(fullPath)
        dir = []
        for d in lst:
            s = os.path.join(fullPath, d)
            if os.path.isdir(s) and os.path.exists(os.path.join(s, "__init__.py")):
                dir.append(d)
        # load the modules
        for d in dir:
            res[d]=__import__(self.folder + "." + d, fromlist = ["*"])
            
        self.plugins = res
        self.fsHandler = FSHandler(self.plugins)
        observer = Observer()
        observer.schedule(self.fsHandler, fullPath, recursive=True)
        observer.start()
