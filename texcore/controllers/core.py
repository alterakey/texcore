from __future__ import with_statement
import logging
import xmlrpclib

from pylons.controllers import XMLRPCController

from texcore.lib import glue
from texcore.lib.exc import TeXOperationError
from texcore.lib.manuscript import Manuscript

log = logging.getLogger(__name__)

class CoreController(XMLRPCController):
    def typeset(self, manuscript):
        return self._process(Manuscript(manuscript.data))

    def typeset_with_encoding(self, encoding, manuscript):
        return self._process(Manuscript(manuscript.data, encoding=encoding))

    def _process(self, manuscript_obj):
        p = glue.fork_proc()
        (stream, error) = p.communicate(manuscript_obj.__str__())
        code = p.wait()
        if code or error:
            return xmlrpclib.Fault(8000, unicode(TeXOperationError(code, error)))
        return xmlrpclib.Binary(stream)
