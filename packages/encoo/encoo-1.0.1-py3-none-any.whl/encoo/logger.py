# -*- coding: utf-8 -*-
import logging
import os


class Logger(logging.Logger):

    def __init__(self,
                 logger_name="logger",
                 log_path="logs\log"):
        super().__init__(logger_name)
        self.log_path = log_path

        self._mk_logs_dir()
        self._fmt_output()

    def _fmt_output(self):

        console_fmt = logging.Formatter(
            fmt="%(name)s--->%(levelname)s--->%(asctime)s--->%(message)s")
        file_fmt = logging.Formatter(
            fmt="%(lineno)d--->%(name)s--->%(levelname)s--->%(asctime)s--->%(message)s")

        file_handler = logging.FileHandler(
            self.log_path, mode="a", encoding="utf-8")

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_fmt)
        self.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_fmt)
        self.addHandler(console_handler)

    def _mk_logs_dir(self):

        log_dir = os.path.dirname(self.log_path)
        if log_dir and not os.path.exists(log_dir):
            os.mkdir(log_dir)


if __name__ == "__main__":
    Logger().debug("This is one debug message..")
