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

It takes in the user ID given to you by the USPS and a list of addresses to verify.
Each address is a dict containing the following required keys:

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

The response will either be list of dicts. Each address
will always contain the following keys:

     :address: The street address
     :city: The city
     :state: The state
     :zip5: The first five numbers of the zip code
     :zip4: The last four numbers of the zip code


Each address can optionally contain the following keys:

    :firm_name: The company name, e.g., XYZ Corp.
    :address_extended: An apartment, suite number, etc
    :urbanization: For Puerto Rico addresses only
    :returntext: Additional information about the address, usually a warning, e.g., "The address you entered was found but more information is needed (such as an apartment, suite, or box number) to match to a specific address."

*firm_name, address_extended and urbanization will return the value
requested if the API does not find a match.*

For multiple addresses, the order in which the addresses
were specified in the request is preserved in the response.

Errors
------

A ValueError will be raised if there's a general error, e.g.,
invalid user id, or if a single address request generates an error.
Except for a general error, multiple addresses requests do not raise errors.
Instead, if one of the addresses generates an error, the
ValueError object is returned along with the rest of the results.


Example
-------

Mutiple addresses error::

    from pyusps import address_information

    addrs = [
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
    address_information.verify('foo_id', addrs)
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
        USPSError('-2147219400: Invalid City.  '),
    ]


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
