from twisted.python import log


class PNCChannelMixin:
    """These are the channel related functions

    We put these into their own class for organization purposes.
    """
    def joined(self, channel):
        """Called when the client joins a channel.
        """
        self.channels.append(channel)
        log.msg("I have joined %s" % channel)

    def kickedFrom(self, channel, kicker, message):
        """Called when the client leaves a channel.
        """
        self.channels.remove(channel)
        args = (channel, kicker, message)
        log.msg("I have been kicked from %s by %s (%s)" % args)

    def left(self, channel):
        """Called when the client leaves a channel.
        """
        self.channels.remove(channel)
        log.msg("I have left %s" % channel)

    def userJoined(self, user, channel):
        """Called when I see another user joining a channel.
        """
        log.msg('%s has joined %s' % (user, channel))

    def userLeft(self, user, channel):
        """Called when I see another user leaving a channel.
        """
        log.msg('%s has left %s' % (user, channel))

    def userQuit(self, user, quitMessage):
        """Called when I see another user disconnect from the network.
        """
        log.msg('%s has quit IRC (%s)' % (user, quitMessage))

    def userKicked(self, kickee, channel, kicker, message):
        """Called when I observe someone else being kicked from a channel.
        """
        log.msg('%s has kicked %s from channel %s (%s)' % (kicker, kickee, channel, message))

    def topicUpdated(self, user, channel, newTopic):
        """Called when the topic is changed.

        In channel, user changed the topic to newTopic.

        Also called when first joining a channel.
        """
        log.msg('%s has changed the topic on channel %s to %s' % (user, channel, newTopic))

    def userRenamed(self, oldnick, newnick):
        """Called when a user changes their nick
        """
        log.msg('%s is now known as %s' % (oldnick, newnick))
