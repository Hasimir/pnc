from twisted.python import log


class PNCCTCPMixin:
    """Handle CTCP messages/responses.

    We put these into their own class for organization purposes.
    """
    def ctcpQuery_ERRMSG(self, user, channel, data):
        # Yeah, this seems strange, but that's what the spec says to do
        # when faced with an ERRMSG query (not a reply).
        nick = user.split('!')[0]
        errmsg = "%s :No error has occurred." % data
        self.ctcpMakeReply(nick, [('ERRMSG', errmsg)])

    def ctcpUnknownReply(self, user, channel, tag, data):
        """Called when a fitting ctcpReply_ method is not found.

        XXX: If the client makes arbitrary CTCP queries,
        this method should probably show the responses to
        them instead of treating them as anomolies.
        """
        log.msg("Unknown CTCP reply from %s to %s: %s %s" % (user, channel, tag, data))
