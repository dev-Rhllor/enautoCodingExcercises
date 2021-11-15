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


if __name__ == '__main__':
    main()
