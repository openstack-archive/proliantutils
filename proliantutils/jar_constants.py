# Copyright 2015 Hewlett-Packard Development Company, L.P.
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

"""Console Jar file mappings with the iLO firmware versions"""

# iLO 4 2.20-2.31: /html/intgapp_225.jar
# iLO 4 2.40-2.42: /html/intgapp_228.jar
# iLO 4 2.44-2.70: /html/intgapp4_231.jar


# iLO 5 1.00 : /html/intgapp_228.jar
# iLO 5 1.10-1.11: /html/intgapp4_239.ja
# iLO 5 1.15-1.19: /html/intgapp4_240.jar
# iLO 5 1.20-1.22: /html/intgapp4_244.jar
# iLO 5 1.30-1.39: /html/intgapp4_245.jar
# iLO 5 1.40-1.43: /html/intgapp4_247.jar


ilo4_mapping = (lambda x: 'intgapp_225.jar' if (x >= 2.30 and x <= 2.31)
                          else 'intgapp_228.jar' if (x >= 2.40 and x <= 2.42)
                          else 'intgapp4_231.jar' if (x >= 2.44 and x <= 2.70)
                          else None)

ilo5_mapping = (lambda x: 'intgapp_228.jar' if x == 1.00
                          else 'intgapp4_239.jar' if (x >= 1.10 and x <= 1.11)
                          else 'intgapp4_240.jar' if (x >= 1.15 and x <= 1.19)
                          else 'intgapp4_244.jar' if (x >= 1.20 and x <= 1.22)
                          else 'intgapp4_245.jar' if (x >= 1.30 and x <= 1.39)
                          else 'intgapp4_247.jar' if (x >= 1.40 and x <= 1.43)
                          else None)
