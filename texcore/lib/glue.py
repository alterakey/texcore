import os
import subprocess

import pylons
from pkg_resources import resource_filename

class DvipdfmxParams(object):
        def __init__(self, **kwargs):
                self.kwargs = kwargs
                self._wrap('embedmap')

        def _wrap(self, kw):
                if self.kwargs.get(kw) is None:
                        self.kwargs[kw] = list()
                else:
                        if not isinstance(self.kwargs[kw], list):
                                self.kwargs[kw] = list(self.kwargs[kw])

        def get(self):
                params = []
                params.append('-p %s' % self.kwargs.get('papersize', 'a4'))
                for p in self.kwargs['embedmap']:
                        params.append('-f %s' % p)
                return ' '.join(params)

def fork_proc(f=subprocess.PIPE, **kwargs):
        lib_root = resource_filename('texcore', 'lib')
        texmf_path = pylons.config.get('texcore.texmf')
        ptex_path = pylons.config.get('texcore.ptex')

        dvipdfmx_params = DvipdfmxParams(**kwargs)

	return subprocess.Popen(
				'PATH=%(ptex_path)s/bin:$PATH TEXMFHOME=%(texmf_path)s make -sf %(here)s/texglue.mk DVIPDFMX_PARAMS="%(dvipdfmx_params)s" pdf-stream' % dict(here=lib_root, texmf_path=texmf_path, ptex_path=ptex_path, dvipdfmx_params=dvipdfmx_params.get()),
				bufsize=8192,
				stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, shell=True
			)
