from twisted.python import log
from twisted.words.protocols import irc


class PNCLoginMixin:
    """These are IRC Server connection related functions.

    We put these into their own class for organization purposes.
    """
    def connectionMade(self):
        log.msg('Connected to IRC Server %s:%s' 
            % (self.address.host, self.address.port))
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        log.msg('Disconnected: %s' % reason)
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        """Called when client has succesfully signed on to server.
        """
        log.msg("Successfully signed on to IRC as %s" % self.nickname)

    def created(self, when):
        """Called with creation date information about the server

        @type when: C{str}
        @param when: A string describing when the server was created, probably.
        """
        log.msg('Created: %s' % when)

    def yourHost(self, info):
        """Called with daemon information about the server

        @type info: C{str}
        @param when: A string describing what software the server is running, probably.
        """
        log.msg('Your Host: %s' % info)

    def myInfo(self, servername, version, umodes, cmodes):
        """Called with information about the server

        @type servername: C{str}
        @param servername: The hostname of this server.

        @type version: C{str}
        @param version: A description of what software this server runs.

        @type umodes: C{str}
        @param umodes: All the available user modes.

        @type cmodes: C{str}
        @param cmodes: All the available channel modes.
        """
        log.msg("My Info: servername='%s', version='%s', umodes='%s', cmodes='%s'" % (servername, version, umodes, cmodes))

    def luserClient(self, info):
        """Called with information about the number of connections

        @type info: C{str}
        @param info: A description of the number of clients and servers
        connected to the network, probably.
        """
        log.msg('luserClient: %s' % info)

    def bounce(self, info):
        """Called with information about where the client should reconnect.

        @type info: C{str}
        @param info: A plaintext description of the address that should be
        connected to.
        """
        log.msg('Bounce: %s' % info)

    def isupport(self, options):
        """Called with various information about what the server supports.

        @type options: C{list} of C{str}
        @param options: Descriptions of features or limits of the server,
        possibly in the form "NAME=VALUE".
        """
        log.msg('Server supports: %s' % options)

    def luserChannels(self, channels):
        """Called with the number of channels existant on the server.

        @type channels: C{int}
        """
        log.msg('luser Channels: %s' % channels)

    def luserOp(self, ops):
        """Called with the number of ops logged on to the server.

        @type ops: C{int}
        """
        log.msg('luser Ops: %s' % ops)

    def luserMe(self, info):
        """Called with information about the server connected to.

        @type info: C{str}
        @param info: A plaintext string describing the number of users and
        servers connected to this server.
        """
        log.msg('luser Me: %s' % info)

    def receivedMOTD(self, motd):
        """Called after we've received a complete MOTD from the server.

        motd is a list of strings, where each string was sent as a seperate
        message from the server.
        """
        for line in motd:
            log.msg(line)
