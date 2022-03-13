import xmltodict
import xml.dom.minidom
from pprint import pprint
from scrapli_netconf.driver import NetconfDriver
from NetconfFilters import (
    netconf_ietf_interfaces_status,
    netconf_ietf_interfaces,
    netconf_ietf_interfaces_config,
    netconf_native_memory_statistics
)


import logging
logging.basicConfig(level=logging.DEBUG,)


def main():
    sandbox_router = {
        'host': 'sandbox-iosxe-latest-1.cisco.com',
        'auth_username': 'developer',
        'auth_password': 'C1sco12345',
        'auth_strict_key': False,
        'port': 830
    }

    with NetconfDriver(**sandbox_router) as connection:
        connection.open()

        # USING SUBTREE FILTERS:

        # Send a get-config to retrieve ieft interfaces.
        interfaces_ietf = connection.get_config("running", filter_=netconf_ietf_interfaces)
        interfaces_ietf_xmldom = xml.dom.minidom.parseString(str(interfaces_ietf.result))
        interfaces_ietf_dict = xmltodict.parse(interfaces_ietf_xmldom.toxml())
        interface_description = interfaces_ietf_dict['rpc-reply']['data']['interfaces']['interface']['description']
        print(f"Interface description for GigabitEthernet2 is {interface_description}")

        # Send a get to retrieve ieft interfaces oper-status from interface.
        # NOTE: ITS DONE USING GET AND NO DATASTORE NEEDED.
        interfaces_ietf_status = connection.get(netconf_ietf_interfaces_status)
        interfaces_ietf_status_xmldom = xml.dom.minidom.parseString(
            str(interfaces_ietf_status.result))
        interfaces_ietf_status_dict = xmltodict.parse(interfaces_ietf_status_xmldom.toxml())
        interfaces_ietf_status = interfaces_ietf_status_dict['rpc-reply']['data']['interfaces-state']['interface']['oper-status']
        print(f"Interface operation status for GigabitEthernet2 is {interfaces_ietf_status}")

        # Sending a 'get' to retrieve oper-status of a Native module.
        native_memory_statistics = connection.get(filter_=netconf_native_memory_statistics)
        native_memory_statistics_xmldom = xml.dom.minidom.parseString(str(native_memory_statistics.result))
        native_memory_statistics_dict = xmltodict.parse(native_memory_statistics_xmldom.toxml())
        pprint(native_memory_statistics_dict)

        # USING XPATH FILTERS (not supported for several devices)
        connection.server_capabilities
        assert(any(":xpath" in capability for capability in connection.server_capabilities))

        # Send a get-config to retrieve the interfaces config and return all namespaces that match with filter.
        netconf_xpath_selection = 'interfaces/interface[name="GigabitEthernet2"]'
        netconf_xpath = connection.get_config(source="running", filter_=netconf_xpath_selection, filter_type="xpath")
        netconf_xpath_xmldom = xml.dom.minidom.parseString(str(netconf_xpath.result))
        netconf_xpath_dict = xmltodict.parse(netconf_xpath_xmldom.toxml())
        pprint(netconf_xpath_dict['rpc-reply']['data']['interfaces'])

        #  Send a 'get' to retrieve oper-status of an interface and filter only the OpenConfig namespace
        netconf_native_xpath_select = """
        <get-config>
                <source><running/></source>
                <filter xmlns:xyz='http://openconfig.net/yang/interfaces'
                        type='xpath'
                        select='/xyz:interfaces/interface[name="GigabitEthernet2"]'/>
        </get-config>"""
        netconf_native_xpath = connection.rpc(filter_=netconf_native_xpath_select)
        netconf_native_xpath_xmldom = xml.dom.minidom.parseString(str(netconf_native_xpath.result))
        netconf_native_xpath_dict = xmltodict.parse(netconf_native_xpath_xmldom.toxml())
        pprint(netconf_native_xpath_dict['rpc-reply']['data']['interfaces'])

        # OHER RPC OPERATIONS

        # Changing description sending a config RPC
        interface_config = netconf_ietf_interfaces_config.format(name="GigabitEthernet2",
                                                                 description="Changed using ScrappliNetconf")
        change_reply = connection.edit_config(config=interface_config, target="running")
        if not change_reply.failed:
            print("Change done")

        # Save the config using custom craft rpc
        save_body = """<cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>"""
        rpc_replay = connection.rpc(filter_=save_body)
        if not rpc_replay.failed:
            print("Save running-config successful")
        connection.close()


if __name__ == '__main__':
    main()
