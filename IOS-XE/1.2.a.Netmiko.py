from netmiko import ConnectHandler
import pandas as pd


def main():
    sandbox_router = {
        'device_type': 'cisco_ios',
        'host': '10.10.20.48',
        'username': 'developer',
        'password': 'C1sco12345',
        'port': 22
    }

    sandbox_connection = ConnectHandler(**sandbox_router)
    sandbox_ip = sandbox_connection.send_command('show ip interface brief', use_textfsm=True)
    sandbox_ip_df = pd.DataFrame(sandbox_ip)
    print(sandbox_ip_df)

    sandbox_connection.send_command(command_string='mkdir test',
                                    expect_string='Create directory filename [test]?',
                                    strip_prompt=False,
                                    strip_command=False)
    sandbox_connection.send_command(command_string='\n')

    dir_command = sandbox_connection.send_command('dir', use_textfsm=True)
    dir_command_df = pd.DataFrame(dir_command)
    print(dir_command_df)

    interface_loopback100 = ['interface loopback100',
                             'description Configured using netmiko',
                             'ip address 1.1.1.1 255.255.255.255']

    sandbox_connection.send_config_set(interface_loopback100)

    sandbox_connection.send_config_from_file('interface_loopback.txt')

    sandbox_ip = sandbox_connection.send_command('show ip interface brief', use_textfsm=True)
    sandbox_ip_df = pd.DataFrame(sandbox_ip)
    print(sandbox_ip_df)


if __name__ == '__main__':
    main()
