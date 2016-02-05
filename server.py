# This is the Twisted Fast Poetry Server, version 1.0

import optparse, os
from twisted.internet.protocol import ServerFactory, Protocol
from subprocess import check_output


def parse_args():
    usage = """usage: %prog [options]

  python server.py 

"""

    parser = optparse.OptionParser(usage)

    help = "The port to listen on. Default to a random available port."
    parser.add_option('--port', type='int', help=help)

    help = "The interface to listen on. Default is localhost."
    parser.add_option('--iface', help=help, default='localhost')

    options, args = parser.parse_args()

    return options


class AppProtocol(Protocol):
    isConnected = True
    processMonitored="-1"

    def makePid(self):
        if self.processMonitored!="-1":
            try:
                return int(self.processMonitored)
            except:
                try:
                    return self.get_pid(self.processMonitored)
                except:
                    return -2
        else:
            return -1

    def dataReceived(self, data):
        self.processMonitored=data
        self.factory.handler(self)


    def connectionLost(self,reason):
        self.isConnected=False
        print "connection lost with %s, reason %s" % (self.transport.getPeer(),reason)

    def get_pid(self,name):
        return int(check_output(["pidof","-s",name]))

    def isProcessAlive(self,pid):
        return os.path.exists("/proc/"+str(pid))



class AppFactory(ServerFactory):

    protocol = AppProtocol

    def __init__(self, handler):
        self.handler = handler


class HeartBeat(): 

    def __init__(self):
        pass

    def getHeartBeatResponse(self,protocolObj):
        pid=protocolObj.makePid()
        if pid!=-1:
            if pid!=-2 and protocolObj.isProcessAlive(pid):
                return "Process Alive"
            else:
                return "Process Dead"
        else:
            return "Machine Alive"

    def handleHeartBeat(self,protocolObj,send_heartbeat):
        if protocolObj.isConnected:
            protocolObj.transport.write(self.getHeartBeatResponse(protocolObj))
            print "Sending Heartbeat to %s",(protocolObj.transport.getPeer())
            send_heartbeat(protocolObj)
        else:
            protocolObj.transport.loseConnection()


def main():
    
    def send_heartbeat(protocolObj):
        reactor.callLater(1,HeartBeat().handleHeartBeat,protocolObj,send_heartbeat)

    options = parse_args()

    factory = AppFactory(send_heartbeat)

    from twisted.internet import reactor

    port = reactor.listenTCP(options.port or 0, factory,
                             interface=options.iface)

    print 'Serving on  %s.' % (port.getHost())

    reactor.run()
    
if __name__ == '__main__':
    main()


