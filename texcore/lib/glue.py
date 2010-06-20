import os
import subprocess

import pylons
from pkg_resources import resource_filename

def fork_proc(f=subprocess.PIPE):
        lib_root = resource_filename('texcore', 'lib')
        texmf_path = pylons.config.get('texcore.texmf')
	return subprocess.Popen(
				'TEXMFHOME=%(texmf_path)s make -sf %(here)s/texglue.mk pdf-stream' % dict(here=lib_root, texmf_path=texmf_path),
				bufsize=8192,
				stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, shell=True
			)
