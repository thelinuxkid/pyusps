import urllib2
import urllib

from lxml import etree
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

api_url = 'http://production.shippingapis.com/ShippingAPI.dll'
address_max = 5

def _find_error(root):
    if root.tag == 'Error':
        num = root.find('Number')
        desc = root.find('Description')
        return (num, desc)

def _get_error(error):
    (num, desc) = error
    return ValueError(
        '{num}: {desc}'.format(
            num=num.text,
            desc=desc.text,
            )
        )

def _get_address_error(address):
    error = address.find('Error')
    if error is not None:
        error = _find_error(error)
        return _get_error(error)

def _parse_address(address):
    result = OrderedDict()
    for child in address.iterchildren():
        # elements are yielded in order
        name = child.tag.lower()
        # More user-friendly names for street
        # attributes
        if name == 'address2':
            name = 'address'
        elif name == 'address1':
            name = 'address_extended'
        elif name == 'firmname':
            name = 'firm_name'
        result[name] = child.text

    return result

def _process_one(address):
    # Raise address error if there's only one item
    error = _get_address_error(address)
    if error is not None:
        raise error

    return _parse_address(address)

def _process_multiple(addresses):
    results = []
    count = 0
    for address in addresses:
        # Return error object if there are
        # multiple items
        error = _get_address_error(address)
        if error is not None:
            result = error
        else:
            result = _parse_address(address)
            if str(count) != address.get('ID'):
                msg = ('The addresses returned are not in the same '
                       'order they were requested'
                       )
                raise IndexError(msg)
        results.append(result)
        count += 1

    return results

def _parse_response(res):
    # General error, e.g., authorization
    error = _find_error(res.getroot())
    if error is not None:
        raise _get_error(error)

    results = res.findall('Address')
    length = len(results)
    if length == 0:
        raise TypeError(
            'Could not find any address or error information'
            )
    if length == 1:
        return _process_one(results.pop())
    return _process_multiple(results)

def _get_response(xml):
    params = OrderedDict([
            ('API', 'Verify'),
            ('XML', etree.tostring(xml)),
            ])
    url = '{api_url}?{params}'.format(
        api_url=api_url,
        params=urllib.urlencode(params),
        )

    res = urllib2.urlopen(url)
    res = etree.parse(res)

    return res

def _create_xml(
    user_id,
    *args
    ):
    root = etree.Element('AddressValidateRequest', USERID=user_id)

    if len(args) > address_max:
        # Raise here. The Verify API will not return an error. It will
        # just return the first 5 results
        raise ValueError(
            'Only {address_max} addresses are allowed per '
            'request'.format(
                address_max=address_max,
                )
            )

    for i,arg in enumerate(args):
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

def verify(user_id, *args):
    xml = _create_xml(user_id, *args)
    res = _get_response(xml)
    res = _parse_response(res)

    return res
