from ncclient import manager
from NetconfFilters import netconf_ietf_interfaces
import xmltodict


def main():
    sandbox_router = {
        'host': 'sandbox-iosxe-latest-1.cisco.com',
        'username': 'developer',
        'password': 'C1sco12345',
        'port': 830,
        'device_params':{'name':"csr"}}

    with manager.connect(**sandbox_router, hostkey_verify=False) as m:
        m.server_capabilities
        interfaces_ietf = m.get_config('running',netconf_ietf_interfaces)
        interfaces_ietf_dict = xmltodict.parse(interfaces_ietf.data_xml)
        interface_description = interfaces_ietf_dict['data']['interfaces']['interface']['description']
        print(f'Interface description for GigabitEthernet2 is {interface_description}')


if __name__ == '__main__':
    main()
