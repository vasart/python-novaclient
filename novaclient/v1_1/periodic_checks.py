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
from novaclient import exceptions
# from rtslib import utils


class LogRecord(object):
    def __init__(self, record_id, log_record_time, log_record_source,
            log_record_message):
        self.id = record_id
        self.log_record_time = log_record_time
        self.log_record_source = log_record_source
        self.log_record_message = log_record_message


class Option(object):
    def __init__(self, name, value):
        self.id = name
        self.enabled = value


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


class PeriodicCheckManager(base.ManagerWithFind):
    """
    Manage :class:`PeriodicCheck` resources.
    """
    resource_class = PeriodicCheck
    is_alphanum_id_allowed = True
    checks_num = 3

    options = [
        Option("Security Checks Enabled", True),
        Option("Clean Tcp When Down", True),
    ]

    def options_update_enabled(self, option_id, enabled):
        for option in PeriodicCheckManager.options:
            if option.id == option_id:
                option.enabled = enabled

    def get_log_records(self):
        log_records = []
        log_records.append(LogRecord("1", "12345", "source1", "message1"))
        log_records.append(LogRecord("2", "12312", "source2", "message2"))
        return log_records

    def get_global_settings(self):
        return PeriodicCheckManager.options

    def get_checks_list(self):
        return PeriodicCheckManager.periodic_checks

    def get_specific_check(self, check_id):
        for index, check in enumerate(PeriodicCheckManager.periodic_checks):
            if int(check.id) == int(check_id):
                return check

    def list(self):
        """
        Get a list of all periodic checks.

        :rtype: list of :class:`PeriodicCheck`.
        """
        return self._list("/periodic_checks",
            "periodic_checks")

    def get(self, periodic_check):
        """
        Get a specific periodic check.

        :param periodic_check: The ID of the :class:`PeriodicCheck` to get.
        :rtype: :class:`PeriodicCheck`
        """
        return self._get("/periodic_checks/%s" % base.getid(periodic_check),
            "periodic_check")

    def delete(self, periodic_check):
        """
        Delete a specific periodic check

        :param periodic_check: The ID of the :class:`PeriodicCheck` to get.
        """
        self._delete("/periodic_checks/%s" % base.getid(periodic_check))

    def _build_body(self, name, desc, timeout, spacing, id):
        return {
            "periodic_check": {
                "name": name,
                "desc": desc,
                "timeout": timeout,
                "spacing": spacing,
                "id": id
            }
        }

    def create(self, name, desc, timeout, spacing, checkid="auto"):
        """
        Create a periodic check.

        :param name: Brief name of the periodic check
        :param desc: Full description of a periodic check
        :param timeout: Timeout for a periodic check to run
        :param checkid: ID for the check (optional). You can use the reserved
                         value ``"auto"`` to have Nova generate a UUID for the
                         check in cases where you cannot simply pass ``None``.
        :rtype: :class:`PeriodicCheck`
        """
        PeriodicCheckManager.checks_num += 1
        checkid = PeriodicCheckManager.checks_num

        try:
            timeout = int(timeout)
        except (TypeError, ValueError):
            raise exceptions.CommandError(_("Timeout must be an integer."))

        if checkid == "auto":
            checkid = None

        body = self._build_body(name, desc, timeout, spacing, checkid)

        return self._create("/periodic_checks", body, "periodic_check")

    def periodic_check_create(self, name, desc, timeout, spacing):
        new_check = PeriodicCheckManager.periodic_checks.append(
                        PeriodicCheck(
                            PeriodicCheckManager.checks_num, name,
                            desc, timeout, spacing))
        PeriodicCheckManager.checks_num += 1
        return new_check

    def periodic_check_delete(self, check_id):
        ind = 0

        for index, check in enumerate(PeriodicCheckManager.periodic_checks):
            if int(check.id) == int(check_id):
                ind = index
                break

        del PeriodicCheckManager.periodic_checks[ind]