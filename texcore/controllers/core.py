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
        return self._process(manuscript, 'UTF-8')

    def typeset_with_encoding(self, encoding, manuscript):
        return self._process(manuscript, encoding)

    def _process(self, manuscript_binary, encoding):
        p = glue.fork_proc()
        try:
            (stream, error) = p.communicate(Manuscript(manuscript_binary.data, encoding=encoding).__str__())
        except UnicodeDecodeError, e:
            return xmlrpclib.Fault(8000, u'Cannot decode input stream as %s' % encoding) 
        except UnicodeEncodeError, e:
            return xmlrpclib.Fault(8000, u'Cannot transcode input stream as native TeX encoding') 
        code = p.wait()
        if code or error:
            return xmlrpclib.Fault(8000, unicode(TeXOperationError(code, error)))
        return xmlrpclib.Binary(stream)
