from netmiko import ConnectHandler
import pandas as pd

def main():
    sandboxRouter= {
        'device_type': 'cisco_ios',
        'host':   'sandbox-iosxe-recomm-1.cisco.com',
        'username': 'developer',
        'password': 'C1sco12345',
        'port' : 22
    }

    sandboxConnection = ConnectHandler(**sandboxRouter)
    sandboxIP = sandboxConnection.send_command("show ip interface brief",use_textfsm=True)
    sandboxIPdf=pd.DataFrame(sandboxIP)
    print(sandboxIPdf)

if __name__ == '__main__':
    main()