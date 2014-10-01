PNC - Not your typical IRC Bouncer
==================================

PNC is an IRC bouncer similar to ZNC with an important difference. Where ZNC
tries to be a proxy between you and a server, PNC attempts to be an IRC server
with a rather unique upstream connection. IRC client connections to PNC are 
entirely decoupled from PNC's connections to upstream servers. This means that
it is not possible for your IRC clients to affect one another.
