import os
import logging

class Processor():
    def __init__(self, logPath="autoappanalysis.log") -> None:
        format = "[%(asctime)s] | %(levelname)s | %(message)s"
        logging.basicConfig(filename=logPath, level=logging.DEBUG, format=format)
        
    def process(self, cmd):
        logging.info(cmd)
        cmdResult = os.popen(cmd).read()
        return cmdResult
    
    def logInfo(self, info):
        logging.info(info)

    def logWarn(self, warn):
        logging.warn(warn)