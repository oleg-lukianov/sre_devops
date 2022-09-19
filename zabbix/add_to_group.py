"""Script for add host in group controller"""
import os
from zabbix_api import *

class AddToGroup:
    """Main class"""
    zabbix_api = ZabbixAPI()
    auth = zabbix_api.zabbix_user_login()
    zabbix_hostid_remove = {}

    def add_to_group(self):
        """Add in group"""
        # path = "/Users/iuad15au/ONE_OLD/git/cim/python"
        path = "/etc/zabbix/scripts"
        dc_files = {
            "ASR-WAN-DNV": "10.187.95.253",
            "ASR-WAN-L9": "10.187.95.254",
            "HO-WAN-DNV": "10.187.95.243",
            "HO-WAN-L9": "10.187.95.244"
        }

        for dc_item in dc_files:
            path_full = path + "/" + dc_files[dc_item]
            # print(f'file = {path_full}')
            if os.path.exists(path_full):
                self.check_hostgroup_to_dc(dc_item)
                self.parse_dc_file(path_full, dc_item)
            else:
                print(f'Not exists file: {path_full}')
                continue

    def parse_dc_file(self, path, dc_item):
        """Parse files with IPs"""
        zabbix_hostgroups = self.zabbix_api.zabbix_hostgroup_get(self.auth)
        zabbix_interfaces = self.zabbix_api.zabbix_hosts_get_interfaces(self.auth)
        # print(zabbix_interfaces.values())
        try:
            zabbix_hostgroupid = zabbix_hostgroups[dc_item]
            # print(f'zabbix_hostgroup={dc_item} zabbix_hostgroupid={zabbix_hostgroupid}')
        except KeyError:
            pass

        dc_files = open(path, "r")
        for line in dc_files.readlines():
            try:
                host_ip = line.split()[0].strip()
            except IndexError:
                continue

            if host_ip:
                if host_ip in zabbix_interfaces.keys():
                    try:
                        zabbix_hostid = zabbix_interfaces[host_ip]
                    except KeyError:
                        pass
                    print(f'Add host_ip={host_ip} hostid={zabbix_hostid} to '
                          f'zabbix_hostgroup={dc_item} (id={zabbix_hostgroupid})')
                    self.zabbix_hostid_remove[zabbix_hostid] = zabbix_hostgroupid
                    self.zabbix_api.zabbix_hostgroup_massadd(
                        self.auth, zabbix_hostid, zabbix_hostgroupid
                        )
        dc_files.close()

    def check_hostgroup_to_dc(self, hostgroup):
        """Get data from Zabbix"""
        zabbix_hostgroups = self.zabbix_api.zabbix_hostgroup_get(self.auth)
        if not hostgroup in zabbix_hostgroups:
            self.zabbix_api.zabbix_hostgroup_create(self.auth, hostgroup)

    # def remove_from_group(self):
    #     hostgroup_get_one = self.zabbix_api.zabbix_hostgroup_get_one(self.auth, zabbix_hostgroupid)
    #     for x in self.zabbix_hostid_remove:
    #         print(x, self.zabbix_hostid_remove[x])

    def main(self):
        """Main function"""
        #self.add_to_group()
        #self.check_hostgroup_to_dc("HO-WAN-L9")
        self.zabbix_api.zabbix_host_create_simple(self.auth, "CN-ICH-S0970744", "127.0.0.1", 10050, 5, 10186, "ci_name", "ci_key",
                            "ci_address", "ci_admin", "ci_owner", "ci_order_number", "ci_main_backup", "ci_searchcode")
        # self.remove_from_group()
        self.zabbix_api.zabbix_user_logout(self.auth)


if __name__ == "__main__":
    add_to_group = AddToGroup()
    try:
        add_to_group.main()
    except KeyboardInterrupt:
        print('\nExit. User press Ctrl+C (KeyboardInterrupt)')
