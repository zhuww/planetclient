from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import defer
from twisted.protocols import basic

def wait(seconds, result=None):
    """returns a deferred that will be fired later"""
    d = defer.Deferred()
    reactor.callLater(seconds, d.callback, result)
    return d

class Speaker(basic.LineReceiver):
    #@defer.inlineCallbacks
    def sendMessage(self, msg):
        print "sending message %s" % msg
        #self.transport.write(msg + '\n')
        self.sendLine(msg)
        #yield wait(2)
    def lineReceived(self, data):
        print data
        msg = raw_input()
        if (msg == "bye"):
            self.disconnect()
        else:
            self.sendMessage(msg)
    def disconnect(self):
        self.transport.loseConnection()
    def getmsg(self):
        msg = raw_input()
        self.sendMessage(msg)
    def connectionMade(self):
        print "connected with the server."
        print "What is your user name?"
        reactor.callLater(1, self.getmsg)

    def connectionLost(self, reason):
        print "disconnected with the server, reason %s." % reason

class SpeakerFactory(Factory):
    def buildProtocol(self, addr):
        return Speaker()

def gotProtocol(p):
    #pass
    p.sendMessage("Weiwei")
    #reactor.callLater(1, p.sendMessage, "Weiwei")
    #reactor.callLater(2, p.sendMessage, "Hello,world")
    #reactor.callLater(3, p.disconnect)

point = TCP4ClientEndpoint(reactor, "cyberska.phas.ubc.ca", 8123)
d = point.connect(SpeakerFactory())
#d.addCallback(gotProtocol)
reactor.run()

