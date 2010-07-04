from __future__ import with_statement
import logging
import xmlrpclib

from pylons.controllers import XMLRPCController

from texcore.lib import glue
from texcore.lib.exc import TeXOperationError
from texcore.lib.manuscript import Manuscript

log = logging.getLogger(__name__)

class CoreController(XMLRPCController):
    def typeset(self, manuscript, params=None):
        if params is None:
            params = dict()

        p = glue.fork_proc(**params)
        try:
            encoding = params.get('encoding', 'UTF-8')
            (stream, error) = p.communicate(Manuscript(manuscript.data, encoding=encoding).__str__())
        except UnicodeDecodeError, e:
            return xmlrpclib.Fault(8000, u'Cannot decode input stream as %s' % encoding) 
        except UnicodeEncodeError, e:
            return xmlrpclib.Fault(8000, u'Cannot transcode input stream as native TeX encoding') 
        code = p.wait()
        if code or error:
            return xmlrpclib.Fault(8000, unicode(TeXOperationError(code, error)))
        return xmlrpclib.Binary(stream)
