from __future__ import with_statement
import logging
import xmlrpclib

from pylons.controllers import XMLRPCController

from texcore.lib import glue
from texcore.lib.exc import TeXOperationError

log = logging.getLogger(__name__)

class CoreController(XMLRPCController):
    def typeset(self, manuscript):
        p = glue.fork_proc()
        (stream, error) = p.communicate(manuscript.data)
        code = p.wait()
        if code or error:
            return xmlrpclib.Fault(8000, unicode(TeXOperationError(code, error)))
        return xmlrpclib.Binary(stream)
