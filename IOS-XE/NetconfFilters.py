netconf_ietf_interfaces = """
<filter>
    <interfaces xmlns='urn:ietf:params:xml:ns:yang:ietf-interfaces'>
        <interface>
            <name>GigabitEthernet2</name>
        </interface>
    </interfaces>
</filter>
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
<config>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
  <interface>
    <name>{name}</name>
    <description>{description}</description>
    <enabled>true</enabled>
  </interface>
  </interfaces>
</config>
"""
netconf_ietf_interfaces_status = """
 <filter>
  <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name>GigabitEthernet2</name>
    </interface>
  </interfaces-state>
</filter>
"""
