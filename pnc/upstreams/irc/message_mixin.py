from pnc.message import downstream_privmsg
from twisted.python import log


class PNCMessageMixin:
    """These are messages directed towards the client.

    We put these into their own class for organization purposes.
    """
    def noticed(self, user, channel, message):
        """Called when I have a notice from a user to me or a channel.

        If the client makes any automated replies, it must not do so in
        response to a NOTICE message, per the RFC::

            The difference between NOTICE and PRIVMSG is that
            automatic replies MUST NEVER be sent in response to a
            NOTICE message. [...] The object of this rule is to avoid
            loops between clients automatically sending something in
            response to something it received.
        """
        if channel == self.nickname:
            log.msg('-%s- %s' % (user, message))
        else:
            log.msg('-%s:%s- %s' % (user, channel, message))

    def privmsg(self, source, target, message):
        """Called when the client receives a message.
        """
        downstream_privmsg(self.irc_network, source, target, message)

        if target == self.nickname:
            log.msg('*%s* %s' % (source, message))
        else:
            log.msg('<%s:%s> %s' % (source, target, message))

    def action(self, source, channel, msg):
        """Called when the client sees someone do an action.
        """
        nick, hostmask = source.split('!', 1)
        log.msg("* (%s) %s %s" % (channel, nick, msg))

    def modeChanged(self, user, channel, set, modes, args):
        """Called when users or channel's modes are changed.

        @type user: C{str}
        @param user: The user and hostmask which instigated this change.

        @type channel: C{str}
        @param channel: The channel where the modes are changed. If args is
        empty the channel for which the modes are changing. If the changes are
        at server level it could be equal to C{user}.

        @type set: C{bool} or C{int}
        @param set: True if the mode(s) is being added, False if it is being
        removed. If some modes are added and others removed at the same time
        this function will be called twice, the first time with all the added
        modes, the second with the removed ones. (To change this behaviour
        override the irc_MODE method)

        @type modes: C{str}
        @param modes: The mode or modes which are being changed.

        @type args: C{tuple}
        @param args: Any additional information required for the mode
        change.
        """
        log.msg('Mode change "%s %s" by %s on %s' % (modes, args, user, channel))
