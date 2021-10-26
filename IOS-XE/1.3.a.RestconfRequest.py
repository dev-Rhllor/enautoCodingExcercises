import requests
import json

# disable warnings from SSL/TLS certificates
requests.packages.urllib3.disable_warnings()


def main():
    sandboxRouter = {
        "host": "10.10.20.48",
        "auth_username": "developer",
        "auth_password": "C1sco12345",
        "port": 443
    }
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}

    #Default request/https port is 443. Parameter is optional. 
    url = f"https://{sandboxRouter['host']}:{sandboxRouter['port']}/restconf/data/netconf-state/capabilities"


    response = requests.get(url, 
                            auth=(sandboxRouter['auth_username'], sandboxRouter['auth_password'],),
                            headers=headers, 
                            verify=False)

    
    capabilities = response.json()['ietf-netconf-monitoring:capabilities']['capability']
    for capability in capabilities:
        print(capability)
    
    # Printing Static routes (equivalent to show run | i route) using Native Yang
    url = f"https://{sandboxRouter['host']}:{sandboxRouter['port']}/restconf/data/Cisco-IOS-XE-native:native/ip/route"

    response = requests.get(url, 
                            auth=(sandboxRouter['auth_username'], sandboxRouter['auth_password'],),
                            headers=headers, 
                            verify=False)
    
    print(response.text)

    # Printing Static routes (equivalent to show run | i route) using Standard Yang
    url = f"https://{sandboxRouter['host']}:{sandboxRouter['port']}/restconf/data/ietf-routing:routing/routing-instance=default/routing-protocols/"
    response = requests.get(url, 
                            auth=(sandboxRouter['auth_username'], sandboxRouter['auth_password'],),
                            headers=headers, 
                            verify=False)
    print(response.text)
 
    # Printing interaces statistics using native yang model 
    url = f"https://{sandboxRouter['host']}:{sandboxRouter['port']}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface=GigabitEthernet2/statistics"

    response = requests.get(url, 
                            auth=(sandboxRouter['auth_username'], sandboxRouter['auth_password'],),
                            headers=headers, 
                            verify=False)
    print(response.text)

    # Print current interfaces using a Standard yang model
    url = f"https://{sandboxRouter['host']}:{sandboxRouter['port']}/restconf/data/ietf-interfaces:interfaces/interface"

    response = requests.get(url, 
                            auth=(sandboxRouter['auth_username'], sandboxRouter['auth_password'],),
                            headers=headers, 
                            verify=False)
    print(response.text)
    # Configure a loopback interfaces using a Standard yang model
    url = f"https://{sandboxRouter['host']}:{sandboxRouter['port']}/restconf/data/ietf-interfaces:interfaces/"
    parameters = {
        "interface": [{
        "name": "Loopback1",
        "description": "My Loopback",
        "type": "iana-if-type:softwareLoopback",
        "enabled": "true",
        "ietf-ip:ipv4": {
            "address": [
                {
                "ip": "172.16.100.1",
                "netmask": "255.255.255.0"
                }
            ]
        }
     }]
}
    response = requests.post(url, 
                            auth=(sandboxRouter['auth_username'], sandboxRouter['auth_password'],),
                            headers=headers,
                            data=json.dumps(parameters), 
                            verify=False)
    print(response.text)
    # Print after configuration a loopback using a Standard yang model
    response = requests.get(url, 
                            auth=(sandboxRouter['auth_username'], sandboxRouter['auth_password'],),
                            headers=headers, 
                            verify=False)
    print(response.text)
    # Remove the loopback interfaces
    url = f"https://{sandboxRouter['host']}:{sandboxRouter['port']}/restconf/data/ietf-interfaces:interfaces/interface=Loopback1"
    response = requests.delete(url, 
                            auth=(sandboxRouter['auth_username'], sandboxRouter['auth_password'],),
                            headers=headers, 
                            verify=False)
    print(response.status_code)

if __name__ == '__main__':
    main()