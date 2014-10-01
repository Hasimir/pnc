from twisted.python import log
from twisted.words.protocols import irc


class IRCClient(irc.IRCClient):
    """Support some replies that twisted doesn't support by default
    """
    def irc_unknown(self, prefix, command, params):
        """Called when we receive an unknown message
        """
        log.msg('irc_unknown(prefix="%s", command="%s", params="%s")' % (prefix, command, params))

    def irc_RPL_STATSCONN(self, prefix, params):
        """Do something with a received RPL_STATSCONN message.

        Returned by 'STATS u' and often during connection.
        """
        self.statsconn(*params)

    def irc_RPL_LUSERSC(self, prefix, params):
        """Do something with a received RPL_LUSERSC message.

        Returned in response to 'LUSERS' and often during connection.
        """
        self.lusersc(*params)

    def irc_RPL_LUSERSG(self, prefix, params):
        """Do something with a received RPL_LUSERSG message.

        Returned in response to 'LUSERS' and often during connection.
        """
        self.lusersg(*params)

    def irc_RPL_MOTD_ALT1(self, prefix, params):
        """Do something with a received RPL_MOTD_ALT message.

        Some servers send this instead of a MOTD.
        """
        self.altMOTD(*params)

    def irc_RPL_MOTD_ALT2(self, prefix, params):
        """Do something with a received RPL_MOTD_ALT message.

        Some servers send this instead of a MOTD.
        """
        self.altMOTD(*params)

    def altMOTD(self, target, message):
        """Called when we receive a MOTD sent on an alternative numeric
        """
        log.msg(message)

    def lusersc(self, target, current_local, max_local, message):
        """Called when we get a RPL_LUSERSC message.
        """
        log.msg('RPL_LUSERSC: %s' % message)

    def lusersg(self, target, current_global, max_global, message):
        """Called when we get a RPL_LUSERSG message.
        """
        log.msg('RPL_LUSERSG: %s' % message)

    def statsconn(self, target, message):
        """Called when we get a RPL_STATSCONN message.
        """
        log.msg('RPL_STATSCONN: %s' % message)
