# -*- coding: utf-8 -*-
import logging
import os

from routes import url_for
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort

from texcore.lib.base import BaseController, render
from texcore.lib.exc import TeXOperationError
from texcore.lib.manuscript import Manuscript
from texcore.lib import glue

log = logging.getLogger(__name__)

class AdhocController(BaseController):

    def index(self):
        return render('index.genshi', extra_vars=dict(error=None))
	
    def create(self):
        manuscript = request.POST['manuscript']
        encoding = request.POST['encoding']
        p = glue.fork_proc()
        try:
            (stream, error) = p.communicate(Manuscript(manuscript.value, encoding).__str__())
        except UnicodeDecodeError:
            return render('index.genshi', extra_vars=dict(error=u'Cannot decode input stream as %s' % encoding))
        except UnicodeEncodeError:
            return render('index.genshi', extra_vars=dict(error=u'Cannot transcode input stream as native TeX encoding'))            
        code = p.wait()
        if code or error:
            return render('index.genshi', extra_vars=dict(error=unicode(TeXOperationError(code, error))))
        response.content_type = 'application/pdf'
        # NB: Use UTF-8 for Safari, Firefox, or other sane browsers,
        # SHIFT-JIS for IE/MacIE, EUC-JP for Netscape 4.7
        response.headerlist.append(('Content-Disposition', 'attachment; filename="%s"' % u'output.pdf'.encode('UTF-8')))
        response.headerlist.append(('Refresh', '0; url=%s' % url_for(controller=u'adhoc', action=u'index')))
        return stream
