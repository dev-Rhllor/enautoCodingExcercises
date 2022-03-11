############ IOSXE Requires a default Namespace in the Config tag ################


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

# This following filter is tricky, if the filter xmlns is not set propperly it returns all namespaces in the module.
netconf_ietf_interfaces_xpath = """
<get-config>
  <source>
    <running/>
  </source>
  <filter xmlns:xyz='urn:ietf:params:xml:ns:yang:ietf-interfaces'
                type='xpath'
                select='/xyz:interfaces/interface[name="GigabitEthernet2"]'/>
</get-config>
"""

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
