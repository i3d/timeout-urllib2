#!/usr/bin/python

import ftplib
import socket
import unittest
import urllib2
import timeout_urllib2


class MockSocket(object):
  def __init__(self):
    self._passiveserver = None

  def connect(self):
    pass

  def close(self):
    pass

  def settimeout(self, timeout):
    pass

  def makefile(self, *args):
    pass

  def listen(self, *args):
    pass

  def getsockname(self):
    pass

  def GetPassiveserver(self):
    return self._passiveserver

  def SetPassiveserver(self, value):
    self._passiveserver = value

  passiveserver = property(GetPassiveserver, SetPassiveserver)


def _raiseTimeout():
  raise socket.timeout

class TimeoutUrllib2UnitTest(unittest.TestCase):

  def testSetupHTTPTimeout(self):
    timeout_urllib2.sethttptimeout(10.0)
    self.assertTrue(timeout_urllib2.TimeoutHTTPConnection._timeout == 10.0)
    found = False
    for handler in urllib2._opener.handlers:
      if handler.__class__.__name__.lower().find('timeouthttph') != -1:
        found = True
    self.assertTrue(found)

  def testSetupHTTPSTimeout(self):
    timeout_urllib2.sethttpstimeout(5.0)
    self.assertTrue(timeout_urllib2.TimeoutHTTPSConnection._timeout == 5.0)
    found = False
    for handler in urllib2._opener.handlers:
      if handler.__class__.__name__.lower().find('timeouthttps') != -1:
        found = True
    self.assertTrue(found)

  def testSetupFTPTimeout(self):
    timeout_urllib2.setftptimeout(5.0)
    found = False
    for handler in urllib2._opener.handlers:
      if handler.__class__.__name__.lower().find('timeoutftp') != -1:
        found = True
        self.assertTrue(handler._timeout == 5.0)
    self.assertTrue(found)

  def testReset(self):
    timeout_urllib2.reset()
    found = False
    for handler in urllib2._opener.handlers:
      if handler.__class__.__name__.lower().find('timeout') != -1:
        found = True
    self.assertTrue(found == False)

  def testHTTPRaiseTimeoutException(self):
    timeout_urllib2.reset()
    socket.getaddrinfo = lambda *x: (('af', 'stype', 'proto', 'name', 'sa'),)
    socket.socket = lambda *x: MockSocket()
    MockSocket.connect = lambda *x: _raiseTimeout()
    self.assertRaises(timeout_urllib2.HTTPConnectionTimeoutError,
                      timeout_urllib2.TimeoutHTTPConnection('fake.com',
                      timeout=5.0).connect)

  def testHTTPSRaiseTimeoutException(self):
    timeout_urllib2.reset()
    socket.getaddrinfo = lambda *x: (('af', 'stype', 'proto', 'name', 'sa'),)
    socket.socket = lambda *x: MockSocket()
    MockSocket.connect = lambda *x: _raiseTimeout()
    self.assertRaises(timeout_urllib2.HTTPSConnectionTimeoutError,
                      timeout_urllib2.TimeoutHTTPSConnection('fake.com',
                      timeout=10).connect)

  def testFTPRaiseTimeoutExceptionConnect(self):
    timeout_urllib2.reset()
    socket.getaddrinfo = lambda *x: (('af', 'stype', 'proto', 'name', 'sa'),)
    socket.socket = lambda *x: MockSocket()
    MockSocket.connect = lambda *x: _raiseTimeout()
    ftplib.FTP.getresp = lambda *x: None
    raised = ''
    try:
      timeout_urllib2.TimeoutFTP('fake.com', 'fake', 'fakepass',
                               timeout=5.0).connect()
    except timeout_urllib2.FTPConnectionTimeoutError, msg:
      raised = 'ftp timeout raised'
    self.assertTrue(raised == 'ftp timeout raised')

  def testFTPRaiseTimeoutExceptionMakePort(self):
    timeout_urllib2.reset()
    socket.getaddrinfo = lambda *x: (('af', 'stype', 'proto', 'name', 'sa'),)
    socket.socket = lambda *x: MockSocket()
    MockSocket.bind = lambda *x: _raiseTimeout()
    ftplib.FTP.sendport = lambda *x: None
    ftplib.FTP.sendeprt = lambda *x: None
    raised = ''
    try:
      timeout_urllib2.TimeoutFTP('fake.com', 'fake', 'fakepass',
                                 timeout=5.0).makeport()
    except timeout_urllib2.FTPConnectionTimeoutError, msg:
      raised = 'ftp timeout raised'
    self.assertTrue(raised == 'ftp timeout raised')

  def testFTPRaiseTimeoutExceptionNtransfercmd(self):
    timeout_urllib2.reset()
    socket.getaddrinfo = lambda *x: (('af', 'stype', 'proto', 'name', 'sa'),)
    socket.socket = lambda *x: MockSocket()
    MockSocket.GetPassiveserver = lambda *x: True
    ftplib.FTP.makepasv = lambda *x: ('fake', 'fake')
    raised = ''
    try:
      timeout_urllib2.TimeoutFTP('fake.com', 'fake', 'fakepass',
                                 timeout=5.0).ntransfercmd('abc')
    except timeout_urllib2.FTPConnectionTimeoutError, msg:
      raised = 'ftp timeout raised'
    self.assertTrue(raised == 'ftp timeout raised')


if __name__ == '__main__':
  unittest.main()
