from twisted.internet import protocol

from pnc.config import config
from pnc.downstreams.irc.irc_server import IRCServer
from pnc.message import downstream_connect, downstream_disconnect


class PNCServerFactory(protocol.ServerFactory):
    """A factory for IRC Server connections.
    """
    irc_protocol = None

    def buildProtocol(self, address):
        """Build our IRC connection.
        """
        self.irc_protocol = IRCServer()
        self.irc_protocol.address = address

        downstream_connect(config.irc_network, self.irc_protocol)
        return self.irc_protocol

    # FIXME: Figure out how to handle client disconnects
