from sdwanAuth import authentication
import requests
import urllib3
import pandas as pd
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():

    sandbox_vmanage = {
        'vmanage_host': '10.10.20.90',
        'vmanage_port': 443,
        'username': 'admin',
        'password': 'C1sco12345'}

    headers = authentication(**sandbox_vmanage)
    base_url = f'https://{sandbox_vmanage["vmanage_host"]}:{sandbox_vmanage["vmanage_port"]}'

    # Retrieve the device inventory
    device_resource = '/dataservice/device'
    response = requests.get(url=f'{base_url}{device_resource}',
                            headers=headers,
                            verify=False)
    response_dict = json.loads(response.text)
    device_inventory = response_dict['data']
    device_inventory_df = pd.DataFrame(device_inventory)
    print(device_inventory_df)

    # Retrieve the device monitor
    device_resource = '/dataservice/device/monitor'
    response = requests.get(url=f'{base_url}{device_resource}',
                            headers=headers,
                            verify=False)
    response_dict = json.loads(response.text)
    device_monitor = response_dict['data']
    device_monitor_df = pd.DataFrame(device_monitor)
    print(device_monitor_df)

    # Retrieve the device vEdge devices inventory.
    device_resource = '/dataservice/device/vedgeinventory/detail'
    response = requests.get(url=f'{base_url}{device_resource}',
                            headers=headers,
                            verify=False)
    response_dict = json.loads(response.text)
    device_vedge_inventory = response_dict['data']
    device_vedge_inventory_df = pd.DataFrame(device_vedge_inventory)
    print(device_vedge_inventory_df)

    # Retrieve statistics of first device
    # This can be done filtering the dict with "for" and "if" but I rather go with pandas just for fun.
    first_device = device_inventory_df['deviceId'][device_inventory_df["device-type"] == "vedge"].head(1).values[0]
    device_resource = f'/dataservice/device/app-route/statistics?deviceId={first_device}&local-color=mpls&remote-color=public-internet'
    response = requests.get(url=f'{base_url}{device_resource}',
                            headers=headers,
                            verify=False)
    response_dict = json.loads(response.text)
    device_statistic = response_dict['data']
    device_statistic_df = pd.DataFrame(device_statistic)
    print(device_statistic_df)

    # Retrieve list of templates of all devices
    device_resource = '/dataservice/template/feature'
    response = requests.get(url=f'{base_url}{device_resource}',
                            headers=headers,
                            verify=False)
    response_dict = json.loads(response.text)
    template_dict = response_dict['data']
    template_df = pd.DataFrame(template_dict)
    print(template_df)

    # List all admin users
    device_resource = '/dataservice/admin/user'
    response = requests.get(url=f'{base_url}{device_resource}',
                            headers=headers,
                            verify=False)
    response_dict = json.loads(response.text)
    users_dict = response_dict['data']
    users_df = pd.DataFrame(users_dict)
    print(users_df)

    # Create an Admin in the NetAdmin Group
    device_resource = '/dataservice/admin/user'
    payload = {'group': ['netadmin'],
               'description': 'User Created With API',
               'userName': 'demouser',
               'password': 'password',
               'locale': 'en_US',
               'resGroupName': 'global'}
    response = requests.post(url=f'{base_url}{device_resource}',
                             headers=headers,
                             data=json.dumps(payload),
                             verify=False)
    if response.status_code == 200:
        print(f'User {payload["userName"]} created')
    else:
        print(f'User {payload["userName"]} NOT created with code {response.status_code}')

    # List the users again
    device_resource = '/dataservice/admin/user'
    response = requests.get(url=f'{base_url}{device_resource}',
                            headers=headers,
                            verify=False)
    response_dict = json.loads(response.text)
    users_dict = response_dict['data']
    users_df = pd.DataFrame(users_dict)
    print(users_df)

    # Change the password of the Admin created
    device_resource = '/dataservice/admin/user/password/demouser'
    payload = {'userName': 'demouser',
               'password': 'demopassword'}
    response = requests.put(url=f'{base_url}{device_resource}',
                            headers=headers,
                            data=json.dumps(payload),
                            verify=False)
    if response.status_code == 200:
        print(f'User password {payload["userName"]} changed')
    else:
        print(f'User password {payload["userName"]} NOT changed with code {response.status_code}')


if __name__ == '__main__':
    main()
