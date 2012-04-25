=========
pyusps
=========

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

Testing
=======

Install using pip::

    pip install pyusps[test]

or easy_install::

    easy_install pyusps[test]

Then run the tests using nose::

     nosetests

Developing
==========

Install using pip::

    pip install pyusps[dev,test]

or easy_install::

    easy_install pyusps[dev,test]

Address Information API
=======================

This API is avaiable via the pyusps.address_information.verify
function. It takes in the user ID given to you by the USPS
and a variable length list of addresses to verify.

Requests
--------

Each address is a dict containing the following required keys.
Only one of state or zip_code is needed:

     :address: The street address
     :city: The city
     :state: The state
     :zip_code: The zip code in one the following formats: xxxxx, xxxxx-xxxx, or xxxxxxxxx

The following keys are optional:

    :firm_name: The company name, e.g., XYZ Corp. Although the API documentation says this field is required, tests show that it isn't.
    :address_extended: An apartment, suite number, etc
    :urbanization: For Puerto Rico addresses only



Responses
---------

The response will either be a dict, if a single address was requested,
or a list of dicts, if multiple addresses were requested. Each address
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

**firm_name, address_extended and urbanization will return the value
requested if the API does not find a match.**

For multiple addresses responses, the order in which the addresses
were specified in the request is preserved.

Errors
------

A ValueError will be raised if there's a general error, e.g.,
invalid user id, or if a single address request generates an error.
Except for a general error, multiple address requests do not raise errors.
Instead, if one of the addresses generates an error, the
ValueError object is returned along with the rest of the results.


Examples
--------

Single address request::

       from pyusps import address_information

       addr = dict([
            ('address', '6406 Ivy Lane'),
            ('city', 'Greenbelt'),
            ('state', 'MD'),
            ])
       address_information.verify('foo_id', addr)
       dict([
           ('address', '6406 IVY LN'),
           ('city', 'GREENBELT'),
           ('state', 'MD'),
           ('zip5', '20770'),
           ('zip4', '1441'),
           ])

Mutiples addresses request::

       from pyusps import address_information

       addrs = [
           dict([
                   ('address', '6406 Ivy Lane'),
                   ('city', 'Greenbelt'),
                   ('state', 'MD'),
                   ]),
           dict([
                   ('address', '8 Wildwood Drive'),
                   ('city', 'Old Lyme'),
                   ('state', 'CT'),
                   ]),
          ]
       address_information.verify('foo_id', *addrs)
       [
        dict([
                ('address', '6406 IVY LN'),
                ('city', 'GREENBELT'),
                ('state', 'MD'),
                ('zip5', '20770'),
                ('zip4', '1441'),
                ]),
        dict([
                ('address', '8 WILDWOOD DR'),
                ('city', 'OLD LYME'),
                ('state', 'CT'),
                ('zip5', '06371'),
                ('zip4', '1844'),
                ]),
        ]

Mutiples addresses error::

       from pyusps import address_information

       addrs = [
           dict([
                   ('address', '6406 Ivy Lane'),
                   ('city', 'Greenbelt'),
                   ('state', 'MD'),
                   ]),
           dict([
                   ('address', '8 Wildwood Drive'),
                   ('city', 'Old Lyme'),
                   ('state', 'NJ'),
                   ]),
          ]
       address_information.verify('foo_id', *addrs)
       [
        dict([
                ('address', '6406 IVY LN'),
                ('city', 'GREENBELT'),
                ('state', 'MD'),
                ('zip5', '20770'),
                ('zip4', '1441'),
                ]),
        ValueError('-2147219400: Invalid City.  '),
        ]

Reference
---------
For more information on the Address Information API visit https://www.usps.com/webtools/htm/Address-Information-v3-1a.htm#_Toc131231385
