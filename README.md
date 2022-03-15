# ENAUTO 300-435 Coding Excersices 
Based on CBT Nuggets ENAUTO Course. These are my approach to solving the several tasks explained in the course. The ones left are due to the lack of resources to simulate them.

The goal of this repo is to understand the exam concepts rather than create a library for future use. 

For production environments please refer to [Cisco DevNet](https://github.com/CiscoDevNet) and look for a tested SDKs.

## Requirements 

Mosts of the requirements can be installed using:
```
pip install requirement.txt
``` 
For **ansible** follow the [official documentation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#)

For **ntc-ansible** follow the [official repo](https://github.com/networktocode/ntc-ansible) for instructions. 


## 1 IOS-XE
Using the IOS-XE always on Sandbox 
### 1.1 NETCONF
With Python, Scrapli (1.1.a) and Nclient (1.1.b) module:
- Using subtree filters:
   - Send a **get-config** RPC to retrieve the interface config using the ieft module. 
   - Send a **get** RPC to collect ietf-interfaces operational state
   - Send a **get** RPC to retrieve oper-status of a Native module.
 - Using XPATH filters:
   - Send a **get-config** to retrieve the interfaces configuration returning all namespaces that match with the filter.
   - Send a **get**  RPC to retrieve oper-status of an interface and filter only the OpenConfig namespace.
 - Send a **config** RPC to change the description sending the GigabitEthernet2 using a template.
 - Send a **custom craft** RPC to save the configuration of the device.

1.1.c Using Python and ncclient module: 
 - Deploy a Netconf Dynamic Telemetry Subscription. 
  

### 1.2 NETMIKO: 
1.2.a Using Python and NETMIKO: 
- send a read only command using **send_command()** feature of NETMIKO and parse it using NTC-Templates and Pandas DataFrame. 
- Send a write command using **send_command()** feature of NETMIKO.
- Configure a loopback interface using **send_config_set**.
- Configure a loopback interface using **send_config_from_file()**.

1.2.b Using Ansible Network Collection for Cisco IOS devices and ntc-ansible
- Gather "show interface brief" using ansible **ios_command** module of the Ansible Network Collection for Cisco IOS devices.
- Gather interface information using **ios facts** module of the Ansible Network Collection for Cisco IOS devices (structured data).
- Gather "show interface brief" using **ntc-ansible** module (structured data).

NOTE: The ntc-ansible module has to be installed in the system. 

### 1.3 RESTCONF: 

1.3.a Using Python and the Request module.
 - Send a **get** request to retrieve capabilities of the device. 
 - Send a **get** request to retrieve statics routes configuration using Native and Standard Yang Data Model 
 - Send a **get** request to retrieve interface operation using Native Yang Data Model and using a name as filter. 
 - Send a **post** request to create a loopback interface using using the Standard Yang Data Model.
 - send a **put** request to replace the loopback interface using the Standard Yang Data Model.
 - send a **patch** request to update the loopback interface using the Standard Yang Data Model.
 - Send a **delete** request to remove the loopback interface. 

1.3.b Using Ansible and RESTCONF: 
 - Print the interfaces Standard Yang Data Model 
 - Send a **patch** request to create a loopback interface using Jinja Template 

## 2 DNA Center 
Using the DNAC Sandbox. 

2.1 Using Python and request library:
 - Send a **get** request and retrieve the **sites list** and print their names and IDs. 
 - Send a **get** request and retrieve the **physical topology** and print it.
 - Send a **get** request and retrieve the **Device List**. Filter the list using *parameters*.
 - Send a **get** request and retrieve the **Device Detail** from one of the devices.
 - Use the assurance API and send a **get** request to retrieve the **client-helath**
   - Going thruogh the dictionatary print the *health score* of the devices ordered by type. 
 - Send a **get** to collect two *devices Id* and using the Command Runner API:
   - Send a **post** to generate a task of running a "show version" in the devices list.
   - Send a **get** to retrieve the *fileId* of the task.
   - Send a **get** to retrieve the *file* and print it.  

## 3 SDWAN 
Using Cisco SDWAN 19.2.2 Sandbox.

3.1 Create an Authenthication function that:
 - send a **post** with the *user* and *password* to retrieve the *jsession cookie* 
 - send a **post** with the *jsession cookie* and retrieve the *X-XSRF-TOKEN*
 - return a formated header with both parameters to be used in futures API-Calls

3.2 Create a python program that authenthicate to the vManage and:
 - send a **get** to retrieve the device inventory. Convert it to a Panda Dataframe frame for better visualization.
 - send a **get** to retrieve the device monitor.  
 - send a **get** to retrieve the vEdge Inventory.
 - send a **get** to retrieve statistics and filter by the first device and *mpls* as local-color and *public-internet* as remote-color.
 - send a **get** to template information for all devices.
 - send a **post** to create a user in the netadmin group. (using Admin API)
 - send a **put** to modify a user password.
 - send a **delete** to remove the newly created user.
 - send a **get** to retrieve the alarms of the devices.
 - send a **get** to retrieve certificate summary of all devices.
 - send a **get** to retrieve the root certificate.

## 4 MERAKI NETWORKING 
Using the always on DEVNET sandbox 
    
- send a **get** to retrieve the list of organizations and collect the *Devnet Sandbox* organization *id*.
- send a **get** to retrieve the list of networks in *Devnet Sandbox* organization and collect *id* of *DevNet Sandbox ALWAYS ON* network.
- send a **get** to list of devives in *DevNet Sandbox ALWAYS ON* network and collect the *serial number* of a wireless device.
- send a **get** to retrieve the wireless radio setting of a wireless device.
- send a **get** to retrieve the *SSID* of the *DevNet Sandbox ALWAYS ON*'* network.
- send a **get** to retrieve wireless clients attached to the any device in the *DevNet SandBox ALWAYS ON*.

