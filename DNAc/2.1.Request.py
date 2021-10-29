import requests
import json
from requests.auth import HTTPBasicAuth
from pprint import pprint


def main():
    base_url = "https://sandboxdnac.cisco.com"
    token_resource = "/dna/system/api/v1/auth/token"
    user = "devnetuser"
    password = "Cisco123!"
    # For retrieving the token a "post" with user and pass is needed.
    response = requests.post(url=f'{base_url}{token_resource}',
                             auth=HTTPBasicAuth(user, password)
                             ).json()
    token = response['Token']
    print(token)
    # Create headers with token for futere request
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': token}
    # get site list (getSite)
    sitelist_resource = "/dna/intent/api/v1/site"
    response = requests.get(url=f'{base_url}{sitelist_resource}',
                            headers=headers
                            ).json()
    site_count = len(response['response'])
    print(f'The amount of sites in {base_url} is \
          {site_count} and have the following names:')
    for site in response['response']:
        print(site['name'])
    # get physical topology (getPhysicalTopology)
    topology_resource = "/dna/intent/api/v1/topology/physical-topology"
    response = requests.get(url=f'{base_url}{topology_resource}',
                            headers=headers
                            ).json()
    print('Physical Topology')
    pprint(response['response'])
    # Get Device List (getDeviceList1)
    device_list_resource = "/dna/intent/api/v1/network-device"
    response = requests.get(url=f'{base_url}{device_list_resource}',
                            headers=headers
                            ).json()
    print('Device List')
    pprint(response['response'])
    # Filterin Device List by softwareType and name spine* (note ".*")
    query_parameters = {'softwareType': 'IOS-XE',
                        'hostname': 'spine.*'}
    response = requests.get(url=f'{base_url}{device_list_resource}',
                            params=query_parameters,
                            headers=headers
                            ).json()
    print('Filtering by:')
    for key in query_parameters.keys():
        print(f'{key} = {query_parameters[key]}')
    pprint(response['response'])

    # using the assurance API to get a list of clients (getOverallClientHealth)
    client_list_resource = "/dna/intent/api/v1/client-health"
    response = requests.get(url=f'{base_url}{client_list_resource}',
                            headers=headers
                            ).json()
    print('Client List')
    pprint(response['response'])
    for site in response['response']:
        name = site['siteId']
        print(f'For the Site {name}')
        for category in site['scoreDetail']:
            type = category['scoreCategory']['value']
            print(f'  Category: {type}:')
            try:
                print(f"    Total Count {category['clientCount']}")
                for health in category['scoreList']:
                    score_category = health['scoreCategory']['value']
                    count = health['clientCount']
                    print(f'    There is {count} clients\
                                with score {score_category}')
            except KeyError:
                pass
    # Run show ver in two devices. Gettin two devices ID
    query_parameters = {'softwareType': 'IOS-XE',
                        'role': 'ACCESS'}
    response = requests.get(url=f'{base_url}{device_list_resource}',
                            params=query_parameters,
                            headers=headers
                            ).json()
    device_list = []
    for device in response['response']:
        device_list.append(device['id'])
    # Running a "show version" cli command
    # (runRead_onlyCommandsOnDevicesToGetTheirReal_timeConfiguration)
    ro_resource = '/dna/intent/api/v1/network-device-poller/cli/read-request'
    commands = ['show version']
    payload = {'commands': commands,
               'description': 'Getting show version',
               'deviceUuids': device_list,
               'name': 'getting show ver of two devices',
               'timeout': 6
               }
    response = requests.post(url=f'{base_url}{ro_resource}',
                             data=json.dumps(payload),
                             headers=headers).json()
    taskurl = response['response']['url']
    # Using the task id, retrieve the file id associated with the response
    response = requests.get(url=f'{base_url}{taskurl}',
                            headers=headers).json()
    file_id = json.loads(response['response']['progress'])['fileId']
    # Retrieve the file information with the cli result of the commands.
    file_resource = f'/dna/intent/api/v1/file/{file_id}'
    response = requests.get(url=f'{base_url}{file_resource}',
                            headers=headers).json()
    pprint(response)


if __name__ == '__main__':
    main()
