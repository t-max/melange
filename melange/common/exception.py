# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
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

"""
Nova base exception handling, including decorator for re-raising
Nova-type exceptions. SHOULD include dedicated exception logging.
"""

import logging
from gettext import gettext as _


class ProcessExecutionError(IOError):
    def __init__(self, stdout=None, stderr=None, exit_code=None, cmd=None,
                 description=None):
        if description is None:
            description = _("Unexpected error while running command.")
        if exit_code is None:
            exit_code = '-'
        message = "%s\nCommand: %s\nExit code: %s\nStdout: %r\nStderr: %r" % (
                  description, cmd, exit_code, stdout, stderr)
        IOError.__init__(self, message)


class MelangeError(Exception):

    def __init__(self, message=None):
        super(MelangeError, self).__init__(message or self._error_message())

    def _error_message(self):
        pass


class ApiError(MelangeError):
    def __init__(self, message='Unknown', code='Unknown'):
        self.message = message
        self.code = code
        super(ApiError, self).__init__('%s: %s' % (code, message))


class NotFound(MelangeError):
    pass


class Duplicate(MelangeError):
    pass


class NotAuthorized(MelangeError):
    pass


class NotEmpty(MelangeError):
    pass


class Invalid(MelangeError):
    pass


class InvalidContentType(Invalid):
    message = _("Invalid content type %(content_type)s.")


class BadInputError(Exception):
    """Error resulting from a client sending bad input to a server"""
    pass


class MissingArgumentError(MelangeError):
    pass


class DatabaseMigrationError(MelangeError):
    pass


def wrap_exception(f):
    def _wrap(*args, **kw):
        try:
            return f(*args, **kw)
        except Exception, e:
            if not isinstance(e, Error):
                #exc_type, exc_value, exc_traceback = sys.exc_info()
                logging.exception('Uncaught exception')
                #logging.error(traceback.extract_stack(exc_traceback))
                raise Error(str(e))
            raise
    _wrap.func_name = f.func_name
    return _wrap
