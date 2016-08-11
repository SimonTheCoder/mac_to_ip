#encoding=utf8
import os
import xml.etree.ElementTree as Etree
import sys

__author__="Simon Shi"

def do_nmap(ip_range):
    '''ip range format is : 192.168.1.x-y
    '''
    print "about to scan %s" % ip_range
    result_pip = os.popen("nmap -n -sP -oX - %s" % ip_range)
    #result,result_content = commands.getstatusoutput("nmap -n -sP -oX - %s" % ip_range)
    return result_pip.read()

def find_mac(nmap_xml,mac_addr):
    mac_addr = mac_addr.lower()
    host_elems = Etree.fromstring(nmap_xml).iter('host')
    for host_elem in host_elems:
        ip_addr = host_elem.find("address").get("addr")
        mac_addr_temp = os.popen("arp %s|grep ether|awk '{print $3}'" % (ip_addr)).read().strip()
        print "ip: [" + ip_addr + "]  mac: ["+ mac_addr_temp + "]"
        if mac_addr == mac_addr_temp:
            return ip_addr
    return None


def find_mac_in_ip_range(mac,ip_range):
    return find_mac(do_nmap(ip_range),mac)

if __name__ == "__main__":
  print find_mac_in_ip_range("00:11:22:33:44:55","192.168.1.1-254")
