#!/usr/bin/python
from __future__ import with_statement
import os
import subprocess

def fork_proc(f=subprocess.PIPE):
	return subprocess.Popen(
				'TEXMFHOME=%(here)s/texcore/lib/texmf make -sf %(here)s/texcore/lib/texglue.mk pdf-stream' % dict(here=os.getcwd()),
				bufsize=8192,
				stdin=f, stdout=subprocess.PIPE, close_fds=True, shell=True
			)
