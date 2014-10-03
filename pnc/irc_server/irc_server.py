from twisted.python import log
from twisted.words.protocols import irc


class IRCServer(irc.IRC):
    """Support some replies that twisted doesn't support by default
    """
    hostname = None
    password = None
    realname = None
    username = None
    registered = False

    def sendServerMessage(self, command, *parameter_list):
        self.sendMessage(command, *parameter_list, prefix='darkstar.frop.org')  # FIXME: Don't hardcode darkstar

    def sendReply(self, numeric, *parameter_list):
        self.sendMessage(numeric, self.nickname, *parameter_list, prefix='darkstar.frop.org')

    def connectionMade(self):
        log.msg('*** client %s connected' % self.hostname)

    def connectionLost(self, reason):
        log.msg('*** %s!%s@%s has disconnected' % (self.nickname, self.username, self.hostname))

    def irc_PASS(self, prefix, command, params):
        """Password message -- Register a password.

        Parameters: <password>

        [REQUIRED]

        Note that IRC requires the client send this *before* NICK
        and USER.
        """
        if not self.nickname and not self.password:
            self.password = params[-1]
        else:
            # FIXME: This should send the proper error numeric
            self.privmsg('darkstar.frop.org', nickname, 'Password invalid!')
            self.transport.loseConnection()
            return

    def irc_NICK(self, prefix, params):
        """Nick message -- Set your nickname.

        Parameters: <nickname>

        [REQUIRED]
        """
        nickname = params[0]
        # FIXME: Check the nick out, including the password if they've sent one
        # Send a 433 if any problems

        # Nick checks out, let them set it as our nick
        if self.registered:
            # FIXME: This should change our upstream nick
            self.sendReply(irc.ERR_ERRONEUSNICKNAME, nickname, ':You can not change your nick.')

        else:
            self.registered = True

            # Send the server connect messages
            self.sendReply(irc.RPL_WELCOME, ':Welcome to PNC!')
            self.sendReply(irc.RPL_YOURHOST, ':Your host is darkstar.frop.org[darkstar.frop.org/3333], running version 0.0.1.')  # FIXME: Don't hardcode this
            self.sendReply(irc.RPL_CREATED, ':This server was created today.')  # FIXME: Replace today with the date/time we started
            self.sendReply(irc.RPL_MYINFO, 'darkstar.frop.org', '0.0.1', 'iw', 'lnst')  # FIXME: Don't hardcode this
            # FIXME: Implement RPL_ISUPPORT here
            self.sendReply(irc.RPL_LUSERCLIENT, ':There are 1 users and 1 invisible on 1 servers')  # FIXME
            self.sendReply(irc.RPL_LUSEROP, '0', ':IRC Operators online')  # FIXME
            self.sendReply(irc.RPL_LUSERCHANNELS, '0', ':Channels formed')
            self.sendReply(irc.RPL_LUSERME, ':I have 1 clients and 0 servers.')
            # 265 <nick> %s %s :Current local users %s, max %s
            # 266 <nick> %s %s :Current global users %s, max %s
            # 250 <nick> :Highest connection count: %s

            # Send the MOTD
            # FIXME: Make this less broken and hardcoded
            self.sendReply(irc.RPL_MOTDSTART, ':darkstar.frop.org message of the day')
            self.sendReply(irc.RPL_MOTD, ":They're all gonna laugh at you!")
            self.sendReply(irc.RPL_ENDOFMOTD, ':end message of the day')

    def irc_USER(self, prefix, params):
        """User message -- Set your realname.

        Parameters: <user> <hostname?> <unused> <realname>
        """
        log.msg('irc_USER: %s' % params)
        self.username, self.hostname, unused, self.realname = params

    def irc_USERHOST(self, prefix, params):
        """Respond to the USERHOST command.
        """
        log.msg('irc_USERHOST: %s' % params)
        self.sendReply(irc.RPL_USERHOST, ':%s=-zwhite@darkstar.frop.org' % self.nickname)

    def irc_PING(self, prefix, params):
        """Ping message

        Parameters: <server1> [ <server2> ]
        """
        #log.msg('irc_PING: %s' % params)
        self.sendServerMessage('PONG', 'darkstar.frop.org', ':' + params[0])

    def irc_PRIVMSG(self, prefix, params):
        """
        """
        log.msg('irc_PRIVMSG: %s' % params)
        target = params[0]
        msg = ' '.join(params[1:])
        self.upstream.msg(target, msg)

    def irc_QUIT(self, prefix, params):
        """Quit

        Parameters: [ <Quit Message> ]
        """
        log.msg('Client %s!%s@%s has signed off: %s' % (self.nickname, self.username, self.hostname, params[0]))
        self.transport.loseConnection()

    def irc_unknown(self, prefix, command, params):
        """Called when we receive an unknown message
        """
        log.msg('irc_unknown(prefix="%s", command="%s", params="%s")' % (prefix, command, params))
