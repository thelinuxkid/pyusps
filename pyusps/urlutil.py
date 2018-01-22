# `fudge.patch` in `pyusps.test.test_address_information` needs the full
# module path as well as the function name as its argument, e.g.,
# "urllib2.urlopen". Create a normalized module path here for
# urllib2/urllib functions in order to support both Python 2 and Python 3.

try:
    from urllib.request import urlopen as _urlopen
except ImportError:
    from urllib2 import urlopen as _urlopen

try:
    from urllib.parse import urlencode as _urlencode
except ImportError:
    from urllib import urlencode as _urlencode

urlopen = _urlopen
urlencode = _urlencode
