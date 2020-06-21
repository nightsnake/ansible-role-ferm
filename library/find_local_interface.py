#!/usr/bin/python

DOCUMENTATION = '''
---
module: find_local_interface
short_description: Return local interface or None
'''

EXAMPLES = '''
- name: Find interface which will be ACCEPT for ssh over iptables/ferm
  find_local_interface:
  register: result

- debug: var=result

'''

from ansible.module_utils.basic import *
import socket
import fcntl
import struct
import array
import re

rfc1918 = re.compile(
    '^(10(\.(25[0-5]|2[0-4][0-9]|1[0-9]{1,2}|[0-9]{1,2})){3}|((172\.(1[6-9]|2[0-9]|3[01]))|192\.168)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{1,2}|[0-9]{1,2})){2})$')


def format_ip(addr):
    return str(ord(addr[0])) + '.' + \
        str(ord(addr[1])) + '.' + \
        str(ord(addr[2])) + '.' + \
        str(ord(addr[3]))


def all_interfaces():
    max_possible = 128  # arbitrary. raise if needed.
    bytes = max_possible * 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', '\0' * bytes)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        s.fileno(),
        0x8912,  # SIOCGIFCONF
        struct.pack('iL', bytes, names.buffer_info()[0])
    ))[0]
    namestr = names.tostring()
    lst = []
    for i in range(0, outbytes, 40):
        name = namestr[i:i + 16].split('\0', 1)[0]
        ip = format_ip(namestr[i + 20:i + 24])
        lst.append((name, ip))
    return lst


def filter_ip():
    res_priv = []
    res_pub = []
    ifs = all_interfaces()
    for k, v in ifs:
        if v.startswith('127'):
            # missing lo (127.0.0.1)
            continue
        elif rfc1918.match(v):
            res_priv.append(k)
        else:
            res_pub.append(k)
    if len(res_priv) == 0:
        return list(set(res_pub))
    else:
        return list(set(res_priv))


def main():
    module = AnsibleModule(argument_spec={})
    result = filter_ip()
    module.exit_json(changed=False, meta=result)


if __name__ == '__main__':
    main()
