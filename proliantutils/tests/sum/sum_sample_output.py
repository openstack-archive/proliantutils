# Copyright 2017 Hewlett Packard Enterprise Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

MODULE = "SUM"

SUM_OUTPUT_DATA = """
Scouting completed, node type:LINUX
Inventory started
Inventory completed

Analysis started
Analysis completed

Analysis started
Analysis completed

Deployment started

Deploying component: hpsmh-7.6.0-11.x86_64.rpm
Component Filename: hpsmh-7.6.0-11.x86_64.rpm
Component Name: HPE System Management Homepage for Linux (AMD64/EM64T)
Version: 7.6.0-11
Deployment Result: Success


Deploying component: ssaducli-2.60-18.0.x86_64.rpm
Component Filename: ssaducli-2.60-18.0.x86_64.rpm
Component Name: HPE Smart Storage Administrator Diagnostic Utility
Version: 2.60-18.0
Deployment Result: Success

Deployment completed

Deployed Components:
  Component Filename: hpsmh-7.6.0-11.x86_64.rpm
  Component Name: HPE System Management Homepage for Linux (AMD64/EM64T)
  Original Version:
  New Version: 7.6.0-11
  Deployment Result: Success

  Component Filename: ssaducli-2.60-18.0.x86_64.rpm
  Component Name: HPE Smart Storage Administrator Diagnostic Utility
  Original Version:
  New Version: 2.60-18.0
  Deployment Result: Success

Exit status: 0
"""

SUM_OUTPUT_DATA_FAILURE = """
Scouting completed, node type:LINUX
Inventory started
Inventory completed

Analysis started
Analysis completed

Analysis started
Analysis completed

Deployment started

Deploying component: hpsmh-7.6.0-11.x86_64.rpm
Component Filename: hpsmh-7.6.0-11.x86_64.rpm
Component Name: HPE System Management Homepage for Linux (AMD64/EM64T)
Version: 7.6.0-11
Deployment Result: Success


Deploying component: ssaducli-2.60-18.0.x86_64.rpm
Component Filename: ssaducli-2.60-18.0.x86_64.rpm
Component Name: HPE Smart Storage Administrator Diagnostic Utility
Version: 2.60-18.0
Deployment Result: Success

Deployment completed

Deployed Components:
  Component Filename: hpsmh-7.6.0-11.x86_64.rpm
  Component Name: HPE System Management Homepage for Linux (AMD64/EM64T)
  Original Version:
  New Version: 7.6.0-11
  Deployment Result: Success

  Component Filename: ssaducli-2.60-18.0.x86_64.rpm
  Component Name: HPE Smart Storage Administrator Diagnostic Utility
  Original Version:
  New Version: 2.60-18.0
  Deployment Result: Update returned an error

Exit status: 0
"""
