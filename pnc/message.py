"""Pass messages between instaniated protocols
"""

# Networks we connect to. Each value is an instaniated PNCClient() or None
upstream_servers = {
    'FEFnet': None
}

# Clients that have connected to us
downstream_clients = {
    'FEFnet': []
}


def downstream_privmsg(network, source, target, message):
    """Send a PRIVMSG to all downstream clients.
    """
    for client in downstream_clients[network]:
        client.sendPRIVMSG(source, target, message)


def upstream_privmsg(network, target, message):
    """Send a PRIVMSG to target through a given network upstream.
    """
    upstream_servers[network].msg(target, message)


def upstream_connection(network, protocol):
    """Called when a new upstream connection is established.
    """
    upstream_servers[network] = protocol


def downstream_connect(network, protocol):
    """Called when a new downstream client connects
    """
    downstream_clients[network].append(protocol)


def downstream_disconnect(network, protocol):
    """Called when a downstream client disconnects.
    """
    downstream_clients[network].remove(protocol)
