from typing import List, Optional, Tuple
from ipaddress import IPv4Address

from ntc_templates.parse import parse_output
from netaddr import EUI, mac_unix_expanded

from .base import BaseDevice, ARPTableEntry, MACTableEntry, Interface, LLDPNeighbor


def _remove_prompt(results: str) -> str:
    """
    remove the trailing prompt from the results of a live_status show
    command.  This only appears to be an issue for the IOS NED. i.e:

    ...
    Gi2/0/48        notconnect   1       auto   auto 10/100/1000BaseTX
    Twe2/1/1        connected    1       full    10G SFP-10GBase-SR
    Twe2/1/2        notconnect   1       auto   auto unknown
    Ap2/0/1         connected    1     a-full a-1000 App-hosting port
    al-shallow-1#    <-- (rude)
    """
    lines = results.splitlines()
    try:
        del lines[-1]
    except IndexError:
        pass
    return "\n".join(lines)


def _normalize_ifname(name: str) -> str:
    """
    Some IOS platforms return fully-qualified interface identifiers, e.g.
    'GigabitEthernet1/1' whereas others use abbreviated names e.g. 'Gi1\1'.
    Since the NCS switchport services uses abbreviated versions for IOS,
    this function will convert the names returned by the device to the
    shortened version
    """
    if name.startswith("FastEthernet"):
        newname = "Fa" + name.split("FastEthernet")[1]
    elif name.startswith("GigabitEthernet"):
        newname = "Gi" + name.split("GigabitEthernet")[1]
    elif name.startswith("TenGigabitEthernet"):
        newname = "Te" + name.split("TenGigabitEthernet")[1]
    elif name.startswith("TwoGigabitEthernet"):
        newname = "Twe" + name.split("TwoGigabitEthernet")[1]
    else:
        return name

    return newname


def parse_speed_duplex(oper_speed: str, oper_duplex: str) -> Tuple[str, str]:
    """
    parse the raw speed/duplex results and return the expected value so we can
    create an Interface.

    duplex: "Full-duplex" --> "full"
    speed: "1000 Mb/s" --> "1000"
    """
    if oper_speed == "Auto-speed":
        speed = "auto"
    elif oper_speed == "1000 Mb/s":
        speed = "1000"
    elif oper_speed == "100 Mb/s":
        speed = "100"
    elif oper_speed == "10 Mb/s":
        speed = "10"
    else:
        speed = "auto"

    if oper_duplex == "Half-duplex":
        duplex = "half"
    elif oper_duplex == "Full-duplex":
        duplex = "full"
    else:
        duplex = "auto"

    return speed, duplex


class IOS(BaseDevice):
    def _run_cmd(self, command: str) -> str:
        """
        use NCS live-status exec to issue a raw show command towards a device.
        platform-specific models are expected to parse this output and return
        structured data.

        :param command: string CLI command, e.g. 'show interface status'
        :returns: raw string output from the device
        """
        show = self.device.live_status.__getitem__("exec").show
        inp = show.get_input()
        inp.args = [command]

        results = show.request(inp)

        return _remove_prompt(results.result)

    def get_interface_details(self, interface: Optional[str] = None) -> List[Interface]:
        """
        Gathers interface operational data from an IOS device by parsing 'show interfaces'

        :interface: optionally get data only for a single interface

        see the ntc_templates test data for this template for details on output structure:
        https://github.com/networktocode/ntc-templates/tree/master/tests/cisco_ios/show_interfaces

        ---
        parsed_sample:
        - interface: "FastEthernet1"
          link_status: "down"
          protocol_status: "down"
          hardware_type: "RP management port"
          address: "6c41.6aba.b47f"
          bia: "6c41.6aba.b47f"
          description: ""
          ...
        """
        # ncs automatically adds the 'show' to the front of the cmd
        command = f"interfaces {interface}" if interface else "interfaces"
        self.log.debug(f"sending 'show {command}' to {self.device.name}")
        reply = self._run_cmd(command)
        # self.log.debug(f" <<<{ self.device.name }>>>: {reply.result}")

        parsed = parse_output(
            platform="cisco_ios",
            command="show interfaces",
            data=reply,
        )

        ret = []
        for entry in parsed:
            speed, duplex = parse_speed_duplex(entry["speed"], entry["duplex"])
            input_errors = (
                0 if entry["input_errors"] == "" else int(entry["input_errors"])
            )
            output_errors = (
                0 if entry["output_errors"] == "" else int(entry["output_errors"])
            )
            record = Interface(
                name=_normalize_ifname(entry["interface"]),
                description=entry["description"],
                admin_status="disabled"
                if "administratively down" in entry["link_status"]
                else "enabled",
                oper_status="up" if "up" in entry["protocol_status"] else "down",
                duplex=duplex,
                speed=speed,
                input_errors=input_errors,
                output_errors=output_errors,
            )

            if record.name.startswith("Vlan"):
                record.is_logical = True

            ret.append(record)

        return ret

    def get_arp_table(
        self, address: Optional[str] = None, vrf: Optional[str] = None
    ) -> List[ARPTableEntry]:
        """
        Gathers ARP data from an IOS device by parsing the output of the CLI
        command 'show ip arp [ address | vrf <VRF>]'

        :address: optionally filter device output by MAC or IP address
        :vrf: optional string name of VRF table to look in

        see the ntc_templates test data for this template for details on output structure:
        https://github.com/networktocode/ntc-templates/tree/master/tests/cisco_ios/show_ip_arp

        TODO: add support(recursion?) for vrf='all' since ios makes you run a separate
              lookup command for every vrf (so rude)

        ---
        parsed_sample:
          - protocol: "Internet"
            address: "172.16.233.229"
            age: "-"
            mac: "0000.0c59.f892"
            type: "ARPA"
            interface: "Ethernet0/0"
        """
        # ncs automatically adds the 'show' to the front of the cmd
        command = "ip arp"
        if vrf is not None:
            command = command + f" vrf {vrf}"
        if address is not None:
            command = command + f" address {address}"
            normalized_address = IPv4Address(address)

        self.log.debug(f"sending 'show {command}' to {self.device.name}")
        reply = self._run_cmd(command)
        # self.log.debug(f" <<<{ self.device.name }>>>: {reply.result}")

        parsed = parse_output(
            platform="cisco_ios",
            command="show ip arp",
            data=reply,
        )

        ret = []
        for entry in parsed:
            if entry["mac"] == "Incomplete":
                continue

            normalized_entry_address = IPv4Address(entry["address"])

            if address is None or normalized_address == normalized_entry_address:
                record = ARPTableEntry(
                    ip_address=IPv4Address(entry["address"]),
                    mac_address=EUI(entry["mac"], dialect=mac_unix_expanded),
                    interface=entry["interface"],
                    vrf=vrf,
                )
                ret.append(arp)

        return ret

    def get_mac_table(self, mac: Optional[str] = None) -> List[MACTableEntry]:
        """
        Gathers dynamically-learned MAC address data from an IOS device by
        parsing the output of the CLI command 'show mac address-table dynamic
        [address <address>]'

        :mac: optionally filter device output by MAC address

        see the ntc_templates test data for this template for details on output structure:
        https://github.com/networktocode/ntc-templates/tree/master/tests/cisco_ios/show_mac-address-table

        ---
        parsed_sample:
        - destination_address: "30a3.30a3.a1c3"
            type: "dynamic"
            vlan: "666"
            destination_port:
            - "Te1/30"
        """
        # ncs automatically adds the 'show' to the front of the cmd
        command = "mac address-table dynamic"
        if mac is not None:
            normalized_mac = EUI(mac, dialect=mac_unix_expanded)
            command = command + f" address {mac}"

        self.log.debug(f"sending 'show {command}' to {self.device.name}")
        reply = self._run_cmd(command)
        # self.log.debug(f" <<<{ self.device.name }>>>: {reply.result}")

        parsed = parse_output(
            platform="cisco_ios",
            command="show mac-address-table",
            data=reply,
        )

        ret = []
        for entry in parsed:
            try:
                vid = int(entry["vlan"])
            except ValueError:
                vid = None

            normalized_entry_mac = EUI(
                entry["destination_address"], dialect=mac_unix_expanded
            )
            # unless there's an on-going broadcast storm we should only be
            # learning an address on a single port -- not sure why the template
            # is modelled this way?
            interface = _normalize_ifname(entry["destination_port"][0])

            if mac is None or normalized_mac == normalized_entry_mac:
                record = MACTableEntry(
                    address=normalized_entry_mac,
                    vlan_id=vid,
                    interface=interface,
                )
                ret.append(record)

        return ret

    def get_lldp_neighbors(self, interface: Optional[str] = None) -> List[LLDPNeighbor]:
        """
        Gathers active LLDP neighbors from an IOS device by
        parsing the output of the CLI command 'show lldp neighbors detail'

        :interface: optionally filter device output by interface

        see the ntc_templates test data for this template for details on output structure:
        https://github.com/networktocode/ntc-templates/blob/master/tests/cisco_ios/show_lldp_neighbors_detail/cisco_ios_show_lldp_neighbors_detail1.yml

        ---
        parsed_sample:
        - local_interface: "Gi1/0/2"
          chassis_id: "7c25.86c9.aaaa"
          neighbor_port_id: "502"
          neighbor_interface: "ge-0/0/0.0"
          neighbor: ""
          system_description: "Juniper Networks, Inc. ex2200-24t-4g , version 12.3R9.4 Build\
          \ date: 2015-02-12 11:25:30 UTC"
          capabilities: "B,R"
          management_ip: ""
          vlan: "1"
          serial: ""
          power_pair: ""
          power_class: ""
          power_device_type: ""
          power_priority: ""
          power_source: ""
          power_requested: ""
        """
        # ncs automatically adds the 'show' to the front of the cmd
        command = "lldp neighbors"

        self.log.debug(f"sending 'show {command}' to {self.device.name}")
        reply = self._run_cmd(command)
        # self.log.debug(f" <<<{ self.device.name }>>>: {reply.result}")

        parsed = parse_output(
            platform="cisco_ios",
            command="show lldp neighbors",
            data=reply,
        )

        ret = []
        for entry in parsed:
            record = LLDPNeighbor(
                local_interface=entry["local_interface"],
                remote_interface=entry["neighbor_interface"],
                remote_system_name=entry["neighbor"],
            )
            if interface is None or entry["local_interface"] == interface:
                ret.append(record)

        return ret
