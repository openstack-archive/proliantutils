#!/usr/bin/python
# Copyright 2017 Hewlett-Packard Enterprise Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


def Integer(value):
    return value


def ObjectName(value):
    return (value,)


PHY_DRIVE_MIB_OUTPUT = {
    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.1.2.0': {
        'cpqDaPhyDrvCntlrIndex': {ObjectName('2.0'): Integer(2)}},
    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.1.2.1': {
        'cpqDaPhyDrvCntlrIndex': {ObjectName('2.1'): Integer(2)}},
    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.1.2.2': {
        'cpqDaPhyDrvCntlrIndex': {ObjectName('2.2'): Integer(2)}},
    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.1.2.3': {
        'cpqDaPhyDrvCntlrIndex': {ObjectName('2.3'): Integer(2)}},
    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.2.2.0': {
        'cpqDaPhyDrvIndex': {ObjectName('2.0'): Integer(0)}},
    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.2.2.1': {
        'cpqDaPhyDrvIndex': {ObjectName('2.1'): Integer(1)}},
    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.2.2.2': {
        'cpqDaPhyDrvIndex': {ObjectName('2.2'): Integer(2)}},
    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.2.2.3': {
        'cpqDaPhyDrvIndex': {ObjectName('2.3'): Integer(3)}},
    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.0': {
        'cpqDaPhyDrvSize': {ObjectName('2.0'): Integer(286102)}},
    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.1': {
        'cpqDaPhyDrvSize': {ObjectName('2.1'): Integer(286102)}},
    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.2': {
        'cpqDaPhyDrvSize': {ObjectName('2.2'): Integer(286102)}},
    'SNMPv2-SMI::enterprises.232.3.2.5.1.1.45.2.3': {
        'cpqDaPhyDrvSize': {ObjectName('2.3'): Integer(286102)}}
}
