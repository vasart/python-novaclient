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
'''
Created on Jul 4, 2014

@author: anaumchev
'''


class CheckResult(object):
    def __init__(self, result_id, time, name, node, result):
        self.id = result_id
        self.time = time
        self.name = name
        self.node = node
        self.result = result


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


class PeriodicCheck(object):
    def __init__(self, check_id, name, desc, timeout):
        self.id = check_id
        self.name = name
        self.desc = desc
        self.timeout = timeout


class PeriodicChecksManager():
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
            'Static file integrity check using IMA/TPM', 600))
        checks.append(PeriodicCheck(1, 'DynMem', 'Dynamic memory check', 300))
        checks.append(PeriodicCheck(2, 'Yet Another Check',
            'One more mock check', 720))
        return checks

    def get_specific_check(self, check_id):
        return self.get_checks_list()[check_id]

    def get_results_list(self):
        results = []
        """Get the list of check results."""
        results.append(checkResult(1, '2014/06/12 12:23:12', 'OpenAttestation',
            1, 'Pass'))
        results.append(checkResult(2, '2014/06/12 12:24:12', 'OpenAttestation',
            2, 'Pass'))
        results.append(checkResult(3, '2014/06/12 12:25:12', 'OpenAttestation',
            3, 'Pass'))
        results.append(checkResult(4, '2014/06/12 12:26:12', 'OpenAttestation',
            4, 'Fail'))
        return results
