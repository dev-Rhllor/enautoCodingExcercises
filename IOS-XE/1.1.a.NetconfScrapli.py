from scrapli_netconf.driver import NetconfDriver
from NetconfFilters import (
    netconf_ietf_interfaces_status,
    netconf_ietf_interfaces,
    netconf_ietf_interfaces_xpath,
    netconf_ietf_interfaces_config
)
import xmltodict
import xml.dom.minidom


def main():
    sandbox_router = {
        'host': 'sandbox-iosxe-latest-1.cisco.com',
        'auth_username': 'developer',
        'auth_password': 'C1sco12345',
        'auth_strict_key': False,
        'port': 830
    }

    # Filtering interface using netconf fiflter
    with NetconfDriver(**sandbox_router) as connection:
        connection.open()

        # For getting realtime oper-status from interface. ITS DONE USING GET AND NO DATASTORE NEEDED.
        interfaces_ietf_status = connection.get(netconf_ietf_interfaces_status)
        interfaces_ietf_status_xmldom = xml.dom.minidom.parseString(
            str(interfaces_ietf_status.result))
        interfaces_ietf_status_dict = xmltodict.parse(interfaces_ietf_status_xmldom.toxml())
        interfaces_ietf_status = interfaces_ietf_status_dict['rpc-reply']['data']['interfaces-state']['interface']['oper-status']
        print(f'Interface operation status for GigabitEthernet2 is {interfaces_ietf_status}')

        # Using Subtree Filter and sending a 'get-config'
        interfaces_ietf = connection.get_config('running', filter_=netconf_ietf_interfaces)
        interfaces_ietf_xmldom = xml.dom.minidom.parseString(str(interfaces_ietf.result))
        interfaces_ietf_dict = xmltodict.parse(interfaces_ietf_xmldom.toxml())
        interface_description = interfaces_ietf_dict['rpc-reply']['data']['interfaces']['interface']['description']
        print(f'Interface description for GigabitEthernet2 is {interface_description}')

        # changing description using netconf
        interface_config = netconf_ietf_interfaces_config.format(name='GigabitEthernet2',
                                                                 description='Changed using Netconf')
        change_reply = connection.edit_config(config=interface_config, target='running')
        print(change_reply)

        # Using Xpath (not supported for several devices) and selecting the ietf-interfaces namespace
        connection.server_capabilities
        if 'urn:ietf:params:netconf:capability:xpath:1.0' in connection.server_capabilities:
            interfaces_ietf_xpath = connection.rpc(filter_=netconf_ietf_interfaces_xpath)
            interfaces_ietf_xpath_xmldom = xml.dom.minidom.parseString(str(interfaces_ietf_xpath.result))
            interfaces_ietf_xpath_dict = xmltodict.parse(interfaces_ietf_xpath_xmldom.toxml())
            interface_description_xpath = interfaces_ietf_xpath_dict['rpc-reply']['data']['interfaces']['interface']['description']
            print(f'Interface description for GigabitEthernet2 is {interface_description_xpath}')

        interface_config = netconf_ietf_interfaces_config.format(name='GigabitEthernet2',
                                                                 description=interface_description)
        change_reply = connection.edit_config(config=interface_config, target='running')
        print(f'Rollback: {change_reply}')
        connection.close()


if __name__ == '__main__':
    main()
