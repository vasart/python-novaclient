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
from novaclient.v1_1 import check_results


class CheckResult(base.Resource):
    """
    A check result is a ternary value (trusted, not_trusted, unknown)
    and a status message.
    """
    HUMAN_ID = True

    def __repr__(self):
        return "<Check result: %s>" % self.name

    def delete(self):
        """
        Delete this check result.
        """
        self.manager.delete(self)


class CheckResultManager(check_results.CheckResultManager):
    """
    Manage :class:`CheckResult` resources.
    """
    resource_class = CheckResult

    def _build_body(self, timestamp, name, node, result, status, id):
        return {
            "check_result": {
                "timestamp": timestamp,
                "name": name,
                "node": node,
                "result": result,
                "status": status,
                "id": id
            }
        }
