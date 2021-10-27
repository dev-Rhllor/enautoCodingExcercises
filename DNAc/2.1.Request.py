import requests
import json
from requests.auth import HTTPBasicAuth
from pprint import pprint
import time


def main():
    base_url="https://sandboxdnac.cisco.com"
    token_resource="/dna/system/api/v1/auth/token"

    user="devnetuser"
    password="Cisco123!"
    ## For retrieving the token a "post" with user and pass is needed. 
    response=requests.post(url=f'{base_url}{token_resource}',
                         auth=HTTPBasicAuth(user,password)
                         ).json()
    token=response['Token']
    print(token)
    ## Create headers with token for futere request
    headers = {'Content-Type' : 'application/json',
              'Accept' : 'application/json',
              'X-Auth-Token':token}
   
    ## get site list (getSite)
    sitelist_resource="/dna/intent/api/v1/site"
    response=requests.get(url=f'{base_url}{sitelist_resource}',
                           headers=headers
                           ).json()
    siteCount=len(response['response'])
    print(f'The amount of sites in {base_url} is {siteCount} and have the following names:')
    for site in response['response']:
        print (site['name'])
    ## get physical topology (getPhysicalTopology)
    topology_resource="/dna/intent/api/v1/topology/physical-topology"
    response=requests.get(url=f'{base_url}{topology_resource}',
                           headers=headers
                           ).json()
    print('Physical Topology')
    pprint(response['response'])
    ## Get Device List (getDeviceList1)
    deviceList_resource="/dna/intent/api/v1/network-device"
    response=requests.get(url=f'{base_url}{deviceList_resource}',
                           headers=headers
                           ).json()
    print('Device List')
    pprint(response['response'])
    #Filterin Device List by softwareType and name spine* (note that any character is ".*")
    queryParameters= {'softwareType': 'IOS-XE',
                      'hostname': 'spine.*',}
    response=requests.get(url=f'{base_url}{deviceList_resource}',params=queryParameters,
                           headers=headers
                           ).json()
    print('Filtering by:')
    for key in queryParameters.keys():
     print(f'{key} = {queryParameters[key]}')
    pprint(response['response'])

    ## using the assurance API to get a list of clients (getOverallClientHealth)
    clientList_resource="/dna/intent/api/v1/client-health"
    response=requests.get(url=f'{base_url}{clientList_resource}',
                           headers=headers
                           ).json()
    print('Client List')
    pprint(response['response'])
    for site in response['response']:
        name= site['siteId']
        print (f'For the Site {name}')
        for category in site['scoreDetail']:
            type =category['scoreCategory']['value']
            print(f'  Category: {type}:')
            try:
                print(f"    Total Count {category['clientCount']}")
                for health in category['scoreList']:
                    scoreCategory=health['scoreCategory']['value']
                    count=health['clientCount']
                    print(f'    There is {count} clients with score {scoreCategory}')
            except:
                pass
    
    ## Run show ver in two devices
    # Gettin two devices ID
    
    queryParameters= {'softwareType': 'IOS-XE',
                      'role': 'ACCESS',}
    response=requests.get(url=f'{base_url}{deviceList_resource}',params=queryParameters,
                           headers=headers
                           ).json()
    deviceList=[]
    for device in response['response']:
        deviceList.append(device['id'])
    
    # Running a "show version" cli command (runRead_onlyCommandsOnDevicesToGetTheirReal_timeConfiguration)
    readOnly_resource='/dna/intent/api/v1/network-device-poller/cli/read-request'
    commands=['show version']
    payload={
            'commands': commands,
            'description': 'Getting show version',
            'deviceUuids': deviceList,
            'name':'getting show ver of two devices' ,
            "timeout": 6
            }
    response=requests.post(url=f'{base_url}{readOnly_resource}',
                           data=json.dumps(payload),
                           headers=headers).json()
    taskUrl=response['response']['url']
    # Using the task id, retrieve the file id associated with the response
    response=requests.get(url=f'{base_url}{taskUrl}',
                          headers=headers).json()
    fileId=json.loads(response['response']['progress'])['fileId']
    # Retrieve the file information with the cli result of the commands.
    file_resource=f'/dna/intent/api/v1/file/{fileId}'
    response=requests.get(url=f'{base_url}{file_resource}',
                           headers=headers).json()
    pprint(response)


    












if __name__ == '__main__':
    main()