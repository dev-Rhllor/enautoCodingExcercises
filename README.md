# enautoCodingExcercises
Based in CBT Nuggets ENAUTO Course. This is my approach to solve the same tasks explained in the course.

## 1 IOS-XE
Using the IOS-XE always on Sandbox 
### 1.1 NETCONF
1.1.a Using Python and Scrapli module: 
 - Send a RPC **get** to collect ietf-interfaces operational state
 - Send a RPC **get-config** using subtree filtering to collect the interface description of the interface GigabitEthernet2.
 - Send a RPC **config**  to change interface description.
 - Send a RPC **get-config** using Xpath filtering to collect the interface description change.
 - Send a RPC **config**  to Rollback the interface description.

1.1.b Using Python and ncclient module: 
- Send a RPC **get-config** using subtree filtering to collect the interface description of the interface GigabitEthernet2.

1.1.c Using the CSR1000v always on Sandbox 
    Deploy a Netconf Telemetry Subscription. 
 

### 1.2 NETMIKO: 
1.2.a Using Python and NETMIKO: 
- Connect to a device, run "ip interface brief" and parse it using NTC-Templates and Pandas DataFrame 

1.2.b Using Ansible and NETMIKO and ntc-ansible
- Gather "show interface brief" using ansible ios_command module
- Gather interface information using "ios facts" module (structured data)
- Gather "show interface brief" using ntc-ansible module (structured data)

NOTE: ntc-ansible and ntc_show_command libraries have to be installed in the system.

### RESTCONF: 

Using the Sandbox IOSXE and Python Request. 
    Collect the capabilities of the device. 
    Collect statics routes using a Standard Yang Data Model 
    Collect interface operation using Native Yang Data Model: 
        Using Gigabit Ethernet 2.  
        Statistics 
    Using the standard Yang Data Model create a loopback interface. 

Using Ansible and RESTCONF: 
    Print the interfaces Standard Yang Data Model 
    Configure a loopback using Jinja Template 

DNA Center 

Using the DNAC Sandbox. 
    Get authenticated and retrieve: 
        Sites 
        Topologies 
        Device  
    Use the assurance API retrieve 
        Wired Client 
        Wireless Client 
    Create a Python program to print for Wired and Wireless the amount of clients in in the scores values. 
    Create a Python program to run a "show version" in at least two devices. 

SDWAN 

Using Cisco SANDBOX SDWAN
    Get Authenticated with the vManage API and conditional if authentication failed, response "login failed" and exit. If suceed print "loging succeed"  
    Getting Device Inventory an converted to a Dictionary 
    Query only vEdge devices 
    Get vEdge using the specific Api Call  
    Compare both outputs 2 vs 3 
    Getting Template Information for all devices. 
    Get templates Information with features 

Using Cisco Devnet reservable LAB 
    Create a user in the netadmin group. (using Admin API)  
    Change password. 
    Get a list of devices and validate the status of certificates. 
    Get a the root certificate. 
    Create a Template using the Template information.  
    Template type should be "aaa,  system-vedge, vpn-vsmart" 
    Mock the Push template to one device. (not actually push it).a  
    Get certificate status summary 
    Get alarms of the devices. 
    Get tunnel statistics for a specific device. 

MERAKI NETWORKING 

Using the always on DEVNET sandbox 
    Get a list of organizations and get Devnet Sanbox ID 
    Get list of networks in Devnet Sandbox Org and collect id of DNSMB3 
    Get a list of devices inside the DNSMB3 
    Choose an SSID and get a list of devices connected. 
    Create a new network inside the org. 
 

Meraki Camara: 
Using the always on DEVNET sandbox 
    Install a MQTT broker in UBUNTU. 
    Asociate a test camara to the MQTT Broker 
    Check real time feed: 
        Light 
        Raw_data 
    Using the REST API retrieve 
        Overview Analytics 
        Live Analytics 
        Recent Analytics 