import os
import subprocess

from pkg_resources import resource_filename

def fork_proc(f=subprocess.PIPE):
	return subprocess.Popen(
				'TEXMFHOME=%(here)s/texmf make -sf %(here)s/texglue.mk pdf-stream' % dict(here=resource_filename('texcore', 'fixtures')),
				bufsize=8192,
				stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, shell=True
			)
