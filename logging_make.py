import logging
import time


class Log:
    def __init__(self, container):

        # start logging
        self.log = logging.getLogger("mylog")
        date = time.strftime("%Y-%m-%d")
        log_config = logging.FileHandler(f"Logs/MainykLog_{date}.log")
        log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        log_config.setFormatter(log_formatter)
        self.log.addHandler(log_config)
        self.log.setLevel(logging.DEBUG)

        self.log.info("Logging started")
