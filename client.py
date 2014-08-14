from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import defer
from twisted.protocols import basic
from getpass import getpass
from threading import Thread
import os,sys,cPickle,re
from foldnplot import main as gui
from dldata import download


DATAPATH = "./data/"

class foldgui(Thread):
    def __init__(self, client, kic):
        Thread.__init__(self)
        self.kic = kic
        self.client = client

    def stop(self):
        for res in self.result:
            res = cPickle.dumps(res)
            #print 'SAVE:'+ res
            self.client.sendLine("SAVE:" + res)

    def run(self):
        download(self.kic, path=DATAPATH)
        self.result = gui(self.kic, path=DATAPATH)
        self.stop()


class Speaker(basic.LineReceiver):
    #@defer.inlineCallbacks
    def sendMessage(self, msg):
        #print "sending message %s" % msg
        self.sendLine(msg)
    def waitInput(self):
        msg = raw_input(">")
        if (msg == "bye"):
            self.disconnect()
        else:
            self.sendMessage(msg)

    def lineReceived(self, data):
        if not data.startswith("#"):
            print data
            self.waitInput()
        elif data.split()[0] == "#NEWUSER":
            while True:
                print """
Set your password (less than 10 characters)
***WARNING*** 
DO NOT USE YOUR BANK PASSWORD
THIS SERVER IS ABSOLUTELY INSECURE.
                """
                password1 = getpass("1st time>")
                password2 = getpass("2ed time>")
                if password1 == password2: break
                else:print "Passwords don't match, try again:"
            self.sendLine(password1)

        elif data.split()[0] == "#LOGIN":
            password = getpass("password:>")
            self.sendLine(password)

        elif data.split()[0] == "#KIC":
            kic = data.split()[1]
            fg = foldgui(self, kic)
            fg.start()
            self.waitInput()



    def disconnect(self):
        self.transport.loseConnection()
    def getmsg(self):
        msg = raw_input(">")
        self.sendMessage(msg)
    def connectionMade(self):
        print "connected with the server."
        print """
What is your user name?
If you a first time user, indicate your preferred user name:
        """
        reactor.callLater(1, self.getmsg)

    def connectionLost(self, reason):
        print "disconnected with the server, reason %s." % reason

    def askpassword(self):
        pass
    def setpassword(self):
        pass

class SpeakerFactory(Factory):
    def buildProtocol(self, addr):
        return Speaker()


if __name__ == "__main__":
    if not os.access(DATAPATH, os.W_OK):
        os.mkdir(DATAPATH)
    point = TCP4ClientEndpoint(reactor, "cyberska.phas.ubc.ca", 8124)
    #point = TCP4ClientEndpoint(reactor, "chopin.phas.ubc.ca", 8123)
    d = point.connect(SpeakerFactory())
    reactor.run()

