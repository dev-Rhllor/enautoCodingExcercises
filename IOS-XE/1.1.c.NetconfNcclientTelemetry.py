from ncclient import manager
import xmltodict
from lxml.etree import fromstring

# logging.basicConfig(level=logging.DEBUG)

sandbox_router = {
    "host": "10.10.20.48",
    "port": "830",
    "username": "developer",
    "password": "C1sco12345",
}

# This generates a dynamic telemetry subscription, when the session is over,
# the subscription is erased from the device.
# Another approach is to configure the telemetry subscription in the device
# and then configure a collector using telegraf to receive the telemetry.

with manager.connect(**sandbox_router, hostkey_verify=False) as m:
    subs = ["/memory-ios-xe-oper:memory-statistics/memory-statistic"]
    for sub in subs:
        rpc = f"""
            <establish-subscription xmlns='urn:ietf:params:xml:ns:yang:ietf-event-notifications'
                                    xmlns:yp='urn:ietf:params:xml:ns:yang:ietf-yang-push'>
                <stream>yp:yang-push</stream>
                <yp:xpath-filter>{sub}</yp:xpath-filter>
                <yp:period>500</yp:period>
            </establish-subscription>
        """
        response = m.dispatch(fromstring(rpc))
        python_resp = xmltodict.parse(response.xml)
        # print(python_resp['rpc-reply']['subscription-result']['#text'])
        # print(python_resp['rpc-reply']['subscription-id']['#text'])

        while True:
            sub_data = m.take_notification()
            python_sub_data = xmltodict.parse(sub_data.notification_xml)
            print(
                f"Sub ID: {python_sub_data['notification']['push-update']['subscription-id']}")
            # print(python_sub_data)
            print(
                f"Name:\
                    {python_sub_data['notification']['push-update']['datastore-contents-xml']['memory-statistics']['memory-statistic'][0]['name']}")
            print(
                f"Total RAM:\
                    {python_sub_data['notification']['push-update']['datastore-contents-xml']['memory-statistics']['memory-statistic'][0]['total-memory']}")
            print(
                f"Used RAM:\
                    {python_sub_data['notification']['push-update']['datastore-contents-xml']['memory-statistics']['memory-statistic'][0]['used-memory']}")
            print(
                f"Free RAM:\
                     {python_sub_data['notification']['push-update']['datastore-contents-xml']['memory-statistics']['memory-statistic'][0]['free-memory']}")
