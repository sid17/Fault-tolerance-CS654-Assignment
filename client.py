# This is the Twisted Get Poetry Now! client, version 3.0.

# NOTE: This should not be used as the basis for production code.

import optparse
import os
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import task
from termcolor import colored

pingFreq=10
heartbeatFReq=10
pingCount=0
heartbeatCount=0

def parse_args():
    usage = """usage: %prog [options] [hostname]:port

The following is the format to run the program
Run it like this:

  python client.py host:port --job job_name --pid(optional) proc_name

"""
    parser = optparse.OptionParser(usage)

    # _, address = parser.parse_args()

    help1 = """The job to execute, either ping or heartbeat or both,  
        use flags : --job ping     --job hb      --job all
    """
    parser.add_option('--job', help=help1)

    help2 = """The pid of the process to monitor for the heartbeat  
        use flags :   --pid 12345   --pid chrome
    """

    parser.add_option('--pid', help=help2)

    options, address = parser.parse_args()


    if not options.job or not options.job in ['ping','hb','all'] :
        print colored(help1, 'red')
        parser.exit()
    
    if not len(address) == 1:
        print colored(parser.format_help(), 'red')
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            print colored("usage hostname:port",'red')
            parser.exit()

        host, port = addr.split(':', 1)

        if not port.isdigit():
            parser.error('Ports must be integers.')

        return (host, int(port))

    return parse_address(address[0]),options


class AppProtocol(Protocol):

    #  the protocol for the TCP connection with the client
    # obtains the response and handles it, the connectionLost is invoked when the connection 
    # with the other end disconnects, the given serves as the client

    response = ''
    deathcount=0
    deathfreq=5

    def connectionMade(self):
        print "Connection Made with host %s " %(self.transport.getPeer())
        if self.factory.process:
            self.transport.write(str(self.factory.process))
        else:
            self.transport.write("-1")

    def handleResponse(self):
        global heartbeatCount,heartbeatFReq
        if self.response=="Process Dead":
            if self.deathcount==0:
                print colored("\n Fatal ! stopped listening heartbeat from the process, either wait for process to come up or please rectify",'red')
            self.deathcount=(self.deathcount+1)%self.deathfreq
            

        
        if heartbeatCount==0:
            if self.response!="Process Dead":
                print colored("\n"+self.response+"",'green')

        heartbeatCount=(heartbeatCount+1)%heartbeatFReq


    def dataReceived(self, data):
        self.response = data
        self.handleResponse()

    def connectionLost(self, reason):
        self.factory.disconnected(reason)



class AppFactory(ClientFactory):

    # Factory, different connections made are an instance of the factory and define the protocol
    # on how a given request connection response is handled, such connections are asynchronous

    protocol = AppProtocol

    def __init__(self, callback, process):
        self.callback = callback
        self.process = process

    def disconnected(self, reason):
        self.callback(reason)


def makeConnection(host, port, callback, monitorProcess):
    
    """
    Make a connection with the client and hear for response till the connection breaks
    """
    from twisted.internet import reactor
    factory = AppFactory(callback, monitorProcess)
    reactor.connectTCP(host, port, factory)


def pingHandler(host):
    global pingCount,pingFreq
    hostname = host
    response = os.system("ping -c 1 " + hostname + ">/dev/null 2>&1")
    if response == 0:
        if pingCount==0:
            print colored("\nPing Success",'green')
        pingCount=(pingCount+1)%pingFreq
    else:
        print colored("\n"+'Fatal '+str(hostname)+' is down!'+"",'red')



def main():
    (host,port),options = parse_args()

    if not options.pid:
        monitorProcess=""
    else:
        monitorProcess=options.pid

    from twisted.internet import reactor

    def handle_error(reason):
        print colored("\nFatal ! stopped listening heartbeat from the virtual machine",'red')
        # reactor.stop()


    if options.job=="ping":
        pingSystem = task.LoopingCall(pingHandler,host)
        pingSystem.start(1.0)
    elif options.job=="hb":
        makeConnection(host, port, handle_error,monitorProcess)
    else:
        pingSystem = task.LoopingCall(pingHandler,host)
        pingSystem.start(1.0)
        makeConnection(host, port, handle_error,monitorProcess)

    reactor.run()


if __name__ == '__main__':
    main()
