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

from novaclient import base
from novaclient.v1_1 import periodic_checks


class PeriodicCheck(base.Resource):
    """
    A check is a periodic task to update trusted pool.
    """
    HUMAN_ID = True

    def __repr__(self):
        return "<Check: %s>" % self.name

    def delete(self):
        """
        Delete this check.
        """
        self.manager.delete(self)


class PeriodicCheckManager(periodic_checks.PeriodicCheckManager):
    """
    Manage :class:`PeriodicCheck` resources.
    """
    resource_class = PeriodicCheck

    def _build_body(self, name, desc, timeout, id):
        return {
            "periodic_check": {
                "name": name,
                "desc": desc,
                "timeout": timeout,
                "id": id
            }
        }
