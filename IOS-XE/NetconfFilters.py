netconf_ietf_interfaces = """
  <interfaces xmlns='urn:ietf:params:xml:ns:yang:ietf-interfaces'>
        <interface>
            <name>GigabitEthernet2</name>
        </interface>
  </interfaces>
"""

netconf_ietf_interfaces_status = """
  <interfaces-state xmlns='urn:ietf:params:xml:ns:yang:ietf-interfaces'>
    <interface>
      <name>GigabitEthernet2</name>
    </interface>
  </interfaces-state>
"""

# IOSXE Requires a default Namespace in the Config tag #
netconf_ietf_interfaces_config = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns='urn:ietf:params:xml:ns:yang:ietf-interfaces'>
    <interface>
      <name>{name}</name>
      <description>{description}</description>
      <enabled>true</enabled>
    </interface>
  </interfaces>
</config>
"""

netconf_native_memory_statistics = """
  <memory-statistics xmlns='http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper'>
  </memory-statistics>
"""
