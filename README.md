# ENAUTO 300-435 Coding Excersices 
Based in CBT Nuggets ENAUTO Course. This is my approach to solve the same tasks explained in the course.

This is not meant to be a code to be used in production environment, this is just code to understand the concepts of the exam rather than creating a library for future use. 

For production environments I strongly recommend to enter the official repo of [Cisco DevNet](https://github.com/CiscoDevNet) and look for a tested SDK. 


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

1.1.c Using Python and ncclient module: 
 - Deploy a Netconf Dynamic Telemetry Subscription. 
  

### 1.2 NETMIKO: 
1.2.a Using Python and NETMIKO: 
- send a read only command using **send_command()** feature of NETMIKO and parse it using NTC-Templates and Pandas DataFrame. 
- Send a write command using **send_command()** feature of NETMIKO.
- Configure a loopback interface using **send_config_set**.
- Configure a loopback interface using **send_config_from_file()**

1.2.b Using Ansible and NETMIKO and ntc-ansible
- Gather "show interface brief" using ansible **ios_command** module
- Gather interface information using **ios facts** module (structured data)
- Gather "show interface brief" using **ntc-ansible** module (structured data)

NOTE: ntc-ansible and ntc_show_command libraries have to be installed in the system.

### 1.3 RESTCONF: 

1.3.a Using Python and the Request.
 - Send a **get** request to retrieve capabilities of the device. 
 - Send a **get** request to retrieve statics routes configuration using Native and Standard Yang Data Model 
 - Send a **get** request to retrieve interface operation using Native Yang Data Model and using a name as filter. 
 - Send a **post** request to create a loopback interface using using the Standard Yang Data Model.
 - Send a **delete** request to remove the loopback interface. 

1.3.b Using Ansible and RESTCONF: 
 - Print the interfaces Standard Yang Data Model 
 - Send a **patch** request to create a loopback interface using Jinja Template 

## 2 DNA Center 
Using the DNAC Sandbox. 

2.1 Using Python and request library:
 - Send a **get** request and retrieve the **sites list** and print their names. 
 - Send a **get** request and retrieve the **physical topology** and print it.
 - Send a **get** request and retrieve the **Device List**. Filter the list using *parameters*.
 - Use the assurance API and send a **get** request to retrieve the **client-helath**
   - Going thruogh the dictionatary print the *health score* of the devices ordered by type. 
 - Send a **get** to collect two *devices Id* and using the Command Runner API:
   - Send a **post** to generate a task of running a "show version" in the devices list.
   - Send a **get** to retrieve the *fileId* of the task.
   - Send a **get** to retrieve the *file* and print it.  

## 3 SDWAN 
Using Cisco SDWAN 19.2 Sandbox.

3.1 Create an Authethication function that:
 - send a **post** with the *user* and *password* to retrieve the *jsession cookie* 
 - send a **post** with the *jsession cookie* and retrieve the *X-XSRF-TOKEN*
 - return a formated header with both parameters to be used in futures API-Calls

3.2 Create a python program that authenthicate to the vManage and:
 - send a **get** to retrieve the device inventory. Convert it to a Panda Dataframe frame for better visualizatin. 
 - send a **get** to retrieve the device monitor. 
 - send a **get** to retrieve the vEdge Inventory.  
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