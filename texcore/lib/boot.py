import logging
from paste.deploy.converters import asbool, aslist
from paste.script.serve import ensure_port_cleanup

def run_scgi_thread(wsgi_app, global_conf,
                    scriptName='', host=None, port=None, socket=None, umask=None,
                    allowedServers='127.0.0.1', logRequest=True,
                    debug=None):
    import flup.server.scgi
    if socket:
        assert host is None and port is None
        sock = socket
    elif host:
        assert host is not None and port is not None
        sock = (host, int(port))
        ensure_port_cleanup([sock])
    else:
        sock = None
    if umask is not None:
        umask = int(umask)
    if debug is None:
        debug = global_conf.get('debug', False)
    s = flup.server.scgi.WSGIServer(
        wsgi_app,
        scriptName=scriptName,
        bindAddress=sock,
        umask=umask,
        allowedServers=aslist(allowedServers),
        debug=asbool(debug),
        loggingLevel=asbool(logRequest) and logging.INFO or logging.WARNING
        )
    # Remove all the private handlers
    for handler in s.logger.handlers:
        s.logger.removeHandler(handler)
    s.run()
