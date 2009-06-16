#!/usr/bin/python
from __future__ import with_statement
import os
import subprocess

def fork_proc(f=subprocess.PIPE):
	return subprocess.Popen(
				'make -sf %(here)s/texcore/lib/texglue.mk pdf-stream BASEDIR=%(here)s/texcore/lib/texplates' % dict(here=os.getcwd()),
				bufsize=8192,
				stdin=f, stdout=subprocess.PIPE, close_fds=True, shell=True
			)
