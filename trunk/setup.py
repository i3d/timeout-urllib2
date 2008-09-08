#!/usr/bin/python2.4
#
# Copyright 2008 Yongjian Xu (i3dmaster@gmail.com)

"""setup file for timeout_urllib2.

@see long description.
"""

__author__ = 'i3dmaster@gmail.com (Yongjian Xu)'

long_description = """Protocol based timeout facility for urllib2.

Currently only support HTTP and HTTPS.

Achived by inheriting httplib.HTTPConnection and httplib.HTTPSConnection
classes and provide a timeout version for both. Timeout has been carefully
implemented per connection base. A HTTPConnectionTimeoutError or
HTTPSConnectionTimeoutError would be raised instead of the general socket.error
so that urlib2 wouldn't throw out URLError exception when timeout is hit."""

from distutils.core import setup

setup(
    name="timeout_urllib2",
    version="0.1",
    description="Protocol/Connection based timeout facility for urllib2",
    long_description=long_description,
    author="Yongjian (Jim) Xu",
    author_email="i3dmaster@gmail.com",
    zip_safe=True,
    url="http://code.google.com/p/timeout-urllib2",
    license="MIT",
    keywords=['python', 'urllib2', 'timeout', 'httplib', 'Python'],
    py_modules=['timeout_urllib2'],
)
