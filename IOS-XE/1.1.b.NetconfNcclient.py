from ncclient import manager
from NetconfFilters import netconf_ietf_interfaces
import xmltodict


def main():
    sandbox_router = {
        'host': '10.10.20.48',
        'username': 'developer',
        'password': 'C1sco12345',
        'port': 830}

    with manager.connect(**sandbox_router, hostkey_verify=False) as m:
        m.server_capabilities
        interfaces_ietf = m.get_config(source="running",
                                       filter=netconf_ietf_interfaces)
        interfaces_ietf_dict = xmltodict.parse(interfaces_ietf.data_xml)
        first_interface_name = interfaces_ietf_dict['data']['interfaces']['interface']['name']
        print(f'First interface name is {first_interface_name}')


if __name__ == '__main__':
    main()
