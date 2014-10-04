from time import sleep

from twisted.internet import protocol, reactor
from twisted.python import log

from pnc.config import config
from pnc.message import upstream_connection
from pnc.upstreams.irc.pnc_client import PNCClient


class PNCClientFactory(config, protocol.ClientFactory):
    """A factory for IRC connections.
    """
    connection_attempts = 0
    connection_attempt_limit = 5
    sourceURL = 'http://pnc.frop.org/'

    def __init__(self):
        self.erroneousNickFallback = '_' + self.nickname

    def buildProtocol(self, address):
        """Build our IRC connection.
        """
        self.irc_protocol = PNCClient()
        self.irc_protocol.address = address

        upstream_connection(self.irc_network, self.irc_protocol)
        return self.irc_protocol

    def clientConnectionLost(self, connector, reason):
        """Reconnect to the server if we get disconnected.
        """
        log.msg('Disconnected from IRC: %s' % reason)
        self.connection_attempts = 0
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        """Handle connection errors.
        """
        self.connection_attempts += 1
        log.msg('Could not connect to IRC (attempt %s/%s): %s' % (self.connection_attempts, self.connection_attempt_limit, reason))

        if self.connection_attempts == self.connection_attempt_limit:
            log.msg('Too many failed connections!')
            reactor.stop()

        else:
            sleep_time = 5 * self.connection_attempts
            log.msg('Reconnecting in %s seconds' % sleep_time)
            sleep(sleep_time)
            connector.connect()
