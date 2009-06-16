from __future__ import with_statement
import logging
import xmlrpclib

from pylons.controllers import XMLRPCController

from texcore.lib import glue

log = logging.getLogger(__name__)

class CoreController(XMLRPCController):
    def typeset(self, manuscript):
        p = glue.fork_proc()
        p.stdin.write(manuscript.data)
        p.stdin.close()
        return xmlrpclib.Binary(p.stdout.read())
