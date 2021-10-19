from ncclient import manager
from NetconfFilters import *
import xmltodict 

def main():
    sandboxRouter = {
    'host':   '10.10.20.48',
    'username': 'developer',
    'password': 'C1sco12345',
    'port' : 830
}

    with manager.connect(**sandboxRouter, hostkey_verify=False) as m:
        m.server_capabilities
        interfaces_ietf= m.get_config(source="running", filter=netconf_ietf_interfaces)
        interfaces_ietfDict = xmltodict.parse(interfaces_ietf.data_xml)
        FirtInterfaceName=interfaces_ietfDict['data']['interfaces']['interface'][0]['name']
        print(f'First interface name is {FirtInterfaceName}')
  
if __name__ == '__main__':
    main()
