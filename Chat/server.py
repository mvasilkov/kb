#!/usr/bin/env python
from twisted.internet import protocol, reactor

transports = set()


class Chat(protocol.Protocol):
    def dataReceived(self, data):
        transports.add(self.transport)

        if ':' not in data:
            return

        user, msg = data.split(':')

        for t in transports:
            if t is not self.transport:
                t.write('{} says: {}'.format(user, msg))


class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()

reactor.listenTCP(9096, ChatFactory())
reactor.run()
