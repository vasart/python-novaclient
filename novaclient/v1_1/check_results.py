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

"""
Check results interface.
"""

from novaclient import base
from novaclient import exceptions
from novaclient.openstack.common.gettextutils import _


class CheckResult(base.Resource):
    """
    A check result is a ternary value (trusted, not_trusted, unknown)
    and a status message.
    """
    HUMAN_ID = True

    def __init__(self, result_id, time, name, node, result, status):
        self.id = result_id
        self.time = time
        self.name = name
        self.node = node
        self.result = result
        self.status = status

    def __repr__(self):
        return "<Check result: %s>" % self.name

    def delete(self):
        """
        Delete this check result.
        """
        self.manager.delete(self)


class CheckResultManager(base.ManagerWithFind):
    """
    Manage :class:`check_result` resources.
    """
    resource_class = CheckResult
    is_alphanum_id_allowed = True
    
    
    results = [
               CheckResult(1, '2014/06/12 12:23:12', 'OpenAttestation', 1, 'trusted', 'Pass'),
               CheckResult(2, '2014/06/12 12:24:12', 'OpenAttestation', 2, 'not_trusted', 'Fail'),
               CheckResult(3, '2014/06/12 12:25:12', 'OpenAttestation', 3, 'trusted', 'Pass'),
               CheckResult(4, '2014/06/12 12:26:12', 'OpenAttestation', 4, 'unknown', 'Error'),
               ]

    def get_results_list(self):
        return self.results

    def list(self):
        """
        Get a list of all check results.

        :rtype: list of :class:`CheckResult`.
        """
        query_string = "?%s"

        return self._list("/check_results%s%s" % query_string, "check_results")

    def get(self, check_result):
        """
        Get a specific check result.

        :param check_result: The ID of the :class:`CheckResult` to get.
        :rtype: :class:`CheckResult`
        """
        return self._get("/check_results/%s" % base.getid(check_result),
            "check_result")

    def delete(self, check_result):
        """
        Delete a specific check result.

        :param check_result: The ID of the :class:`CheckResult` to get.
        """
        self._delete("/check_results/%s" % base.getid(check_result))
        
    def result_delete(self, result_id):
        ind = 0 
         
        for index, result in enumerate(self.results):
            if int(result.id) == int(result_id):
                ind = index                
                break
            
        del self.results[ind]
