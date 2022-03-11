from ncclient import manager
from NetconfFilters import (
    netconf_ietf_interfaces_status,
    netconf_ietf_interfaces,
    netconf_ietf_interfaces_xpath,
    netconf_ietf_interfaces_config,
    netconf_native_memory_statistics
)
import xmltodict
import logging

logging.basicConfig(
       level=logging.DEBUG,
   )


def main():
    sandbox_router = {
        'host': 'sandbox-iosxe-latest-1.cisco.com',
        'username': 'developer',
        'password': 'C1sco12345',
        'device_params':{'name':'csr'},
        'port': 830}
    
    # Using Subtree Filter and sending a 'get-config'
    # Selecting subtree as a filter option in Ncclient adds an additional filter tag to the RPC. 
    with manager.connect(**sandbox_router, hostkey_verify=False) as m:
        m.server_capabilities
        interfaces_ietf = m.get_config(source="running",
                                       filter=("subtree",netconf_ietf_interfaces))
        interfaces_ietf_dict = xmltodict.parse(interfaces_ietf.data_xml)
        interface_description = interfaces_ietf_dict['data']['interfaces']['interface']['description']
        print(f'Interface description for GigabitEthernet2 is {interface_description}')

        # For getting realtime oper-status from interface. ITS DONE USING GET AND NO DATASTORE NEEDED.
        interfaces_ietf_status = m.get(("subtree",netconf_ietf_interfaces_status))
        interfaces_ietf_status_dict = xmltodict.parse(interfaces_ietf_status.data_xml)
        interfaces_ietf_status = interfaces_ietf_status_dict['data']['interfaces-state']['interface']['oper-status']
        print(f'Interface operation status for GigabitEthernet2 is {interfaces_ietf_status}')

        # Changing description using netconf
        interface_config = netconf_ietf_interfaces_config.format(name='GigabitEthernet2',
                                                                 description='Changed using NcclientNetconf')
        change_reply = m.edit_config(interface_config, target="running")
        print(change_reply)


if __name__ == '__main__':
    main()
