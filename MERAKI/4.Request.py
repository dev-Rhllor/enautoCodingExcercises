import requests
import urllib3
import json
import pandas as pd
from pprint import pprint
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():

    headers = {
        'X-Cisco-Meraki-API-Key': '6bec40cf957de430a6f1f2baa056b99a4fac9ea0',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    base_url = 'https://api.meraki.com/api/v1'

    # Retrieve the device inventory and creating a Panda DF for better visualization.
    device_resource = '/organizations'
    response = requests.get(url=f'{base_url}{device_resource}',
                            headers=headers,
                            verify=False)
    response_dict = json.loads(response.text)
    organization_df = pd.DataFrame(response_dict)
    print(organization_df)

    # Collect the DevNet SandBox ID
    # This can be done filtering the dict the with "for" and "if" as follows, but I rather go with pandas just for fun.
    # for organization in response_dict:
    #    if organization['name'] == 'DevNet SandBox':
    #        DevNet_SandBox_id = organization['id']
    DevNet_SandBox_org_id = organization_df['id'][organization_df['name'] == 'DevNet Sandbox'].values[0]
    print(DevNet_SandBox_org_id)

    # Getting networks of 'DevNet SandBox' organization.
    device_resource = f'/organizations/{DevNet_SandBox_org_id}/networks'
    response = requests.get(url=f'{base_url}{device_resource}',
                            headers=headers,
                            verify=False)
    response_dict = json.loads(response.text)
    SandBox_networks = pd.DataFrame(response_dict)
    print(SandBox_networks)

    # Collect the 'DevNet SandBox ALWAYS ON' network id
    DevNet_SandBox_net_id = SandBox_networks['id'][SandBox_networks['name'] == 'DevNet Sandbox ALWAYS ON'].values[0]
    print(DevNet_SandBox_net_id)

    # Get network devices
    device_resource = f'/networks/{DevNet_SandBox_net_id}/devices'
    response = requests.get(url=f'{base_url}{device_resource}',
                            headers=headers,
                            verify=False)
    response_dict = json.loads(response.text)
    SandBox_networks_devices = pd.DataFrame(response_dict)
    print(SandBox_networks_devices)

    # Collect the serial of a wireless device
    DevNet_wireless_serial = SandBox_networks_devices['serial'][SandBox_networks_devices.model.str.startswith("MR")].head(1).values[0]
    print(DevNet_wireless_serial)

    # Collect wireless radio settings of a device.
    device_resource = f'/devices/{DevNet_wireless_serial}/wireless/radio/settings'
    response = requests.get(url=f'{base_url}{device_resource}',
                            headers=headers,
                            verify=False)
    response_dict = json.loads(response.text)
    pprint(response_dict)

    # Get SSID of 'DevNet SandBox ALWAYS ON' network.
    device_resource = f'/networks/{DevNet_SandBox_net_id}/wireless/ssids'
    response = requests.get(url=f'{base_url}{device_resource}',
                            headers=headers,
                            verify=False)
    response_dict = json.loads(response.text)
    network_ssid = pd.DataFrame(response_dict)
    print(network_ssid)

    # Get wireles clients attached to the any device in the 'DevNet SandBox ALWAYS ON"
    dates = {
        't0': round(time.mktime(time.strptime('Nov 20, 2021 @ 00:00:00', '%b %d, %Y @ %H:%M:%S'))),
        't1': round(time.mktime(time.strptime('Nov 21, 2021 @ 00:00:00', '%b %d, %Y @ %H:%M:%S')))
    }

    device_resource = f'/networks/{DevNet_SandBox_net_id}/wireless/clients/connectionStats'
    response = requests.get(url=f'{base_url}{device_resource}',
                            headers=headers,
                            params=dates,
                            verify=False)
    response_dict = json.loads(response.text)
    wireless_clients = pd.DataFrame(response_dict)
    print(wireless_clients)


if __name__ == '__main__':
    main()
