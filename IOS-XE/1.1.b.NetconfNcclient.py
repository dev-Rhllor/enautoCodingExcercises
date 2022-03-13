from ncclient import manager
from ncclient.xml_ import to_ele
import xmltodict
from pprint import pprint
from NetconfFilters import (
    netconf_ietf_interfaces_status,
    netconf_ietf_interfaces,
    netconf_ietf_interfaces_config,
    netconf_native_memory_statistics,
)


# import logging
# logging.basicConfig(level=logging.DEBUG,)


def main():
    sandbox_router = {
        'host': 'sandbox-iosxe-latest-1.cisco.com',
        'username': 'developer',
        'password': 'C1sco12345',
        'device_params': {'name': 'csr'},
        'port': 830}

    with manager.connect(**sandbox_router, hostkey_verify=False) as m:

        # USING SUBTREE FILTERS:

        # Send a get-config to retrieve ieft interfaces.
        # NOTE:Selecting subtree as a filter option in Ncclient adds an additional filter tag to the RPC.
        interfaces_ietf = m.get_config(source="running",
                                       filter=("subtree", netconf_ietf_interfaces))
        interfaces_ietf_dict = xmltodict.parse(interfaces_ietf.data_xml)
        interface_description = interfaces_ietf_dict['data']['interfaces']['interface']['description']
        print(f"Interface description for GigabitEthernet2 is {interface_description}")

        # Send a get to retrieve ieft interfaces oper-status from interface.
        # NOTE: ITS DONE USING GET AND NO DATASTORE NEEDED.
        interfaces_ietf_status = m.get(("subtree", netconf_ietf_interfaces_status))
        interfaces_ietf_status_dict = xmltodict.parse(interfaces_ietf_status.data_xml)
        interfaces_ietf_status = interfaces_ietf_status_dict['data']['interfaces-state']['interface']['oper-status']
        print(f"Interface operation status for GigabitEthernet2 is {interfaces_ietf_status}")

        # Sending a 'get' to retrieve oper-status of a Native module.
        native_memory_statistics = m.get(filter=("subtree", netconf_native_memory_statistics))
        native_memory_statistics_dict = xmltodict.parse(native_memory_statistics.data_xml)
        pprint(native_memory_statistics_dict)

        # USING XPATH FILTERS (not supported for several devices)
        m.server_capabilities
        assert(":xpath" in m.server_capabilities)

        # Send a get-config to retrieve the interfaces config and return all namespaces that match with filter.
        netconf_xpath_selection = "interfaces/interface[name='GigabitEthernet2']"
        netconf_xpath = m.get_config(source="running", filter=("xpath", netconf_xpath_selection))
        netconf_xpath_dict = xmltodict.parse(netconf_xpath.data_xml)
        pprint(netconf_xpath_dict['data']['interfaces'])

        # Send a 'get' to retrieve oper-status of an interface and filter only the OpenConfig namespace
        netconf_OC_namespace = {'xyz': 'http://openconfig.net/yang/interfaces'}
        netconf_OC_xpath_select = "/xyz:interfaces/interface[name='GigabitEthernet2']"
        netconf_OC_xpath = m.get_config(source="running", filter=('xpath', (netconf_OC_namespace, netconf_OC_xpath_select)))
        netconf_OC_xpath_dict = xmltodict.parse(netconf_OC_xpath.data_xml)
        pprint(netconf_OC_xpath_dict['data']['interfaces'])

        # OHER RPC OPERATIONS

        # Changing description sending a config RPC
        interface_config = netconf_ietf_interfaces_config.format(name='GigabitEthernet2',
                                                                 description='Changed using NcclientNetconf')
        change_reply = m.edit_config(interface_config, target="running")
        if change_reply.ok:
            print("Change done")

        # Save the config using custom craft rpc
        save_body = """<cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>"""
        rpc_replay = m.dispatch(to_ele(save_body))
        if rpc_replay.ok:
            print("Save running-config successful")


if __name__ == '__main__':
    main()
