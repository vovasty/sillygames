import os

def loadPlugins(basepath, folder):
    res = []
    # check subfolders
    fullPath = os.path.abspath(os.path.join(basepath, folder))
    lst = os.listdir(fullPath)
    dir = []
    for d in lst:
        s = os.path.join(fullPath, d)
        if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
            dir.append(d)
    # load the modules
    for d in dir:
        res.append(__import__(folder + "." + d, fromlist = ["*"]))
    return res

