from time import sleep

from twisted.internet import protocol, reactor
from twisted.python import log

from pnc.message import upstream_connection
from pnc.irc_client.pnc_client import PNCClient


class PNCClientFactory(protocol.ClientFactory):
    """A factory for IRC connections.
    """
    connection_attempts = 0
    connection_attempt_limit = 5
    irc_protocol = None
    sourceURL = 'http://pnc.frop.org/'

    def __init__(self, nickname, realname='PNC User', username=None, password=None):
        self.nickname = nickname
        self.realname = realname
        self.username = username
        self.password = password
        self.erroneousNickFallback = '_' + nickname

    def buildProtocol(self, address):
        """Build our IRC connection.
        """
        self.irc_protocol = PNCClient(self.nickname)
        self.irc_protocol.factory = self

        # Set the various connection attributes
        self.irc_protocol.hostname = None
        self.irc_protocol.password = None
        self.irc_protocol.realname = self.realname
        self.irc_protocol.username = self.username or self.nickname

        # CTCP responses
        self.irc_protocol.userinfo = None
        # fingerReply is a callable returning a string, or a str()able object.
        self.irc_protocol.fingerReply = None
        self.irc_protocol.versionName = None
        self.irc_protocol.versionNum = None
        self.irc_protocol.versionEnv = None

        upstream_connection('FEFnet', self.irc_protocol)
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
