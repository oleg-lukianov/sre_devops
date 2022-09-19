"""Class connect to Zabbix REST API"""
import json
from typing import cast
import types
import inspect
import logging
import configparser
import os
import requests

__version__ = '0.1'
__author__ = 'Oleg Lukianov'

FILE_CONFIG = "config.ini"
config = configparser.ConfigParser()
config.read(FILE_CONFIG)

try:
    URL = config['zabbix.web']['url']
    ZABBIX_API_USER = config['zabbix.web']['zabbix_api_user']
    ZABBIX_API_PASSWORD = config['zabbix.web']['zabbix_api_password']
except KeyError:
    print(f'Need create config file "{FILE_CONFIG}"')
    os._exit(1)

class LoggingLocal:
    """Class using only to log"""

    @staticmethod
    def output(code, func_name, response):
        """Function using write in log"""
        logging.info('Code=%d---%s---%s', code, func_name, response)


class ZabbixAPI:
    """Class for integration with Zabbix REST API"""
    logging_local = LoggingLocal()

    def zabbix_user_login(self):
        """Function login"""
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": ZABBIX_API_USER,
                "password": ZABBIX_API_PASSWORD
            },
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        self.logging_local.output(
            str(response.status_code),
            this_function_name,
            str(response.json())
            )
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

        try:
            result = response.json()['result']
        except KeyError:
            result = "None"

        return result

    def zabbix_user_logout(self, auth):
        """Function logout"""
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "user.logout",
            "params": [],
            "id": 1,
            "auth": auth
        }
        response = requests.post(URL, json=data, verify=False)
        self.logging_local.output(
            str(response.status_code),
            this_function_name,
            str(response.json())
            )
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

    def zabbix_trigger_update(self, auth, triggerid, status):
        """Function update triiger"""
        this_function_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "trigger.update",
            "params": [{
                "triggerid": triggerid,
                "status": status
            }],
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        self.logging_local.output(
            str(response.status_code),
            this_function_name,
            str(response.json())
            )
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

    def zabbix_host_create(self, auth, name, host_ip, port, groupids, templateids, ci_name, ci_key,
                            ci_address, ci_admin, ci_owner, ci_order_number, ci_main_backup, ci_searchcode):
        """Function create host"""
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        logging.warning('Run function=%s (name=%s ip=%s ci_name=%s ci_key=%s groupids=%s templateids=%s)',
                        this_function_name, name, host_ip, ci_name, ci_key, groupids, templateids)
        ci_name = ci_name[:63]
        data = {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": name,
                "interfaces": [{
                    "type": 2,
                    "main": 1,
                    "useip": 1,
                    "ip": host_ip,
                    "dns": ci_key,
                    "port": port,
                    "details": {
                        "version": 3,
                        "bulk": 1,
                        "securityname": "{$SNMPV3_LOGIN}",
                        "contextname": "",
                        "securitylevel": 2,
                        "authpassphrase": "{$SNMPV3_AUTH_PASSPHRASE}",
                        "privpassphrase": "{$SNMPV3_PRIV_PASSPHRASE}",
                        "authprotocol": 1,
                        "privprotocol": 0
                    }
                }],
                "groups": [{
                    "groupid": groupids
                }],
                # "templates": [{
                #     "templateid": templateids
                # }],
                "inventory_mode": 0,
                "inventory": {
                    "name": ci_searchcode,
                    "alias": ci_key,
                    "type_full": ci_name,
                    "location": ci_address,
                    "poc_1_name": ci_admin,
                    "poc_2_name": ci_owner,
                    "tag": ci_order_number,
                    "notes": ci_main_backup
                }
            },
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        self.logging_local.output(
            str(response.status_code),
            this_function_name,
            str(response.json())
            )
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

    def zabbix_host_create_simple(self, auth, name, host_ip, port, groupids, templateids, ci_name, ci_key,
                            ci_address, ci_admin, ci_owner, ci_order_number, ci_main_backup, ci_searchcode):
        """Function create host simple"""
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        logging.warning('Run function=%s (name=%s ip=%s ci_name=%s ci_key=%s groupids=%s templateids=%s)',
                        this_function_name, name, host_ip, ci_name, ci_key, groupids, templateids)
        ci_name = ci_name[:63]
        data = {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": name,
                "interfaces": [{
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": host_ip,
                    "dns": ci_key,
                    "port": port,
                }],
                "groups": [{
                    "groupid": groupids
                }],
                # "templates": [{
                #     "templateid": templateids
                # }],
                "inventory_mode": 0,
                "inventory": {
                    "name": ci_searchcode,
                    "alias": ci_key,
                    "type_full": ci_name,
                    "location": ci_address,
                    "poc_1_name": ci_admin,
                    "poc_2_name": ci_owner,
                    "tag": ci_order_number,
                    "notes": ci_main_backup
                }
            },
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        self.logging_local.output(
            str(response.status_code),
            this_function_name,
            str(response.json())
            )
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

    def zabbix_host_update_interface(self, auth, interfaceid, host_ip, port, dns):
        """Function is not ready, need fix"""
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        logging.warning('Run function=%s (interfaceid=%s ip=%s port=%s dns=%s)',
                        this_function_name, interfaceid, host_ip, port, dns)
        data = {
            "jsonrpc": "2.0",
            "method": "hostinterface.update",
            "params": {
                "interfaceid": interfaceid,
                "dns": dns,
                "port": port,
                "ip": host_ip,
                "details": {
                        "version": 3,
                        "bulk": 1,
                        "securityname": "{$SNMPV3_LOGIN}",
                        "contextname": "",
                        "securitylevel": 2,
                        "authpassphrase": "{$SNMPV3_AUTH_PASSPHRASE}",
                        "privpassphrase": "{$SNMPV3_PRIV_PASSPHRASE}",
                        "authprotocol": 1,
                        "privprotocol": 0
                    }
            },
            "auth": auth,
            "id": 1
        }
        # print(f'data = {data}\n')
        response = requests.post(URL, json=data, verify=False)
        self.logging_local.output(
            str(response.status_code),
            this_function_name,
            str(response.json())
            )
        # print(f'{str(response.status_code)} {this_function_name} {str(response.json())}\n')
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

    def zabbix_host_update(self, auth, hostid, host_ip, port, groupid, templateids, ci_name, ci_key,
                            ci_address, ci_admin, ci_owner, ci_order_number, ci_main_backup,
                            ci_provider, ci_criticaly, zabbix_name, ci_searchcode):
        """Function update host inventory"""
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        logging.warning('Run function=%s (hostid=%s ip=%s ci_name=%s ci_key=%s)',
                        this_function_name, hostid, host_ip, ci_name, ci_key)
        ci_name = ci_name[:63]
        data = {
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": {
                "hostid": hostid,
                "host": zabbix_name,
                "inventory_mode": 0,
                "tags": {
                    "tag": "Provider",
                    "value": ci_provider
                    },
                "inventory": {
                    "name": ci_searchcode,
                    "alias": ci_key,
                    "type_full": ci_name,
                    "location": ci_address,
                    "poc_1_name": ci_admin,
                    "poc_2_name": ci_owner,
                    "tag": ci_order_number,
                    "notes": ci_main_backup,
                    "asset_tag": ci_criticaly
                }
            },
            "auth": auth,
            "id": 1
        }
        # print(f'data = {data}\n')
        response = requests.post(URL, json=data, verify=False)
        self.logging_local.output(
            str(response.status_code),
            this_function_name,
            str(response.json())
            )
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

    @staticmethod
    def zabbix_hosts_get(auth):
        """Get host data"""
        zabbix_hosts = {}
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "selectInterfaces": ["dns"],
                "output": [
                    "host"
                ]
            },
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('data = %s', data)
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

        for i in json.loads(response.text)["result"]:
            zabbix_hosts[i["interfaces"][0]["dns"]] = i["hostid"]

        return zabbix_hosts


    @staticmethod
    def zabbix_hosts_get_interfaceid(auth, hostid):
        """Get host interfaceid"""
        interfaceid = None
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "selectInterfaces": ["interfaceid"],
                "output": ["host"],
                "hostids": hostid
            },
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('data = %s', data)
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass
        for i in json.loads(response.text)["result"]:
            interfaceid = i["interfaces"][0]["interfaceid"]
        return int(interfaceid)


    @staticmethod
    def zabbix_hosts_get_by_hostname(auth):
        """Get host ids by hostane"""
        zabbix_hosts_hn = {}
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "host"
                ]
            },
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('data = %s', data)
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass
        for i in json.loads(response.text)["result"]:
            zabbix_hosts_hn[i["host"]] = i["hostid"]
        return zabbix_hosts_hn




    @staticmethod
    def zabbix_hosts_get_names(auth):
        """Get host names"""
        zabbix_host_names = []
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "host"
                ]
            },
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('data = %s', data)
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass
        for i in json.loads(response.text)["result"]:
            hostname = i["host"]
            zabbix_host_names.append(hostname)
        return zabbix_host_names





    @staticmethod
    def zabbix_hosts_get_interface(auth, hostid):
        """Get ID host interface"""
        interface = "127.0.0.1"
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "selectGroups": "extend",
                "selectInterfaces": ["interfaceid"],
                "hostids": hostid
            },
            "auth": auth,
            "id": 1
        }
        # print(f'data = {data}\n')
        response = requests.post(URL, json=data, verify=False)
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

        for i in json.loads(response.text)["result"]:
            try:
                interface = i["interfaces"][0]["interfaceid"]
            except KeyError:
                pass
        # print(f'{response.json()}\n')

        return interface

    @staticmethod
    def zabbix_hosts_get_interfaces(auth):
        """Get IP host"""
        interfaces = {}
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                # "filter": {
                #     "host": [
                #         "CK-KorsunShevchenkivskyi-Shevchenka31-UkrTelecom"
                #     ]
                # },
                "selectInterfaces": ["ip"]
            },
            "auth": auth,
            "id": 1
        }
        # print(f'data = {data}\n')
        response = requests.post(URL, json=data, verify=False)
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

        for i in json.loads(response.text)["result"]:
            # print(i)
            try:
                interfaces[i["interfaces"][0]["ip"]] = i["hostid"]
                # print(i["hostid"])
                # print(i["interfaces"][0]["ip"])
            except KeyError:
                pass
        # print(f'{response.json()}\n')

        return interfaces

    @staticmethod
    def zabbix_hosts_get_interfaceids(auth):
        """Get ID hosts interfaces"""
        interfaces = {}
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "selectGroups": "extend",
                "selectInterfaces": ["interfaceid"]
            },
            "auth": auth,
            "id": 1
        }
        # print(f'data = {data}\n')
        response = requests.post(URL, json=data, verify=False)
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

        for i in json.loads(response.text)["result"]:
            try:
                interfaces[i["hostid"]] = i["interfaces"][0]["interfaceid"]
            except KeyError:
                pass
        # print(f'{response.json()}\n')

        return interfaces

    @staticmethod
    def zabbix_hosts_get_interfacedns(auth):
        """Get hosts interface dns-name"""
        interfaces = []
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "selectInterfaces": ["dns"],
                "output": [
                    "host"
                ]
            },
            "auth": auth,
            "id": 1
        }
        # print(f'data = {data}\n')
        response = requests.post(URL, json=data, verify=False)
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

        for i in json.loads(response.text)["result"]:
            try:
                interfaces.append(i["interfaces"][0]["dns"])
                # interfaces[i["hostid"]] = i["interfaces"][0]["dns"]
            except KeyError:
                pass
        # print(f'{response.json()}\n')
        # print(f'{interfaces}\n')

        return interfaces


    @staticmethod
    def zabbix_hosts_get_templates(auth, zabbix_hostid):
        """Get hosts templates id"""
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        template = 0
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "selectParentTemplates": ["templateid"],
                "output": ["hostid"],
                "hostids": zabbix_hostid
            },
            "auth": auth,
            "id": 1
        }
        # print(f'data = {data}\n')
        response = requests.post(URL, json=data, verify=False)
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass
        for i in json.loads(response.text)["result"]:
            try:
                templarr = i["parentTemplates"]
                if len(templarr) > 0:
                    template = (i["parentTemplates"][0]["templateid"])
            except KeyError:
                pass
        # print(f'{response.json()}\n')
        # print(f'{template}\n')
        return int(template)


    def zabbix_host_unlink_template(self, auth, hostid, templateid):
        """Function unlink and clear template from the host"""
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        logging.warning('Run function=%s (hostid=%s templateid=%s)',
                        this_function_name, hostid, templateid)
        data = {
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": {
                "hostid": hostid,
                "templates_clear": [
                    { "templateid": templateid }
                ]
            },
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        self.logging_local.output(
            str(response.status_code),
            this_function_name,
            str(response.json())
            )
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass


    def zabbix_hostgroup_create(self, auth, name):
        """Create hostgroup"""
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "hostgroup.create",
            "params": {
                "name": name
            },
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        self.logging_local.output(
            str(response.status_code),
            this_function_name,
            str(response.json())
            )
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

    @staticmethod
    def zabbix_hostgroup_get(auth):
        """Get all hostgroups"""
        zabbix_hostgroup = {}
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": []
                }
            },
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

        for i in json.loads(response.text)["result"]:
            zabbix_hostgroup[i["name"]] = i["groupid"]

        return zabbix_hostgroup

    @staticmethod
    def zabbix_hostgroup_get_one(auth, groupid):
        """Get all hostid from hostgroup"""
        zabbix_hostgroup = []
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid"],
                "selectGroups": "extend",
                # "filter": {
                #     "host": [
                #         "DP-Robocha176-Datagroup"
                #     ],

                # },
                "groupids": groupid
            },
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

        for i in json.loads(response.text)["result"]:
            zabbix_hostgroup.append(i["hostid"])
            # print(f'i={i}')
        # print(response.text)

        return zabbix_hostgroup

    @staticmethod
    def zabbix_hostgroup_massadd(auth, hostid, groupid):
        """Add hostgroup to host"""
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "hostgroup.massadd",
            "params": {
                "groups": [
                    {
                        "groupid": groupid
                    }
                ],
                "hosts": [
                    {
                        "hostid": hostid
                    }
                ]
            },
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

    @staticmethod
    def zabbix_hostgroup_massremove(auth, hostid, groupid):
        """Remove hostgroup"""
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "hostgroup.massremove",
            "params": {
                "groups": [
                    {
                        "groupid": groupid
                    }
                ],
                "hosts": [
                    {
                        "hostid": hostid
                    }
                ]
            },
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

    @staticmethod
    def zabbix_templates_get(auth):
        """Get all templates"""
        zabbix_templates = {}
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        data = {
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend",
                "filter": {
                    "host": []
                }
            },
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        # print(str(response.status_code), this_function_name, str(response.json()))
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass

        for i in json.loads(response.text)["result"]:
            zabbix_templates[i["templateid"]] = i["host"]
            # zabbix_templates[i["host"]] = i["templateid"]

        return zabbix_templates

    @staticmethod
    def zabbix_template_massadd(auth, hostid, templateid):
        """Add template"""
        this_function_name = cast(types.FrameType,inspect.currentframe()).f_code.co_name
        logging.warning('Run function=%s (hostid=%s templateid=%s)',
                        this_function_name, hostid, templateid)
        data = {
            "jsonrpc": "2.0",
            "method": "template.massadd",
            "params": {
                "templates": [
                    {
                        "templateid": templateid
                    }
                ],
                "hosts": [
                    {
                        "hostid": hostid
                    }
                ]
            },
            "auth": auth,
            "id": 1
        }
        response = requests.post(URL, json=data, verify=False)
        try:
            if response.json()["error"]:
                logging.warning('%s = %s', this_function_name, str(response.json()))
                logging.warning('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
        except KeyError:
            pass




# zabbix_api = ZabbixAPI()
# zabbix_api.zabbix_user_login()
# auth = zabbix_api.zabbix_user_login()

## using zabbix_host_create_simple
#zabbix_api.zabbix_host_create_simple(auth, "CN-ICH-S0970744", "127.0.0.1", 10050, 5, 10186, "ci_name", "ci_key",
#                            "ci_address", "ci_admin", "ci_owner", "ci_order_number", "ci_main_backup", "ci_searchcode")

## using zabbix_host_create
# zabbix_api.zabbix_host_create(auth, "CN-ICH-S0970744", "127.0.0.1", 161, 19, None, None, None,
#                               None, None, None, None, None)


# zabbix_api.zabbix_trigger_update(auth, 19573, 1)

## using template
# zabbix_templates = zabbix_api.zabbix_templates_get(auth)
# for i in zabbix_templates:
#     print(f'{i} = {zabbix_templates[i]}')
# print(zabbix_templates["10444"])

## using hostgroup
# zabbix_hostgroups = zabbix_api.zabbix_hostgroup_get(auth)
# for i in zabbix_hostgroups:
#     print(f'{zabbix_hostgroups[i]} = {i}')
# print(f'{zabbix_hostgroups["Discovered hosts"]}')

## using host
# zabbix_hosts = zabbix_api.zabbix_hosts_get(auth)
# for i in zabbix_hosts:
    # print(f'{i} = {zabbix_hosts[i]}')
# print(zabbix_hosts["OD-KIL-R077011"])

## using host_update
# zabbix_api.zabbix_host_update_interface(auth, 3227, "127.0.0.1", 888, "AIT-122843")
# print(zabbix_api.zabbix_hosts_get_interface(auth, 13629))
# zabbix_interfaceids = zabbix_api.zabbix_hosts_get_interfaceids(auth)
# print(zabbix_interfaceids["13629"])

## using host_get
# zabbix_api.zabbix_hosts_get(auth)

## using
# interfaces = zabbix_api.zabbix_hosts_get_interfaces(auth)
# print(interfaces)

## using zabbix_hostgroup_get_one
# hostgroup_get_one = zabbix_api.zabbix_hostgroup_get_one(auth, 937)
# print(hostgroup_get_one)

# zabbix_api.zabbix_user_logout(auth)
