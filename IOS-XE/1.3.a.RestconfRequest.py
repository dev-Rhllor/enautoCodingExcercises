import requests
import json

# disable warnings from SSL/TLS certificates
requests.packages.urllib3.disable_warnings()


def main():
    sandbox_router = {
        'host': '10.10.20.48',
        'auth_username': 'developer',
        'auth_password': 'C1sco12345',
        'port': 443
    }
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}

    # Default request/https port is 443. Parameter is optional.
    base_url = f"https://{sandbox_router['host']}:{sandbox_router['port']}/restconf/data"
    resource = '/netconf-state/capabilities'
    response = requests.get(
        url=f'{base_url}{resource}',
        auth=(sandbox_router['auth_username'],
              sandbox_router['auth_password']),
        headers=headers,
        verify=False)
    c_dict = response.json()
    capabilities = c_dict['ietf-netconf-monitoring:capabilities']['capability']
    for capability in capabilities:
        print(capability)
    # Printing Static routes (show run | i route) using Native Yang
    resource = '/Cisco-IOS-XE-native:native/ip/route'

    response = requests.get(url=f'{base_url}{resource}',
                            auth=(sandbox_router['auth_username'],
                                  sandbox_router['auth_password']),
                            headers=headers,
                            verify=False)
    print(response.text)

    # Printing Static routes (show run | i route) using Standard Yang
    resource = '/ietf-routing:routing/routing-instance=default/routing-protocols/'
    response = requests.get(url=f'{base_url}{resource}',
                            auth=(sandbox_router['auth_username'],
                                  sandbox_router['auth_password']),
                            headers=headers,
                            verify=False)
    print(response.text)
    # Printing interaces statistics using native yang model
    resource = '/Cisco-IOS-XE-interfaces-oper:interfaces/interface=GigabitEthernet2/statistics'
    response = requests.get(url=f'{base_url}{resource}',
                            auth=(sandbox_router['auth_username'],
                                  sandbox_router['auth_password']),
                            headers=headers,
                            verify=False)
    print(response.text)
    # Print current interfaces using a Standard yang model
    resource = '/ietf-interfaces:interfaces/interface'
    response = requests.get(url=f'{base_url}{resource}',
                            auth=(sandbox_router['auth_username'],
                                  sandbox_router['auth_password']),
                            headers=headers,
                            verify=False)
    interface_dict = json.loads(response.text)
    print(interface_dict['ietf-interfaces:interface'])

    # Configure a loopback interfaces using a POST and the Standard yang model. Note that URI is the parent resource under which the new resource is created
    resource = '/ietf-interfaces:interfaces/'
    parameters = {'interface': [{'name': 'Loopback1',
                                 'description': 'My Loopback',
                                 'type': 'iana-if-type:softwareLoopback',
                                 'enabled': 'true',
                                 'ietf-ip:ipv4': {'address': [{'ip': '172.16.100.1',
                                                  'netmask': '255.255.255.0'}]}
                                 }
                                ]
                  }
    response = requests.post(url=f'{base_url}{resource}',
                             auth=(sandbox_router['auth_username'],
                                   sandbox_router['auth_password']),
                             headers=headers,
                             data=json.dumps(parameters),
                             verify=False)
    print(response.text)
    # Print after configuration a loopback using a Standard yang model
    response = requests.get(url=f'{base_url}{resource}',
                            auth=(sandbox_router['auth_username'],
                                  sandbox_router['auth_password']),
                            headers=headers,
                            verify=False)
    print(response.text)
    # Replace the loopback interface using PUT and the Standard yang model. (Note the resource changes and the URI in a PUT request is that of the newly created
    # resource itself )
    resource = '/ietf-interfaces:interfaces/interface=Loopback1'
    parameters = {'interface': [{'name': 'Loopback1',
                                 'type': 'iana-if-type:softwareLoopback',
                                 'enabled': 'true',
                                 'ietf-ip:ipv4': {'address': [{'ip': '172.16.100.2',
                                                  'netmask': '255.255.255.0'}]}
                                 }
                                ]
                  }
    response = requests.put(url=f'{base_url}{resource}',
                            auth=(sandbox_router['auth_username'],
                                  sandbox_router['auth_password']),
                            headers=headers,
                            data=json.dumps(parameters),
                            verify=False)
    # Print after configuration a loopback using a Standard yang model
    response = requests.get(url=f'{base_url}{resource}',
                            auth=(sandbox_router['auth_username'],
                                  sandbox_router['auth_password']),
                            headers=headers,
                            verify=False)
    print(response.text)
    # Update the loopback interface using PATH and the Standard yang model.
    resource = '/ietf-interfaces:interfaces/interface=Loopback1'
    parameters = {'interface': [{'name': 'Loopback1',
                                 'description': 'Description updated'}]}
    response = requests.patch(url=f'{base_url}{resource}',
                              auth=(sandbox_router['auth_username'],
                                    sandbox_router['auth_password']),
                              headers=headers,
                              data=json.dumps(parameters),
                              verify=False)
    # Print after configuration a loopback using a Standard yang model
    response = requests.get(url=f'{base_url}{resource}',
                            auth=(sandbox_router['auth_username'],
                                  sandbox_router['auth_password']),
                            headers=headers,
                            verify=False)
    print(response.text)
    # Remove the loopback interfaces
    resource = '/ietf-interfaces:interfaces/interface=Loopback1'
    response = requests.delete(url=f'{base_url}{resource}',
                               auth=(sandbox_router['auth_username'],
                                     sandbox_router['auth_password']),
                               headers=headers,
                               verify=False)
    print(response.status_code)


if __name__ == '__main__':
    main()
