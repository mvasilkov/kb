#!/usr/bin/env python
from twisted.internet import protocol, reactor

colors = ['7f8c8d', 'c0392b', '2c3e50', '8e44ad', '27ae60']
transports = set()


def esc_markup(msg):
    return (msg.replace('&', '&amp;')
            .replace('[', '&bl;')
            .replace(']', '&br;'))


class Chat(protocol.Protocol):
    def connectionMade(self):
        self.color = colors.pop()
        colors.insert(0, self.color)

    def dataReceived(self, data):
        transports.add(self.transport)

        if ':' not in data:
            return

        user, msg = data.split(':', 1)

        for t in transports:
            if t is not self.transport:
                t.write('[b][color={}]{}:[/color][/b] {}'
                        .format(self.color, user,
                                esc_markup(msg)))


class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()

reactor.listenTCP(9096, ChatFactory())
reactor.run()
