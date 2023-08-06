# -*- coding: utf-8 -*-
#
#  Tumgreyspf
#  Copyright © 2004-2005, Sean Reifschneider, tummy.com, ltd.
#
#  pypolicyd-spf changes
#  Copyright © 2007,2008,2009,2010 Scott Kitterman <scott@kitterman.com>
#
#  dkimpy-milter changes
#  Copyright © 2018 Scott Kitterman <scott@kitterman.com>
#  Note: Derived from pypolicydspfsupp.py version before relicensing to Apache
#        2.0 license - 100% GPL
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2 as published
    by the Free Software Foundation.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.'''

import syslog
import os
import sys
import stat
import socket
import ipaddress
import spf_engine.policydspfsupp as policydspfsupp

class HostsDataset(object):
    '''Hold a group of host related dataset objects'''

    def __init__(self, dataset):
        self.dataset = []
        # Self.dataset will end up being a list of DataSetItem(s).
        for item in dataset:
            item = item.rstrip(']')
            item = item.lstrip('[')
            self.dataset.append(self.DatasetItem(item))

    class DatasetItem(object):
        '''Individual dataset item'''

        def __init__(self, item):
            self.item = item
            self.isipv4 = False
            self.isipv4cidr = False
            self.isipv6 = False
            self.isipv6cidr = False
            self.ishostname = False
            self.isdomain = False
            self.negative = False
            if self.item[0] == '!':
                self.item = item[1:]
                self.negative = True
            try:
                self.item = ipaddress.ip_address(self.item)
                if isinstance(self.item, ipaddress.IPv4Address):
                    self.isipv4 = True
                elif isinstance(self.item, ipaddress.IPv6Address):
                    self.isipv6 = True
            except ValueError as e:
                try:
                    self.item = ipaddress.ip_network(self.item)
                    if isinstance(self.item, ipaddress.IPv4Network):
                        self.isipv4cidr = True
                    elif isinstance(self.item, ipaddress.IPv6Network):
                        self.isipv6cidr = True
                except ValueError as e2:
                    if self.item[0] == '.' and len(self.item.split('.')) > 2:
                        self.isdomain = True
                    elif len(self.item.split('.')) > 1:  # It has a '.' in it
                        self.ishostname = True
                    else:
                        raise policydspfsupp.ConfigException('Unknown dataset item: {0}'
                                              .format(item))

    def match(self, connectip):
        '''Check if the connect IP is part of the dataset'''
        source = ipaddress.ip_address(connectip)
        for item in self.dataset:
            if item.isdomain or item.ishostname:
                result = self.matchname(source)   # Match host/domains first
                if result:
                    return(result)
            elif item.isipv4 or item.isipv4cidr:  # Then IPv4/6 addresses or
                if isinstance(source, ipaddress.IPv4Address):  # networks
                    return(self.match4(source))   # depending on the item type
            elif item.isipv6 or item.isipv6cidr:  # and connect type
                if isinstance(source, ipaddress.IPv6Address):
                    return(self.match6(source))

    def matchname(self, source):
        '''Does source IP address relate to a domain/hostname in the dataset'''
        match = False
        matchone = False
        negativeone = False
        matchdomain = False
        negativedomain = False
        ptrlist = self.getptr(source)
        for item in self.dataset:
            if item.isdomain:
                for ptr in ptrlist:
                    # Strip the leading '.' off the domain name for exact match
                    if item.item[1:] == ptr[-len(item.item)+1:]:
                        matchdomain = True
                        negativedomain = item.negative
            elif item.ishostname:
                for ptr in ptrlist:
                    if item.item == ptr:
                        matchone = True
                        negativeone = item.negative
        if matchdomain and not negativedomain:
            match = True
        if matchone and not negativeone:
            return True
        if matchone and negativeone:
            match = False
        return(match)

    def getptr(self, source):
        '''Get validated PTR name of IP address'''
        results = []
        s = Session()
        ptrnames = s.dns(source.reverse_pointer, 'PTR', timeout=self.conf.get('DNSTimeout'))
        for name in ptrnames:
            if isinstance(source, ipaddress.IPv4Address):
                ips = s.dns(name, 'A')
                for ip in ips:
                    ip = ipaddress.IPv4Address(ip)
                    if ip == source:
                        results.append(name)
            if isinstance(source, ipaddress.IPv6Address):
                ips = s.dns(name, 'AAAA')
                for ip in ips:
                    ip = ipaddress.IPv6Address(ip)
                if ip == source:
                    results.append(name)
        return results

    def match4(self, source):
        '''Is the source IP related to a IPv4 address/network in the dataset'''
        match = False
        matchone = False
        negativeone = False
        matchcidr = False
        negativecidr = False
        for item in self.dataset:
            if item.isipv4:
                if source == item.item:
                    matchone = True
                    negativeone = item.negative
            elif item.isipv4cidr:
                if source in item.item:
                    matchcidr = True
                    negativecidr = item.negative
        if matchcidr and not negativecidr:
            match = True
        if matchone and not negativeone:
            return True
        if matchone and negativeone:
            match = False
        return(match)

    def match6(self, source):
        '''Is the source IP realted to a IPv6 address/network in the dataset'''
        match = False
        matchone = False
        negativeone = False
        matchcidr = False
        negativecidr = False
        for item in self.dataset:
            if item.isipv6:
                if source == item.item:
                    matchone = True
                    negativeone = item.negative
            elif item.isipv6cidr:
                if source in item.item:
                    matchcidr = True
                    negativecidr = item.negative
        if matchcidr and not negativecidr:
            match = True
        if matchone and not negativeone:
            return True
        if matchone and negativeone:
            match = False
        return(match)


def _dataset_to_list(dataset):
    """Convert a dataset (as defined in dkimpymilter.8) and return a python
       list of values.  For multiline datasets like KeyTable and SigningTable a
       key : values dictionary is returned"""
    if not isinstance(dataset, str):
        # If it was a csl with more than one value, it's already a list, we
        # only need to remove the name from the first value.
        if dataset[0][:4] == 'csl:':
            dataset[0] = dataset[0][4:]
        for item in dataset:
            dataset[dataset.index(item)] = item.strip().strip(',')
        return dataset
    elif isinstance(dataset, str):
        if dataset[0] == '/' or dataset[:5] == 'file:' or dataset[:7] == 'refile:':
            # This is a flat file dataset, which are key value:value stores
            ds = []
            dsd = {}
            if dataset[0] == '/' or dataset[:2] == './' or dataset[:3] == '../':
                dsname = dataset
            elif dataset[:5] == 'file:':
                dsname = dataset[5:]
            elif dataset[:7] == 'refile:':
                dsname = dataset[7:]
            dsf = open(dsname, 'r')
            for line in dsf.readlines():
                if line[0] != '#':
                    if len(line.split()) == 1:
                        if len(line.split(':')) == 1:
                            ds.append(line.strip())
                        else:
                            for element in line.split(':'):
                                ds.append(element.strip().strip(':'))
                    elif len(line.split()) == 2: # key value:value:value
                        key, values = line.split()
                        values = values.split(':')
                        dsd.update({key:values})
            dsf.close()
            if ds:
                return ds
            elif dsd:
                return dsd
        # If it's a str and csl, it has one value and we return a list
        if dataset[:4] == 'csl:':
            datalist = dataset[4:].split(',')
            for item in datalist:
                datalist[datalist.index(item)] = item.strip().strip(',')
            return datalist
        else:
            datalist = dataset.split(',')
            for item in datalist:
                datalist[datalist.index(item)] = item.strip().strip(',')
            return datalist
        if dataset[-3:] == '.db' or dataset[:3] == 'db:':
            #  This is a Sleepycat (Oracle) DB  dataset, which we dont support
            raise policydspfsupp.ConfigException('Unsupported dataset db datase: {0}'
                                      .format(type(dataset)))
