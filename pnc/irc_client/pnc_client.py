from twisted.python import log
from twisted.words.protocols import irc

from pnc.irc_client.channel_mixin import PNCChannelMixin
from pnc.irc_client.ctcp_mixin import PNCCTCPMixin
from pnc.irc_client.error_mixin import PNCErrorMixin
from pnc.irc_client.irc_client import IRCClient
from pnc.irc_client.login_mixin import PNCLoginMixin
from pnc.irc_client.message_mixin import PNCMessageMixin


class PNCClient(PNCChannelMixin, PNCCTCPMixin, PNCErrorMixin, PNCLoginMixin, PNCMessageMixin, IRCClient):
    """The object representing the IRC connection
    """
    def __init__(self, nickname):
        self.channels = []
        self.nickname = nickname

    def msg(self, target, message, *args, **kwargs):
        """Called to send an IRC message.
        """
        print 'IRCClient: sending msg %s->%s' % (target, message)
        irc.IRCClient.msg(self, target, message, *args, **kwargs)
        print 'IRCClient: sent msg'

        if target[0] in irc.CHANNEL_PREFIXES:
            log.msg("<%s:%s> %s" % (self.nickname, target, message))

        else:
            log.msg("*%s*> %s" % (target, message))

    def nickChanged(self, nick):
        """Called when my nick has been changed.
        """
        self.nickname = nick

    def alterCollidedNick(self, nickname):
        """Generate altered version of a nickname

        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.

        @param nickname: The nickname a user is attempting to register.
        @type nickname: C{str}

        @returns: A string that is in some way different from the nickname.
        @rtype: C{str}
        """
        return '_' + nickname

    def handleCommand(self, command, prefix, params):
        """Dispatch commands to the appropriate functions.
        """
        if hasattr(self, 'irc_%s' % command):
            # Dispatch this command to self.irc_<command>
            getattr(self, 'irc_%s' % command)(prefix, params)

        else:
            self.irc_unknown(prefix, command, params)
