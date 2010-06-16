# -*- coding: utf-8 -*-
import logging
import os

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort

from texcore.lib.base import BaseController, render
from texcore.lib.exc import TeXOperationError
from texcore.lib import glue

log = logging.getLogger(__name__)

class AdhocController(BaseController):

    def index(self):
        return render('index.genshi', extra_vars=dict(failed=False))
	
    def create(self):
        manuscript = request.POST['manuscript']
        p = glue.fork_proc()
        (stream, error) = p.communicate(manuscript.value)
        code = p.wait()
        if code or error:
            return render('index.genshi', extra_vars=dict(code=code, error=error, failed=True))
        response.content_type = 'application/pdf'
        # NB: Use UTF-8 for Safari, Firefox, or other sane browsers,
        # SHIFT-JIS for IE/MacIE, EUC-JP for Netscape 4.7
        response.headerlist.append(('Content-Disposition', 'attachment; filename="%s"' % u'output.pdf'.encode('UTF-8')))
        return stream
