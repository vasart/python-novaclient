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
        self.value = value


class PeriodicCheck(base.Resource):
    """
    A check is a periodic task to update trusted pool.
    """
    HUMAN_ID = True

    def __init__(self, check_id, name, desc, timeout, spacing):
        self.id = check_id
        self.name = name
        self.desc = desc
        self.timeout = timeout
	self.spacing = spacing

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

    def get_log_records(self):
        log_records = []
        log_records.append(LogRecord("1", "12345", "source1", "message1"))
        log_records.append(LogRecord("2", "12312", "source2", "message2"))
        return log_records

    def get_global_settings(self):
        options = []
        options.append(Option("Security Checks Enabled", True))
        options.append(Option("Clean Tcp When Down", True))
        options.append(Option("OpenAttestation Location", "192.168.255.4"))
        return options

    def get_checks_list(self):
        checks = []
        checks.append(PeriodicCheck(0, 'OpenAttestation',
            'Static file integrity check using IMA/TPM', 600, 1200))
        checks.append(PeriodicCheck(1, 'DynMem', 'Dynamic memory check', 300,
	    600))
        checks.append(PeriodicCheck(2, 'Yet Another Check',
            'One more mock check', 720, 1440))
        return checks

    def get_specific_check(self, check_id):
        return self.get_checks_list()[check_id]

    def list(self):
        """
        Get a list of all periodic checks.

        :rtype: list of :class:`PeriodicCheck`.
        """
        query_string = "?%s"

        return self._list("/periodic_checks%s" % query_string,
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

        try:
            timeout = int(timeout)
        except (TypeError, ValueError):
            raise exceptions.CommandError(_("Timeout must be an integer."))

        if checkid == "auto":
            checkid = None

        body = self._build_body(name, desc, timeout, checkid)

        return self._create("/periodic_checks", body, "periodic_check")
