======
pyusps
======

Description
===========

pyusps is a pythonic wrapper for the USPS Ecommerce APIs.
Currently, only the Address Information API is supported.

Installation
============

Install using pip::

    pip install pyusps

or easy_install::

    easy_install pyusps

Address Information API
=======================

This API is avaiable via the `pyusps.address_information.verify`
function.

Requests
--------

It takes in the user ID given to you by the USPS and an iterable of addresses to verify.
You can only supply up to 5 addresses at a time due to the API's limits.
Each address is a dict-like (e.g. supports `__getitem__()`) containing the following
required keys:

     :address: The street address
     :city: The city
     :state: The state
     :zip_code: The zip code in one the following formats: xxxxx, xxxxx-xxxx, or xxxxxxxxx

*Only one of state or zip_code is needed.*

The following keys are optional:

    :firm_name: The company name, e.g., XYZ Corp. Although the API documentation says this field is required, tests show that it isn't.
    :address_extended: An apartment, suite number, etc
    :urbanization: For Puerto Rico addresses only

Responses
---------

The response will either be list of `dict`s or `USPSError`s. Each `dict`
will always contain the following keys:

     :address: The street address
     :city: The city
     :state: The state
     :zip5: The first five numbers of the zip code
     :zip4: The last four numbers of the zip code


Each `dict` can optionally contain the following keys:

    :firm_name: The company name, e.g., XYZ Corp.
    :address_extended: An apartment, suite number, etc
    :urbanization: For Puerto Rico addresses only
    :returntext: Additional information about the address, usually a warning, e.g., "The address you entered was found but more information is needed (such as an apartment, suite, or box number) to match to a specific address."

*firm_name, address_extended and urbanization will return the value
requested if the API does not find a match.*

If the USPS can't find an address, then in the response list, instead of a `dict` you
will receive a `USPSError`. `USPSError` is a subclass of `RuntimeError`, and has the
additional attributes of `code` and  `description` for the error.

The order in which the addresses
were specified in the request is preserved in the response.

Errors
------

- ValueError will be raised if you request more than 5 addresses.
- RuntimeError will be raised when the API returns a response that we can't parse
  or otherwise doesn't make sense (You shouldn't run into this).
- A USPSError will be raised if the supplied user_id is invalid.

Example
-------

Mutiple addresses, one of them isn't found so an error is returned::

    >>> from pyusps import address_information

    >>> addrs = [
        {
            "address": "6406 Ivy Lane",
            "city": "Greenbelt",
            "state": "MD",
        },
        {
            "address": "8 Wildwood Drive",
            "city": "Old Lyme",
            "state": "NJ",
        },
    ]
    >>> results = address_information.verify('foo_id', addrs)
    >>> results
    [
        {
            'address': '6406 IVY LN',
            'city': 'GREENBELT',
            'returntext': 'Default address: The address you entered was found but more '
                        'information is needed (such as an apartment, suite, or box '
                        'number) to match to a specific address.',
            'state': 'MD',
            'zip4': '1435',
            'zip5': '20770'
        },
        USPSError('-2147219400: Invalid City.'),
    ]
    >>> results[1].code
    '-2147219400'
    >>> res[1].description
    'Invalid City.'


Reference
---------
For more information on the Address Information API visit https://www.usps.com/business/web-tools-apis/address-information-api.htm

Developing
==========

External dependencies
---------------------

    - libxml2-dev
    - libxslt1-dev
    - build-essential
    - python-dev or python3-dev
    - python-setuptools or python3-setuptools
    - virtualenvwrapper

Setup
-----

To start developing, run the following commands from the project's base
directory. You can download the source from
https://github.com/thelinuxkid/pyusps::

    mkvirtualenv pyusps
    python setup.py develop
    # At this point, pyusps will already be in easy-install.pth.
    # So, pip will not attempt to download it
    pip install pyusps[test]

If you like to use ipython you can install it with the dev
requirement::

    pip install pyusps[dev]

Testing
-------

To run the unit-tests run the following command from the project's
base directory::

    nosetests
