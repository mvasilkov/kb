from kivy.support import install_twisted_reactor
install_twisted_reactor()

from twisted.internet import reactor, protocol

from kivy.app import App
from kivy.config import Config


def esc_markup(msg):
    return (msg.replace('&', '&amp;')
            .replace('[', '&bl;')
            .replace(']', '&br;'))


class ChatClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write('CONNECT')
        self.factory.app.on_connect(self.transport)

    def dataReceived(self, data):
        self.factory.app.on_message(data)


class ChatClientFactory(protocol.ClientFactory):
    protocol = ChatClient

    def __init__(self, app):
        self.app = app


class ChatApp(App):
    def connect(self):
        host = self.root.ids.server.text
        self.nick = self.root.ids.nickname.text
        print('-- connecting to ' + host)
        reactor.connectTCP(host, 9096,
                           ChatClientFactory(self))

    def disconnect(self):
        print('-- disconnecting')
        if self.conn:
            self.conn.loseConnection()
            del self.conn
        self.root.current = 'login'
        self.root.ids.chat_logs.text = ''

    def send_msg(self):
        msg = self.root.ids.message.text
        self.conn.write('%s:%s' % (self.nick, msg))
        self.root.ids.chat_logs.text += (
            '[b][color=2980b9]{}:[/color][/b] {}\n'
            .format(self.nick, esc_markup(msg)))
        self.root.ids.message.text = ''

    def on_connect(self, conn):
        print('-- connected')
        self.conn = conn
        self.root.current = 'chatroom'

    def on_message(self, msg):
        self.root.ids.chat_logs.text += msg + '\n'

if __name__ == '__main__':
    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '900')

    ChatApp().run()
