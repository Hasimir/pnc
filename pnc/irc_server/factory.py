from twisted.internet import protocol

from pnc.irc_server.irc_server import IRCServer
from pnc.message import downstream_connect, downstream_disconnect


class PNCServerFactory(protocol.ServerFactory):
    """A factory for IRC Server connections.
    """
    irc_protocol = None

    def __init__(self, nickname):
        self.nickname = nickname

    def buildProtocol(self, address):
        """Build our IRC connection.
        """
        self.irc_protocol = IRCServer()
        self.irc_protocol.factory = self
        self.irc_protocol.nickname = self.nickname

        downstream_connect('FEFnet', self.irc_protocol)
        return self.irc_protocol

    # FIXME: Figure out how to handle client disconnects
