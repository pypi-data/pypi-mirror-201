import logging
import datetime
import os, sys


class Logger(object):
    __msgfmt = '%(asctime)s.%(msecs)03d | %(filename)s:%(funcName)s[%(lineno)d] | %(levelname)s : %(message)s'
    __datefmt = '%Y-%m-%d %H:%M:%S'

    def __init__(self, filename=None):
        if filename is None:
            filename = ''
        logname = '{:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())+filename
        self.logger = logging.getLogger(logname)
        self.__checkFilePath(filename)
        self.__setupFileLog(filename)
        self.__setupConsoleLog()

        # python 3.6 版本 不支持`stacklevel`参数关键字，需要另设置 `.d .i .w .e .x` 方法
        ver = sys.version_info
        if ver.major < 3 or (ver.major == 3 and ver.minor <= 6):
            self.d = self.logger.debug
            self.i = self.logger.info
            self.w = self.logger.warning
            self.e = self.logger.error
            self.x = self.logger.critical
            self.exc = self.logger.exception

    def __setupFileLog(self, file):
        if file is None or len(file) == 0:
            return
        formatter = logging.Formatter(self.__msgfmt)
        formatter.datefmt = self.__datefmt
        file_handler = logging.FileHandler(file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)

    def __setupConsoleLog(self):
        formatter = logging.Formatter(self.__msgfmt)
        formatter.datefmt = self.__datefmt
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)

    def __checkFilePath(self, filename):
        arr = filename.split('/')
        if len(arr) == 1:
            return
        makeFilePath(filename)

    def d(self, *args):
        msg = ' '.join(['%s'%i for i in args])
        self.logger.debug(msg, stacklevel=2)

    def i(self, *args):
        msg = ' '.join(['%s'%i for i in args])
        self.logger.info(msg, stacklevel=2)

    def w(self, *args):
        msg = ' '.join(['%s'%i for i in args])
        self.logger.warning(msg, stacklevel=2)

    def e(self, *args):
        msg = ' '.join(['%s'%i for i in args])
        self.logger.error(msg, stacklevel=2)

    def exc(self, *args):
        msg = ' '.join(['%s'%i for i in args])
        self.logger.exception(msg, stacklevel=3)

    def x(self, *args):
        msg = ' '.join(['%s'%i for i in args])
        self.logger.critical(msg, stacklevel=2)


def makeFilePath(path):
    arr = path.split('/')
    if len(arr) == 1:
        return
    filepath = os.path.join(*arr[:-1])
    if os.path.exists(filepath):
        return
    paths = filepath.split('/')
    for i in range(len(paths)):
        folder = '/'.join(paths[:i + 1])
        if not os.path.exists(folder):
            os.mkdir(folder)
    return filepath


def test():
    log = Logger()
    log.d('debug')
    log.i('info')
    log.e('error')
    try:
        a = 1/0
        log.d(a)
    except:
        log.exc('做除法的时候出错')
    log.i('come here')
    pass


if __name__ == '__main__':
    test()
