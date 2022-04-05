from collections import OrderedDict
from typing import Iterable

from lxml import etree

import pyusps.urlutil

ADDRESS_MAX = 5

class USPSError(ValueError):
    """
    An error from the USPS API, such as a bad `user_id` or when an address is not found.

    Inherits from ValueError. Also has attributes `code: str` and `description: str`.
    """
    code: str
    description: str

    def __init__(self, code: str, description: str) -> None:
        self.code = code
        self.description = description
        super().__init__(f"{code}: {description}")

    def __eq__(self, o: object) -> bool:
        return (
            isinstance(o, USPSError) and
            self.code == o.code and
            self.description == o.description
        )

def _get_error(node):
    if node.tag != 'Error':
        return None
    code = node.find('Number').text
    description = node.find('Description').text
    return USPSError(code, description)

def _get_address_error(address):
    error_node = address.find('Error')
    if error_node is None:
        return None
    else:
        return _get_error(error_node)

def _parse_address(address):
    result = OrderedDict()
    # More user-friendly names for street
    # attributes
    m = {
        "address2": "address",
        "address1": "address_extended",
        "firmname": "firm_name",
    }
    for child in address.iterchildren():
        # elements are yielded in order
        name = child.tag.lower()
        name = m.get(name, name)
        result[name] = child.text
    return result

def _process_multiple(addresses):
    results = []
    for i, address in enumerate(addresses):
        # Return error object if there are
        # multiple items
        error = _get_address_error(address)
        if error is not None:
            result = error
        else:
            if str(i) != address.get('ID'):
                msg = ('The addresses returned are not in the same '
                       'order they were requested'
                       )
                raise IndexError(msg)
            result = _parse_address(address)
        results.append(result)

    return results

def _parse_response(res):
    # General error, e.g., authorization
    error = _get_error(res.getroot())
    if error is not None:
        raise error

    results = res.findall('Address')
    if len(results) == 0:
        raise TypeError(
            'Could not find any address or error information'
            )
    return _process_multiple(results)

def _get_response(xml):
    params = OrderedDict([
            ('API', 'Verify'),
            ('XML', etree.tostring(xml)),
            ])
    param_string = pyusps.urlutil.urlencode(params)
    url = f'https://production.shippingapis.com/ShippingAPI.dll?{param_string}'
    res = pyusps.urlutil.urlopen(url)
    res = etree.parse(res)
    return res

def _create_xml(
    user_id,
    addresses: Iterable,
    ):
    root = etree.Element('AddressValidateRequest', USERID=user_id)

    for i, arg in enumerate(addresses):
        if i >= ADDRESS_MAX:
            # Raise here. The Verify API will not return an error. It will
            # just return the first 5 results
            raise ValueError(f'Only {ADDRESS_MAX} addresses are allowed per request')

        address = arg['address']
        city = arg['city']
        state = arg.get('state', None)
        zip_code = arg.get('zip_code', None)
        address_extended = arg.get('address_extended', None)
        firm_name = arg.get('firm_name', None)
        urbanization = arg.get('urbanization', None)

        address_el = etree.Element('Address', ID=str(i))
        root.append(address_el)

        # Documentation says this tag is required but tests
        # show it isn't
        if firm_name is not None:
            firm_name_el = etree.Element('FirmName')
            firm_name_el.text = firm_name
            address_el.append(firm_name_el)

        address_1_el = etree.Element('Address1')
        if address_extended is not None:
            address_1_el.text = address_extended
        address_el.append(address_1_el)

        address_2_el = etree.Element('Address2')
        address_2_el.text = address
        address_el.append(address_2_el)

        city_el = etree.Element('City')
        city_el.text = city
        address_el.append(city_el)

        state_el = etree.Element('State')
        if state is not None:
            state_el.text = state
        address_el.append(state_el)

        if urbanization is not None:
            urbanization_el = etree.Element('Urbanization')
            urbanization_el.text = urbanization
            address_el.append(urbanization_el)

        zip5 = None
        zip4 = None
        if zip_code is not None:
            zip5 = zip_code[:5]
            zip4 = zip_code[5:]
            if zip4.startswith('-'):
                zip4 = zip4[1:]

        zip5_el = etree.Element('Zip5')
        if zip5 is not None:
            zip5_el.text = zip5
        address_el.append(zip5_el)

        zip4_el = etree.Element('Zip4')
        if zip4 is not None:
            zip4_el.text = zip4
        address_el.append(zip4_el)

    return root

def verify(user_id: str, addresses: Iterable) -> "list[OrderedDict]":
    xml = _create_xml(user_id, addresses)
    res = _get_response(xml)
    res = _parse_response(res)

    return res
