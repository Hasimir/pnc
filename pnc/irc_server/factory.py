from time import sleep

from twisted.internet import protocol, reactor
from twisted.python import log

from pnc.irc_server.irc_server import IRCServer


class PNCServerFactory(protocol.ServerFactory):
    """A factory for IRC Server connections.
    """
    irc_protocol = None

    def __init__(self, factories, nickname):
        self.factories = factories
        self.nickname = nickname

    def buildProtocol(self, address):
        """Build our IRC connection.
        """
        self.irc_protocol = IRCServer()
        self.irc_protocol.factory = self
        self.irc_protocol.nickname = self.nickname
        self.irc_protocol.upstream = self.factories['irc_client'].irc_protocol

        return self.irc_protocol
