# -*- coding: utf-8 -*-

"""package scinstr
author    Benoit Dubois
copyright FEMTO ENGINEERING, 2019
license   GPL v3.0+
brief     Emulation of basic SCPI DMM
"""

import logging
import time
import random

import signalslot as ss

import scinstr.cnt.cnt532x0a as cnt532x0a

# Only to mime real device import (detection of circular reference)
import socket
import usbtmc


# =============================================================================
class Cnt532x0aEmul(cnt532x0a.Cnt532x0aAbstract):
    """Emulate 532x0a counter device.
    """

    def __init__(self, *args, **kwargs):
        """The constructor.
        :returns: None
        """
        logging.info("Init Counter test device: %r", self)
        super().__init__()
        self._is_connected = False
        for idx, value in enumerate(args):
            logging.info('Counter test device non-keyworded argument %02d: %r',
                         idx, value)
        for key, value in kwargs.items():
            logging.info('Counter test device named argument %r: %r', key, value)
        logging.info("Counter test device %r initialization done", self)

    def is_connected(self):
        return self._is_connected

    def connect(self):
        """Connection process to DMM.
        :returns: True if connection success other False (Bool)
        """
        logging.info("Connected to Counter test device: %r", self)
        self._is_connected = True
        return True

    def close(self):
        """Closing process with DMM.
        :returns: None
        """
        self._is_connected = False
        logging.info("Connection to Counter test device %r closed", self)

    def get_error(self):
        """Subclass method to emulate response of device.
        """
        return ["+0,\"No error\""]

    @property
    def timeout(self):
        """Gets timeout on socket operations.
        :returns: timeout value in second (float)
        """
        logging.info("Get Counter test device timeout: %r", self._timeout)
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """Sets timeout on socket operations.
        :param timeout: timeout value in second (float)
        :returns: None
        """
        self._timeout = timeout
        logging.info("Set Counter test device timeout: %r", timeout)

    def _write(self, data):
        """Emulate write process
        :param data: data writes to device (str)
        :returns: None
        """
        logging.info("Write %r to Counter test device %r", data, self)

    def _read(self, length):
        """Emulate read process.
        :param length: length of message to read (int)
        :returns: Message reads from device (str)
        """
        time.sleep(1.0)
        #data = self._random_gen()
        data = "{:+.12E}".format(100.0e6 + 0.00005)
        logging.info("Read %r from Counter test device %r", data, self)
        return data

    def _random_gen(self):
        """Return a random value: use to emulate data input acquisition.
        """
        return "{:+.12E}".format(random.uniform(-1.0, 1.0) + 100e6)


# =============================================================================
class SCnt532x0aEmul(Cnt532x0aEmul):
    """Class derived from Cnt532x0aEmul class to add signal/slot facilities.
    """

    connected = ss.Signal()
    closed = ss.Signal()
    id_checked = ss.Signal(['flag'])
    out_updated = ss.Signal(['value'])

    def connect(self, **kwargs):
        """Abstract protocol connect process. Derived classes must implement
        the connect process dedicated to the specific protocol used.
        :returns: None
        """
        retval = super().connect()
        if retval is True:
            self.connected.emit()
        return retval

    def close(self, **kwargs):
        """Abstract protocol closing process. Derived classes must implement
        the closing process dedicated to the specific protocol used.
        :returns: None
        """
        super().close()
        self.closed.emit()

    def check_interface(self, **kwargs):
        retval = super().check_interface()
        self.id_checked.emit(flag=retval)
        return retval

    def data_read(self, **kwargs):
        retval = super().data_read()
        if retval is not None:
            self.out_updated.emit(value=retval)
            return retval

    def set_timeout(self, timeout, **kwargs):
        """Sets timeout on operations.
        :param timeout: timeout value in second (float)
        :returns: None
        """
        self.timeout = timeout
        logging.info("Set Counter test device timeout: %r", timeout)

    def get_timeout(self):
        """Gets timeout on socket operations.
        :returns: timeout value in second (float)
        """
        logging.info("Get Counter test device timeout: %r", self.timeout)
        return self.timeout

    def set_pid(self, pid, **kwargs):
        """Set PID used to speak with device through USB.
        :param pid:
        :returns: None
        """
        self.pid = pid
        logging.info("Set Counter test device PID: %r", pid)

    def get_pid(self):
        """Get PID.
        :returns: pid
        """
        logging.info("Get Counter test device PID: %r", self.pid)
        return self.pid

    def set_vid(self, vid, **kwargs):
        """Set VID used to speak with device through USB.
        :param vid:
        :returns: None
        """
        self.vid = vid
        logging.info("Set Counter test device vid: %r", vid)

    def get_vid(self):
        """Get VID.
        :returns: vid
        """
        logging.info("Get Counter test device vid: %r", self.vid)
        return self.vid

    def set_ip(self, ip, **kwargs):
        """Sets IP address used to speak with device.
        :param ip: IP address (str)
        :return: None
        """
        self._ip = ip
        logging.info("Set Counter test device ip: %r", ip)

    def get_ip(self):
        """Gets IP used to speak with device.
        :returns: IP address (str)
        """
        logging.info("Get Counter test device ip: %r", self._ip)
        return self._ip

    def set_port(self, port, **kwargs):
        """Sets internet port used to speak with device.
        :param port: port used by counter532x0a (int)
        :returns: None
        """
        self._port = port
        logging.info("Set Counter test device port: %r", port)

    def get_port(self):
        """Gets internet port used to speak with device.
        :returns: port used by counter532x0a (int)
        """
        logging.info("Get Counter test device port: %r", self._port)
        return self._port


# =============================================================================
def check_cnt():
    """Check the Cnt532x0aEmul class: connect to the counter, configure
    frequency measurement then collect and print data to standard output.
    """
    from datetime import datetime

    date_fmt = "%d/%m/%Y %H:%M:%S"
    log_format = "%(asctime)s %(levelname) -8s %(filename)s " + \
                 " %(funcName)s (%(lineno)d): %(message)s"
    logging.basicConfig(level=logging.INFO,
                        datefmt=date_fmt,
                        format=log_format)

    cnt = Cnt532x0aEmul(0x2a8d, 0x1601, timeout=4.8)
    # cnt = Cnt532x0aEmul(ip="192.168.0.61", port=5025, timeout=2.8)
    if cnt.connect() is not True:
        print("Connection failed")
        return
    cnt.reset()

    print("IDN:", cnt.query("*IDN?"))
    cnt.write("CONF:FREQ 100.0E6\n")
    cnt.write("TRIG:SOUR IMM\n")
    cnt.write("TRIG:SLOP POS\n")
    cnt.write("SENS:FREQ:GATE:SOUR TIME\n")
    cnt.write("SENS:FREQ:GATE:TIME 1.0\n")
    print("Error config?:", cnt.get_error())

    try:
        while True:
            value = cnt.data_read()
            now = datetime.utcnow()
            if value is None or value == "":
                print("# No data @", now)
            else:
                print(now, value)
    except KeyboardInterrupt:
        cnt.write("ABORT")
    except Exception as er:
        logging.error("# Exception during acquisition: %r", er)

    print("Final error?:", cnt.get_error())

    cnt.close()


# =============================================================================
if __name__ == '__main__':
    check_cnt()
