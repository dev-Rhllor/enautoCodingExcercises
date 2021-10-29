from netmiko import ConnectHandler
import pandas as pd


def main():
    sandbox_router = {
        'device_type': 'cisco_ios',
        'host': 'sandbox-iosxe-recomm-1.cisco.com',
        'username': 'developer',
        'password': 'C1sco12345',
        'port': 22
    }

    sandbox_connection = ConnectHandler(**sandbox_router)
    sandbox_ip = sandbox_connection.send_command("show ip interface brief", use_textfsm=True)
    sandbox_ip_df = pd.DataFrame(sandbox_ip)
    print(sandbox_ip_df)


if __name__ == '__main__':
    main()
